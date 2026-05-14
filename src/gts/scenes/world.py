"""Overworld scene with the player's spawn area and exterior buildings."""

from __future__ import annotations

from .scene import Prop, Scene
from ..assets import AssetLoader
from .. import config


# Drawn in order, behind the buildings.
SCENERY = [
    ("playground", "background/playground2.png"),
    ("forest",     "background/forest2.png"),
]

# Each entry produces a collidable prop that switches scenes on E.
BUILDINGS = [
    ("bank",    "bank/bank2.png",      "bank"),
    ("gunshop", "gunshop/gun_shop.png", "gunshop"),
    ("house",   "house/hous.png",      "house"),
]


class WorldScene(Scene):
    name = "world"
    bg_color = config.COLOR_WORLD_BG

    def load(self, loader: AssetLoader) -> None:
        px, py = config.INITIAL_PLAYER_POS
        offsets = config.WORLD_OBJECT_OFFSETS

        props: list[Prop] = [Prop(loader.image("background/mapbg.png"), [-px, -py])]

        for key, path in SCENERY:
            ox, oy = offsets[key]
            props.append(Prop(loader.image(path), [px + ox, py + oy]))

        for key, path, target in BUILDINGS:
            ox, oy = offsets[key]
            props.append(
                Prop(loader.image(path), [px + ox, py + oy], collidable=True, target_scene=target)
            )

        self.props = props
