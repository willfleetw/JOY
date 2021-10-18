from Actions.Action import Action
import AlarmManager
import Variables

from datetime import *
from word2number import w2n

class Timer(Action):
    _offset: str
    _unit: str
    _audio_file: str
    _volume: float

    def __init__(self, offset: str = "", unit: str = "", audio_file: str = "", volume: float = 100) -> None:
        self._offset = offset
        self._unit = unit
        self._audio_file = audio_file

        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        self._volume = volume/100

        super().__init__()

    def execute(self, cmd_context) -> None:
        offset = Variables.replace_tags_in_string(self._offset, cmd_context)

        try:
            offset = w2n.word_to_num(offset)
        except:
            offset = 0

        unit = Variables.replace_tags_in_string(self._unit, cmd_context)
        scale = 0
        if unit == "hours" or unit == "hour":
            scale = 3600
        elif unit == "minutes" or unit == "minute":
            scale = 60
        else:
            scale = 1

        audio_file = Variables.replace_tags_in_string(self._audio_file, cmd_context)
        AlarmManager.add_alarm(timedelta(seconds=offset * scale), audio_file, self._volume, is_timer=True)

        return super().execute(cmd_context)

class CancelTimers(Action):
    def __init__(self) -> None:
        super().__init__()

    def execute(self, cmd_match) -> None:
        AlarmManager.clear_all_timers()
        return super().execute(cmd_match)