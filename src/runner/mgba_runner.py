import subprocess
import time
from pathlib import Path


class MgbaRunner:
    def __init__(self, cfg):
        self.cfg = cfg
        self.process = None
        self.base_dir = Path(__file__).resolve().parents[2]

    def start(self):
        mgba_path = Path(self.cfg["mgba_path"]).expanduser().resolve()
        rom_path = Path(self.cfg["rom_path"]).expanduser().resolve()
        if not mgba_path.exists():
            raise FileNotFoundError(f"mGBA not found: {mgba_path}")
        if not rom_path.exists():
            raise FileNotFoundError(f"ROM not found: {rom_path}")

        self.process = subprocess.Popen(
            [str(mgba_path), str(rom_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1.5)
        self._auto_start_game()

    def _auto_start_game(self):
        script_path = self.base_dir / "scripts" / "start_game.applescript"
        if script_path.exists():
            subprocess.run(
                ["osascript", str(script_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
