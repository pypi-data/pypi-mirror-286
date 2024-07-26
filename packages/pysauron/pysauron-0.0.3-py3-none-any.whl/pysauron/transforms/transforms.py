import random
import torch
import os
import numpy as np
from PIL import Image

__all__ = [
    "FrameDrop",
    "ChangeDirection",
    "RandomAnomalyInject",
]



class FrameDrop:

    def __init__(self, k=1, always_apply=False, p=0.5) -> None:
        self.p = p
        self.always_apply = always_apply

        self.k = k

    def __call__(
        self, 
        video: torch.Tensor, 
        label: int, 
        temporal_label: torch.Tensor = None
    ) -> torch.Tensor:
        """
        The input is a video tensor.

        Args:
            video (torch.Tensor): Input video tensor with shape (T, H, W, C).
        """
        if (random.random() < self.p) or self.always_apply:
            vid_len = video.shape[0]
            indices = random.sample(range(vid_len), self.k)

            video[indices] = 0.
            tmp = temporal_label.copy()
            tmp[indices] = 1.

            if isinstance(label, (int, np.int64)):
                label = 1.
            elif isinstance(label, np.ndarray):
                label[indices] = 0.

        return video, label, tmp

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class ChangeDirection:

    def __init__(self, always_apply=False, p=0.5) -> None:
        self.p = p
        self.always_apply = always_apply


    def __call__(
        self, 
        video: torch.Tensor, 
        label: int, 
        temporal_label: torch.Tensor = None
    ) -> torch.Tensor:
        """
        The input is a video tensor.

        Args:
            video (torch.Tensor): Input video tensor with shape (T, H, W, C).
        """
        if (random.random() < self.p) or self.always_apply:
            video = video.flip(dims=(0, ))
            if isinstance(label, (int, np.int64)):
                label = 1 # no matter what, label is changed to anomaly
            else:
                label = torch.flip(label, dims=[0])
            if temporal_label is not None:
                temporal_label = temporal_label[::-1]
        
        return video, label, temporal_label


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class RandomAnomalyInject:
    
    def __init__(
        self, 
        anomaly_folder='assets/anomalies/animals', 
        anomaly_shape=64,
        always_apply=False, 
        p=0.5) -> None:

        self.p = p 
        self.always_apply = always_apply
        self.anomaly_shape = (anomaly_shape, anomaly_shape)
        self.anomalies = [
            os.path.join(anomaly_folder, el) for el in os.listdir(anomaly_folder)
        ]

    def __call__(
        self, 
        video: torch.Tensor, 
        label: int, 
        temporal_label: torch.Tensor = None
    ) -> torch.Tensor:
        """
        The input is a video tensor.

        Args:
            video (torch.Tensor): Input video tensor with shape (T, H, W, C).
        """
        if (random.random() < self.p) or self.always_apply:
            anomaly = self.load_anomaly()
            anomaly_height, anomaly_width, _ = anomaly.shape

            y = random.randint(0, video.shape[1] - anomaly_height)
            x = random.randint(0, video.shape[2] - anomaly_width)
            
            for t in range(video.shape[0]): 
                video[t][y:y + anomaly_height, x:x + anomaly_width, :] = anomaly
            
            if isinstance(label, (int, np.int64)):
                label = 1 # no matter what, label is changed to anomaly
            else:
                for t in range(label.shape[0]): 
                    label[t][y:y + anomaly_height, x:x + anomaly_width] = 1.
            
            if temporal_label is not None:
                temporal_label[:] = 1. 
        
        return video, label, temporal_label

    
    def load_anomaly(self) -> torch.Tensor:
        anomaly = random.choice(self.anomalies)
        image = Image.open(anomaly).convert('RGBA')
        image = image.resize(self.anomaly_shape)
        image = np.array(image)
        tensor = torch.from_numpy(image)
        return tensor[:, :, :3]


    @property
    def available_anomalies(self):
        return [Image.open(el) for el in self.anomalies]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"