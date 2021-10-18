from Actions.Action import Action
import Command
import Variables

import time

class GetUserSpeech(Action):
    _wait_time: float
    _output_variable_name: str

    def __init__(self, wait_time: float, output_variable_name: str) -> None:
        self._wait_time = wait_time
        self._output_variable_name = output_variable_name

        super().__init__()

    def execute(self, cmd_context) -> None:
        time.sleep(self._wait_time)

        if self._output_variable_name != None:
            Variables.Variables[self._output_variable_name] = Command.LastHeardSpeech

        return super().execute(cmd_context)