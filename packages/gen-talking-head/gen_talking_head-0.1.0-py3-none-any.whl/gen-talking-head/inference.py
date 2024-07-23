import os
import cv2
import numpy as np
from PIL import Image
from typing import List, Tuple
from tqdm import tqdm
import subprocess, platform
from model.common import audio
from model.common.crop import crop_faces, measure_crop_rect_in_video
from model.common.pitch import extract_f0_from_wav_and_mel
from model.common.hparams import hparams as hp
from model.module import BatchDetectFace, BatchDetectLandmarks, BatchSynthesizeLip, PasteFace
from tools.common import load_yaml


class AudioDrivenTalkingHeadInference(object):

    def __init__(self, cfg_path='config/base.yaml', lang='ZH', batch_size: int = 8):
        self.device = 'cuda'
        self.ref_size = 256
        self.lang = lang
        self.batch_size = batch_size
        # 加载模型
        self.cfg = load_yaml(cfg_path)
        model_path = self.cfg['pre_trained_model']
        self._synthesize_lip = BatchSynthesizeLip(
            lnet_ckpt_path=model_path['pitchlip'][lang], enet_ckpt_path=model_path['enet'],
            device=self.device)
        self._detect_face = BatchDetectFace(ckpt_path=model_path['s3fd'], device=self.device)
        self._detect_landmarks = BatchDetectLandmarks(device=self.device)
        self._paste_face = PasteFace(
            image_portrait_enhancement_model_path=model_path['image_portrait_enhancement'],
            gfpgan_ckpt_path=model_path['gfpgan'], gpen_ckpt_path=model_path['gpen'],
            retinaface_ckpt_path=model_path['retinaface'], parsenet_ckpt_path=model_path['parsenet'],
            device=self.device)

        self._init_cache()

    def __call__(self, video_path: str, audio_path: str, output_folder: str):
        self._init_cache()
        frames, mel_chunks, f0_chunks = zip(*list(self._yield_frame_and_mel(video_path, audio_path)))
        patches, crop_rects = self._crop_videos(frames, step=int(round(self.fps * 0.2)))

        patches_gen = []
        self.pbar = tqdm(total=self.nframes)
        for valid, scope, cur_rects, cur_landmarks in self._detect(patches):
            i, j = scope
            cur_patches = patches[i: j]
            cur_mel_chunks = mel_chunks[i: j]
            cur_f0_chunks = f0_chunks[i: j]
            patches_gen.extend(self._synthesize(cur_patches, cur_rects, cur_landmarks, cur_mel_chunks, cur_f0_chunks))
        frames_gen = self._blend_into_frames(frames, patches_gen, crop_rects)
        output_path = self._write_mp4(frames=frames_gen, audio_path=audio_path, output_folder=output_folder,
                                      fps=self.fps)
        return output_path

    def update_lnet_parameters(self, lnet_parameters_path: str):
        """ 更新lnet微调参数 """
        self._synthesize_lip.update_lnet(lnet_parameters_path)
        print('update lnet parameters from: {}'.format(lnet_parameters_path))

    def _init_cache(self):
        # TODO 暂时用成员变量做缓存，不支持单例；
        self.fps = 25.
        self.nframes = 0
        self.nfinished = 0

    def _crop_videos(self, frames, step: int = 25):
        """ 剪切视频区域，减少人脸检测计算代价
            通常人脸移动速度有限，为了减少计算代价此处按步长检测人脸
        """
        self.nframes = len(frames)
        H, W = frames[0].shape[:2]
        last_crop_rect = (0, 0, W, H)
        patches, crop_rects = [], []
        for idx in range(len(frames) // step + 1):
            if idx * step < len(frames):
                cur_frames = frames[idx * step:(idx + 1) * step]
                cur_patches, crop_rect = self._crop_frames(cur_frames, last_crop_rect=last_crop_rect)
                patches.extend(cur_patches)
                crop_rects.extend([crop_rect] * len(cur_patches))
                last_crop_rect = crop_rect
        return patches, crop_rects

    def _detect(self, patches, smooth_kernel_size=11, smooth_limit=3):
        """ 人脸框及关键点检测
            以人脸消失/出现的帧作为切点，将视频帧依次切分成N段；迭代以输出每段的检测结果
            input:
                patches:
                smooth_kernel_size:
                smooth_limit:
            yield:
                has_face:
                scope:
                rects
                landmarks:
        """

        def smooth_h(rects, smooth_kernel_size: int, smooth_limit: int):
            rects = rects if isinstance(rects, np.ndarray) else np.asarray(rects)
            margin, kernel = int(smooth_kernel_size) // 2, np.ones(smooth_kernel_size) / smooth_kernel_size
            if len(rects) > smooth_kernel_size:
                # delta_ly = np.convolve(rects[:, 1], kernel, 'valid') - rects[margin: -margin, 1]
                # rects[margin: -margin, 1] = rects[margin: -margin, 1] + np.clip(delta_ly, -smooth_limit, smooth_limit)
                # 减少rect高度可能导致生成图像崩坏；ry增加（patch_size=256时的相对值）以避免崩坏问题
                rects[margin: -margin, 3] = np.convolve(rects[:, 3], kernel, 'valid') + 3
                pass
            return rects

        patches = np.asarray(patches)
        rects, landmarks = [], []
        for idx in range(len(patches) // self.batch_size + 1):
            if idx * self.batch_size < len(patches):
                bpatches = patches[idx * self.batch_size: (idx + 1) * self.batch_size]
                brects = self._detect_face(bpatches)
                blandmarks = self._detect_landmarks(bpatches, brects)
                rects.extend(brects)
                landmarks.extend(blandmarks)
        # 此处切分没有人脸的片段
        cur_head, cur_rear = 0, 0
        for idx, rect in enumerate(rects):
            if rect is None:
                if cur_rear > cur_head:
                    loc_landmarks = np.asarray(landmarks[cur_head: cur_rear])
                    # 原视频说话时下巴开闭导致人脸框高度不稳定；直接按人脸框帖回五官会抖动，此处平滑人脸框Y轴坐标
                    loc_rects = smooth_h(rects[cur_head: cur_rear], smooth_kernel_size, smooth_limit)
                    scope = (cur_head, cur_rear)
                    yield True, scope, loc_rects, loc_landmarks
                cur_head = idx + 1
            else:
                if cur_head > cur_rear:
                    scope = (cur_rear, cur_head)
                    yield False, scope, None, None
                cur_rear = idx + 1
        if cur_rear > cur_head:
            loc_landmarks = np.asarray(landmarks[cur_head: cur_rear])
            loc_rects = smooth_h(rects[cur_head: cur_rear], smooth_kernel_size, smooth_limit)
            scope = (cur_head, cur_rear)
            yield True, scope, loc_rects, loc_landmarks
        else:
            scope = (cur_rear, cur_head)
            yield False, scope, None, None

    def _synthesize(self, patches, rects, landmarks, mel_chunks, f0_chunks):
        patches_gen = []
        if not (rects is None or landmarks is None):
            for bpatches, brects, blandmarks, bmel_chunks, bf0_chunks in _yield_batch(
                    patches, rects, landmarks, mel_chunks, f0_chunks, self.batch_size):
                bpatches_gen = self._get_synthesize_faces(bpatches, brects, blandmarks, bmel_chunks, bf0_chunks)
                patches_gen.extend(bpatches_gen)
                self.nfinished += len(bpatches_gen)
                self.pbar.update(len(bpatches_gen))
        else:
            patches_gen = patches
            self.nfinished += len(patches_gen)
            self.pbar.update(len(patches_gen))
        return patches_gen

    def _write_mp4(self, frames, audio_path: str, output_folder: str, fps: float = 25.):
        os.makedirs(output_folder, exist_ok=True)
        H, W = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        gen_path = os.path.join(output_folder, 'gen.mp4')
        result_path = os.path.join(output_folder, 'result.mp4')
        writer = cv2.VideoWriter(gen_path, fourcc, fps, (W, H))
        for frame in frames:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            writer.write(frame)
        writer.release()
        command = 'ffmpeg -loglevel error -y -i {} -i {} -strict -2 -q:v 1 {}'.format(audio_path, gen_path, result_path)
        subprocess.call(command, shell=platform.system() != 'Windows')
        return result_path

    def _get_synthesize_faces(self, bpatches, brects, blandmarks, bmel_chunks, bf0_chunks):
        brefs = _wrap_reference(bpatches, brects, blandmarks, image_size=self.ref_size)
        bmels = np.reshape(bmel_chunks, [len(bmel_chunks), bmel_chunks.shape[1], bmel_chunks.shape[2], 1])
        bfaces_synt = self._synthesize_lip(brefs, bmels, bf0_chunks)
        return self._paste_face(bpatches, bfaces_synt, brects, enhancer_region='full')

    def _blend_into_frames(self, frames, patches, crop_rects):
        frames = [_blend_full_frame(frame, patch, rect) for frame, patch, rect in zip(frames, patches, crop_rects)]
        return frames

    def _yield_frame_and_mel(self, video_path: str, audio_path: str):
        """ 由于视频和音频可能体量过大，此处采用生成器读取
            “目标音频”长度若超过“源视频”，则“源视频”从头循环以匹配超出部分；
        """
        assert os.path.exists(video_path), 'video path does not exist'
        assert os.path.exists(audio_path), 'audio path does not exist'

        stream = cv2.VideoCapture(video_path)
        if video_path.endswith('.jpeg') or video_path.endswith('.jpg') or video_path.endswith('.png'):
            self.fps = 25
            nframes = 1
        else:
            self.fps = stream.get(cv2.CAP_PROP_FPS)
            nframes = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
        if nframes >= 1:
            wav = audio.load_wav(audio_path, hp.sample_rate)
            mel = audio.melspectrogram(wav)
            f0 = extract_f0_from_wav_and_mel(
                wav, mel.T, hop_size=hp.hop_size, audio_sample_rate=hp.sample_rate)
            # TODO 根据超参计算
            mel_step_size, mel_idx_multiplier, i = 16, 80. / self.fps, 0
            flag = True
            while flag:
                still_reading, frame = stream.read()
                if not still_reading:
                    stream.release()
                    stream = cv2.VideoCapture(video_path)
                    continue
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                start_idx = int(i * mel_idx_multiplier)
                if start_idx + mel_step_size >= len(mel[0]) or start_idx >= len(mel[0]) - 1:
                    stream.release()
                    break
                mel_chunk = mel[:, start_idx: start_idx + mel_step_size]
                f0_chunk = f0[start_idx: start_idx + mel_step_size]
                yield frame, mel_chunk, f0_chunk
                i += 1

    def _crop_frames(self, frames: List[np.ndarray] or np.ndarray, last_crop_rect=None) -> (Tuple, Tuple):
        if not isinstance(frames, list) and not isinstance(frames, tuple):
            frames = [frames]
        H, W = frames[0].shape[:2]
        crop_rect = None
        for frame in frames:
            landmarks = self._detect_landmarks.detect_single(frame)
            if not (np.mean(landmarks) == -1 or landmarks is None):
                crop_rect = measure_crop_rect_in_video(frame, landmarks, output_size=self.ref_size * 2)
                break

        if crop_rect is None:
            if last_crop_rect is None:
                return None, None
            else:
                crop_rect = last_crop_rect
        x1, y1, x2, y2 = crop_rect
        cropped_frames = []
        for frame in frames:
            try:
                cropped_frames.append(cv2.resize(frame[y1: y2, x1: x2], (self.ref_size, self.ref_size)))
            except:
                print('crop frame err:', frame.shape, crop_rect)
                cropped_frames = None
                crop_rect = None
        return cropped_frames, crop_rect


def _blend_full_frame(frame, patch, crop_rect):
    H, W = frame.shape[:2]
    x1, y1, x2, y2 = crop_rect
    patch = cv2.resize(patch, (x2 - x1, y2 - y1))
    tmp_frame = frame.copy()
    tmp_frame[y1:y2, x1:x2] = patch
    return tmp_frame


def _yield_batch(patches, rects, landmarks, mel_chunks, f0_chunks, batch_size=8):
    for idx in range(len(patches) // batch_size + 1):
        if idx * batch_size < len(patches):
            bpatches = np.asarray(patches[idx * batch_size: (idx + 1) * batch_size])
            brects = np.asarray(rects[idx * batch_size: (idx + 1) * batch_size])
            blandmarks = np.asarray(landmarks[idx * batch_size: (idx + 1) * batch_size])
            bmel_chunks = np.asarray(mel_chunks[idx * batch_size: (idx + 1) * batch_size])
            bf0_chunks = np.asarray(f0_chunks[idx * batch_size: (idx + 1) * batch_size])
            yield bpatches, brects, blandmarks, bmel_chunks, bf0_chunks
        else:
            break


def _wrap_reference(bframes, brects, blandmarks, image_size=256):
    crops, quads = crop_faces(bframes, blandmarks, output_size=image_size)
    inverse_transforms = [
        calc_alignment_coefficients(quad + 0.5, [[0, 0], [0, image_size], [image_size, image_size], [image_size, 0]])
        for quad in quads]
    brefs = []
    for inverse_transform, crop, full_frame, coords in zip(inverse_transforms, crops, bframes, brects):
        imc_pil = paste_image(inverse_transform, crop, Image.fromarray(cv2.resize(full_frame, (image_size, image_size))))
        H, W = full_frame.shape[:2]
        x1, y1, x2, y2 = coords

        # print(x1, y1, x2, y2)
        face_stab = cv2.resize(np.array(imc_pil.convert('RGB')), (W, H))[y1: y2, x1: x2]
        oface = full_frame[y1: y2, x1: x2]
        face_stab = cv2.resize(face_stab, (image_size, image_size))
        oface = cv2.resize(oface, (image_size, image_size))
        ref = oface.copy()
        oface[image_size // 2:] = 0
        ref = np.concatenate((oface, ref, ref), axis=2) / 255
        brefs.append(ref)
    brefs = np.asarray(brefs)
    return np.asarray(brefs)


def calc_alignment_coefficients(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
    a = np.matrix(matrix, dtype=float)
    b = np.array(pb).reshape(8)
    res = np.dot(np.linalg.inv(a.T * a) * a.T, b)
    return np.array(res).reshape(8)


def paste_image(inverse_transform, img, orig_image):
    pasted_image = orig_image.copy().convert('RGBA')
    projected = img.convert('RGBA').transform(orig_image.size, Image.PERSPECTIVE, inverse_transform, Image.BILINEAR)
    pasted_image.paste(projected, (0, 0), mask=projected)
    return pasted_image


if __name__ == '__main__':
    inference = AudioDrivenTalkingHeadInference('./config/base.yaml')
    inference.update_lnet_parameters('/tmp/tmptus8e830/checkpoint_step000002500.pth')
    video_path = '/home/czz/Algo_GenTalkingHead_Inference-4090/test_samples/QHFTBaiQiuEn1_1.mp4'
    audio_path = '/home/czz/Algo_GenTalkingHead_Inference-4090/test_samples/output_CN_speaker2.wav'
    frames = inference(video_path, audio_path, '../test_samples/QHFTBaiQiuEn1_cn')
