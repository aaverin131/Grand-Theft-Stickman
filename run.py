"""Entry point for Grand Theft Stickman."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))

from gts.game import Game  # noqa: E402

Game().run()
