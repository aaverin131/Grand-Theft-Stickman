from gts.input import facing_from_input, movement_delta


def test_movement_delta_left_only():
    assert movement_delta(up=False, down=False, left=True, right=False, speed=4) == (4, 0)


def test_movement_delta_diagonal():
    assert movement_delta(up=True, down=False, left=False, right=True, speed=3) == (-3, 3)


def test_movement_delta_opposing_keys_cancel():
    assert movement_delta(up=True, down=True, left=True, right=True, speed=5) == (0, 0)


def test_movement_delta_idle_is_zero():
    assert movement_delta(up=False, down=False, left=False, right=False, speed=5) == (0, 0)


def test_facing_left_then_right():
    assert facing_from_input(left=True, right=False) == "left"
    assert facing_from_input(left=False, right=True) == "right"


def test_facing_none_when_no_horizontal_input():
    assert facing_from_input(left=False, right=False) is None


def test_facing_left_wins_when_both_pressed():
    assert facing_from_input(left=True, right=True) == "left"
