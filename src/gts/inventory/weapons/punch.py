from __future__ import annotations

from ... import config
from ...animation import FrameSequence
from ...assets import AssetLoader
from .base import AnimatedSwingWeapon


class Punch(AnimatedSwingWeapon):
    def __init__(self, loader: AssetLoader, frame_hold: int = config.ANIMATION_FRAME_HOLD):
        sprite = loader.image("stickman/weapon/punch/punchstill.png")
        super().__init__(
            name="punch",
            icon=sprite,
            hold=sprite,
            swing=FrameSequence(
                loader.frames("stickman/weapon/punch/punch animation", prefix="pixil-frame-"),
                frame_hold=frame_hold,
                loop=False,
            ),
        )
