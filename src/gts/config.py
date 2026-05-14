"""Game-wide constants and FPS-scaling helpers."""

from pathlib import Path

# --- Paths --------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT_DIR / "Assets"
SAVES_FILE = ROOT_DIR / "saves.csv"

# --- Window -------------------------------------------------------------------
WINDOW_TITLE = "Grand Theft Stickman"
# Monitor size minus this margin on each axis.
WINDOW_MARGIN = 200

# --- Game loop ----------------------------------------------------------------
TARGET_FPS = 70
# Reference FPS. Speed and animation rates scale relative to this so motion
# is consistent across refresh rates.
BASE_FPS = 72

# --- Player -------------------------------------------------------------------
PLAYER_BASE_SPEED = 5
SPRINT_MULTIPLIER = 2
ANIMATION_FRAME_HOLD = 15
DANCE_FRAME_HOLD = 15
INITIAL_PLAYER_POS = (300, 100)

# --- Combat -------------------------------------------------------------------
BULLET_SPEED = 10

# --- Economy ------------------------------------------------------------------
STARTING_MONEY = 10
STARTING_HEALTH = 100

# --- Colors -------------------------------------------------------------------
COLOR_WORLD_BG = (120, 214, 60)
COLOR_INTERIOR_BG = (0, 0, 0)
COLOR_COLLISION_OUTLINE = (255, 0, 0)
COLOR_TEXT = (0, 0, 0)

# --- Inventory / toolbar ------------------------------------------------------
INVENTORY_SLOTS = 8
TOOLBAR_SLOT_WIDTH = 103
TOOLBAR_OFFSET_X = -410.5     # toolbar left edge relative to screen center
TOOLBAR_FROM_BOTTOM = 120     # toolbar top edge offset from screen bottom
TOOLBAR_ITEM_INSET_X = 2.5    # icon X offset inside a slot
TOOLBAR_ITEM_INSET_Y = 3      # icon Y offset inside a slot
TOOLBAR_FRAME_INSET = 3       # selection-frame inset

# --- Save UI ------------------------------------------------------------------
SAVE_BUTTON_SIZE = 100

# --- World object placements --------------------------------------------------
# Offsets from the player's spawn position for each prop in the overworld.
# `background` is anchored to -playerxy and handled separately.
WORLD_OBJECT_OFFSETS = {
    "bank":        (984,  -190),
    "gunshop":     (372,  -370),
    "playground":  (-250,  625),
    "forest":      (-400,  770),
    "house":       (-512, -140),
}

# --- Derived helpers ----------------------------------------------------------
def fps_scaled_speed(fps: int = TARGET_FPS) -> int:
    """Player speed scaled so movement is consistent across FPS targets."""
    return PLAYER_BASE_SPEED if fps == BASE_FPS else int(fps / 14.4)


def fps_scaled_frame_hold(fps: int = TARGET_FPS) -> int:
    """How many game ticks each animation frame is shown for."""
    return ANIMATION_FRAME_HOLD if fps == BASE_FPS else int(fps / 4.8)
