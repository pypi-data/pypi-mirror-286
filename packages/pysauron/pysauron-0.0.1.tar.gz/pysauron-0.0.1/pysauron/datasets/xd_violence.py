import torch 
import re
import numpy as np
from pathlib import Path
from torchvision.datasets.video_utils import VideoClips
from torchvision import get_video_backend

from typing import Optional, Callable

import warnings
warnings.filterwarnings("ignore")



class XDViolence(torch.utils.data.Dataset):
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
        _video_width: int = 0,
        _video_height: int = 0,
        _debug: bool = False
    ):

        self._debug = _debug

        self.root  = Path(root)
        self.test_mode = test_mode
        self.transforms = transforms

        self.video_paths = self._parse_video_path()
        self._parse_labels(self.video_paths)
        
        if self.test_mode:
            self.annotations = self._temporal_testing_annotations(self.video_paths)

        backend = get_video_backend()
        if backend == 'pyav':
            _video_width = 0
            _video_height = 0

        self.video_clips = VideoClips(
            video_paths=self.video_paths,
            clip_length_in_frames=frames_per_clip,
            frames_between_clips=step_between_clips,
            frame_rate=frame_rate,
            num_workers=num_workers,
            output_format=output_format,
            _video_width=_video_width,
            _video_height=_video_width,
        )

    def _parse_video_path(self):
        video_paths = list()
        search_pattern = 'videos/*' if self.test_mode else  '*/*' 
        for path in self.root.glob(search_pattern):
            video_paths.append(path.as_posix())

        if self._debug:
            return video_paths[:2]
        return video_paths

    
    def _parse_labels(self, video_paths):
        pattern = r'_label_([A-Z\d-]+)\.mp4'
        self.labels = [re.search(pattern, el).group(1) for el in video_paths]

    
    def _temporal_testing_annotations(self, video_paths):
        annotations_file = self.root / 'annotations.txt'

        annotations_map = {}
        with open(annotations_file, 'r') as file:
            for line in file:
                fields = line.strip().split()
                annotations_map[fields[0]] = list(map(int, fields[1:]))
        
        annotations = list()
        for el in video_paths:
            filename = el.split('/')[-1].replace('.mp4', '')
            if filename in annotations_map:
                annotations.append(annotations_map[filename])
            else:
                annotations.append([-1, -1])
        return annotations


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
        label = 0 if 'a' in label.lower() else 1
        
        if self.test_mode:
            temporal_annot = self.annotations[video_idx]

            clip_pts = self.video_clips.clips[video_idx][clip_idx] // 512
            start_idx = clip_pts[0].item()
            end_idx = clip_pts[-1].item()

            temporal_label = np.zeros(end_idx - start_idx + 1)

            for idx, index in enumerate(range(start_idx, end_idx + 1)):
                for i in range(0, len(temporal_annot) // 2, 2):
                    if temporal_annot[i] <= index <= temporal_annot[i+1]:
                        temporal_label[idx] = 1
            
            if self.transforms:
                video, label, temporal_label = self.transforms(
                    video, label, temporal_label)

            return video, label, temporal_label 
        else:
            if self.transforms:
                video, label, _ = self.transforms(
                    video, label)

            return video, label

    def __len__(self):
        return self.video_clips.num_clips()

    @property
    def num_videos(self):
        return self.video_clips.num_videos()
        