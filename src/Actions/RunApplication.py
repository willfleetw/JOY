from Actions.Action import Action
import Variables

import subprocess

class RunApplication(Action):
    _executable: str
    _arguments: list[str]
    _working_directory: str
    _wait_for_finish: str
    _stdout_variable_name: str
    _stderr_variable_name: str

    def __init__(
            self,
            executable: str = None,
            arguments: list[str] = [],
            working_directory: str = None,
            wait_for_finish:bool = False,
            stdout_variable_name: str = None,
            stderr_variable_name: str = None
        ) -> None:

        self._executable = executable
        self._arguments = arguments
        self._working_directory = working_directory
        self._wait_for_finish = wait_for_finish
        self._stdout_variable_name = stdout_variable_name
        self._stderr_variable_name = stderr_variable_name

        super().__init__()

    def execute(self, cmd_context) -> None:
        args: list[str] = []
        if self._executable != None:
            args.append(Variables.replace_tags_in_string(self._executable, cmd_context))
        for argument in self._arguments:
            args.append(Variables.replace_tags_in_string(argument, cmd_context))

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self._working_directory)

        if self._wait_for_finish:
            stdout, stderr = process.communicate()
            if self._stdout_variable_name != None:
                Variables.Variables[self._stdout_variable_name] = stdout.decode(errors='ignore').strip()
            if self._stderr_variable_name != None:
                Variables.Variables[self._stderr_variable_name] = stderr.decode(errors='ignore').strip()

        return super().execute(cmd_context)