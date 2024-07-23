from typing import Callable

import gymnasium as gym
import minari
import numpy as np
import torch
from tensordict import TensorDict
from torch.utils.data import Dataset
from tqdm import tqdm


class MinariEpisodeDataset(Dataset):
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name

        try:
            dataset = minari.load_dataset(dataset_name)
            self.dataset = dataset
            return
        except:
            self.dataset = None

    def create(
        self,
        env,
        n_samples: int,
        policy: Callable[[np.ndarray], np.ndarray] | None = None,
    ):
        assert self.dataset is None, "Dataset already exists"

        if not isinstance(env, minari.DataCollector):
            env = minari.DataCollector(env)

        for _ in tqdm(range(n_samples), total=n_samples, desc="Collecting data"):
            obs, info = env.reset()
            done = False
            while not done:
                if policy is not None:
                    action = policy(obs)
                else:
                    action = env.action_space.sample()  # <- use your policy here
                obs, rew, terminated, truncated, info = env.step(action)
                done = terminated or truncated
        dataset = env.create_dataset(self.dataset_name)
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx: int) -> minari.EpisodeData:
        return self.dataset[idx]

    def __iter__(self):
        return iter(self.dataset)

    def info(self):
        print(f"Observation space: {self.dataset.observation_space}")
        print(f"Action space: {self.dataset.action_space}")
        print(f"Total episodes: {self.dataset.total_episodes:,}")
        print(f"Total steps: {self.dataset.total_steps:,}")


class MinariTrajectoryDataset(Dataset):
    def __init__(
        self,
        minari_dataset: MinariEpisodeDataset,
        traj_len: int,
        custom_info: dict[str, Callable[[minari.EpisodeData], torch.Tensor]] = {},
    ):
        self.minari_dataset = minari_dataset
        self.traj_len = traj_len
        self.book = self.build_book(self.minari_dataset, self.traj_len)
        self.info = self.build_info(custom_info)

    def build_info(
        self, custom_info: dict[str, Callable[[minari.EpisodeData], torch.Tensor]]
    ) -> dict[str, dict[str, torch.Tensor]]:
        info: dict[str, dict[str, torch.Tensor]] = {
            "observations": {},
            "actions": {},
            "rewards": {},
            "terminated": {},
            "truncated": {},
            "timesteps": {},
            **{key: {} for key in custom_info},
        }
        for ep in self.minari_dataset:
            info["observations"][ep.id] = torch.tensor(ep.observations)
            info["actions"][ep.id] = torch.tensor(ep.actions)
            info["rewards"][ep.id] = torch.tensor(ep.rewards)
            info["terminated"][ep.id] = torch.tensor(ep.terminations)
            info["truncated"][ep.id] = torch.tensor(ep.truncations)
            info["timesteps"][ep.id] = torch.arange(ep.total_timesteps)
            for key, func in custom_info.items():
                info[key][ep.id] = func(ep)
        return info

    @staticmethod
    def build_book(minari_dataset: MinariEpisodeDataset, traj_len: int):
        book = {}
        traj_id = 0

        for ep in minari_dataset:
            if ep.total_timesteps < traj_len:
                continue

            for start_idx in range(ep.total_timesteps - traj_len):
                book[traj_id] = (ep.id, start_idx, start_idx + traj_len)
                traj_id += 1

        return book

    def __len__(self) -> int:
        return len(self.book)

    def __getitem__(self, index: int | list[int]) -> dict:
        match index:
            case int():
                return self._get_by_idx(index).to_dict()
            case list():
                return torch.stack([self._get_by_idx(i) for i in index]).to_dict()
            case slice():
                index = list(range(*index.indices(len(self))))
                return self[index]
            case np.ndarray():
                index = index.tolist()
                return self[index]
            case torch.Tensor():
                index = index.tolist()
                return self[index]
            case _:
                raise ValueError(f"Invalid index type: {type(index)}")

    def _get_by_idx(self, index: int) -> TensorDict:
        ep_id, start_idx, end_idx = self.book[index]

        return TensorDict(
            {
                key: torch.tensor(self.info[key][ep_id][start_idx:end_idx])
                for key in self.info.keys()
            },
            batch_size=[],
        )

    def sample(self, n: int) -> TensorDict:
        # index = torch.randperm(len(self))[:n]
        index = torch.randint(0, len(self), (n,))
        return self[index]
