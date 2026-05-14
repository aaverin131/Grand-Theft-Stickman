"""Scene manager: holds named scenes and tracks the active one."""

from __future__ import annotations

from .scene import Scene


class SceneManager:
    def __init__(self, scenes: dict[str, Scene], initial: str):
        if initial not in scenes:
            raise KeyError(f"unknown initial scene: {initial!r}")
        self._scenes = scenes
        self._current = initial

    @property
    def current(self) -> Scene:
        return self._scenes[self._current]

    @property
    def current_name(self) -> str:
        return self._current

    def switch_to(self, name: str) -> None:
        if name not in self._scenes:
            raise KeyError(f"unknown scene: {name!r}")
        self._current = name

    def has(self, name: str) -> bool:
        return name in self._scenes
