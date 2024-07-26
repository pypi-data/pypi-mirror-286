import pytest
import numpy as np


def test_ucfcrime_size(ucfcrime_dataset):
    # testing for number of videos in _debug mode
    assert ucfcrime_dataset.num_videos == 2
    # testing for number of clips
    assert len(ucfcrime_dataset) == 2926


def test_xdviolence_size(xdviolence_dataset):
    # testing for number of videos in _debug mode
    assert xdviolence_dataset.num_videos == 2
    # testing for number of clips
    assert len(xdviolence_dataset) == 4899


def test_avenue_size(avenue_dataset):
    # testing for number of videos in _debug mode
    assert avenue_dataset.num_videos == 2
    # testing for number of clips
    assert len(avenue_dataset) == 2620


def test_shanghaitech_size(shanghaitech_dataset):
    # testing for number of videos in _debug mode
    assert shanghaitech_dataset.num_videos == 2
    # testing for number of clips
    assert len(shanghaitech_dataset) == 249

@pytest.mark.parametrize("idx", [1, 10])
def test_ucfcrime_sample(idx, ucfcrime_dataset):
    video, label, temporal_label = ucfcrime_dataset[idx]

    # checking sample: # of frames 
    assert video.shape[0] == 16
    # checking sample: channelis last 
    assert video.shape[-1] == 3
    # testing temporal labels
    assert video.shape[0] == temporal_label.shape[0]


@pytest.mark.parametrize("idx", [1, 10])
def test_xdviolence_sample(idx, xdviolence_dataset):
    video, label, temporal_label = xdviolence_dataset[idx]

    # checking sample: # of frames 
    assert video.shape[0] == 16
    # checking sample: channelis last 
    assert video.shape[-1] == 3
    # testing temporal labels
    assert video.shape[0] == temporal_label.shape[0]


@pytest.mark.parametrize("idx", [1, 10])
def test_avenue_sample(idx, avenue_dataset):
    video, label, temporal_label = avenue_dataset[idx]
    
    # checking sample: # of frames 
    assert video.shape[0] == 16
    # checking sample: channelis last 
    assert video.shape[-1] == 3
    # testing temporal labels
    assert video.shape[0] == temporal_label.shape[0]


@pytest.mark.parametrize("idx", [1, 10])
def test_shanghaitech_sample(idx, shanghaitech_dataset):
    video, label, temporal_label = shanghaitech_dataset[idx]
    
    # checking sample: # of frames 
    assert video.shape[0] == 16
    # checking sample: channelis last 
    assert video.shape[-1] == 3
    # testing temporal labels
    assert video.shape[0] == temporal_label.shape[0]


@pytest.mark.parametrize("idx", [1, 10])
def test_ucfcrime_labels(idx, ucfcrime_dataset):
    video, label, temporal_label = ucfcrime_dataset[idx]

    # check video labels
    # label corresponds to the whole video label, NOT sub-clip
    assert label == 1.
    # check temporal labels 
    assert np.sum(temporal_label) == 0.


@pytest.mark.parametrize("idx", [1, 10])
def test_xdviolence_labels(idx, xdviolence_dataset):
    video, label, temporal_label = xdviolence_dataset[idx]

    # check video labels
    assert label == 0.
    # check temporal labels 
    assert np.sum(temporal_label) == 0.


@pytest.mark.parametrize("idx", [1, 10])
def test_avenue_labels(idx, avenue_dataset):
    video, label, temporal_label = avenue_dataset[idx]

    # check temporal labels 
    assert np.sum(temporal_label) == 0.


@pytest.mark.parametrize("idx", [1, 10])
def test_shanghaitech_labels(idx, shanghaitech_dataset):
    video, label, temporal_label = shanghaitech_dataset[idx]

    # check video labels
    assert label == 0.
    # check temporal labels 
    assert np.sum(temporal_label) == 0.