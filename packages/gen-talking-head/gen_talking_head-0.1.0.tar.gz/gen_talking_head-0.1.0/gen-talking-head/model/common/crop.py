import cv2
import numpy as np
import PIL
from PIL import Image
import scipy
from scipy.ndimage import gaussian_filter1d


def measure_crop_rect_in_video(img, lm, output_size=1024):
    img = Image.fromarray(img) if isinstance(img, np.ndarray) else img
    lm = np.array(lm)
    c, x, y = compute_transform(lm)
    quad = np.stack([c - x - y, c - x + y, c + x + y, c + x - y])
    qsize = np.hypot(*x) * 2
    # Shrink.
    shrink = int(np.floor(qsize / output_size * 0.5))
    if shrink > 1:
        rsize = (int(np.rint(float(img.size[0]) / shrink)), int(np.rint(float(img.size[1]) / shrink)))
        img = img.resize(rsize, Image.ANTIALIAS)
        quad /= shrink
        qsize /= shrink
    # Crop.
    border = max(int(np.rint(qsize * 0.1)), 3)
    outer_rect = (int(np.floor(min(quad[:, 0]))), int(np.floor(min(quad[:, 1]))), int(np.ceil(max(quad[:, 0]))),
             int(np.ceil(max(quad[:, 1]))))
    outer_rect = (max(outer_rect[0] - border, 0), max(outer_rect[1] - border, 0), min(outer_rect[2] + border, img.size[0]),
             min(outer_rect[3] + border, img.size[1]))
    if outer_rect[2] - outer_rect[0] < img.size[0] or outer_rect[3] - outer_rect[1] < img.size[1]:
        quad -= outer_rect[0:2]
    # Transform.
    quad = (quad + 0.5).flatten()
    lx = max(min(quad[0], quad[2]), 0)
    ly = max(min(quad[1], quad[7]), 0)
    rx = min(max(quad[4], quad[6]), img.size[0])
    ry = min(max(quad[3], quad[5]), img.size[0])
    inner_rect = (int(np.floor(lx)), int(np.floor(ly)), int(np.ceil(rx)), int(np.ceil(ry)))

    olx, oly, orx, ory = outer_rect
    ilx, ily, irx, iry = inner_rect
    y1, y2, x1, x2 = oly + ily, min(oly + iry, img.size[1]), olx + ilx, min(olx + irx, img.size[0])
    return x1, y1, x2, y2


def crop_faces(imgs, lms, center_sigma=0.0, xy_sigma=0.0, output_size=1024):
    imgs = [Image.fromarray(img) for img in imgs]

    cs, xs, ys = [], [], []
    for lm in lms:
        c, x, y = compute_transform(lm)
        cs.append(c)
        xs.append(x)
        ys.append(y)
    cs = np.stack(cs)
    xs = np.stack(xs)
    ys = np.stack(ys)
    if center_sigma != 0:
        cs = gaussian_filter1d(cs, sigma=center_sigma, axis=0)
    if xy_sigma != 0:
        xs = gaussian_filter1d(xs, sigma=xy_sigma, axis=0)
        ys = gaussian_filter1d(ys, sigma=xy_sigma, axis=0)
    quads = np.stack([cs - xs - ys, cs - xs + ys, cs + xs + ys, cs + xs - ys], axis=1)
    quads = list(quads)
    crops = []
    for quad, img in zip(quads, imgs):
        crop = crop_image(img, output_size, quad)
        crops.append(crop)
    return crops, quads


def compute_transform(lm, scale=1.0):
    lm = np.array(lm)
    # lm_chin = lm[0: 17]  # left-right
    # lm_eyebrow_left = lm[17: 22]  # left-right
    # lm_eyebrow_right = lm[22: 27]  # left-right
    # lm_nose = lm[27: 31]  # top-down
    # lm_nostrils = lm[31: 36]  # top-down
    lm_eye_left = lm[36: 42]  # left-clockwise
    lm_eye_right = lm[42: 48]  # left-clockwise
    lm_mouth_outer = lm[48: 60]  # left-clockwise
    # lm_mouth_inner = lm[60: 68]  # left-clockwise
    # Calculate auxiliary vectors.
    eye_left = np.mean(lm_eye_left, axis=0)
    eye_right = np.mean(lm_eye_right, axis=0)
    eye_avg = (eye_left + eye_right) * 0.5
    eye_to_eye = eye_right - eye_left
    mouth_left = lm_mouth_outer[0]
    mouth_right = lm_mouth_outer[6]
    mouth_avg = (mouth_left + mouth_right) * 0.5
    eye_to_mouth = mouth_avg - eye_avg
    # Choose oriented crop rectangle.
    x = eye_to_eye - np.flipud(eye_to_mouth) * [-1, 1]
    x /= np.hypot(*x)
    x *= max(np.hypot(*eye_to_eye) * 2.0, np.hypot(*eye_to_mouth) * 1.8)

    x *= scale
    y = np.flipud(x) * [-1, 1]
    c = eye_avg + eye_to_mouth * 0.1
    return c, x, y


def crop_image(filepath, output_size, quad, enable_padding=False):
    x = (quad[3] - quad[1]) / 2
    qsize = np.hypot(*x) * 2
    # read image
    if isinstance(filepath, PIL.Image.Image):
        img = filepath
    else:
        img = PIL.Image.open(filepath)
    transform_size = output_size
    # Shrink.
    shrink = int(np.floor(qsize / output_size * 0.5))
    if shrink > 1:
        rsize = (int(np.rint(float(img.size[0]) / shrink)), int(np.rint(float(img.size[1]) / shrink)))
        img = img.resize(rsize, PIL.Image.ANTIALIAS)
        quad /= shrink
        qsize /= shrink
    # Crop.
    border = max(int(np.rint(qsize * 0.1)), 3)
    crop = (int(np.floor(min(quad[:, 0]))), int(np.floor(min(quad[:, 1]))), int(np.ceil(max(quad[:, 0]))),
            int(np.ceil(max(quad[:, 1]))))
    crop = (max(crop[0] - border, 0), max(crop[1] - border, 0), min(crop[2] + border, img.size[0]),
            min(crop[3] + border, img.size[1]))
    if (crop[2] - crop[0] < img.size[0] or crop[3] - crop[1] < img.size[1]):
        img = img.crop(crop)
        quad -= crop[0:2]
    # Pad.
    pad = (int(np.floor(min(quad[:, 0]))), int(np.floor(min(quad[:, 1]))), int(np.ceil(max(quad[:, 0]))),
           int(np.ceil(max(quad[:, 1]))))
    pad = (max(-pad[0] + border, 0), max(-pad[1] + border, 0), max(pad[2] - img.size[0] + border, 0),
           max(pad[3] - img.size[1] + border, 0))
    if enable_padding and max(pad) > border - 4:
        pad = np.maximum(pad, int(np.rint(qsize * 0.3)))
        img = np.pad(np.float32(img), ((pad[1], pad[3]), (pad[0], pad[2]), (0, 0)), 'reflect')
        h, w, _ = img.shape
        y, x, _ = np.ogrid[:h, :w, :1]
        mask = np.maximum(1.0 - np.minimum(np.float32(x) / pad[0], np.float32(w - 1 - x) / pad[2]),
                          1.0 - np.minimum(np.float32(y) / pad[1], np.float32(h - 1 - y) / pad[3]))
        blur = qsize * 0.02
        img += (scipy.ndimage.gaussian_filter(img, [blur, blur, 0]) - img) * np.clip(mask * 3.0 + 1.0, 0.0, 1.0)
        img += (np.median(img, axis=(0, 1)) - img) * np.clip(mask, 0.0, 1.0)
        img = PIL.Image.fromarray(np.uint8(np.clip(np.rint(img), 0, 255)), 'RGB')
        quad += pad[:2]
    # Transform.
    img = img.transform((transform_size, transform_size), PIL.Image.QUAD, (quad + 0.5).flatten(), PIL.Image.BILINEAR)
    if output_size < transform_size:
        img = img.resize((output_size, output_size), PIL.Image.ANTIALIAS)
    return img


def Laplacian_Pyramid_Blending_with_mask(A, B, m, num_levels = 6):
    # generate Gaussian pyramid for A,B and mask
    GA = A.copy()
    GB = B.copy()
    GM = m.copy()
    gpA = [GA]
    gpB = [GB]
    gpM = [GM]
    for i in range(num_levels):
        GA = cv2.pyrDown(GA)
        GB = cv2.pyrDown(GB)
        GM = cv2.pyrDown(GM)
        gpA.append(np.float32(GA))
        gpB.append(np.float32(GB))
        gpM.append(np.float32(GM))

    # generate Laplacian Pyramids for A,B and masks
    lpA  = [gpA[num_levels-1]] # the bottom of the Lap-pyr holds the last (smallest) Gauss level
    lpB  = [gpB[num_levels-1]]
    gpMr = [gpM[num_levels-1]]
    for i in range(num_levels-1,0,-1):
        # Laplacian: subtract upscaled version of lower level from current level
        # to get the high frequencies
        LA = np.subtract(gpA[i-1], cv2.pyrUp(gpA[i]))
        LB = np.subtract(gpB[i-1], cv2.pyrUp(gpB[i]))
        lpA.append(LA)
        lpB.append(LB)
        gpMr.append(gpM[i-1]) # also reverse the masks

    # Now blend images according to mask in each level
    LS = []
    for la,lb,gm in zip(lpA,lpB,gpMr):
        gm = gm[:,:,np.newaxis]
        ls = la * gm + lb * (1.0 - gm)
        LS.append(ls)

    # now reconstruct
    ls_ = LS[0]
    for i in range(1,num_levels):
        ls_ = cv2.pyrUp(ls_)
        ls_ = cv2.add(ls_, LS[i])
    return ls_
