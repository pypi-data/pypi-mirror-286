# Torch Lure


<a href="https://www.youtube.com/watch?v=wCzCOYCfY9g" target="_blank">
  <img src="http://img.youtube.com/vi/wCzCOYCfY9g/maxresdefault.jpg" alt="Chandelure" style="width: 100%;">
</a>


<!-- # Depndencies -->
<!-- 
```
pip install git+https://github.com/Farama-Foundation/Minari.git@19565bd8cd33f2e4a3a9a8e4db372044b01ea8d3
``` -->


## Installations
```sh
pip install torchlure
```

## Usage
```py
import torchlure as lure

# Optimizers
lure.SophiaG(lr=1e-3, weight_decay=0.2)

# Functions
lure.tanh_exp(x)
lure.TanhExp()

lure.quantile_loss(y_pred, y_target, quantile=0.5)
lure.QuantileLoss(quantile=0.5)

lure.RMSNrom(dim=256, eps=1e-6)

# Noise Scheduler
lure.LinearNoiseScheduler(beta=1e-4, beta_end=0.02, num_timesteps=1000)
lure.CosineNoiseScheduler(max_beta=0.999, s=0.008, num_timesteps=1000):


lure.ReLUKAN(width=[11, 16, 16, 2], grid=5, k=3)

lure.create_relukan_network(
    input_dim=11,
    output_dim=2,
    hidden_dim=32,
    num_layers=3,
    grid=5,
    k=3,
)

```

```py
import torchlure as lure

# Optimizers
lure.SophiaG(lr=1e-3, weight_decay=0.2)

# Functions
lure.tanh_exp(x)
lure.TanhExp()

lure.quantile_loss(y_pred, y_target, quantile=0.5)
lure.QuantileLoss(quantile=0.5)

lure.RMSNrom(dim=256, eps=1e-6)

# Noise Scheduler
lure.LinearNoiseScheduler(beta=1e-4, beta_end=0.02, num_timesteps=1000)
lure.CosineNoiseScheduler(max_beta=0.999, s=0.008, num_timesteps=1000):
```

### Dataset



```py
import gymnasium as gym
import numpy as np
import torch
from torchlure.datasets import MinariEpisodeDataset, MinariTrajectoryDataset
from torchtyping import TensorType

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


env = gym.make("Hopper-v4")
minari_dataset = MinariEpisodeDataset("Hopper-random-v0")
minari_dataset.create(env, n_episodes=100, exist_ok=True)
minari_dataset.info()
# Observation space: Box(-inf, inf, (11,), float64)
# Action space: Box(-1.0, 1.0, (3,), float32)
# Total episodes: 100
# Total steps: 2,182

traj_dataset = MinariTrajectoryDataset(minari_dataset, traj_len=20, {
    "returns": lambda ep: return_to_go(torch.tensor(ep.rewards), 0.99),
})

traj = traj_dataset[2]
traj = traj_dataset[[3, 8, 15]]
traj = traj_dataset[np.arange(16)]
traj = traj_dataset[torch.arange(16)]
traj = traj_dataset[-16:]
traj["observations"].shape, traj["actions"].shape, traj["rewards"].shape, traj[
    "terminated"
].shape, traj["truncated"].shape, traj["timesteps"].shape
# (torch.Size([16, 20, 4, 4, 16]),
#  torch.Size([16, 20]),
#  torch.Size([16, 20]),
#  torch.Size([16, 20]),
#  torch.Size([16, 20]),
#  torch.Size([16, 20]))


```

<!-- # %%
dataset = D4RLDataset(
    dataset_id= "hopper-medium-expert-v2.2405",
    d4rl_name= "hopper-medium-expert-v2",
    env_id= "Hopper-v4",
)

# if you are download it once
dataset = D4RLDataset(
    dataset_id= "hopper-medium-expert-v2.2405",
) -->
<!-- See all datasets [here](https://github.com/pytorch/rl/blob/3a7cf6af2a08089f11e0ed8cad3dd1cea0e253fb/torchrl/data/datasets/d4rl_infos.py) -->