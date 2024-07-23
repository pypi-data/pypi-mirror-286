from model.losses.sync_loss import LipSyncLoss
from model.losses.vgg_loss import VGG19PerceptualLoss
from model.losses.arcface_loss import ArcFaceLoss

import torch
from torch.nn import functional as F


def d_loss_func(real, fake):
    loss_real = F.binary_cross_entropy(real, torch.ones((len(real), 1)).to(real.device))
    loss_fake = F.binary_cross_entropy(fake, torch.zeros((len(real), 1)).to(real.device))
    return loss_real + loss_fake


def g_loss_func(fake):
    loss_fake = F.binary_cross_entropy(fake, torch.ones((len(fake), 1)).to(fake.device))
    return loss_fake
