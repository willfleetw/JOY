from Actions.Action import Action
import Variables

from word2number import w2n

class TextRemovePrefix(Action):
    _text: str
    _prefix: str
    _output_variable_name: str

    def __init__(self, text: str = "", prefix: str = "", output_variable_name: str = "") -> None:
        self._text = text
        self._output_variable_name = output_variable_name
        self._prefix = prefix

        super().__init__()

    def execute(self, cmd_context) -> None:
        Variables.Variables[self._output_variable_name] = Variables.replace_tags_in_string(self._text, cmd_context).removeprefix(self._prefix)

        return super().execute(cmd_context)

class TextRemoveSuffix(Action):
    _text: str
    _suffix: str
    _output_variable_name: str

    def __init__(self, text: str = "", suffix: str = "", output_variable_name: str = "") -> None:
        self._text = text
        self._output_variable_name = output_variable_name
        self._suffix = suffix

        super().__init__()

    def execute(self, cmd_context) -> None:
        Variables.Variables[self._output_variable_name] = Variables.replace_tags_in_string(self._text, cmd_context).removesuffix(self._suffix)

        return super().execute(cmd_context)

class TextParseNumber(Action):
    _text: str
    _output_variable_name: str

    def __init__(self, text: str = "", output_variable_name: str = "") -> None:
        self._text = text
        self._output_variable_name = output_variable_name

        super().__init__()

    def execute(self, cmd_context) -> None:
        value = str(w2n.word_to_num(Variables.replace_tags_in_string(self._text, cmd_context)))
        Variables.Variables[self._output_variable_name] = value

        return super().execute(cmd_context)

class SetVariable(Action):
    _value: str
    _output_variable_name: str

    def __init__(self, value: str = "", output_variable_name: str = "") -> None:
        self._value = value
        self._output_variable_name = output_variable_name

        super().__init__()

    def execute(self, cmd_context) -> None:
        Variables.Variables[self._output_variable_name] = Variables.replace_tags_in_string(self._value, cmd_context)

        return super().execute(cmd_context)