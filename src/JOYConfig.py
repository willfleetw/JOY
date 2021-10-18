from Actions.Action import *
from Actions.CloseApplication import *
from Actions.GetUserSpeech import *
from Actions.Keyboard import *
from Actions.If import *
from Actions.PlayAudio import *
from Actions.RunApplication import *
from Actions.RunCommand import *
from Actions.SayText import *
from Actions.SetSystemVolume import *
from Actions.TextOperations import *
from Actions.Timer import *
from Actions.While import *
from Actions.Condition import *
from Command import *
import Variables

import yaml

def parse_getuserspeech(config) -> GetUserSpeech:
    wait_time = 2.5
    if "WaitTime" in config:
        wait_time = float(config["WaitTime"])

    output_variable_name = None
    if "OutputVariableName" in config:
        output_variable_name = config["OutputVariableName"]

    return GetUserSpeech(wait_time=wait_time, output_variable_name=output_variable_name)

def parse_saytext(config) -> SayText:
    text = ""
    if "Text" in config:
        text = config["Text"]

    return SayText(text=text)

def parse_playaudio(config) -> PlayAudio:
    audio_file = ""
    if "AudioFile" in config:
        audio_file = config["AudioFile"]

    volume = 100
    if "Volume" in config:
        volume = config["Volume"]

    wait_for_finish = False
    if "WaitForFinish" in config:
        wait_for_finish = config["WaitForFinish"]

    return PlayAudio(audio_file=audio_file, volume=volume, wait_for_finish=wait_for_finish)

def parse_stopallsounds(config) -> StopAllSounds:
    return StopAllSounds()

def parse_setsystemvolume(config) -> SetSystemVolume:
    volume = ""
    if "Volume" in config:
        volume = config["Volume"]

    return SetSystemVolume(volume=volume)

def parse_runapplication(config) -> RunApplication:
    executable = None
    if "Executable" in config:
        executable = config["Executable"]

    arguments = []
    if "Arguments" in config:
        arguments = config["Arguments"]

    working_directory = None
    if "WorkingDirectory" in config:
        working_directory = config["WorkingDirectory"]

    wait_for_finish = False
    if "WaitForFinish" in config:
        wait_for_finish = config["WaitForFinish"]

    stdout_variable = None
    if "StdOutVariable" in config:
        stdout_variable = config["StdOutVariable"]

    stderr_variable = None
    if "StdErrVariable" in config:
        stdout_variable = config["StdErrVariable"]

    return RunApplication(
        executable=executable,
        arguments=arguments,
        working_directory=working_directory,
        wait_for_finish=wait_for_finish,
        stdout_variable_name=stdout_variable,
        stderr_variable_name=stderr_variable
        )

def parse_runcommand(config) -> RunCommand:
    command_name = ""
    if "CommandName" in config:
        command_name = config["CommandName"]

    return RunCommand(command_name=command_name)

def parse_closeapplication(config) -> CloseApplication:
    application = ""
    if "Application" in config:
        application = config["Application"]

    return CloseApplication(application=application)

def parse_setvariable(config) -> SetVariable:
    value = ""
    if "Value" in config:
        value = config["Value"]

    output_variable = ""
    if "OutputVariable" in config:
        output_variable = config["OutputVariable"]

    return SetVariable(value=value, output_variable_name=output_variable)

def parse_textremoveprefix(config) -> TextRemovePrefix:
    text = ""
    if "Text" in config:
        text = config["Text"]

    prefix = ""
    if "Prefix" in config:
        prefix = config["Prefix"]

    output_variable = ""
    if "OutputVariable" in config:
        output_variable = config["OutputVariable"]

    return TextRemovePrefix(text=text, prefix=prefix, output_variable_name=output_variable)

def parse_textremovesuffix(config) -> TextRemoveSuffix:
    text = ""
    if "Text" in config:
        text = config["Text"]

    suffix = ""
    if "Suffix" in config:
        suffix = config["Suffix"]

    output_variable = ""
    if "OutputVariable" in config:
        output_variable = config["OutputVariable"]

    return TextRemoveSuffix(text=text, suffix=suffix, output_variable_name=output_variable)

def parse_textparsenumber(config) -> TextParseNumber:
    text = ""
    if "Text" in config:
        text = config["Text"]

    output_variable = ""
    if "OutputVariable" in config:
        output_variable = config["OutputVariable"]

    return TextParseNumber(text=text, output_variable_name=output_variable)

def parse_if(config) -> If:
    condition_sets: list[ConditionSet] = []
    if "ConditionSets" in config:
        for conditionset in config["ConditionSets"]:
            condition_sets.append(parse_conditionset(conditionset))

    true_actions: list[Action] = []
    if "TrueActions" in config:
        for action in config["TrueActions"]:
            true_actions.append(parse_action(action))

    false_actions: list[Action] = []
    if "FalseActions" in config:
        for action in config["FalseActions"]:
            false_actions.append(parse_action(action))

    return If(condition_sets=condition_sets, true_actions=true_actions, false_actions=false_actions)

def parse_while(config) -> While:
    condition_sets: list[ConditionSet] = []
    if "ConditionSets" in config:
        for conditionset in config["ConditionSets"]:
            condition_sets.append(parse_conditionset(conditionset))

    actions: list[Action] = []
    if "Actions" in config:
        for action in config["Actions"]:
            actions.append(parse_action(action))

    return While(condition_sets=condition_sets, actions=actions)

def parse_timer(config) -> Timer:
    offset = ""
    if "Offset" in config:
        offset = config["Offset"]

    unit = ""
    if "Unit" in config:
        unit = config["Unit"]

    audio_file = ""
    if "AudioFile" in config:
        audio_file = config["AudioFile"]

    volume = 100
    if "Volume" in config:
        volume = config["Volume"]

    return Timer(offset=offset, unit=unit, audio_file=audio_file, volume=volume)

def parse_canceltimers(config) -> CancelTimers:
    return CancelTimers()

def parse_sendkeys(config) -> SendKeys:
    keys = ""
    if "Keys" in config:
        keys = config["Keys"]

    return SendKeys(keys=keys)

def parse_conditionset(config) -> ConditionSet:
    conditions: list[Condition] = []
    if "Conditions" in config:
        for condition in config["Conditions"]:
            conditions.append(parse_condition(condition))

    return ConditionSet(conditions=conditions)

def parse_equals(config) -> Equals:
    left_operand = ""
    if "LeftOperand" in config:
        left_operand = config["LeftOperand"]

    right_operand = ""
    if "RightOperand" in config:
        right_operand = config["RightOperand"]

    negate = False
    if "Negate" in config:
        negate = config["Negate"]

    return Equals(left_operand=left_operand, right_operand=right_operand, negate=negate)

def parse_condition(config) -> Condition:
    condition: Condition = None

    condition_type = config["Type"]
    if condition_type == "Equals":
        condition = parse_equals(config)

    return condition

def parse_action(config) -> Action:
    action: Action = None

    action_type = config["Type"]
    if action_type == "SayText":
        action = parse_saytext(config)
    elif action_type == "GetUserSpeech":
        action = parse_getuserspeech(config)
    elif action_type == "PlayAudio":
        action = parse_playaudio(config)
    elif action_type == "StopAllSounds":
        action = parse_stopallsounds(config)
    elif action_type == "SetSystemVolume":
        action = parse_setsystemvolume(config)
    elif action_type == "RunApplication":
        action = parse_runapplication(config)
    elif action_type == "RunCommand":
        action = parse_runcommand(config)
    elif action_type == "CloseApplication":
        action = parse_closeapplication(config)
    elif action_type == "SetVariable":
        action = parse_setvariable(config)
    elif action_type == "TextRemovePrefix":
        action = parse_textremoveprefix(config)
    elif action_type == "TextRemoveSuffix":
        action = parse_textremovesuffix(config)
    elif action_type == "TextParseNumber":
        action = parse_textparsenumber(config)
    elif action_type == "If":
        action = parse_if(config)
    elif action_type == "While":
        action = parse_while(config)
    elif action_type == "Timer":
        action = parse_timer(config)
    elif action_type == "CancelTimers":
        action = parse_canceltimers(config)
    elif action_type == "SendKeys":
        action = parse_sendkeys(config)

    return action

def load_commands(config):
    global Commands
    command_list = config["Commands"]
    for command_name in command_list:
        command = command_list[command_name]
        regex_str: str = Variables.replace_tags_in_string(command["Regex"])

        actions: list[Action] = []
        for action in command["Actions"]:
            actions.append(parse_action(action))

        Commands[command_name] = Command(command_name, regex_str, actions)

    startup_commands = config["StartupCommands"]
    if startup_commands != None:
        for command in startup_commands:
            Commands[command].execute("", wait_to_finish=True)


def load_config(config_path) -> None:
    with open(config_path) as file:
        config = yaml.safe_load(file)

    starting_variables = config["StartingVariables"]
    for variableName in starting_variables:
        Variables.Variables[variableName] = starting_variables[variableName]

    load_commands(config)