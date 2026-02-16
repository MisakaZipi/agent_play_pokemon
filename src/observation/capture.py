import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image


class ScreenCapture:
    def __init__(self, cfg, frames_dir: Path):
        self.cfg = cfg
        self.frames_dir = frames_dir
        self.last_frame = None
        self.window_id = None
        self.persist = cfg["capture"].get("persist_frames", False)

    def _resolve_window_id(self):
        if self.window_id:
            return self.window_id
        script = (
            'tell application "System Events" to '
            'tell (first process whose name is "mGBA") to '
            'if (count of windows) > 0 then '
            'return id of first window '
            'else return "" end if'
        )
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=False,
        )
        window_id = result.stdout.strip()
        self.window_id = window_id if window_id else None
        return self.window_id

    def grab_frame(self):
        window_id = self._resolve_window_id()
        if not window_id:
            # No window found, return last frame to keep loop stable.
            return self.last_frame

        ts = int(time.time() * 1000)
        tmp_path = self.frames_dir / f"frame_{ts}.png"

        subprocess.run(
            ["screencapture", "-x", "-l", str(window_id), str(tmp_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

        if not tmp_path.exists():
            return self.last_frame

        with Image.open(tmp_path) as img:
            frame = np.array(img.convert("RGB"))

        if not self.persist:
            tmp_path.unlink(missing_ok=True)

        self.last_frame = frame
        return frame

    def persist_frame(self, frame):
        # Frames are already persisted via screencapture when enabled.
        # Keep hook for future debug saves.
        return
