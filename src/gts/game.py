"""Game orchestrator: window, main loop, scene/inventory/HUD wiring."""

from __future__ import annotations

import datetime as _dt

import pygame

from . import config
from .aim import aim_angle_facing
from .assets import AssetLoader
from .entities import Player
from .input import facing_from_input, movement_delta
from .inventory import Blade, Glock, Inventory, Punch
from .persistence import SaveFile, SaveRecord
from .scenes import (
    BankScene,
    BasementScene,
    GunshopScene,
    HouseScene,
    SceneManager,
    WorldScene,
)
from .ui import HUD, SaveMenu


def _sprite_pivot(
    center: tuple[float, float], sprite: pygame.Surface, top_left_offset: tuple[int, int]
) -> tuple[float, float]:
    """Center point a sprite would occupy if blitted at `center + offset`."""
    w, h = sprite.get_size()
    return (center[0] + top_left_offset[0] + w / 2, center[1] + top_left_offset[1] + h / 2)


PLAYER_FOOT_SIZE = (40, 30)
PLAYER_FOOT_OFFSET_Y = 30
DANCE_SOUND = "stickman/fortnite dance/fortnitedance.mp3"
ICON_PATH = "icon2.png"
HEAD_IMAGE = "stickman/weapon/head.png"
# Sprite offsets matched to the original game's action() blits.
WEAPON_BLIT_OFFSET = (-50, -50)
HEAD_BLIT_OFFSET = (-19, -34)
EMPTY_SLOT_TOKEN = "1"
SAVE_TIMESTAMP_FMT = "%Y-%m-%d %I:%M %p"


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()

        info = pygame.display.Info()
        margin = config.WINDOW_MARGIN
        size = (max(640, info.current_w - margin), max(480, info.current_h - margin))
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption(config.WINDOW_TITLE)

        self.loader = AssetLoader(config.ASSET_DIR)
        pygame.display.set_icon(self.loader.image(ICON_PATH))

        frame_hold = config.fps_scaled_frame_hold(config.TARGET_FPS)
        self.player = Player(self.loader, frame_hold=frame_hold)

        scenes = {
            "world": WorldScene(),
            "bank": BankScene(),
            "gunshop": GunshopScene(),
            "house": HouseScene(),
            "basement": BasementScene(),
        }
        for s in scenes.values():
            s.load(self.loader)
        self.scenes = SceneManager(scenes, "world")

        self.inventory = Inventory(config.INVENTORY_SLOTS)
        self.inventory.put(0, Punch(self.loader, frame_hold=frame_hold))
        self.inventory.put(1, Glock(self.loader))
        self.inventory.put(2, Blade(self.loader, frame_hold=frame_hold))

        self.font = pygame.font.SysFont("Arial", 24)
        self.hud = HUD(self.font)
        self.save_menu = SaveMenu()
        self.savefile = SaveFile(config.SAVES_FILE)

        self.toolbar_image = self.loader.image("gui/toolbar.png")
        self.toolbar_frame = self.loader.image("gui/toolbarframe.png")
        self.save_button_image = self.loader.image("gui/saveoption/savebutton.png")
        self.save_list_image = self.loader.image("gui/saveoption/savelistempty.png")
        self.save_slot_image = self.loader.image("gui/saveoption/saveslot.png")
        self.head_image = self.loader.image(HEAD_IMAGE)

        self.clock = pygame.time.Clock()
        self.running = True

    def run(self) -> None:
        try:
            while self.running:
                self._tick()
                pygame.display.flip()
        finally:
            pygame.quit()

    def _tick(self) -> None:
        self.clock.tick(config.TARGET_FPS)
        screen_size = self.screen.get_size()

        e_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.MOUSEWHEEL:
                self.inventory.cycle(event.y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._on_mouse_down(event, screen_size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    e_pressed = True
                elif event.key == pygame.K_ESCAPE:
                    if self.scenes.current_name != "world":
                        self.scenes.switch_to("world")
                elif event.key == pygame.K_f and not self.player.dancing:
                    self.player.start_dance()
                    self.loader.sound(DANCE_SOUND).play()

        keys = pygame.key.get_pressed()
        sprint = bool(keys[pygame.K_LSHIFT])
        speed = config.fps_scaled_speed(config.TARGET_FPS) * (
            config.SPRINT_MULTIPLIER if sprint else 1
        )
        up, down = bool(keys[pygame.K_w]), bool(keys[pygame.K_s])
        left, right = bool(keys[pygame.K_a]), bool(keys[pygame.K_d])
        moving = any((up, down, left, right))
        facing = facing_from_input(left=left, right=right)

        sw, sh = screen_size
        center = (sw / 2, sh / 2)
        aim_angle = 0.0
        if self.player.aiming:
            aim_angle, aim_facing = aim_angle_facing(pygame.mouse.get_pos(), center)
            facing = aim_facing

        scene = self.scenes.current
        weapon = self.inventory.active
        dash_dx, dash_dy = weapon.dash_delta() if weapon is not None else (0.0, 0.0)
        dashing = dash_dx != 0.0 or dash_dy != 0.0
        if dashing:
            # dash_delta is the player's intended motion; the world translates opposite.
            dx, dy = -dash_dx, -dash_dy
            moving = False
            if dash_dx > 0:
                facing = "right"
            elif dash_dx < 0:
                facing = "left"
        else:
            dx, dy = movement_delta(up=up, down=down, left=left, right=right, speed=speed)
        if dx or dy:
            scene.translate(dx, dy)
            if scene.name == "world":
                foot = self._player_foot_rect(screen_size)
                blocking = self._first_blocking_prop(scene, foot)
                if blocking is not None:
                    if e_pressed and blocking.target_scene is not None and not dashing:
                        self.scenes.switch_to(blocking.target_scene)
                        e_pressed = False
                    else:
                        scene.translate(-dx, -dy)
                        moving = False

        if weapon is not None:
            weapon.update()

        active_scene = self.scenes.current
        active_scene.draw_background(self.screen)
        active_scene.draw_props(self.screen)

        weapon_in_hand = weapon is not None and (self.player.aiming or not weapon.requires_aim)
        sprite = self.player.update(
            moving=moving, sprint=sprint, facing=facing, show_weapon=weapon_in_hand
        )
        self.screen.blit(
            sprite,
            (center[0] - sprite.get_width() / 2, center[1] - sprite.get_height() / 2),
        )
        if weapon_in_hand:
            overlay_angle = aim_angle if self.player.aiming else 0.0
            self._draw_aim(center, weapon.aim_sprite(), overlay_angle, self.player.facing)

        self._draw_hud(screen_size)

    def _on_mouse_down(self, event: pygame.event.Event, screen_size: tuple[int, int]) -> None:
        if event.button not in (1, 3):
            return

        if event.button == 1:
            overlay_size = self.save_list_image.get_size()
            on_save_button = HUD.save_button_rect(screen_size).collidepoint(event.pos)
            if on_save_button and not self.save_menu.is_open:
                self.savefile.append(self._snapshot())
            if on_save_button or self.save_menu.is_open:
                self.save_menu.handle_click(event.pos, screen_size, overlay_size)
                return

        weapon = self.inventory.active
        if weapon is not None and not weapon.requires_aim:
            if event.button == 1:
                weapon.fire("primary")
            else:
                sw, sh = screen_size
                direction = (event.pos[0] - sw / 2, event.pos[1] - sh / 2)
                weapon.fire("secondary", direction=direction)
            return

        if event.button == 3:
            self.player.toggle_aim()
            return
        if self.player.aiming and weapon is not None:
            weapon.fire()

    def _draw_hud(self, screen_size: tuple[int, int]) -> None:
        self.screen.blit(self.toolbar_image, HUD.toolbar_pos(screen_size))
        for i in range(self.inventory.size):
            w = self.inventory.slot(i)
            if w is not None:
                self.screen.blit(w.icon, HUD.slot_icon_pos(screen_size, i))
        self.screen.blit(
            self.toolbar_frame, HUD.slot_frame_pos(screen_size, self.inventory.selected)
        )
        self.screen.blit(self.save_button_image, HUD.save_button_pos(screen_size))
        self.screen.blit(self.hud.fps_surface(self.clock.get_fps()), (10, 10))

        if self.save_menu.is_open:
            overlay_size = self.save_list_image.get_size()
            overlay_rect = SaveMenu.overlay_rect(screen_size, overlay_size)
            self.screen.blit(self.save_list_image, overlay_rect.topleft)
            slot_h = self.save_slot_image.get_height()
            slot_x = overlay_rect.left + 10
            for i, record in enumerate(self.savefile.four_slots()):
                y = overlay_rect.top + 10 + i * (slot_h + 4)
                self.screen.blit(self.save_slot_image, (slot_x, y))
                if record is not None:
                    self._draw_save_summary(record, slot_x + 10, y + 8)

    def _draw_save_summary(self, record: SaveRecord, x: int, y: int) -> None:
        line = f"${record.money}  HP {record.health}  {record.condition}  {record.timestamp}"
        self.screen.blit(self.font.render(line, True, config.COLOR_TEXT), (x, y))

    def _player_foot_rect(self, screen_size: tuple[int, int]) -> pygame.Rect:
        sw, sh = screen_size
        w, h = PLAYER_FOOT_SIZE
        return pygame.Rect(int(sw / 2 - w / 2), int(sh / 2 + PLAYER_FOOT_OFFSET_Y), w, h)

    @staticmethod
    def _first_blocking_prop(scene, foot: pygame.Rect):
        for prop in scene.collidable_props():
            rect = prop.image.get_bounding_rect().move(int(prop.pos[0]), int(prop.pos[1]))
            if rect.colliderect(foot):
                return prop
        return None

    def _draw_aim(
        self,
        center: tuple[float, float],
        weapon_sprite: pygame.Surface,
        angle: float,
        facing: str,
    ) -> None:
        head_pivot = _sprite_pivot(center, self.head_image, HEAD_BLIT_OFFSET)
        wpn_pivot = _sprite_pivot(center, weapon_sprite, WEAPON_BLIT_OFFSET)

        head = pygame.transform.rotate(self.head_image, angle)
        wpn = pygame.transform.rotate(weapon_sprite, angle)
        if facing == "left":
            head = pygame.transform.flip(head, False, True)
            wpn = pygame.transform.flip(wpn, False, True)

        self.screen.blit(wpn, wpn.get_rect(center=wpn_pivot))
        self.screen.blit(head, head.get_rect(center=head_pivot))

    def _snapshot(self) -> SaveRecord:
        slots: list[str] = []
        for i in range(1, config.INVENTORY_SLOTS):
            w = self.inventory.slot(i)
            slots.append(w.name if w is not None else EMPTY_SLOT_TOKEN)
        return SaveRecord(
            name="stickman.png",
            x=int(self.player.world_pos[0]),
            y=int(self.player.world_pos[1]),
            money=config.STARTING_MONEY,
            health=config.STARTING_HEALTH,
            slots=slots,
            condition=self.scenes.current_name,
            timestamp=_dt.datetime.now().strftime(SAVE_TIMESTAMP_FMT),
        )
