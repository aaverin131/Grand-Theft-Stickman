from gts.aim import aim_angle_facing

CENTER = (500, 400)


def test_mouse_to_the_right_is_zero_angle_right():
    angle, facing = aim_angle_facing((600, 400), CENTER)
    assert facing == "right"
    assert angle == 0.0


def test_mouse_directly_above_is_ninety_facing_right():
    angle, facing = aim_angle_facing((500, 300), CENTER)
    assert facing == "right"
    assert angle == 90.0


def test_mouse_directly_below_is_negative_ninety_facing_right():
    angle, facing = aim_angle_facing((500, 500), CENTER)
    assert facing == "right"
    assert angle == -90.0


def test_mouse_to_the_left_flips_to_facing_left():
    angle, facing = aim_angle_facing((400, 400), CENTER)
    assert facing == "left"
    # raw angle would be 180; after flip the helper mirrors the sign
    assert abs(angle) == 180.0


def test_mouse_at_center_is_safe_default():
    angle, facing = aim_angle_facing(CENTER, CENTER)
    assert angle == 0.0
    assert facing == "right"


def test_mouse_upper_left_quadrant_faces_left():
    _, facing = aim_angle_facing((400, 300), CENTER)
    assert facing == "left"


def test_mouse_lower_right_quadrant_faces_right():
    _, facing = aim_angle_facing((600, 500), CENTER)
    assert facing == "right"
