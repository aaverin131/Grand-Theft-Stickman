"""Interior scenes: bank, gun shop, house, basement."""

from __future__ import annotations

from .. import config
from ..assets import AssetLoader
from .scene import Prop, Scene


def _single_backdrop(loader: AssetLoader, image_path: str) -> list[Prop]:
    px, py = config.INITIAL_PLAYER_POS
    return [Prop(loader.image(image_path), [px, py])]


class BankScene(Scene):
    name = "bank"
    bg_color = config.COLOR_INTERIOR_BG

    def load(self, loader: AssetLoader) -> None:
        self.props = _single_backdrop(loader, "bank/bankinside.png")


class GunshopScene(Scene):
    name = "gunshop"
    bg_color = config.COLOR_INTERIOR_BG

    def load(self, loader: AssetLoader) -> None:
        self.props = _single_backdrop(loader, "gunshop/gunshopinside.png")


class HouseScene(Scene):
    name = "house"
    bg_color = config.COLOR_INTERIOR_BG

    def load(self, loader: AssetLoader) -> None:
        self.props = _single_backdrop(loader, "house/housinside.png")


class BasementScene(Scene):
    name = "basement"
    bg_color = config.COLOR_INTERIOR_BG

    def load(self, loader: AssetLoader) -> None:
        self.props = []
