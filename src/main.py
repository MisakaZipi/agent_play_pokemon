import json
import time
from pathlib import Path

from runner.mgba_runner import MgbaRunner
from observation.capture import ScreenCapture
from observation.sampler import AdaptiveSampler
from state.detector import SceneDetector


def load_config():
    config_path = Path(__file__).resolve().parents[1] / "config" / "config.json"
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dirs(cfg):
    logs_dir = Path(cfg["paths"]["logs_dir"])
    frames_dir = Path(cfg["paths"]["frames_dir"])
    logs_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir, frames_dir


def main():
    cfg = load_config()
    logs_dir, frames_dir = ensure_dirs(cfg)

    runner = MgbaRunner(cfg)
    runner.start()

    capture = ScreenCapture(cfg, frames_dir=frames_dir)
    detector = SceneDetector()
    sampler = AdaptiveSampler(cfg["capture"])

    while True:
        frame = capture.grab_frame()
        if frame is None:
            time.sleep(0.5)
            continue
        scene = detector.classify(frame)
        fps = sampler.next_fps(scene)
        capture.persist_frame(frame)
        time.sleep(max(0.001, 1.0 / fps))


if __name__ == "__main__":
    main()
