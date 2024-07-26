import torch 
import numpy as np
from pathlib import Path
from torchvision.datasets.video_utils import VideoClips

from typing import Optional, Callable

import warnings
warnings.filterwarnings("ignore")



class UCFCrime(torch.utils.data.Dataset):
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
        _debug: bool = True
    ):

        self._debug = _debug
        self.root  = Path(root)
        self.test_mode = test_mode
        self.transforms = transforms

        self._parse_label_file()
        if self.test_mode:
            self.annotations = self._temporal_testing_annotations()

        video_paths = self._parse_video_path()
        self.video_clips = VideoClips(
            video_paths=video_paths,
            clip_length_in_frames=frames_per_clip,
            frames_between_clips=step_between_clips,
            frame_rate=frame_rate,
            num_workers=num_workers,
            output_format=output_format
        )

    def _parse_video_path(self):
        video_paths = list()

        for el in self.labels:
            el = el.split('/')[-1]
            video_paths.append(list(self.root.rglob(el))[0].as_posix())
        
        if self._debug:
            return video_paths[:2]
        return video_paths

    def _parse_label_file(self):
        if self.test_mode:
            labels_file = self.root / 'UCF_Crimes-Train-Test-Split' / 'Anomaly_Detection_splits' / 'Anomaly_Test.txt'
        else:
            labels_file = self.root / 'Anomaly_Train.txt'
        
        with open(labels_file, 'r') as file:
            self.labels = [line.strip() for line in file]
        
        if self._debug:
            self.labels = self.labels[:2]
    
    
    def _temporal_testing_annotations(self):
        annotations_file = self.root / 'Temporal_Anomaly_Annotation_for_Testing_Videos.txt'

        annotations = list()
        with open(annotations_file, 'r') as file:
            for line in file:
                fields = line.strip().split()
                
                sample = {
                    'filename': fields[0],
                    'anomaly_type': fields[1],
                    'start_end_idx': list(map(int, fields[2:]))
                }
                annotations.append(sample)
        return annotations


    def __getitem__(self, idx: int):
        """ For video with id idx, loads self.NUM_SEGMENTS * self.FRAMES_PER_SEGMENT 
            frames from evenly chosen locations across the video
            
            Args:
                idx: Video sample index
            Returns:
                A tuple of (video, label). Label is a single integer. Video is either
                1) A batch of shape (NUM_IMAGES x HEIGHT x WIDTH x CHANNELS) in the range [0, 1]
                2) or anything else if a custom transform is used
        """
        video_idx, clip_idx = self.video_clips.get_clip_location(idx)
        video, audio, info, video_idx = self.video_clips.get_clip(idx)
        
        label = self.labels[video_idx]
        label = 0 if 'normal' in label.lower() else 1
        
        if self.test_mode:
            temporal_annot = self.annotations[video_idx]['start_end_idx']

            clip_pts = self.video_clips.clips[video_idx][clip_idx] // 512
            start_idx = clip_pts[0].item()
            end_idx = clip_pts[-1].item()

            temporal_label = np.zeros(end_idx - start_idx + 1)

            for idx, index in enumerate(range(start_idx, end_idx + 1)):
                if (temporal_annot[0] <= index <= temporal_annot[1] or 
                    temporal_annot[2] <= index <= temporal_annot[3]):
                    temporal_label[idx] = 1

            if self.transforms:
                video, label, temporal_label = self.transforms(video, label, temporal_label)
            
            return video, label, temporal_label 
        else:
            if self.transforms:
                video, label, _ = self.transforms(video, label)
            
            return video, label

    def __len__(self):
        return self.video_clips.num_clips()

    @property
    def num_videos(self):
        return self.video_clips.num_videos()
        