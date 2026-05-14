import pytest

from gts.animation import FrameSequence


def _frames(n):
    return [object() for _ in range(n)]


def test_empty_frames_rejected():
    with pytest.raises(ValueError):
        FrameSequence([], frame_hold=1, loop=False)


def test_invalid_frame_hold_rejected():
    with pytest.raises(ValueError):
        FrameSequence(_frames(2), frame_hold=0, loop=False)


def test_non_looping_latches_on_last_frame():
    frames = _frames(3)
    seq = FrameSequence(frames, frame_hold=1, loop=False)
    assert seq.step() is frames[0]
    assert seq.step() is frames[1]
    assert seq.step() is frames[2]
    assert seq.finished is True
    # Subsequent steps stay on the last frame.
    assert seq.step() is frames[2]
    assert seq.finished is True


def test_looping_wraps():
    frames = _frames(2)
    seq = FrameSequence(frames, frame_hold=1, loop=True)
    seq.step()  # frame 0
    seq.step()  # frame 1
    assert seq.step() is frames[0]
    assert seq.finished is False


def test_frame_hold_holds_frames():
    frames = _frames(2)
    seq = FrameSequence(frames, frame_hold=3, loop=False)
    for _ in range(3):
        assert seq.step() is frames[0]
    for _ in range(3):
        assert seq.step() is frames[1]
    assert seq.finished is True


def test_reset_clears_state():
    frames = _frames(2)
    seq = FrameSequence(frames, frame_hold=1, loop=False)
    seq.step()
    seq.step()
    assert seq.finished is True
    seq.reset()
    assert seq.finished is False
    assert seq.current is frames[0]
