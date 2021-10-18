from Actions.Action import Action
from Command import Commands
import Variables

class RunCommand(Action):
    _command_name: str

    def __init__(self, command_name: str) -> None:
        self._command_name = command_name
        super().__init__()

    def execute(self, cmd_context) -> None:
        Commands[Variables.replace_tags_in_string(self._command_name, cmd_context)].execute(cmd_context[0])
        return super().execute(cmd_context)