""" 预处理上传的微调视频，以便训练 """

import os, subprocess, platform
import cv2
import numpy as np
from tqdm import tqdm

from model.module import BatchDetectFace
from model.common import audio
from model.common.hparams import hparams as hp
from model.common.pitch import extract_f0_from_wav_and_mel





if __name__ == '__main__':

    ckpt_path = '../weights/s3fd.pth'
    video_path = '/home/cy/Algo_GenTalkingHead_Based_on_VideoRetalking/test_samples/CEO.mp4'

    tvp = TalkingVideoPreprocess(ckpt_path)

    tvp(video_path, '../tmp')

