from collections.abc import Callable
from typing import Literal

import einops as ein
import torch
from torchtyping import TensorType

Reduction = Literal["none", "mean", "sum"]


def tanh_exp(x, threshold=3.0):
    """
    TanhExp(x) = x * tanh(exp(x))

    - Clamp is necessary to prevent overflow. Using torch.where alone is insufficient;
        there might be issues when x is small.

    - TanhExp converges to 1 when x is large;  x*tanh(exp(x)) - x < 0f64 if x > 3
    """
    return torch.where(
        x > threshold,
        x,
        x * torch.tanh(torch.exp(torch.clamp(x, max=threshold))),
    )


def return_to_go(rewards: TensorType[..., "T"], gamma: float) -> TensorType[..., "T"]:
    if gamma == 1.0:
        return rewards.flip(-1).cumsum(-1).flip(-1)

    seq_len = rewards.shape[-1]
    rtgs = torch.zeros_like(rewards)
    rtg = torch.zeros_like(rewards[..., 0])

    for i in range(seq_len - 1, -1, -1):
        rtg = rewards[..., i] + gamma * rtg
        rtgs[..., i] = rtg

    return rtgs


def quantile_loss(y_pred, y_true, tau, reduction: Reduction = "mean"):
    errors = y_true - y_pred
    loss = torch.max(tau * errors, (tau - 1) * errors)

    match reduction:
        case "none":
            return loss
        case "mean":
            return torch.mean(loss)
        case "sum":
            return torch.sum(loss)
        case _:
            raise ValueError(f"Invalid reduction mode: {reduction}")


def expectile_loss(y_pred, y_true, tau, reduction: Reduction = "mean"):
    errors = y_true - y_pred
    weight = torch.where(errors > 0, tau, 1 - tau)
    loss = weight * errors**2

    match reduction:
        case "none":
            return loss
        case "mean":
            return torch.mean(loss)
        case "sum":
            return torch.sum(loss)
        case _:
            raise ValueError(f"Invalid reduction mode: {reduction}")


def rolling_window(
    tensor: TensorType["batch_dims...", "T", "C"],
    window_size: int,
    stride: int = 1,
) -> TensorType["batch_dims...", "T-W", "W", "C"]:
    """
    Create rolling windows over the time dimension of a tensor.

    Args:
        tensor: Input tensor of shape (..., T, C)
        window_size: Size of the window
        stride: Stride of the window

    Returns:
        Tensor of shape (..., T-W, W, C)
    """
    *batch_dims, T, C = tensor.shape
    windows = tensor.unfold(-2, window_size, stride)
    windows = ein.rearrange(windows, "... t w c -> ... t w c")
    return windows


def apply_rolling_window(
    func: Callable[[TensorType["B", "W", "C"]], TensorType["B", "W", "out"]],
    tensor: TensorType["B", "T", "C"],
    window_size: int,
    stride: int = 1,
) -> TensorType["B", "T-W", "out"]:
    """
    Apply a function over rolling windows of the input tensor.

    Args:
        func: Function to apply to each window
        tensor: Input tensor of shape (B, T, C)
        window_size: Size of the window
        stride: Stride of the window

    Returns:
        Tensor of shape (B, T-W, out)
    """
    windows = rolling_window(tensor=tensor, window_size=window_size, stride=stride)
    batch_size, seq_length, num_windows, num_channels = windows.shape
    flattened_windows = ein.rearrange(windows, "b t w c -> (b t) w c")
    processed_windows = func(flattened_windows)
    output_tensor = ein.rearrange(processed_windows, "(b t) c -> b t c", b=batch_size)
    return output_tensor
