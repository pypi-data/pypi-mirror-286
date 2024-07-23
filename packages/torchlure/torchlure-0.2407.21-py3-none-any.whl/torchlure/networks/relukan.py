import einops as ein
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchtyping import TensorType


class ReLUKANLayer(nn.Module):
    def __init__(
        self, input_dim: int, g: int, k: int, output_dim: int, train_ab: bool = True
    ):
        super().__init__()
        self.g, self.k, self.r = g, k, 4 * g * g / ((k + 1) * (k + 1))
        self.input_dim, self.output_dim = input_dim, output_dim

        phase_low = torch.arange(-k, g, dtype=torch.float32) / g
        phase_height = phase_low + (k + 1) / g
        self.phase_low = nn.Parameter(
            phase_low.repeat(input_dim, 1),
            requires_grad=train_ab,
        )
        self.phase_height = nn.Parameter(
            phase_height.repeat(input_dim, 1),
            requires_grad=train_ab,
        )

        self.equal_size_conv = nn.Conv2d(1, output_dim, (g + k, input_dim))

    def forward(self, x: TensorType["B", "input_dim"]) -> TensorType["B", "output_dim"]:
        x = x.unsqueeze(-1)
        x1 = F.relu(x - self.phase_low)
        x2 = F.relu(self.phase_height - x)
        x = x1 * x2 * self.r
        x = x * x
        x = ein.rearrange(x, "... in gk -> ... 1 gk in")
        x = self.equal_size_conv(x)
        x = ein.rearrange(x, "... out 1 1 -> ... out")
        return x


class ReLUKAN(nn.Module):
    def __init__(self, width: list[int], grid: int, k: int):
        super().__init__()
        self.width = width
        self.grid = grid
        self.k = k
        self.rk_layers = []
        for i in range(len(width) - 1):
            self.rk_layers.append(ReLUKANLayer(width[i], grid, k, width[i + 1]))
        self.rk_layers = nn.ModuleList(self.rk_layers)

    def forward(self, x: TensorType[..., "input_dim"]) -> TensorType[..., "output_dim"]:
        original_shape = x.shape
        x = x.reshape(-1, original_shape[-1])

        for rk_layer in self.rk_layers:
            x = rk_layer(x)

        output_shape = (*original_shape[:-1], x.shape[-1])
        x = x.reshape(output_shape)
        return x


def create_relukan_network(
    input_dim: int, output_dim: int, hidden_dim: int, num_layers: int, grid: int, k: int
) -> ReLUKAN:
    width = [input_dim] + [hidden_dim] * (num_layers - 1) + [output_dim]
    return ReLUKAN(width, grid, k)
