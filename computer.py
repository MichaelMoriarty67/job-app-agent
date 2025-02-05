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
        screenshot = pyautogui.screenshot()
        self.result = screenshot
