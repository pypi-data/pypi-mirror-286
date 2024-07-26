import torch 
import scipy
import numpy as np
from pathlib import Path
from torchvision.datasets.video_utils import VideoClips

from typing import Optional, Callable


class Avenue(torch.utils.data.Dataset):
    def __init__(
        self, 
        root: str, 
        frames_per_clip:int = 16,
        step_between_clips: int = 1,
        test_mode:bool = False,
        transforms: Optional[Callable] = None, 
        frame_rate: Optional[int] = None,
        num_workers: int = 1,
        output_format: str = "THWC",
        _debug: bool = False
    ):

        self._debug = _debug 
        self.root = Path(root)
        self.test_mode = test_mode 
        self.transforms = transforms

        self.video_paths = self._parse_video_path()
        self._parse_labels()

        self.video_clips = VideoClips(
            video_paths=self.video_paths,
            clip_length_in_frames=frames_per_clip,
            frames_between_clips=step_between_clips,
            frame_rate=frame_rate,
            num_workers=num_workers,
            output_format=output_format,
        )

    def _parse_video_path(self):
        video_paths = list()
        search_pattern = 'testing_videos/*' if self.test_mode else 'training_videos/*'
        for path in sorted(self.root.glob(search_pattern), 
                key=lambda x: int(str(x).split('/')[-1].split('.')[0])): 
            video_paths.append(path.as_posix())
        
        if self._debug:
            return video_paths[:2]
        return video_paths
    

    def _parse_labels(self):
        self.labels = list()
        search_pattern = (
            'ground_truth_demo/testing_label_mask/*' if self.test_mode else 'training_vol/*'
        )
        for path in sorted(self.root.glob(search_pattern), 
                key=lambda x: int(str(x).split('/')[-1].split('.')[0].replace('_label', '').replace('vol', ''))):

            mat = scipy.io.loadmat(path)
            if self.test_mode:
                self.labels.append(mat['volLabel'].squeeze())
            else:
                self.labels.append(mat['vol'])
        
        if self._debug:
            self.labels = self.labels[:2]

    def _parse_temporal(self, visual_labels):
        temporal_label = np.zeros(visual_labels.shape[0])
        for idx, el in enumerate(visual_labels):
            if 1 in np.unique(el):
                temporal_label[idx] = 1.
        return temporal_label

    def __getitem__(self, idx: int):
        """ For video with id idx, loads self.NUM_SEGMENTS * self.FRAMES_PER_SEGMENT 
            frames from evenly chosen locations across the video
            
            Args:
                idx: Video sample index
            Returns:
                A tuple of (video, label). Label is a single integer. Video is either
                1) A batch of shape (NUM_IMAGES x CHANNELS x HEIGHT x WIDTH)
                2) or anything else if a custom transform is used
        """
        video_idx, clip_idx = self.video_clips.get_clip_location(idx)
        video, audio, info, video_idx = self.video_clips.get_clip(idx)
        
        label = self.labels[video_idx]

        clip_pts = self.video_clips.clips[video_idx][clip_idx] #// 512
        start_idx = clip_pts[0].item()
        end_idx = clip_pts[-1].item()

        
        label = label[start_idx : end_idx + 1]
        common_dtype = np.result_type(*label)
        label = [arr.astype(common_dtype) for arr in label]
        label = torch.tensor(label)

        temporal_label = self._parse_temporal(label)

        if self.transforms:
            video, label, temporal_label = self.transforms(video, label, temporal_label)
            
        return video, label, temporal_label

    def __len__(self):
        return self.video_clips.num_clips()

    @property
    def num_videos(self):
        return self.video_clips.num_videos()