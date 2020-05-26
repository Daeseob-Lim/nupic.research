# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2020, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import torch
import torch.nn.functional as F
from torch import nn
from torch.nn.modules.utils import _pair as pair
from torch.nn.parameter import Parameter


class MaskedLinear(nn.Module):
    """
    Masked weights remain at zero because their gradient is always zero.

    This is designed to be used as a finetuning layer with a fixed mask. It
    doesn't initialize its own weights, bias, or mask. The caller needs to
    provide this initialization, e.g. by loading a checkpoint generated by
    another dynamic mask class.

    If the caller prunes this class's weights dynamically during training, the
    caller needs to zero the optimizer's momentum for this weight.
    """
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features

        self.weight = Parameter(torch.Tensor(out_features, in_features))
        self.register_buffer("weight_mask",
                             torch.Tensor(out_features, in_features))

        if bias:
            self.bias = Parameter(torch.Tensor(out_features))
        else:
            self.bias = None

    def extra_repr(self):
        s = f"{self.in_features}, {self.out_features}"
        if self.bias is None:
            s += ", bias=False"
        return s

    def forward(self, x):
        if self.training:
            w = self.weight * self.weight_mask
        else:
            w = self.weight

        return F.linear(x, w, self.bias)


class MaskedConv2d(nn.Module):
    """
    Masked weights remain at zero because their gradient is always zero.

    This is designed to be used as a finetuning layer with a fixed mask. It
    doesn't initialize its own weights, bias, or mask. The caller needs to
    provide this initialization, e.g. by loading a checkpoint generated by
    another dynamic mask class.

    If the caller prunes this class's weights dynamically during training, the
    caller needs to zero the optimizer's momentum for this weight.
    """
    def __init__(self, in_channels, out_channels, kernel_size, stride=1,
                 padding=0, dilation=1, groups=1, bias=True,
                 mask_mode="channel_to_channel"):
        """
        @param mask_mode (string)
        Determines how large the weight mask tensor needs to be.
        """
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = pair(kernel_size)
        self.stride = pair(stride)
        self.padding = pair(padding)
        self.dilation = pair(dilation)
        self.groups = groups

        self.weight = Parameter(torch.Tensor(out_channels, in_channels,
                                             *self.kernel_size))

        if mask_mode == "channel_to_channel":
            weight_mask = torch.Tensor(out_channels, in_channels, 1, 1)
        elif mask_mode == "weight_to_weight":
            weight_mask = torch.Tensor(out_channels, in_channels,
                                       *self.kernel_size)
        else:
            raise ValueError(f"Unrecognized mask_mode: {mask_mode}")
        self.register_buffer("weight_mask", weight_mask)

        if bias:
            self.bias = Parameter(torch.Tensor(out_channels))
        else:
            self.bias = None

    def extra_repr(self):
        s = (f"{self.in_channels}, {self.out_channels}, "
             f"kernel_size={self.kernel_size}, stride={self.stride}")
        if self.padding != (0,) * len(self.padding):
            s += f", padding={self.padding}"
        if self.dilation != (1,) * len(self.dilation):
            s += f", dilation={self.dilation}"
        if self.groups != 1:
            s += f", groups={self.groups}"
        if self.bias is None:
            s += ", bias=False"
        return s

    def forward(self, x):
        if self.training:
            w = self.weight * self.weight_mask
        else:
            w = self.weight

        return F.conv2d(
            x, w, self.bias, self.stride, self.padding, self.dilation,
            self.groups
        )


__all__ = [
    "MaskedLinear",
    "MaskedConv2d",
]
