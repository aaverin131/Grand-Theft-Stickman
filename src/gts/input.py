"""Pure input-mapping helpers used by the game loop."""

from __future__ import annotations


def movement_delta(
    *, up: bool, down: bool, left: bool, right: bool, speed: int
) -> tuple[int, int]:
    """Return the world-translation delta for the given WASD state.

    The world moves opposite to the player: pressing 'a' shifts props right.
    """
    dx = (int(left) - int(right)) * speed
    dy = (int(up) - int(down)) * speed
    return dx, dy


def facing_from_input(*, left: bool, right: bool) -> str | None:
    """Return the facing the player should adopt given horizontal input.

    Returns None when neither key is held so vertical-only motion preserves
    the previous facing.
    """
    if left:
        return "left"
    if right:
        return "right"
    return None
