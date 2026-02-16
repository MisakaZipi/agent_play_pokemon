import time

import pyautogui
import subprocess


def focus_mgba():
    subprocess.run(["osascript", "-e", 'tell application "mGBA" to activate'], check=False)
    time.sleep(1.0)


def press(key: str, hold_s: float = 1.0, delay_s: float = 1.0):
    print(f"[test_controls] press {key} (hold={hold_s}s)")
    pyautogui.keyDown(key)
    time.sleep(hold_s)
    pyautogui.keyUp(key)
    time.sleep(delay_s)


def main():
    print("[test_controls] Focusing mGBA window...")
    focus_mgba()
    time.sleep(2)

    # Directions
    press("up")
    press("right")
    press("down")
    press("left")

    # Enter opens menu/options
    press("enter")

    # X confirm (A button)
    press("x")

    # Enter bag (if in menu)
    press("enter")

    # Z closes bag / options
    press("z")
    press("z")

    print("[test_controls] Done.")


if __name__ == "__main__":
    main()
