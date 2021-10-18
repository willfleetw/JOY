from Actions.Action import Action
import Audio
import Variables

class SayText(Action):
    _text: str

    def __init__(self, text: str = "") -> None:
        self._text = text

        super().__init__()

    def execute(self, cmd_context) -> None:
        Audio.text_to_speech(Variables.replace_tags_in_string(self._text, cmd_context))

        return super().execute(cmd_context)