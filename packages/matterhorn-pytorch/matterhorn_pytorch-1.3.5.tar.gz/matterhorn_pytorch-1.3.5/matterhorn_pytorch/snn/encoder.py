# -*- coding: UTF-8 -*-
"""
脉冲神经网络的编码机制。
注意：此单元可能会改变张量形状。
"""


import torch
import torch.nn as nn
import matterhorn_pytorch.snn.functional as _SF
from matterhorn_pytorch.snn.skeleton import Module as _Module
from typing import Callable as _Callable


class Encoder(_Module):
    def __init__(self) -> None:
        """
        编码器的基类。
        """
        super().__init__()


    def extra_repr(self) -> str:
        """
        额外的表达式，把参数之类的放进来。
        Returns:
            repr_str (str): 参数表
        """
        return super().extra_repr()


class Direct(Encoder):
    def __init__(self) -> None:
        """
        直接编码，直接对传入的脉冲（事件）数据进行编码
        """
        super().__init__()
    

    def forward_step(self, x: torch.Tensor) -> torch.Tensor:
        """
        单步前向传播函数。
        Args:
            x (torch.Tensor): 输入张量，形状为[B,...]
        Returns:
            y (torch.Tensor): 输出张量，形状为[B,...]
        """
        return x
    

    def forward_steps(self, x: torch.Tensor) -> torch.Tensor:
        """
        多步前向传播函数，直接将第二个维度作为时间维度，转置到首个维度上。
        Args:
            x (torch.Tensor): 输入张量，形状为[B,T,...]
        Returns:
            y (torch.Tensor): 输出张量，形状为[T,B,...]
        """
        idx = [i for i, j in enumerate(x.shape)]
        assert len(idx) >= 2, "There is no temporal dimension."
        idx[0], idx[1] = idx[1], idx[0]
        y = x.permute(*idx)
        return y


class Poisson(Encoder):
    def __init__(self, time_steps: int = 1) -> None:
        """
        泊松编码（速率编码），将值转化为脉冲发放率（多步）
        Args:
            time_steps (int): 生成的时间步长
        """
        super().__init__()
        self.time_steps = time_steps


    def extra_repr(self) -> str:
        """
        额外的表达式，把参数之类的放进来。
        Returns:
            repr_str (str): 参数表
        """
        return ", ".join(["time_steps=%d" % self.time_steps]) + ((", " + super().extra_repr()) if len(super().extra_repr()) else "")


    def forward_step(self, x: torch.Tensor) -> torch.Tensor:
        """
        单步前向传播函数。
        Args:
            x (torch.Tensor): 输入张量，形状为[B,...]
        Returns:
            y (torch.Tensor): 输出张量，形状为[B,...]
        """
        min_value = torch.min(x)
        max_value = torch.max(x)
        if max_value == min_value:
            x = torch.full_like(x, 0.5)
        else:
            x = (x - min_value) / (max_value - min_value)
        r = torch.rand_like(x)
        y = _SF.le(r, x)
        return y
    

    def forward_steps(self, x: torch.Tensor) -> torch.Tensor:
        """
        多步前向传播函数。
        Args:
            x (torch.Tensor): 输入张量，形状为[B,...]
        Returns:
            y (torch.Tensor): 输出张量，形状为[T, B,...]
        """
        res_shape = [self.time_steps] + list(x.shape)
        v = torch.ones(*res_shape).to(x) * x
        y = self.forward_step(v)
        return y


class Temporal(Encoder):
    def __init__(self, time_steps: int = 1, prob: float = 1.0, transform: _Callable = lambda x: x) -> None:
        """
        时间编码，在某个时间之前不会产生脉冲，在某个时间之后随机产生脉冲
        Args:
            time_steps (int): 生成的时间步长
            prob (float): 若达到了时间，以多大的概率发放脉冲，范围为[0, 1]
            transform (Callable): 将数据x如何变形
        """
        super().__init__()
        self.time_steps = time_steps
        self.prob = prob
        self.transform = transform
        self.reset()


    def extra_repr(self) -> str:
        """
        额外的表达式，把参数之类的放进来。
        Returns:
            repr_str (str): 参数表
        """
        return ", ".join(["time_steps=%d" % self.time_steps, "prob=%g" % self.prob]) + ((", " + super().extra_repr()) if len(super().extra_repr()) else "")


    def reset(self) -> _Module:
        """
        重置编码器
        """
        self.current_time_step = 0
        return super().reset()


    def forward_step(self, x: torch.Tensor) -> torch.Tensor:
        """
        单步前向传播函数。
        Args:
            x (torch.Tensor): 输入张量，形状为[B,...]
        Returns:
            y (torch.Tensor): 输出张量，形状为[B,...]
        """
        x = self.transform(x)
        f = _SF.le(x, self.current_time_step)
        r = _SF.le(torch.rand_like(x), self.prob)
        y = f * r
        self.current_time_step += 1
        return y
    

    def forward_steps(self, x: torch.Tensor, time_steps: int) -> torch.Tensor:
        """
        多步前向传播函数。
        Args:
            x (torch.Tensor): 输入张量，形状为[B,...]
        Returns:
            y (torch.Tensor): 输出张量，形状为[T, B,...]
        """
        y_seq = []
        for t in range(time_steps):
            y_seq.append(self.forward_step(x))
        y = torch.stack(y_seq)
        return y