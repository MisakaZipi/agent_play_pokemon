import subprocess
import sys
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

        if not self._is_mgba_running():
            self.process = subprocess.Popen(
                [str(mgba_path), str(rom_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        time.sleep(1.5)

    def _is_mgba_running(self):
        result = subprocess.run(
            ["pgrep", "-x", "mGBA"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
