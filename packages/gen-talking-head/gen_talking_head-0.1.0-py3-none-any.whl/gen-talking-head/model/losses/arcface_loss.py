
# refer to https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch
# weight download from https://pan.baidu.com/s/1CL-l4zWqsI1oDuEEYVhj-g  pwd=e8pw
import torch
import torch.nn as nn
import torch.nn.functional as F

from model.losses.iresnet import iresnet100


class ArcFaceLoss(nn.Module):

    def __init__(self, checkpoint_path=None):
        super(ArcFaceLoss, self).__init__()
        self.backbone = iresnet100()

        if checkpoint_path:
            self.backbone.load_state_dict(torch.load(checkpoint_path))

        for p in self.parameters():
            p.requires_grad = False

    def feature_loss(self, x):
        return (x[:x.shape[0] // 2] - x[x.shape[0] // 2:]).pow(2).mean()

    def forward(self, x: torch.Tensor):
        x = F.interpolate(x, (112, 112), mode='bilinear')
        x = x.sub_(0.5).div_(0.5)
        x = self.backbone(x)
        return self.feature_loss(x)








