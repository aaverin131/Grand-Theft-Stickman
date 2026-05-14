import pytest

from gts.scenes import (
    BankScene,
    BasementScene,
    GunshopScene,
    HouseScene,
    Scene,
    SceneManager,
    WorldScene,
)


def test_world_scene_has_six_props_three_collidable(loader):
    scene = WorldScene()
    scene.load(loader)
    assert len(scene.props) == 6
    assert len(scene.collidable_props()) == 3


def test_world_collidable_props_carry_target_scenes(loader):
    scene = WorldScene()
    scene.load(loader)
    targets = {p.target_scene for p in scene.collidable_props()}
    assert targets == {"bank", "gunshop", "house"}


def test_translate_mutates_positions(loader):
    scene = WorldScene()
    scene.load(loader)
    before = [list(p.pos) for p in scene.props]
    scene.translate(5, -3)
    after = [list(p.pos) for p in scene.props]
    for b, a in zip(before, after, strict=True):
        assert a[0] == b[0] + 5
        assert a[1] == b[1] - 3


def test_scene_manager_switch_to_unknown_raises(loader):
    world = WorldScene()
    world.load(loader)
    mgr = SceneManager({"world": world}, initial="world")
    with pytest.raises(KeyError):
        mgr.switch_to("nope")


def test_scene_manager_initial_must_exist():
    with pytest.raises(KeyError):
        SceneManager({}, initial="world")


def test_scene_manager_tracks_current(loader):
    world = WorldScene()
    world.load(loader)
    bank = BankScene()
    bank.load(loader)
    mgr = SceneManager({"world": world, "bank": bank}, initial="world")
    assert mgr.current_name == "world"
    mgr.switch_to("bank")
    assert mgr.current_name == "bank"
    assert mgr.current is bank


def test_interior_scenes_load_one_backdrop(loader):
    for cls in (BankScene, GunshopScene, HouseScene):
        scene = cls()
        scene.load(loader)
        assert len(scene.props) == 1
        assert scene.props[0].collidable is False


def test_basement_scene_is_empty(loader):
    scene = BasementScene()
    scene.load(loader)
    assert scene.props == []


def test_base_scene_load_must_be_overridden():
    with pytest.raises(NotImplementedError):
        Scene().load(None)  # type: ignore[arg-type]
