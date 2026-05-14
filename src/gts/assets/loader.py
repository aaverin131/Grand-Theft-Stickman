"""Cached image and sound loader."""

from __future__ import annotations

import re
from pathlib import Path

import pygame


_NUM_SUFFIX = re.compile(r"(\d+)$")


def _frame_index(name: str) -> int:
    """Extract the trailing integer from a frame name for natural ordering."""
    match = _NUM_SUFFIX.search(name)
    return int(match.group(1)) if match else 0


class AssetLoader:
    """Cache-backed loader for images, image directories, and sounds.

    `convert_alpha()` is called on every image, so the pygame display must
    be initialized before any image method is called.
    """

    def __init__(self, root: Path | str):
        self.root = Path(root)
        self._images: dict[Path, pygame.Surface] = {}
        self._dirs: dict[Path, dict[str, pygame.Surface]] = {}
        self._sounds: dict[Path, pygame.mixer.Sound] = {}

    def _resolve(self, *parts) -> Path:
        path = Path(*parts)
        return path if path.is_absolute() else self.root.joinpath(path)

    def image(self, *parts) -> pygame.Surface:
        """Load a single alpha-converted image."""
        key = self._resolve(*parts)
        cached = self._images.get(key)
        if cached is None:
            cached = pygame.image.load(str(key)).convert_alpha()
            self._images[key] = cached
        return cached

    def image_dir(self, *parts) -> dict[str, pygame.Surface]:
        """Load every PNG in a directory, keyed by filename stem."""
        key = self._resolve(*parts)
        cached = self._dirs.get(key)
        if cached is None:
            cached = {
                p.stem: pygame.image.load(str(p)).convert_alpha()
                for p in sorted(key.iterdir())
                if p.suffix.lower() == ".png"
            }
            self._dirs[key] = cached
        return cached

    def frames(self, *parts, prefix: str = "") -> list[pygame.Surface]:
        """Return PNGs in a directory matching `prefix`, ordered by trailing integer."""
        images = self.image_dir(*parts)
        matching = [(name, img) for name, img in images.items() if name.startswith(prefix)]
        matching.sort(key=lambda item: _frame_index(item[0]))
        return [img for _, img in matching]

    def sound(self, *parts) -> pygame.mixer.Sound:
        key = self._resolve(*parts)
        cached = self._sounds.get(key)
        if cached is None:
            cached = pygame.mixer.Sound(str(key))
            self._sounds[key] = cached
        return cached
