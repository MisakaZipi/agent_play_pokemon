import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image
try:
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID,
    )
except Exception:  # pragma: no cover
    CGWindowListCopyWindowInfo = None


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
        window_id = self._resolve_window_id_quartz()
        if window_id:
            self.window_id = window_id
            return self.window_id
        process_name = self.cfg.get("window", {}).get("process_name", "mGBA")
        script = (
            'tell application "System Events" to '
            f'tell (first process whose name is "{process_name}") to '
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

    def _resolve_window_id_quartz(self):
        if CGWindowListCopyWindowInfo is None:
            return None
        owner_name = self.cfg.get("window", {}).get("process_name", "mGBA")
        windows = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly, kCGNullWindowID
        )
        for w in windows:
            if w.get("kCGWindowOwnerName") == owner_name and w.get("kCGWindowLayer") == 0:
                return w.get("kCGWindowNumber")
        return None

    def _resolve_window_bounds(self):
        bounds = self._resolve_window_bounds_quartz()
        if bounds:
            return bounds
        process_name = self.cfg.get("window", {}).get("process_name", "mGBA")
        script = (
            'tell application "System Events" to '
            f'tell (first process whose name is "{process_name}") to '
            'if (count of windows) > 0 then '
            'set pos to position of first window '
            'set sz to size of first window '
            'return (item 1 of pos) & "," & (item 2 of pos) & "," & (item 1 of sz) & "," & (item 2 of sz) '
            'else return "" end if'
        )
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=False,
        )
        value = result.stdout.strip()
        if not value:
            return None
        parts = value.split(",")
        if len(parts) != 4:
            return None
        try:
            return tuple(int(float(p)) for p in parts)
        except ValueError:
            return None

    def _resolve_window_bounds_quartz(self):
        if CGWindowListCopyWindowInfo is None:
            return None
        owner_name = self.cfg.get("window", {}).get("process_name", "mGBA")
        windows = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly, kCGNullWindowID
        )
        for w in windows:
            if w.get("kCGWindowOwnerName") == owner_name and w.get("kCGWindowLayer") == 0:
                bounds = w.get("kCGWindowBounds")
                if bounds:
                    x = int(bounds.get("X", 0))
                    y = int(bounds.get("Y", 0))
                    w_ = int(bounds.get("Width", 0))
                    h_ = int(bounds.get("Height", 0))
                    if w_ > 0 and h_ > 0:
                        return x, y, w_, h_
        return None

    def _log(self, msg: str):
        log_path = self.frames_dir.parent / "capture.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(msg + "\n")

    def grab_frame(self):
        window_id = self._resolve_window_id()
        if not window_id:
            bounds = self._resolve_window_bounds()
            if not bounds:
                self._log("[capture] window_id not found; bounds not found")
                return self.last_frame
            x, y, w, h = bounds
            ts = int(time.time() * 1000)
            tmp_path = self.frames_dir / f"frame_{ts}.png"
            result = subprocess.run(
                ["screencapture", "-x", "-R", f"{x},{y},{w},{h}", str(tmp_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                check=False,
            )
            if not tmp_path.exists():
                self._log(
                    f"[capture] screencapture -R failed rc={result.returncode} err={result.stderr.decode(errors='ignore')}"
                )
                return self.last_frame
            with Image.open(tmp_path) as img:
                frame = np.array(img.convert("RGB"))
            if not self.persist:
                tmp_path.unlink(missing_ok=True)
            else:
                self._log(f"[capture] saved {tmp_path.name} (bounds)")
            self.last_frame = frame
            return frame

        ts = int(time.time() * 1000)
        tmp_path = self.frames_dir / f"frame_{ts}.png"

        result = subprocess.run(
            ["screencapture", "-x", "-l", str(window_id), str(tmp_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=False,
        )

        if not tmp_path.exists():
            self._log(f"[capture] screencapture failed rc={result.returncode} err={result.stderr.decode(errors='ignore')}")
            return self.last_frame

        with Image.open(tmp_path) as img:
            frame = np.array(img.convert("RGB"))

        if not self.persist:
            tmp_path.unlink(missing_ok=True)
        else:
            self._log(f"[capture] saved {tmp_path.name}")

        self.last_frame = frame
        return frame

    def persist_frame(self, frame):
        # Frames are already persisted via screencapture when enabled.
        # Keep hook for future debug saves.
        return
