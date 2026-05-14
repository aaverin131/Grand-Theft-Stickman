import pytest

from gts.inventory import Inventory


def test_initial_slots_are_none():
    inv = Inventory(size=4)
    assert list(inv) == [None, None, None, None]
    assert inv.active is None
    assert inv.selected == 0


def test_size_must_be_positive():
    with pytest.raises(ValueError):
        Inventory(size=0)


def test_cycle_wraps_forward_and_backward():
    inv = Inventory(size=3)
    inv.cycle(1)
    assert inv.selected == 1
    inv.cycle(2)
    assert inv.selected == 0
    inv.cycle(-1)
    assert inv.selected == 2


def test_selected_setter_modulos():
    inv = Inventory(size=4)
    inv.selected = 9
    assert inv.selected == 1
    inv.selected = -1
    assert inv.selected == 3


def test_put_rejects_out_of_range():
    inv = Inventory(size=2)
    with pytest.raises(IndexError):
        inv.put(2, None)
    with pytest.raises(IndexError):
        inv.put(-1, None)


def test_put_and_active(loader):  # noqa: ARG001 — fixture pulls in pygame init
    from gts.inventory import Glock

    inv = Inventory(size=3)
    glock = Glock(_loader_for_test())
    inv.put(1, glock)
    inv.selected = 1
    assert inv.active is glock
    assert inv.slot(1) is glock
    assert inv.slot(0) is None


def _loader_for_test():
    from gts import config
    from gts.assets import AssetLoader

    return AssetLoader(config.ASSET_DIR)
