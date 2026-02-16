on run
  tell application "System Events"
    tell process "mGBA"
      set frontmost to true
      delay 0.5
      -- Press Enter/A to pass title screens
      key code 36
      delay 0.5
      -- Press A to select default menu item (Continue/New Game)
      key code 36
      delay 0.5
      -- Small buffer to allow load
      key code 36
    end tell
  end tell
end run
