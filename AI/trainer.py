import numpy as np
from random import uniform
import math
from torch import nn
from torch.masked import masked_tensor
import torch

hiddennodes = 10
inodes = 660
#inodes=6
onodes = 71
#onodes=7

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        #self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(inodes, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, onodes)
        )

    def forward(self, x):
        x = torch.flatten(x)
        logits = self.linear_relu_stack(x)
        valuation = (logits[onodes-1] + 1) / 2
        #nn.Sigmoid()(logits[onodes-1])
        logits = logits[0:onodes-1]
        #logits = nn.Softmax(dim=0)(logits)
        return logits , valuation

    def loss_fn():
        return

    def train_one_epoch():
        return

