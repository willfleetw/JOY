from Actions.Action import Action
import Variables

import keyboard

class SendKeys(Action):
    _keys: str

    def __init__(self, keys: str) -> None:
        self._keys = keys

        super().__init__()

    def execute(self, cmd_context) -> None:
        keys = Variables.replace_tags_in_string(self._keys, cmd_context)

        keyboard.send(keys)

        return super().execute(cmd_context)