""" 图像检测和处理模块 """

import cv2
import torch
import numpy as np
from face_alignment import FaceAlignment, LandmarksType
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

from model.common.crop import Laplacian_Pyramid_Blending_with_mask
from model.third_party.face_detection.detection.sfd.sfd_detector import SFDDetector as FaceDetector
from model.third_party.GFPGAN.gfpgan import GFPGANer
from model.third_party.GPEN.gpen_face_enhancer import FaceEnhancement
from model.net.wav2lip_with_pitch import PitchLipModel
from model.net.Enet_pitch import ENetPitch


class BatchDetectFace(object):

    def __init__(self, ckpt_path='s3fd.pth', device='cuda'):
        self._detector = FaceDetector(device=device, path_to_detector=ckpt_path)
        print('Initialized s3fd from: {}.'.format(ckpt_path))

    def __call__(self, bimgs, pad=(0, 0, 0, 0)):
        _, h, w, _ = bimgs.shape
        # TODO 暂时只取第一个人脸框
        detected_faces = self._detector.detect_from_batch(bimgs)
        results = []
        for i, d in enumerate(detected_faces):
            if len(d) == 0:
                results.append(None)
                continue
            d = d[0]
            x1, y1, x2, y2 = map(int, d[:-1])
            x1 = max(0, x1 + pad[0])
            y1 = max(0, y1 + pad[1])
            x2 = min(w, x2 + pad[2])
            y2 = min(h, y2 + pad[3])
            results.append((x1, y1, x2, y2))
        return results


class BatchDetectLandmarks(object):

    def __init__(self, device='cuda'):
        self._face_alignment = FaceAlignment(LandmarksType.TWO_D, device=device)

    def __call__(self, bimgs, brects=None):
        blandmarks = []
        for img_np, rect in zip(bimgs, brects):
            blandmarks.append(self.detect_single(img_np, rect))
        return blandmarks

    def detect_single(self, img_np, rect=None):
        if rect is not None:
            rect = [rect]
        lm = self._face_alignment.get_landmarks_from_image(img_np, detected_faces=rect)
        if lm is None or len(lm) == 0:
            return -1. * np.ones([68, 2])
        else:
            lm = lm[0]
            if lm.shape != (68, 2):
                return -1. * np.ones([68, 2])
        return lm


class BatchSynthesizeLip(object):

    def __init__(self, lnet_ckpt_path, enet_ckpt_path, device='cuda'):
        self.device = device
        self.model = self.load_model(lnet_ckpt_path, enet_ckpt_path).to(self.device)
        self.model.requires_grad = False
        print('Initialized wav2lip_pitch from: {}.'.format(lnet_ckpt_path))
        print('Initialized ENet from: {}.'.format(enet_ckpt_path))

    def __call__(self, brefs: np.ndarray, bmels, bf0) -> np.ndarray:
        brefs = torch.FloatTensor(np.transpose(brefs, (0, 3, 1, 2)))
        bmels = torch.FloatTensor(np.transpose(bmels, (0, 3, 1, 2)))
        brefs = brefs.to(self.device)
        bmels = bmels.to(self.device)
        bf0 = torch.FloatTensor(bf0).to(self.device)

        with torch.no_grad():
            brefs = brefs[:, [2, 1, 0, 5, 4, 3, 8, 7, 6]]
            mask_ref, id_ref, stab_ref = torch.split(brefs, 3, dim=1)
            brefs = torch.cat((mask_ref, id_ref), dim=1)

            pred, low_res = self.model(bmels, bf0, brefs, stab_ref)
            pred = torch.clamp(pred, 0, 1)
        pred = np.uint8(pred[:, [2, 1, 0]].permute(0, 2, 3, 1).cpu().clamp_(0, 1).numpy() * 255)
        return pred

    def load_model(self, pitchlip_ckpt_path, enet_ckpt_path):
        pitch_lip_model = PitchLipModel().eval()
        checkpoint = torch.load(pitchlip_ckpt_path)
        state_dict = {k.replace('net.', ''): v for k, v in checkpoint["state_dict"].items()
                      if k.startswith('net.')}
        pitch_lip_model.load_state_dict(state_dict)

        E_net = ENetPitch(lnet=pitch_lip_model)
        checkpoint = torch.load(enet_ckpt_path)
        state_dict = {k.replace('module.', ''): v for k, v in checkpoint["state_dict"].items()
                      if 'low_res' not in k}
        E_net.load_state_dict(state_dict, strict=False)
        return E_net

    def update_lnet(self, pitchlip_ckpt_path):
        self.model.low_res.load_state_dict(torch.load(pitchlip_ckpt_path))


class PasteFace(object):

    def __init__(self,
                 image_portrait_enhancement_model_path,
                 gfpgan_ckpt_path,
                 gpen_ckpt_path,
                 retinaface_ckpt_path,
                 parsenet_ckpt_path,
                 device='cuda'):
        self.portrait_enhancement = pipeline(Tasks.image_portrait_enhancement, model=image_portrait_enhancement_model_path)
        # self.restorer = GFPGANer(
        #     model_path=gfpgan_ckpt_path, upscale=1, arch='clean', channel_multiplier=2, bg_upsampler=None)
        print('Initialized GFPGAN from: {}.'.format(gfpgan_ckpt_path))
        self.enhancer = FaceEnhancement(
            gpen_ckpt_path, retinaface_ckpt_path, parsenet_ckpt_path, device=device)
        print('Initialized GPEN from: {}.'.format(gpen_ckpt_path))
        print('Initialized Retinaface from: {}.'.format(retinaface_ckpt_path))
        print('Initialized ParseNet from: {}.'.format(parsenet_ckpt_path))

    def __call__(self, full_img_list, crop_frames, crop_rects, enhancer_region='full'):
        pics = []
        for index, crop_frame in enumerate(crop_frames):
            ff = full_img_list[index].copy()
            clx, cly, crx, cry = crop_rects[index]
            p = cv2.resize(crop_frame.astype(np.uint8), (crx - clx, cry - cly))
            ff[cly:cry, clx:crx] = p
            if enhancer_region == 'none':
                pp = ff
            else:
                # 此处修复导致形象和色调失真严重，不再调用该处理
                # cropped_faces, restored_faces, restored_img = self.restorer.enhance(
                #     ff, has_aligned=False, only_center_face=True, paste_back=True)
                restored_img = ff
                if enhancer_region == 'lip':
                    mm = [0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0]
                else:
                    mm = [0, 255, 255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0]

                mouse_mask = self.enhancer.faceparser.process(restored_img, mm)[0] / 255
                height, width = ff.shape[:2]
                restored_img, ff, full_mask = [
                    cv2.resize(x, (512, 512)) for x in(restored_img, ff, np.float32(mouse_mask))]
                img = Laplacian_Pyramid_Blending_with_mask(restored_img, ff, full_mask, 10)
                pp = np.uint8(cv2.resize(np.clip(img, 0, 255), (width, height)))
                try:
                    pp, orig_faces, enhanced_faces = self.enhancer.process(pp, full_img_list[index], bbox=[cly, cry, clx, crx],
                                                                      face_enhance=False, possion_blending=True)
                except:
                    # TODO: 异常原因及备用处理
                    pass

                pp_enh = self.portrait_enhancement(pp)[OutputKeys.OUTPUT_IMG]
                pp_enh = cv2.resize(pp_enh, (width, height))
                mouse_mask = cv2.resize(mouse_mask, (width, height))
                pp[np.where(mouse_mask == 1)] = pp_enh[np.where(mouse_mask == 1)]

            pics.append(pp)
        return np.asarray(pics)

