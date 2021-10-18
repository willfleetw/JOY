from Actions.Action import Action
import Variables

from sys import platform
import os

class CloseApplication(Action):
    _application: str

    def __init__(self, application: str = "") -> None:
        self._application = application

        super().__init__()

    def execute(self, cmd_context) -> None:
        app = Variables.replace_tags_in_string(self._application, cmd_context)
        if platform == "linux" or platform == "linux2":
            os.system(f"killall {app}")
        elif platform == "win32":
            os.system(f"TASKKILL /F /IM {app}")

        return super().execute(cmd_context)