import torch 
import numpy as np
from PIL import Image
from pathlib import Path
from torchvision.datasets.video_utils import VideoClips

from typing import Optional, Callable

import warnings
warnings.filterwarnings("ignore")


class ShanghaiTech(torch.utils.data.Dataset):
    def __init__(
        self,
        root: str, 
        frames_per_clip: int = 16, 
        step_between_clips: int = 1,
        test_mode: bool = False,
        transforms: Optional[Callable] = None, 
        frame_rate: Optional[int] = None, 
        num_workers: int = 1,
        output_format: str = "THWC",
        _debug: bool = True
    ):

        self._debug = _debug
        self.root = Path(root)
        self.test_mode = test_mode
        self.transforms = transforms 

        self.step_between_clips = step_between_clips
        self.frames_per_clip = frames_per_clip

        if self.test_mode:
            self.videos_count = 0
            self.labels = self._temporal_testing_annotations()
            self.video_clips_path = self._form_frame_samples()
        else:
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
        for el in sorted((self.root / 'training' / 'videos').glob('*.avi')):
            video_paths.append(el.as_posix())
        
        if self._debug:
            return video_paths[:2]

        return video_paths

    def _temporal_testing_annotations(self):
        labels = list()
        for el in sorted((self.root / 'testing' / 'test_frame_mask').glob('*.npy')):
            sample_labels = np.load(el)
            self.videos_count += 1

            if self._debug and self.videos_count == 2:
                break

            for i in range(0, len(sample_labels) - self.frames_per_clip, self.step_between_clips):
                start_idx = i
                end_idx = i + self.frames_per_clip
                labels.append(sample_labels[start_idx : end_idx])

        return labels

    def _form_frame_samples(self):
        samples = list()
        for video_name in sorted((self.root / 'testing' / 'frames').glob('*')):
            sorted_frames = sorted(video_name.glob('*.jpg'))
            for i in range(0, len(sorted_frames) - self.frames_per_clip, self.step_between_clips):
                start_idx = i
                end_idx = i + self.frames_per_clip
                samples.append(
                    (sorted_frames[start_idx : end_idx], start_idx, end_idx)
                )
        return samples


    def _load_video_samples(self, paths):
        sample = list()
        for el in paths:
            sample.append(np.array(Image.open(el)))
        return torch.from_numpy(np.array(sample))

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

        if self.test_mode:
            samples_path, _, _ = self.video_clips_path[idx]
            video = self._load_video_samples(samples_path)
            temporal_label = self.labels[idx]
            label = np.any(temporal_label).astype(int)

            if self.transforms:
                video, label, temporal_label = self.transforms(
                    video, label, temporal_label)

            return video, label, temporal_label
        else:

            video_idx, clip_idx = self.video_clips.get_clip_location(idx)
            video, audio, info, video_idx = self.video_clips.get_clip(idx)

            label = 0

            if self.transforms:
                video, label, _ = self.transform(video, label)

            return video, label
    
    def __len__(self):
        if self.test_mode:
            return len(self.labels)
        else:
            return self.video_clips.num_clips()

    @property
    def num_videos(self):
        if self.test_mode:
            return self.videos_count 
        else:
            return self.video_clips.num_videos()