
import os
import functools
import torch
from torch import nn
from torch.nn import functional as F

from model.net.base_blocks import Conv2d, Conv1d, Conv2dTranspose, Embedding, LambdaLayer, nonorm_Conv2d
from model.common.pitch import f0_to_coarse


class PitchLipModel(nn.Module):

    def __init__(self, pitch_ckpt_path=None):
        """ pitch_ckpt_path checkpoint of audio2motion_vae,
            downloaded from: https://github.com/yerfor/GeneFacePlusPlus?tab=readme-ov-file
        """
        super(PitchLipModel, self).__init__()

        self.face_encoder_blocks = nn.ModuleList([
            nn.Sequential(Conv2d(6, 16, kernel_size=7, stride=1, padding=3)),  # 96,96

            nn.Sequential(Conv2d(16, 32, kernel_size=3, stride=2, padding=1),  # 48,48
                          Conv2d(32, 32, kernel_size=3, stride=1, padding=1, residual=True),
                          Conv2d(32, 32, kernel_size=3, stride=1, padding=1, residual=True)),

            nn.Sequential(Conv2d(32, 64, kernel_size=3, stride=2, padding=1),  # 24,24
                          Conv2d(64, 64, kernel_size=3, stride=1, padding=1, residual=True),
                          Conv2d(64, 64, kernel_size=3, stride=1, padding=1, residual=True),
                          Conv2d(64, 64, kernel_size=3, stride=1, padding=1, residual=True)),

            nn.Sequential(Conv2d(64, 128, kernel_size=3, stride=2, padding=1),  # 12,12
                          Conv2d(128, 128, kernel_size=3, stride=1, padding=1, residual=True),
                          Conv2d(128, 128, kernel_size=3, stride=1, padding=1, residual=True)),

            nn.Sequential(Conv2d(128, 256, kernel_size=3, stride=2, padding=1),  # 6,6
                          Conv2d(256, 256, kernel_size=3, stride=1, padding=1, residual=True),
                          Conv2d(256, 256, kernel_size=3, stride=1, padding=1, residual=True)),

            nn.Sequential(Conv2d(256, 512, kernel_size=3, stride=2, padding=1),  # 3,3
                          Conv2d(512, 512, kernel_size=3, stride=1, padding=1, residual=True), ),

            nn.Sequential(Conv2d(512, 512, kernel_size=3, stride=1, padding=0),  # 1, 1
                          Conv2d(512, 512, kernel_size=1, stride=1, padding=0)), ])

        self.audio_encoder = nn.Sequential(
            Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            Conv2d(32, 32, kernel_size=3, stride=1, padding=1, residual=True),
            Conv2d(32, 32, kernel_size=3, stride=1, padding=1, residual=True),

            Conv2d(32, 64, kernel_size=3, stride=(3, 1), padding=1),
            Conv2d(64, 64, kernel_size=3, stride=1, padding=1, residual=True),
            Conv2d(64, 64, kernel_size=3, stride=1, padding=1, residual=True),

            Conv2d(64, 128, kernel_size=3, stride=3, padding=1),
            Conv2d(128, 128, kernel_size=3, stride=1, padding=1, residual=True),
            Conv2d(128, 128, kernel_size=3, stride=1, padding=1, residual=True),

            Conv2d(128, 256, kernel_size=3, stride=(3, 2), padding=1),
            Conv2d(256, 256, kernel_size=3, stride=1, padding=1, residual=True),

            Conv2d(256, 512, kernel_size=3, stride=1, padding=0),
            Conv2d(512, 512, kernel_size=1, stride=1, padding=0),)

        mel_feat_dim = 128
        feat_dim = mel_feat_dim
        self.pitch_embed = Embedding(300, mel_feat_dim, None)
        self.pitch_encoder = nn.Sequential(*[
                nn.Conv1d(feat_dim, feat_dim , 3, 1, 1, bias=False),
                nn.BatchNorm1d(feat_dim),
                nn.GELU(),
                nn.Conv1d(feat_dim, feat_dim, 3, 1, 1, bias=False)
            ])
        self.pitch_16to1 = nn.Sequential(
            Conv1d(feat_dim, 128, 3, 3, 1),
            Conv1d(128, 128, 3, 2, 1),
            Conv1d(128, 128, 3, 1, 1),
            Conv1d(128, 128, kernel_size=3, stride=1, padding=0),
        )
        self.compose = nn.Linear(640, 512)

        self.downsampler = LambdaLayer(
            lambda x: F.interpolate(x.transpose(1, 2), scale_factor=0.5, mode='nearest').transpose(1, 2))

        self.face_decoder_blocks = nn.ModuleList([
            nn.Sequential(Conv2d(512, 512, kernel_size=1, stride=1, padding=0),),

            nn.Sequential(Conv2dTranspose(1024, 512, kernel_size=3, stride=1, padding=0), # 3,3
            Conv2d(512, 512, kernel_size=3, stride=1, padding=1, residual=True),),

            nn.Sequential(Conv2dTranspose(1024, 512, kernel_size=3, stride=2, padding=1, output_padding=1),
            Conv2d(512, 512, kernel_size=3, stride=1, padding=1, residual=True),
            Conv2d(512, 512, kernel_size=3, stride=1, padding=1, residual=True),), # 6, 6

            nn.Sequential(Conv2dTranspose(768, 384, kernel_size=3, stride=2, padding=1, output_padding=1),
            Conv2d(384, 384, kernel_size=3, stride=1, padding=1, residual=True),
            Conv2d(384, 384, kernel_size=3, stride=1, padding=1, residual=True),), # 12, 12

            nn.Sequential(Conv2dTranspose(512, 256, kernel_size=3, stride=2, padding=1, output_padding=1),
            Conv2d(256, 256, kernel_size=3, stride=1, padding=1, residual=True),
            Conv2d(256, 256, kernel_size=3, stride=1, padding=1, residual=True),), # 24, 24

            nn.Sequential(Conv2dTranspose(320, 128, kernel_size=3, stride=2, padding=1, output_padding=1),
            Conv2d(128, 128, kernel_size=3, stride=1, padding=1, residual=True),
            Conv2d(128, 128, kernel_size=3, stride=1, padding=1, residual=True),), # 48, 48

            nn.Sequential(Conv2dTranspose(160, 64, kernel_size=3, stride=2, padding=1, output_padding=1),
            Conv2d(64, 64, kernel_size=3, stride=1, padding=1, residual=True),
            Conv2d(64, 64, kernel_size=3, stride=1, padding=1, residual=True),),]) # 96,96

        self.output_block = nn.Sequential(Conv2d(80, 32, kernel_size=3, stride=1, padding=1),
            nn.Conv2d(32, 3, kernel_size=1, stride=1, padding=0),
            nn.Sigmoid())

        if pitch_ckpt_path:
            self.load_pitch_encoder(pitch_ckpt_path)

    def pitch_modules_requires_grad(self, req=True):
        self.pitch_embed.requires_grad_(req)
        self.pitch_encoder.requires_grad_(req)
        self.pitch_16to1.requires_grad_(req)

    def load_pitch_encoder(self, ckpt_path):
        pitch_ckpt = torch.load(ckpt_path)['state_dict']['model']
        pitch_embed_weight = nn.Parameter(pitch_ckpt['pitch_embed.weight'])
        self.pitch_embed.weight = pitch_embed_weight
        new_dict = {k[14:]: pitch_ckpt[k] for k in pitch_ckpt.keys() if k.startswith('pitch_encoder')}
        self.pitch_encoder.load_state_dict(new_dict)

    def forward(self, audio_sequences, f0, face_sequences):
        '''
        hubert = (B, T, 2, 1024)
        f0 = (B, T, 16)
        face_sequences = (B, 6, T, 96, 96)
        '''
        B = audio_sequences.size(0)
        input_dim_size = len(face_sequences.size())
        if input_dim_size > 4:
            audio_sequences = torch.cat([audio_sequences[:, i] for i in range(audio_sequences.size(1))], dim=0)
            f0 = torch.cat([f0[:, i] for i in range(f0.size(1))], dim=0)
            face_sequences = torch.cat([face_sequences[:, :, i] for i in range(face_sequences.size(2))], dim=0)
        # f0 = torch.mean(f0, dim=1).unsqueeze(-1)

        f0_coarse = f0_to_coarse(f0)
        pitch_emb = self.pitch_embed(f0_coarse)
        pitch_feat = self.pitch_encoder(pitch_emb.transpose(1, 2))  # B 128 16
        pitch_feat = self.pitch_16to1(pitch_feat).unsqueeze(-1)

        audio_embedding = self.audio_encoder(audio_sequences)  # B, 512, 1, 1
        audio_embedding = torch.cat([audio_embedding, pitch_feat], dim=1)
        audio_embedding = self.compose(audio_embedding.squeeze(-1).squeeze(-1)).unsqueeze(-1).unsqueeze(-1)

        feats = []
        x = face_sequences
        for f in self.face_encoder_blocks:
            x = f(x)
            feats.append(x)

        x = audio_embedding
        for f in self.face_decoder_blocks:
            x = f(x)
            try:
                x = torch.cat((x, feats[-1]), dim=1)
            except Exception as e:
                print(x.size())
                print(feats[-1].size())
                raise e

            feats.pop()

        x = self.output_block(x)

        if input_dim_size > 4:
            x = torch.split(x, B, dim=0)  # [(B, C, H, W)]
            outputs = torch.stack(x, dim=2)  # (B, C, T, H, W)

        else:
            outputs = x

        return outputs


class Wav2Lip_disc_qual(nn.Module):
    def __init__(self):
        super(Wav2Lip_disc_qual, self).__init__()

        self.face_encoder_blocks = nn.ModuleList([
            nn.Sequential(nonorm_Conv2d(3, 32, kernel_size=7, stride=1, padding=3)),  # 48,96

            nn.Sequential(nonorm_Conv2d(32, 64, kernel_size=5, stride=(1, 2), padding=2),  # 48,48
                          nonorm_Conv2d(64, 64, kernel_size=5, stride=1, padding=2)),

            nn.Sequential(nonorm_Conv2d(64, 128, kernel_size=5, stride=2, padding=2),  # 24,24
                          nonorm_Conv2d(128, 128, kernel_size=5, stride=1, padding=2)),

            nn.Sequential(nonorm_Conv2d(128, 256, kernel_size=5, stride=2, padding=2),  # 12,12
                          nonorm_Conv2d(256, 256, kernel_size=5, stride=1, padding=2)),

            nn.Sequential(nonorm_Conv2d(256, 512, kernel_size=3, stride=2, padding=1),  # 6,6
                          nonorm_Conv2d(512, 512, kernel_size=3, stride=1, padding=1)),

            nn.Sequential(nonorm_Conv2d(512, 512, kernel_size=3, stride=2, padding=1),  # 3,3
                          nonorm_Conv2d(512, 512, kernel_size=3, stride=1, padding=1), ),

            nn.Sequential(nonorm_Conv2d(512, 512, kernel_size=3, stride=1, padding=0),  # 1, 1
                          nonorm_Conv2d(512, 512, kernel_size=1, stride=1, padding=0)), ])

        self.binary_pred = nn.Sequential(nn.Conv2d(512, 1, kernel_size=1, stride=1, padding=0), nn.Sigmoid())
        self.label_noise = .0

    def get_lower_half(self, face_sequences):
        return face_sequences[:, :, face_sequences.size(2) // 2:]

    def to_2d(self, face_sequences):
        B = face_sequences.size(0)
        face_sequences = torch.cat([face_sequences[:, :, i] for i in range(face_sequences.size(2))], dim=0)
        return face_sequences

    def perceptual_forward(self, false_face_sequences):
        false_face_sequences = self.to_2d(false_face_sequences)
        false_face_sequences = self.get_lower_half(false_face_sequences)

        false_feats = false_face_sequences
        for f in self.face_encoder_blocks:
            false_feats = f(false_feats)

        false_pred_loss = F.binary_cross_entropy(self.binary_pred(false_feats).view(len(false_feats), -1),
                                                 torch.ones((len(false_feats), 1)).cuda())

        return false_pred_loss

    def forward(self, face_sequences):
        face_sequences = self.to_2d(face_sequences)
        face_sequences = self.get_lower_half(face_sequences)

        x = face_sequences
        for f in self.face_encoder_blocks:
            x = f(x)

        return self.binary_pred(x).view(len(x), -1)


if __name__ == '__main__':

    model = PitchLipModel()

    hubert = torch.randn([8, 5, 1024, 16])
    f0 = torch.randn([8, 5, 16])
    face_sequences = torch.randn([8, 6, 5, 96, 96])

    out = model(hubert, f0, face_sequences)
    print(out.shape)


