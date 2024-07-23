import cv2
import numpy as np

from model.third_party.GPEN.face_detect.retinaface_detection import RetinaFaceDetection
from model.third_party.GPEN.face_parse.face_parsing import FaceParse
from model.third_party.GPEN.face_model.face_gan import FaceGAN
from model.third_party.GPEN.align_faces import warp_and_crop_face, get_reference_facial_points
from model.common.crop import Laplacian_Pyramid_Blending_with_mask


class FaceEnhancement(object):
    def __init__(self,
                 gpen_ckpt_path,
                 retinaface_ckpt_path,
                 parsenet_ckpt_path,
                 device='cuda'):
        self.srmodel = None
        self.use_sr = False
        self.size = 512
        self.threshold = 0.9

        self.facedetector = RetinaFaceDetection(retinaface_ckpt_path, device)
        self.faceparser = FaceParse(parsenet_ckpt_path, device=device)
        self.facegan = FaceGAN(gpen_ckpt_path, self.size, channel_multiplier=2, narrow=1, device=device)

        # the mask for pasting restored faces back
        self.mask = np.zeros((512, 512), np.float32)
        cv2.rectangle(self.mask, (26, 26), (486, 486), (1, 1, 1), -1, cv2.LINE_AA)
        self.mask = cv2.GaussianBlur(self.mask, (101, 101), 11)
        self.mask = cv2.GaussianBlur(self.mask, (101, 101), 11)

        self.kernel = np.array((
                [0.0625, 0.125, 0.0625],
                [0.125, 0.25, 0.125],
                [0.0625, 0.125, 0.0625]), dtype="float32")

        # get the reference 5 landmarks position in the crop settings
        default_square = True
        inner_padding_factor = 0.25
        outer_padding = (0, 0)
        self.reference_5pts = get_reference_facial_points(
                (self.size, self.size), inner_padding_factor, outer_padding, default_square)

        self.facegan.model.requires_grad = False
        self.faceparser.faceparse.requires_grad = False
        self.facedetector.net.requires_grad = False

    def mask_postprocess(self, mask, thres=20):
        mask[:thres, :] = 0; mask[-thres:, :] = 0
        mask[:, :thres] = 0; mask[:, -thres:] = 0        
        mask = cv2.GaussianBlur(mask, (101, 101), 11)
        mask = cv2.GaussianBlur(mask, (101, 101), 11)
        return mask.astype(np.float32)
    
    def process(self, img, ori_img, bbox=None, face_enhance=True, possion_blending=False):
        if self.use_sr:
            img_sr = self.srmodel.process(img)
            if img_sr is not None:
                img = cv2.resize(img, img_sr.shape[:2][::-1])

        facebs, landms = self.facedetector.detect(img.copy())

        orig_faces, enhanced_faces = [], []
        height, width = img.shape[:2]
        full_mask = np.zeros((height, width), dtype=np.float32)
        full_img = np.zeros(ori_img.shape, dtype=np.uint8)

        for i, (faceb, facial5points) in enumerate(zip(facebs, landms)):
            if faceb[4]<self.threshold: continue
            fh, fw = (faceb[3]-faceb[1]), (faceb[2]-faceb[0])

            facial5points = np.reshape(facial5points, (2, 5))

            of, tfm_inv = warp_and_crop_face(img, facial5points, reference_pts=self.reference_5pts, crop_size=(self.size, self.size))

            # enhance the face
            if face_enhance:
                ef = self.facegan.process(of)
            else:
                ef = of
                    
            orig_faces.append(of)
            enhanced_faces.append(ef)
            
            # print(ef.shape)
            # tmp_mask = self.mask
            '''
            0: 'background' 1: 'skin'   2: 'nose'
            3: 'eye_g'  4: 'l_eye'  5: 'r_eye'
            6: 'l_brow' 7: 'r_brow' 8: 'l_ear'
            9: 'r_ear'  10: 'mouth' 11: 'u_lip'
            12: 'l_lip' 13: 'hair'  14: 'hat'
            15: 'ear_r' 16: 'neck_l'    17: 'neck'
            18: 'cloth'
            '''

            # no ear, no neck, no hair&hat,  only face region
            mm = [0, 255, 255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0]
            mask_sharp = self.faceparser.process(ef, mm)[0]/255.
            tmp_mask = self.mask_postprocess(mask_sharp)
            tmp_mask = cv2.resize(tmp_mask, ef.shape[:2])
            mask_sharp = cv2.resize(mask_sharp, ef.shape[:2])

            tmp_mask = cv2.warpAffine(tmp_mask, tfm_inv, (width, height), flags=3)
            mask_sharp = cv2.warpAffine(mask_sharp, tfm_inv, (width, height), flags=3)

            if min(fh, fw)<100: # gaussian filter for small faces
                ef = cv2.filter2D(ef, -1, self.kernel)
            
            if face_enhance:
                tmp_img = cv2.warpAffine(ef, tfm_inv, (width, height), flags=3)
            else:
                tmp_img = cv2.warpAffine(of, tfm_inv, (width, height), flags=3)

            mask = tmp_mask - full_mask
            full_mask[np.where(mask>0)] = tmp_mask[np.where(mask>0)]
            full_img[np.where(mask>0)] = tmp_img[np.where(mask>0)]

        mask_sharp = cv2.GaussianBlur(mask_sharp, (0,0), sigmaX=1, sigmaY=1, borderType = cv2.BORDER_DEFAULT)

        full_mask = full_mask[:, :, np.newaxis]
        mask_sharp = mask_sharp[:, :, np.newaxis]

        if self.use_sr and img_sr is not None:
            img = cv2.convertScaleAbs(img_sr*(1-full_mask) + full_img*full_mask)
        
        elif possion_blending is True:
            if bbox is not None:
                y1, y2, x1, x2 = bbox
                mask_bbox = np.zeros_like(mask_sharp)
                mask_bbox[y1:y2 - 5, x1:x2] = 1
                full_img, ori_img, full_mask = [cv2.resize(x,(512,512)) for x in (full_img, ori_img, np.float32(mask_sharp * mask_bbox))]
            else:
                full_img, ori_img, full_mask = [cv2.resize(x,(512,512)) for x in (full_img, ori_img, full_mask)]
            
            img = Laplacian_Pyramid_Blending_with_mask(full_img, ori_img, full_mask, 6)
            img = np.clip(img, 0 ,255)
            img = np.uint8(cv2.resize(img, (width, height)))

        else:
            img = cv2.convertScaleAbs(ori_img*(1-full_mask) + full_img*full_mask)
            img = cv2.convertScaleAbs(ori_img*(1-mask_sharp) + img*mask_sharp)

        return img, orig_faces, enhanced_faces

    def process_batch(self, bimg, blandmarks5p):
        _, height, width, _ = bimg.shape
        orig_faces, tfm_invs = [], []
        for img, landmarks5p in zip(bimg, blandmarks5p):
            orig_face, tfm_inv = warp_and_crop_face(img, landmarks5p.T, reference_pts=self.reference_5pts,
                                                    crop_size=(self.size, self.size))
            orig_faces.append(orig_face)
            tfm_invs.append(tfm_inv)
        orig_faces = np.concatenate([orig_face[np.newaxis] for orig_face in orig_faces], axis=0)
        enhanced_faces = self.facegan.process_batch(orig_faces)
        outputs = []
        for enhanced_face, tfm_inv in zip(enhanced_faces, tfm_invs):
            enhanced_face = cv2.warpAffine(enhanced_face, tfm_inv, (width, height), flags=3)
            outputs.append(enhanced_face)
        # print(t2- t1, t3-t2, t4- t3)
        outputs = np.concatenate([output[np.newaxis] for output in outputs], axis=0)
        return outputs

    def blend_batch(self, bimgs, borig_imgs, brects, blandmarks5p):
        _, height, width, _ = bimgs.shape
        bfaces, btfm_inv = [], []

        for img, landmarks5p in zip(bimgs, blandmarks5p):
            face, tfm_inv = warp_and_crop_face(img, landmarks5p.T, reference_pts=self.reference_5pts,
                                               crop_size=(self.size, self.size))
            bfaces.append(face)
            btfm_inv.append(tfm_inv)

        bfaces = np.concatenate([face[np.newaxis] for face in bfaces], axis=0)
        bmask_sharp = self.faceparser.process_batch(bfaces, self.mm) / 255.

        # imgs = []
        # for face, tfm_inv, orig_img, mask_sharp, rect in zip(bfaces, btfm_inv, borig_imgs, bmask_sharp, brects):
        #     full_img = np.zeros(orig_img.shape, dtype=np.uint8)
        #     tmp_mask = self.mask_postprocess(mask_sharp)
        #     tmp_mask = cv2.resize(tmp_mask, face.shape[:2])
        #     mask_sharp = cv2.resize(mask_sharp, face.shape[:2])
        #     tmp_mask = cv2.warpAffine(tmp_mask, tfm_inv, (width, height), flags=3)
        #     mask_sharp = cv2.warpAffine(mask_sharp, tfm_inv, (width, height), flags=3)
        #     tmp_img = cv2.warpAffine(face, tfm_inv, (width, height), flags=3)
        #
        #     # mask = tmp_mask - full_mask
        #     mask = tmp_mask
        #     full_img[np.where(mask>0)] = tmp_img[np.where(mask>0)]
        #     mask_sharp = cv2.GaussianBlur(mask_sharp, (0,0), sigmaX=1, sigmaY=1, borderType=cv2.BORDER_DEFAULT)
        #     mask_sharp = mask_sharp[:, :, np.newaxis]
        #
        #     x1, y1, x2, y2 = rect
        #     mask_bbox = np.zeros_like(mask_sharp)
        #     mask_bbox[y1:y2 - 5, x1:x2] = 1
        #     full_img, ori_img, full_mask = [cv2.resize(x, (512, 512)) for x in
        #                                     (full_img, orig_img, np.float32(mask_sharp * mask_bbox))]
        #     img = Laplacian_Pyramid_Blending_with_mask(full_img, ori_img, full_mask, 6)
        #     img = np.clip(img, 0, 255)
        #     img = np.uint8(cv2.resize(img, (width, height)))
        #     imgs.append(img)

        # inp = [(face, tfm_inv, orig_img, mask_sharp, rect, width, height)
        #        for face, tfm_inv, orig_img, mask_sharp, rect in zip(bfaces, btfm_inv, borig_imgs, bmask_sharp, brects)]
        # print(len(list(zip(inp))))
        b = bfaces.shape[0]
        bheight = [height for _ in range(b)]
        bwidth = [width for _ in range(b)]
        results = self.executor.map(FaceEnhancement._blend, bfaces, btfm_inv, borig_imgs, bmask_sharp, brects, bwidth, bheight)
        imgs, masks = [], []
        for result in results:
            img, mask = result
            imgs.append(img)
            masks.append(mask)
        imgs = np.stack(imgs)
        masks = np.stack(masks)
        return imgs, masks

    @staticmethod
    def _blend(face, tfm_inv, orig_img, mask_sharp, rect, width, height):
        full_img = np.zeros(orig_img.shape, dtype=np.uint8)
        tmp_mask = FaceEnhancement.mask_postprocess(mask_sharp)
        tmp_mask = cv2.resize(tmp_mask, face.shape[:2])
        mask_sharp = cv2.resize(mask_sharp, face.shape[:2])
        tmp_mask = cv2.warpAffine(tmp_mask, tfm_inv, (width, height), flags=3)
        mask_sharp = cv2.warpAffine(mask_sharp, tfm_inv, (width, height), flags=3)
        tmp_img = cv2.warpAffine(face, tfm_inv, (width, height), flags=3)

        mask = tmp_mask
        full_img[np.where(mask > 0)] = tmp_img[np.where(mask > 0)]
        mask_sharp = cv2.GaussianBlur(mask_sharp, (0, 0), sigmaX=1, sigmaY=1, borderType=cv2.BORDER_DEFAULT)
        mask_sharp = mask_sharp[:, :, np.newaxis]

        x1, y1, x2, y2 = rect
        mask_bbox = np.zeros_like(mask_sharp)
        mask_bbox[y1:y2 - 5, x1:x2] = 1
        full_img, ori_img, full_mask = [cv2.resize(x, (512, 512)) for x in
                                        (full_img, orig_img, np.float32(mask_sharp * mask_bbox))]

        # print(mask_sharp.shape, mask_bbox.shape, full_mask.shape)
        img = Laplacian_Pyramid_Blending_with_mask(full_img, ori_img, full_mask, 6)
        img = np.clip(img, 0, 255)
        img = np.uint8(cv2.resize(img, (width, height)))
        full_mask = cv2.resize(full_mask, (width, height))
        return img, full_mask