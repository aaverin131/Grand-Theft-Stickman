from __future__ import annotations

from ... import config
from ...animation import FrameSequence
from ...assets import AssetLoader
from .base import AnimatedSwingWeapon


class Blade(AnimatedSwingWeapon):
    def __init__(self, loader: AssetLoader, frame_hold: int = config.ANIMATION_FRAME_HOLD):
        sprite = loader.image("stickman/weapon/blade/knifehold.png")
        super().__init__(
            name="blade",
            icon=sprite,
            hold=sprite,
            swing=FrameSequence(
                loader.frames("stickman/weapon/blade/blade animation 1", prefix="pixil-frame-"),
                frame_hold=frame_hold,
                loop=False,
            ),
        )
