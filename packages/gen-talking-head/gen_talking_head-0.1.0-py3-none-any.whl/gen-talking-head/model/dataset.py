""" 微调数据集 """

import os, subprocess, platform
import shutil
import cv2
import numpy as np
import random
from glob import glob
from tqdm import tqdm
import tempfile

import torch
from torch.utils.data import Dataset

from model.module import BatchDetectFace
import model.common.audio as audio
from model.common.hparams import hparams as hp
from model.common.pitch import extract_f0_from_wav_and_mel
from tools.common import load_yaml


class PitchLipSyncDataset(Dataset):

    def __init__(self, video_path, cfg, out_dir=None):
        self.cfg = load_yaml(cfg) if isinstance(cfg, str) else cfg
        s3fd_ckpt_path = self.cfg['pre_trained_model']['s3fd']
        self.preprocessor = TalkingVideoPreprocess(s3fd_ckpt_path)

        out_dir = tempfile.mktemp(dir=self.cfg['cache_dir']) if out_dir is None else out_dir
        self.out_dir = os.path.join(out_dir, 'preprocessed')
        print('Preprocessed data would save to: {}.'.format(self.out_dir))
        self.preprocessor(video_path, self.out_dir)

    def __getitem__(self, idx):

        while 1:
            img_names = list(glob(os.path.join(self.out_dir, '*.jpg')))
            if len(img_names) <= 3 * hp.syncnet_T:
                continue

            img_name = random.choice(img_names)
            wrong_img_name = random.choice(img_names)
            while wrong_img_name == img_name:
                wrong_img_name = random.choice(img_names)

            window_fnames = self.get_window(img_name)
            wrong_window_fnames = self.get_window(wrong_img_name)
            if window_fnames is None or wrong_window_fnames is None:
                continue

            window = self.read_window(window_fnames, img_size=hp.img_size)
            if window is None:
                continue

            wrong_window = self.read_window(wrong_window_fnames, img_size=hp.img_size)
            if wrong_window is None:
                continue

            try:
                mel_and_f0 = np.load(os.path.join(self.out_dir, 'mel_and_f0.npz'))
                orig_mel = mel_and_f0['mel']
                f0 = mel_and_f0['f0']

            except Exception as e:
                continue

            mel = self.crop_audio_window(orig_mel.copy(), img_name)

            if mel.shape[0] != hp.syncnet_mel_step_size:
                continue

            indiv_mels, indiv_f0 = self.get_segmented_mels_and_f0(orig_mel.copy(), f0.copy(), img_name)
            if indiv_mels is None:
                continue

            window = self.prepare_window(window)
            y = window.copy()
            window[:, :, window.shape[2] // 2:] = 0.

            wrong_window = self.prepare_window(wrong_window)
            x = np.concatenate([window, wrong_window], axis=0)

            x = torch.FloatTensor(x)
            mel = torch.FloatTensor(mel.T).unsqueeze(0)
            indiv_mels = torch.FloatTensor(indiv_mels).unsqueeze(1)
            indiv_f0 = torch.FloatTensor(indiv_f0)
            y = torch.FloatTensor(y)
            return x, indiv_mels, indiv_f0, mel, y

    def __len__(self):
        return 99999999

    # def __del__(self):
    #     shutil.rmtree(self.out_dir)ß

    def get_frame_id(self, frame):
        return int(os.path.basename(frame).split('.')[0])

    def get_window(self, start_frame):
        start_id = self.get_frame_id(start_frame)
        vidname = os.path.dirname(start_frame)
        window_fnames = []
        for frame_id in range(start_id, start_id + hp.syncnet_T):
            frame = os.path.join(vidname, '{}.jpg'.format(frame_id))
            if not os.path.isfile(frame):
                return None
            window_fnames.append(frame)
        return window_fnames

    def read_window(self, window_fnames, img_size):
        if window_fnames is None: return None
        window = []
        for fname in window_fnames:
            img = cv2.imread(fname)
            if img is None:
                return None
            try:
                img = cv2.resize(img, (img_size, img_size))
            except Exception as e:
                return None
            window.append(img)
        return window

    def crop_audio_window(self, spec, start_frame, step=hp.syncnet_mel_step_size):
        if type(start_frame) == int:
            start_frame_num = start_frame
        else:
            start_frame_num = self.get_frame_id(start_frame)  # 0-indexing ---> 1-indexing
        # TODO 80
        start_idx = int(80 * (start_frame_num / float(hp.fps)))
        end_idx = start_idx + step
        return spec[start_idx: end_idx]

    def get_segmented_mels_and_f0(self, mel, f0, start_frame):
        mels, sf0 = [], []
        start_frame_num = self.get_frame_id(start_frame) + 1  # 0-indexing ---> 1-indexing
        if start_frame_num - 2 < 0: return None, None
        for i in range(start_frame_num, start_frame_num + hp.syncnet_T):
            m = self.crop_audio_window(mel, i - 2)
            f = self.crop_audio_window(f0, i - 2)
            if m.shape[0] != hp.syncnet_mel_step_size or f.shape[0] != hp.syncnet_mel_step_size:
                return None, None
            mels.append(m.T)
            sf0.append(f)
        mels = np.asarray(mels)
        sf0 = np.asarray(sf0)
        return mels, sf0

    def prepare_window(self, window):
        # 3 x T x H x W
        x = np.asarray(window) / 255.
        x = np.transpose(x, (3, 0, 1, 2))
        return x


class TalkingVideoPreprocess(object):

    def __init__(self, ckpt_path, batch_size=8, device='cuda'):
        """
        :param ckpt_path: s3fd.pth
        :param batch_size:
        :param device:
        """
        self.ckpt_path = ckpt_path
        self.batch_size = batch_size
        self.device = device
        self._detect_face = BatchDetectFace(ckpt_path=self.ckpt_path, device=self.device)

    def __call__(self, video_path, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        audio_path = extract_audio_from_video(video_path, output_dir)
        _ = extract_f0(audio_path, output_dir)

        nframes, nfaces = 0, 0
        for i, image in enumerate(self._get_face_images(video_path)):
            if image is not None:

                save_path = os.path.join(output_dir, '{}.jpg'.format(i))
                cv2.imwrite(save_path, image)
                nfaces += 1
            nframes += 1
        if nfaces / nframes <= 0.7:
            raise AssertionError('Video has too many frames without faces.')

    def _get_face_images(self, video_path):
        def _to_faces(bframes):
            brects = self._detect_face(np.asarray(bframes))
            for i, rect in enumerate(brects):
                if rect is None:
                    yield None
                x1, y1, x2, y2 = rect
                # y2 += int(round(0.02 * (y2 - y1)))  # 略微扩展下巴
                yield bframes[i][y1:y2, x1:x2].copy()

        video_stream = cv2.VideoCapture(video_path)
        nframes = int(video_stream.get(cv2.CAP_PROP_FRAME_COUNT))
        pbar = tqdm(total=nframes)
        bframes = []
        while 1:
            still_reading, frame = video_stream.read()
            if not still_reading:
                video_stream.release()
                break
            pbar.update(1)
            bframes.append(frame)
            if len(bframes) == self.batch_size:
                yield from _to_faces(bframes)
                bframes = []

        if len(bframes) > 0:
            yield from _to_faces(bframes)


def extract_audio_from_video(video_path, output_dir):
    output_path = os.path.join(output_dir, 'audio.wav')
    command = 'ffmpeg -loglevel error -y -i {} -ar 16000 -strict -2 {}'.format(video_path, output_path)
    subprocess.call(command, shell=platform.system() != 'Windows')
    return output_path


def extract_f0(audio_path, output_dir):
    output_path = os.path.join(output_dir, 'mel_and_f0.npz')
    wav = audio.load_wav(audio_path, hp.sample_rate)
    mel = audio.melspectrogram(wav).T
    f0 = extract_f0_from_wav_and_mel(
        wav, mel, hop_size=hp.hop_size, audio_sample_rate=hp.sample_rate)
    np.savez(output_path, mel=mel, f0=f0)
    return output_path


if __name__ == '__main__':
    video_path = '/home/cy/Algo_GenTalkingHead_Based_on_VideoRetalking/test_samples/CEO.mp4'

    dataset = PitchLipSyncDataset(video_path, '../config/base.yaml')

    iter = iter(dataset)
    x, indiv_mels, indiv_f0, mel, y = next(iter)
    print(x.shape)
    print(indiv_mels.shape)
    print(indiv_f0.shape)
    print(mel.shape)
    print(y.shape)
