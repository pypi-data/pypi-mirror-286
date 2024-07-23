import os.path

import torch.nn as nn
import torch


class VGG19PerceptualLoss(nn.Module):
    """
     Simplified version of the VGG19 "feature" block
     This module's only job is to return the "feature loss" for the inputs
    """

    def __init__(self, checkpoint_path=None):
        super(VGG19PerceptualLoss, self).__init__()

        channel_in = 3
        width = 64
        self.conv1 = nn.Conv2d(channel_in, width, 3, 1, 1)
        self.conv2 = nn.Conv2d(width, width, 3, 1, 1)

        self.conv3 = nn.Conv2d(width, 2 * width, 3, 1, 1)
        self.conv4 = nn.Conv2d(2 * width, 2 * width, 3, 1, 1)

        self.conv5 = nn.Conv2d(2 * width, 4 * width, 3, 1, 1)
        self.conv6 = nn.Conv2d(4 * width, 4 * width, 3, 1, 1)
        self.conv7 = nn.Conv2d(4 * width, 4 * width, 3, 1, 1)
        self.conv8 = nn.Conv2d(4 * width, 4 * width, 3, 1, 1)

        self.conv9 = nn.Conv2d(4 * width, 8 * width, 3, 1, 1)
        self.conv10 = nn.Conv2d(8 * width, 8 * width, 3, 1, 1)
        self.conv11 = nn.Conv2d(8 * width, 8 * width, 3, 1, 1)
        self.conv12 = nn.Conv2d(8 * width, 8 * width, 3, 1, 1)

        self.conv13 = nn.Conv2d(8 * width, 8 * width, 3, 1, 1)
        self.conv14 = nn.Conv2d(8 * width, 8 * width, 3, 1, 1)
        self.conv15 = nn.Conv2d(8 * width, 8 * width, 3, 1, 1)
        self.conv16 = nn.Conv2d(8 * width, 8 * width, 3, 1, 1)

        self.mp = nn.MaxPool2d(kernel_size=2, stride=2)
        self.relu = nn.ReLU()

        if checkpoint_path:
            self.load_params(checkpoint_path)

        for p in self.parameters():
            p.requires_grad = False

    def load_params(self, checkpoint_path):
        # checkpoint is downloaded from 'https://download.pytorch.org/models/vgg19-dcbb9e9d.pth'
        print(os.path.exists(checkpoint_path))
        state_dict = torch.load(checkpoint_path)
        for ((name, source_param), target_param) in zip(state_dict.items(), self.parameters()):
            target_param.data = source_param.data
        print('Loaded Parameters of PerceptualLoss from %s.' % checkpoint_path)

    def feature_loss(self, x):
        return (x[:x.shape[0] // 2] - x[x.shape[0] // 2:]).pow(2).mean()

    def forward(self, x):
        """
        :param x: Expects x to be the target and source to concatenated on dimension 0
        :return: Feature loss
        """
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        loss = self.feature_loss(x)

        x = self.mp(x)  # 64x64
        x = self.relu(self.conv3(x))
        x = self.relu(self.conv4(x))
        loss += self.feature_loss(x)

        x = self.mp(x)  # 32x32
        x = self.relu(self.conv5(x))
        x = self.relu(self.conv6(x))
        x = self.relu(self.conv7(x))
        x = self.relu(self.conv8(x))
        loss += self.feature_loss(x)

        x = self.mp(x)  # 16x16
        x = self.relu(self.conv9(x))
        x = self.relu(self.conv10(x))
        x = self.relu(self.conv11(x))
        x = self.relu(self.conv12(x))
        loss += self.feature_loss(x)

        x = self.mp(x)  # 8x8
        x = self.relu(self.conv13(x))
        x = self.relu(self.conv14(x))
        x = self.relu(self.conv15(x))
        x = self.relu(self.conv16(x))
        loss += self.feature_loss(x)
        return loss


if __name__ == '__main__':

    perceptual_loss = VGG19PerceptualLoss(checkpoint_path='../../checkpoints/vgg19-dcbb9e9d.pth')

