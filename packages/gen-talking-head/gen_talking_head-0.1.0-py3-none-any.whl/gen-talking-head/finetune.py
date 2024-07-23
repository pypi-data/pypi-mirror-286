""" 微调接口 """

import os
from tqdm import tqdm

import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader

from model.common.hparams import hparams as hp
from model.dataset import PitchLipSyncDataset
from model.losses import VGG19PerceptualLoss, LipSyncLoss, ArcFaceLoss, g_loss_func, d_loss_func
from model.net.wav2lip_with_pitch import PitchLipModel, Wav2Lip_disc_qual

from tools.common import load_yaml

local_rank = 0
DEVICE = torch.device('cuda')


def requires_grad(model, flag=True):
    for p in model.parameters():
        p.requires_grad = flag


class Model(nn.Module):

    def __init__(self, cfg, lang='ZH', device=DEVICE):
        super(Model, self).__init__()
        self.cfg = load_yaml(cfg) if isinstance(cfg, str) else cfg
        model_path = self.cfg['pre_trained_model']
        self.device = device

        self.net = PitchLipModel().to(self.device)
        self.Disc = Wav2Lip_disc_qual().to(self.device)
        self.optimizer_G = optim.Adam(self.net.parameters(), lr=hp.initial_learning_rate)
        self.optimizer_D = optim.Adam(self.Disc.parameters(), lr=hp.disc_initial_learning_rate)
        self.load_model(model_path['pitchlip'][lang])
        self.net.pitch_modules_requires_grad(False)

        self.loss_func_reco = nn.L1Loss(reduction='mean')
        self.loss_func_perc = VGG19PerceptualLoss(model_path['vgg']).to(self.device)
        self.loss_func_iden = ArcFaceLoss(model_path['arc_face']).to(self.device)
        self.loss_func_sync = LipSyncLoss(model_path['lipsync'][lang]).to(self.device)
        lamb = self.cfg['trainer']['lambda']
        self.lamb_reco = lamb['l1']
        self.lamb_perc = lamb['vgg']
        self.lamb_iden = lamb['arcface']
        self.lamb_sync = lamb['syncnet']
        self.lamb_adv = lamb['adv']

    def load_model(self, pitchlip_ckpt_path):
        checkpoint = torch.load(pitchlip_ckpt_path)
        state_dict = {
            k.replace('net.', ''): v for k, v in checkpoint["state_dict"].items() if k.startswith('net.')}
        self.net.load_state_dict(state_dict)
        state_dict = {
            k.replace('Disc.', ''): v for k, v in checkpoint["state_dict"].items() if k.startswith('Disc.')}
        self.Disc.load_state_dict(state_dict)
        self.optimizer_G.load_state_dict(checkpoint['optimizer_g'])
        self.optimizer_D.load_state_dict(checkpoint['optimizer_d'])
        print('Loaded checkpoint from {}'.format(pitchlip_ckpt_path))

    def infer(self, x, indiv_mels, indiv_f0):
        x = x.cuda(non_blocking=True)
        indiv_mels = indiv_mels.cuda(non_blocking=True)
        indiv_f0 = indiv_f0.cuda(non_blocking=True)
        g = self.net(indiv_mels, indiv_f0, x)
        return g

    def forward(self, x, indiv_mels, indiv_f0, mel, gt):
        return self._step(x, indiv_mels, indiv_f0, mel, gt)

    def _step(self, x, indiv_mels, indiv_f0, mel, gt):
        self.net.train()
        self.Disc.train()
        mel = mel.cuda(non_blocking=True)
        gt = gt.cuda(non_blocking=True)

        # update LNet
        self.optimizer_G.zero_grad()
        self.optimizer_D.zero_grad()
        requires_grad(self.Disc, False)
        g = self.infer(x, indiv_mels, indiv_f0)
        loss, loss_dict = self._compute_losses(g, gt, mel)  # get total loss
        g_loss = g_loss_func(fake=self.Disc(g))
        g_loss = torch.sum(g_loss)
        g_total_loss = loss + g_loss * self.lamb_adv

        # update Discriminator
        self.optimizer_D.zero_grad()
        requires_grad(self.Disc, True)
        d_loss = d_loss_func(real=self.Disc(gt), fake=self.Disc(g.detach()))
        d_loss = torch.sum(d_loss)
        d_total_loss = d_loss

        total_loss = g_total_loss + d_total_loss
        loss_dict['g_loss'] = g_loss
        loss_dict['d_loss'] = d_loss
        return total_loss, loss_dict

    def _compute_losses(self, g, gt, mel):
        reco_loss = self.loss_func_reco(g, gt)
        x = torch.cat([g, gt], dim=0)
        perc_loss = sum([self.loss_func_perc(x[:, :, t]) for t in range(hp.syncnet_T)]) / hp.syncnet_T
        iden_loss = sum([self.loss_func_iden(x[:, :, t]) for t in range(hp.syncnet_T)]) / hp.syncnet_T
        sync_loss = self.loss_func_sync(mel, g)
        reco_loss, perc_loss, iden_loss, sync_loss = map(torch.sum, (reco_loss, perc_loss, iden_loss, sync_loss))
        total_loss = (reco_loss * self.lamb_reco + reco_loss * self.lamb_reco +
                      iden_loss * self.lamb_iden + sync_loss * self.lamb_sync)
        loss_dict = {
            'reco': reco_loss,
            'perc': perc_loss,
            'iden': iden_loss,
            'sync': sync_loss,
        }
        return total_loss, loss_dict


class Trainer(object):

    def __init__(self, video_path: str, out_dir: str, cfg_path='config/base.yaml', lang='ZH', device=DEVICE):
        self.out_dir = out_dir
        self.cfg = load_yaml(cfg_path)
        self.device = device

        self.model = Model(self.cfg, lang=lang).to(self.device)
        setting = self.cfg['trainer']
        milestones = setting['milestones']
        self.schedule_G = optim.lr_scheduler.MultiStepLR(self.model.optimizer_G, milestones, gamma=setting['gamma'])
        self.schedule_D = optim.lr_scheduler.MultiStepLR(self.model.optimizer_D, milestones, gamma=setting['gamma'])

        # self.out_dir = tempfile.mktemp(dir=self.cfg['cache_dir'])
        os.makedirs(self.out_dir, exist_ok=True)

        train_dataset = PitchLipSyncDataset(video_path, self.cfg, out_dir=self.out_dir)
        self.train_dataloader = torch.utils.data.DataLoader(
            train_dataset, batch_size=setting['batch_size'], num_workers=setting['num_worker'])

        self.fix_samples = None
        self.nsteps = setting['nsteps']
        self.global_step = 0

        self.running_reco_loss = 0.
        self.running_sync_loss = 0.
        self.running_perc_loss = 0.
        self.running_iden_loss = 0.
        self.running_g_loss = 0.
        self.running_d_loss = 0.

        self.checkpoint_path = None

    def train(self):
        while self.global_step < self.nsteps:
            prog_bar = tqdm(enumerate(self.train_dataloader))
            for step, (x, indiv_mels, indiv_f0, mel, gt) in prog_bar:
                if not (self.global_step < self.nsteps):
                    break
                loss, loss_dict = self.model(x, indiv_mels, indiv_f0, mel, gt)
                torch.sum(loss).backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=3, norm_type=2.)
                self.model.optimizer_G.step()
                self.model.optimizer_D.step()
                self.schedule_G.step()
                self.schedule_D.step()

                self._record(loss_dict)
                prog_bar.set_description(
                    'GlobalStep: {}/{}, '
                    'ReconstructionLoss: {:.4f}, PerceptualLoss: {:.4f}, IdenLoss: {:.4f}, SyncLoss: {:.4f}, g_loss: {:.4f}, d_loss: {:.4f}'
                    .format(self.global_step, self.nsteps,
                            self.running_reco_loss, self.running_perc_loss, self.running_iden_loss,
                            self.running_sync_loss,
                            self.running_g_loss, self.running_d_loss)
                )

                self.global_step += 1
        self.save()
        return self.checkpoint_path

    def _record(self, loss_dict, k=0.5):
        reco_loss = torch.mean(loss_dict['reco']).item()
        perc_loss = torch.mean(loss_dict['perc']).item()
        iden_loss = torch.mean(loss_dict['iden']).item()
        sync_loss = torch.mean(loss_dict['sync']).item()
        g_loss = torch.mean(loss_dict['g_loss']).item()
        d_loss = torch.mean(loss_dict['d_loss']).item()
        if self.global_step == 0:
            self.running_reco_loss = reco_loss
            self.running_perc_loss = perc_loss
            self.running_iden_loss = iden_loss
            self.running_sync_loss = sync_loss
            self.running_g_loss = g_loss
            self.running_d_loss = d_loss
        else:
            self.running_reco_loss = k * self.running_reco_loss + (1 - k) * reco_loss
            self.running_perc_loss = k * self.running_perc_loss + (1 - k) * perc_loss
            self.running_iden_loss = k * self.running_iden_loss + (1 - k) * iden_loss
            self.running_sync_loss = k * self.running_sync_loss + (1 - k) * sync_loss
            self.running_g_loss = k * self.running_g_loss + (1 - k) * g_loss
            self.running_d_loss = k * self.running_d_loss + (1 - k) * d_loss

    def save(self):
        self.checkpoint_path = os.path.join(
            self.out_dir, "fine_tuned_{:09d}.pth".format(self.global_step))
        torch.save(self.model.net.state_dict(), self.checkpoint_path)
        print("Saved checkpoint:", self.checkpoint_path)


if __name__ == '__main__':
    cfg_path = './config/base.yaml'
    video_path = '/home/czz/Algo_GenTalkingHead_Inference-4090/test_samples/QHFTBaiQiuEn1_1.mp4'
    out_dir = '/tmp'
    trainer = Trainer(video_path, cfg_path, out_dir)
    checkpoint_path = trainer.train()
    print(checkpoint_path)
