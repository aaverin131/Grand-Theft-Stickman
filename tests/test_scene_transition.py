import pygame

from gts.scenes import WorldScene
from gts.scenes.transitions import find_scene_transition


def test_finds_target_when_player_overlaps_collidable(loader):
    scene = WorldScene()
    scene.load(loader)
    bank = next(p for p in scene.collidable_props() if p.target_scene == "bank")
    rect = bank.image.get_bounding_rect().move(int(bank.pos[0]), int(bank.pos[1]))
    assert find_scene_transition(scene, rect) == "bank"


def test_returns_none_when_player_is_far_away(loader):
    scene = WorldScene()
    scene.load(loader)
    rect = pygame.Rect(99999, 99999, 10, 10)
    assert find_scene_transition(scene, rect) is None


def test_returns_none_when_collidable_prop_has_no_target():
    from gts.scenes.scene import Prop, Scene

    class _Stub(Scene):
        name = "stub"

        def load(self, loader):  # noqa: ARG002
            self.props = [
                Prop(image=pygame.Surface((10, 10)), pos=[0, 0], collidable=True, target_scene=None)
            ]

    scene = _Stub()
    scene.load(None)
    assert find_scene_transition(scene, pygame.Rect(0, 0, 10, 10)) is None
