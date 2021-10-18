from Actions.Action import Action

import re
from threading import Thread

class Command(object):
    _name: str = ""
    _regex = None
    _actions: list[Action] = []

    _last_match = None

    def __init__(self, name:str, regex_pattern:str, actions: list[Action]) -> None:
        self._name = name
        self._regex = re.compile(regex_pattern)
        self._actions = actions

    def matches(self, speech: str) -> bool:
        self._last_match = self._regex.match(speech)
        return self._last_match != None

    def execute(self, speech: str, wait_to_finish: bool = False) -> None:
        print(f"Executing: {self._name} <= {speech}")
        thread = Thread(target=self._execute_impl, args=(), daemon=True)
        thread.start()
        if wait_to_finish:
            thread.join()

    def _execute_impl(self) -> None:
        try:
            for action in self._actions:
                action.execute(self._last_match)
        except Exception as e:
            print(f"Error during executing '{self._name}': {e}")

        return

Commands: dict[str, Command] = {}
global LastHeardSpeech
LastHeardSpeech: str = ""