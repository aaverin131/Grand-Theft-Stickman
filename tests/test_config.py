from gts import config


def test_fps_scaled_speed_at_base_returns_player_base_speed():
    assert config.fps_scaled_speed(config.BASE_FPS) == config.PLAYER_BASE_SPEED


def test_fps_scaled_speed_off_base_uses_ratio():
    assert config.fps_scaled_speed(72) == config.PLAYER_BASE_SPEED
    assert config.fps_scaled_speed(70) == int(70 / 14.4)
    assert config.fps_scaled_speed(144) == int(144 / 14.4)


def test_fps_scaled_frame_hold_at_base_returns_constant():
    assert config.fps_scaled_frame_hold(config.BASE_FPS) == config.ANIMATION_FRAME_HOLD


def test_fps_scaled_frame_hold_off_base_uses_ratio():
    assert config.fps_scaled_frame_hold(70) == int(70 / 4.8)
    assert config.fps_scaled_frame_hold(144) == int(144 / 4.8)


def test_world_object_offsets_keys():
    assert set(config.WORLD_OBJECT_OFFSETS) == {
        "bank",
        "gunshop",
        "playground",
        "forest",
        "house",
    }


def test_inventory_slot_count():
    assert config.INVENTORY_SLOTS == 8


def test_asset_dir_exists():
    assert config.ASSET_DIR.is_dir()
