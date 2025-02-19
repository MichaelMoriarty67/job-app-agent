import base64
import subprocess
from pathlib import Path
from uuid import uuid4
import pyautogui
import keyboard


class ComputerUseAction:
    def __init__(self, action: str, **kwargs):

        actions = [
            "key",
            "type",
            "mouse_move",
            "left_click",
            "left_click_drag",
            "right_click",
            "middle_click",
            "double_click",
            "screenshot",
            "cursor_position",
        ]

        self.action = action if action in actions else None
        self.kwargs = kwargs

        self.result = None

    def run_action(self):
        # control the screen depending on the action
        if self.action == "mouse_move":
            x_coord, y_coord = self.kwargs["coordinate"]
            pyautogui.moveTo(x=x_coord, y=y_coord)

            self._finish_action()

        elif self.action == "screenshot":
            self._finish_action()

        else:
            print("Don't have this action coded yet")

    def _finish_action(self):
        screenshot = self._take_screenshot()
        self.result = screenshot

    def _take_screenshot(self) -> str:
        """Takes a screenshot and returns the base64-encoded image."""
        screenshot_path = Path(f"/tmp/screenshot_{uuid4().hex}.png")

        # Use macOS built-in screencapture utility
        # -C flag captures cursor in image as well
        subprocess.run(["screencapture", "-x", "-C", str(screenshot_path)], check=True)

        # Read and encode the image in base64
        with open(screenshot_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
