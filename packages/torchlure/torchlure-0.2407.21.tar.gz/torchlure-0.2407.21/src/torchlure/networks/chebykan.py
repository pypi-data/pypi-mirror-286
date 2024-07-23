import torch
from torch import nn
from torchtyping import TensorType
from typing import Literal


class ChebyKANLayer(nn.Module):
    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        degree: int,
        poly_type: Literal["T", "U"] = "U",
        init_method: Literal["xavier", "he", "lecun"] = "xavier",
    ):
        super().__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.degree = degree
        self.poly_type = poly_type
        self.coeffs = nn.Parameter(torch.empty(input_dim, output_dim, degree + 1))
        self._init_coeffs(init_method)

    def _init_coeffs(self, method: str) -> None:
        match method:
            case "xavier":
                nn.init.xavier_uniform_(self.coeffs)
            case "he":
                nn.init.kaiming_uniform_(self.coeffs, a=1.0)
            case "lecun":
                nn.init.uniform_(self.coeffs, -1, 1) * (3.0 / self.input_dim) ** 0.5
            case _:
                raise ValueError(f"Unknown init_method: {method}")

    @staticmethod
    def compute_cheby_polynomials(
        x: torch.Tensor, degree: int, poly_type: str
    ) -> torch.Tensor:
        if poly_type == "U":
            U = [torch.ones_like(x), 2 * x]
            for n in range(2, degree + 1):
                U.append(2 * x * U[n - 1] - U[n - 2])
        elif poly_type == "T":
            U = [torch.ones_like(x), x]
            for n in range(2, degree + 1):
                U.append(2 * x * U[n - 1] - U[n - 2])
        else:
            raise ValueError(f"Unknown poly_type: {poly_type}")
        return torch.stack(U, dim=-1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.tanh(x)
        cheby_polys = self.compute_cheby_polynomials(x, self.degree, self.poly_type)
        output = torch.einsum("...id,iod->...o", cheby_polys, self.coeffs)
        return output


class ChebyKAN(nn.Module):
    def __init__(
        self,
        width: list[int],
        degree: int,
        poly_type: Literal["T", "U"] = "U",
        init_method: Literal["xavier", "he", "lecun"] = "xavier",
    ):
        super().__init__()
        self.width = width
        self.degree = degree
        self.poly_type = poly_type
        layers = []
        for i in range(len(width) - 1):
            layer = ChebyKANLayer(
                width[i], width[i + 1], degree, poly_type, init_method
            )
            layers.append(layer)
        self.layers = nn.ModuleList(layers)

    def forward(self, x: TensorType[..., "input_dim"]) -> TensorType[..., "output_dim"]:
        for layer in self.layers:
            x = layer(x)
        return x


def create_chebykan_network(
    input_dim: int,
    output_dim: int,
    hidden_dim: int,
    num_layers: int,
    degree: int,
    poly_type: Literal["T", "U"] = "U",
    init_method: Literal["xavier", "he", "lecun"] = "xavier",
) -> ChebyKAN:
    width = [input_dim] + [hidden_dim] * (num_layers - 1) + [output_dim]
    return ChebyKAN(width, degree, poly_type, init_method)
