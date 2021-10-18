import re
from datetime import *
import os

import AlarmManager

Variables: dict[str, str] = {}
__var_regex = re.compile("{[a-zA-Z0-9:% ]+}")

def parse_tag(tag: str, cmd_context = None) -> str:
    value: str = ""

    if tag == "{}":
        return value

    var: str = tag[1:-1]

    if var.startswith("TIME:"):
        now = datetime.now()
        try:
            value = now.strftime(var.removeprefix("TIME:"))
        except:
            value = "could not get formatted time"

    elif var == "NUMALARMS":
        value += str(AlarmManager.num_alarms())

    elif var == "ALARMS":
        count = 1
        for alarm_string in AlarmManager.get_alarms_strings():
            alarm_string = alarm_string.removesuffix(" ")
            value += f"{count}, {alarm_string}, "
            count += 1

    elif var.startswith("ENV:"):
        env_var = var.removeprefix("ENV:")
        if env_var in os.environ:
            value = os.environ[env_var]
        else:
            value = "variable not set"

    elif var == "CMD":
        value = cmd_context.string

    elif var.startswith("CMD:"):
        segment_number = var.removeprefix("CMD:")
        try:
            segment_number = int(segment_number) + 1
            value = cmd_context.group(segment_number)
        except:
            return "not a valid command segment"

    elif var in Variables:
        value = Variables[var]

    else:
        value = "variable not set"

    return value

"""
Replace any variable tags {...} with their respective value, and look for cmd segment tokens {CMD:<num>}
"""
def replace_tags_in_string(text: str, cmd_context = None) -> str:
    compiled_text: str = text
    for tag in __var_regex.findall(text):
        replace_value = parse_tag(tag, cmd_context)

        if replace_value != None:
            compiled_text = compiled_text.replace(tag, replace_value)

    return compiled_text