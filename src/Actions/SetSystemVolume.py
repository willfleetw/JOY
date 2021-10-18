from Actions.Action import Action
import Variables

import subprocess
from sys import platform
from word2number import w2n

class SetSystemVolume(Action):
    _volume: str

    def __init__(self, volume: str = "") -> None:
        self._volume = volume

        super().__init__()

    def execute(self, cmd_context) -> None:
        volume = Variables.replace_tags_in_string(self._volume, cmd_context)

        try:
            volume = w2n.word_to_num(volume)
        except:
            volume = 100

        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100

        if platform == "linux" or platform == "linux2":
            #not tested!
            subprocess.call(["amixer", "-D", "pulse", "sset", "Master", f"{volume}%"])
        if platform == "win32":
            subprocess.call([
                'C:/WINDOWS/System32/WindowsPowerShell/v1.0/powershell.exe',
                '-NoProfile', '-ExecutionPolicy', 'Unrestricted',
                './res/scripts/set_system_volume.ps1', f'"{volume/100}"'
                ])

        return super().execute(cmd_context)