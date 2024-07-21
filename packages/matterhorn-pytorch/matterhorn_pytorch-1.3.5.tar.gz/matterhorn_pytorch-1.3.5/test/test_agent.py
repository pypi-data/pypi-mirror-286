import torch
import torch.nn as nn
from matterhorn_pytorch.snn import Agent


class DemoModel(nn.Module):
    def forward(self, x: torch.Tensor, y: int):
        print(x.shape, y)
        return torch.zeros_like(x), y


if __name__ == "__main__":
    a = Agent(DemoModel(), multi_time_step = True)
    data = torch.rand(3, 4, 4)
    res, _ = a(data, 3)
    print(res, _)