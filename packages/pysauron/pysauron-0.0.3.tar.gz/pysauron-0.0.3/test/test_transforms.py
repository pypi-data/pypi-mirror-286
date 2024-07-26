import pytest
import numpy as np


@pytest.mark.parametrize("idx", [75])
def test_framedrop(idx, shanghaitech_dataset, frame_drop_transform):
    # original video, label, and temporal labelss
    video, label, temporal_label = shanghaitech_dataset[idx]
    # values after transform
    shanghaitech_dataset.transforms = frame_drop_transform
    video_t, label_t, temporal_label_t = shanghaitech_dataset[idx]

    assert label != label_t 
    assert np.any(temporal_label != temporal_label_t)


@pytest.mark.parametrize("idx", [75])
def test_changedirection(idx, avenue_dataset, change_direction_transform):
    # original video, label, and temporal labelss
    video, label, temporal_label = avenue_dataset[idx]
    # values after transform
    avenue_dataset.transforms = change_direction_transform
    video_t, label_t, temporal_label_t = avenue_dataset[idx]

    assert np.array_equal(temporal_label, temporal_label_t[::-1])


@pytest.mark.parametrize("idx", [75])
def test_randomanomalyinject(idx, avenue_dataset, random_anomaly_inject_transform):
    # original video, label, and temporal labelss
    video, label, temporal_label = avenue_dataset[idx]
    # values after transform
    avenue_dataset.transforms = random_anomaly_inject_transform
    video_t, label_t, temporal_label_t = avenue_dataset[idx]

    assert np.sum(temporal_label_t) == video.shape[0]
