"""Mouse-to-aim conversion helpers."""

from __future__ import annotations

import math


def aim_angle_facing(
    mouse_pos: tuple[float, float], center: tuple[float, float]
) -> tuple[float, str]:
    """Return the aim angle (degrees) and player facing for a mouse position.

    The angle is measured the same way the original game's `action()` does it:
    the y axis is inverted (atan2 negated), and when the player faces left the
    sign is mirrored so that the same rotation applied to a flipped sprite
    points in the intended direction.
    """
    dx = mouse_pos[0] - center[0]
    dy = mouse_pos[1] - center[1]
    if dx == 0 and dy == 0:
        return 0.0, "right"
    angle = -math.degrees(math.atan2(dy, dx))
    facing = "left" if angle > 90 or angle < -90 else "right"
    if facing == "left":
        angle = -angle
    return angle, facing
