from __future__ import annotations

from ... import config
from ...animation import FrameSequence
from ...assets import AssetLoader
from .base import AnimatedSwingWeapon


class Blade(AnimatedSwingWeapon):
    requires_aim = False
    DASH_DISTANCE = 320.0
    # The dash plays much faster than a normal swing so the burst feels snappy.
    DASH_FRAME_HOLD_DIVISOR = 5

    def __init__(self, loader: AssetLoader, frame_hold: int = config.ANIMATION_FRAME_HOLD):
        sprite = loader.image("stickman/weapon/blade/knifehold.png")
        dash_hold = max(1, frame_hold // self.DASH_FRAME_HOLD_DIVISOR)
        super().__init__(
            name="blade",
            icon=sprite,
            hold=sprite,
            swing=FrameSequence(
                loader.frames("stickman/weapon/blade/blade animation 1", prefix="pixil-frame-"),
                frame_hold=frame_hold,
                loop=False,
            ),
            secondary=FrameSequence(
                loader.frames("stickman/weapon/blade/blade animation 2", prefix="pixil-frame-"),
                frame_hold=dash_hold,
                loop=False,
            ),
            dash_distance=self.DASH_DISTANCE,
        )
