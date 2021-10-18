from Actions.Action import Action
import Audio
import Variables

class PlayAudio(Action):
    _audio_file: str
    _volume: float
    _wait_for_finish: bool

    def __init__(self, audio_file: str = "", volume: float = 100, wait_for_finish: bool = False) -> None:
        self._audio_file = audio_file

        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        self._volume = volume / 100

        self._wait_for_finish = wait_for_finish

        super().__init__()

    def execute(self, cmd_context) -> None:
        Audio.play_audio_file(Variables.replace_tags_in_string(self._audio_file, cmd_context), self._volume, self._wait_for_finish)

        return super().execute(cmd_context)

class StopAllSounds(Action):
    def execute(self, cmd_context) -> None:
        Audio.stop_all_sounds()

        return super().execute(cmd_context)