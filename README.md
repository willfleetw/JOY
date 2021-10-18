# JOY
**Voice activated personal assistant**

## Description

The name is a reference to Blade Runner 2049, my favorite movie :).

JOY is a personal project inspired from [VoiceAttack](https://store.steampowered.com/app/583010/VoiceAttack/), a Windows program sold on Steam which allows users to control their PC and games via voice commands. It is really quite good, with a clear and functional UI. I recommend you give it a look, it even has a quite generous free demo!

I quite like VoiceAttack, but unfortunately it is not cross-platform, it only runs on Windows. I would like to make a cross-platform project, with more fine control over behavior. The end goal is to run JOY on something like a Raspberry Pi, clipped to a user's waist, and a headset/earpiece being used to interact with JOY.

JOY supports user defined commands and actions, variables, and text to speech.

JOY works entirely offline, no need for internet access to perform speech recognition. See https://alphacephei.com/vosk/models for a list of pre-trained speech recognition models for various languages. Download and extract one to `model` directory. Small models are faster and still quite accurate for native speakers, so that is what I use. Larger models are slower, but generally more accurate. Since we are using pre-trained models, JOY technically works with any of the listed languages on the previous link, but has not been tested for any language other than English.

JOY is implemented via open source libraries and language models, primarily using [vosk](https://alphacephei.com/vosk/) for speech recognition, [pygame](https://www.pygame.org/news) for playing audio, and [pyttsx3](https://pypi.org/project/pyttsx3/) for Text-To-Speech.

Since JOY is built on top of vosk, it allows for any language to be recognized, but currently command regex is using English. Hopefully it will be possible to make this work with any language that has a vosk model and works well with regex.

## Usage
```
usage: JOY.exe [-h] [-l] [-f FILENAME] [-m MODEL_PATH] [-d DEVICE] [-r SAMPLERATE] [-c CONFIG_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-devices    show list of audio devices and exit
  -f FILENAME, --filename FILENAME
                        audio file to store recording to
  -m MODEL_PATH, --model MODEL_PATH
                        Path to the model
  -d DEVICE, --device DEVICE
                        input device (numeric ID or substring)
  -r SAMPLERATE, --samplerate SAMPLERATE
                        sampling rate
  -c CONFIG_PATH, --config_path CONFIG_PATH
                        Path to YAML configuration file
```

## Configuration
Configuring JOY takes place via a single YAML file. By default, JOY attempts to read `./JOY.yml`, but you can specify the path via `./JOY.exe -c CONFIG_PATH`.

The config file consists of two main parts:
1. Pre-setting variables. [See Variables and Tags](#Variables-and-Tags)
2. Configuring commands. [See Commands](#Commands)

An example config file is packaged with every JOY release, and that file includes various example commands showcasing the power and flexibility of JOY. Generally, the config files looks like this:
```
# These variables get assigned their respective value at startup
StartingVariables:
  Name: joy
  UserName: User

# List of Commands, including name, regex, and subsequent actions to be executed
Commands:
  Open Youtube:
    Regex: "^({Name} )?open you( )?tube$"
    Actions:
      - Type: PlayAudio
        AudioFile: "{SpeechClipsDir}/Yes User.mp3"
        Volume: 30
      - Type: RunApplication
        Executable: "{BrowserExePath}"
        Arguments: [https://www.youtube.com/]

  ...
```

## Commands
The point of JOY is to recognize human speech, and execute various user defined commands.
These commands are defined via the YAML config file, and follow the same general format.

Commands always have three things:
1. A name, which can be used for later referencing
2. A regex, which defines how human speech gets mapped to the command
3. A list of Actions, which define what the command is supposed to do once spoken

Each action is specified via the "Type" field, and will have different functions and parameters based on "Type". See [Actions](#Actions) for a full list of available Actions and their uses.

## Variables and Tags
JOY allows the user to store information in variables via Actions and retrieve it for later use via tags. Any string you write in the configuration file, except for Action types, Command names, and Variable names, allows you retrieve variable values via tags, i.e. `{UserName}` or `{currentSong}`.

This allows you to store the path to a directory containing audio files, and then later access them directly via audio file name, i.e.: `{AudioFileDirectory}/Acknowledge.mp3` could become `C:/Users/foobar/Documents/Audio Clips/Acknowledge.mp3`. Such an example allows you to avoid writing long directory paths over and over again, they also allow you to quickly and dynamically change the directory you play sounds from!

Note, variable names are CASE SENSITIVE, so be careful when spelling them out!

Creating and updating variables is done in two ways:
1. Specifying starting variables via the "StartingVariables" field in the config file
2. Executing various Actions which allow for storing output to variables

Tags can be used for things other than just accessing variables, they also allow you to access various information, such as the exact phrase spoken by the user, or specific parts of the phrase that were spoken, such as if the user said "Close Spotify" or "Open Spotify", or even the current time!

| Tag | Description |
| :---: | :-----------: |
| `{variableName}` | Replaced with the value of `variableName` |
| `{CMD}` | Replaced with entire spoken phrase of the executed command |
| `{CMD:x}` | Replaced with the regex group `x` of the spoken phrase of the executed command |
| `{TIME:fmt}` | Replaced with the current time, formatted according to `fmt`. [See formatting rules](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) |
| `{ENV:variableName}` | Replaced with the value of the environment variable `variableName` |

## Actions
You can omit any of the listed options for any given Action, and the value will be replaced with a default value.

### **CancelTimers** Action
Cancel all currently set timers.

### **CloseApplication** Action
Close the specified application.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Application | The specific application name to close | `string` | Name of application to close |

### **GetUserSpeech** Action
Store the last spoken phrase by the user into the given variable name.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| WaitTime | The amount of time to wait before storing the last spoken phrase | `float` | `2.5` |
| OutputVariableName | The name of the variable to store the last spoken phrase into | `string` | `None` |

### **If** Action
If ANY of the specified condition sets are true, execute each Action in TrueActions. Else, execute each Action
in FalseActions.
See [Conditional Statements](#Conditional-Statements) for more info on using conditional expressions.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| ConditionSets | List of ConditionSets to evaluate | `List of ConditionSets` | `[]` |
| TrueActions | List of Actions to execute if ANY ConditionSets are true | `List of Actions` | `[]` |
| FalseActions | List of Actions to execute if ALL ConditionSets are false | `List of Actions` | `[]` |

### **SendKeys** Action
Emulate a combination of keyboard strokes to the active window.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Keys   | The combination of keys to send to the active window | `string` | `''` |

### **PlayAudio** Action
Plays the specified audio file at the given volume, optionally waiting until the file completes before continuing on to the next Action.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| AudioFile | The path to the specific audio file to play | `string` | `""` |
| Volume | Volume to play AudioFile at. Clamped between 0 and 100 | `float` | `100` |
| WaitForFinish | Wait until the audio file completes before completing action | `bool` | `False` |

### **RunApplication** Action
Run the specified application, using the given command line arguments. If specified to wait until the program stops running, then you can also store the stdout and stderr streams to specific variables.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Executable | Path to the executable you want to run | `string` | If not included, first value in `Arguments` is used instead |
| Arguments | The command line arguments to pass to the application | `List of strings` | `[]` |
| WorkingDirectory | Directory to run the executable from inside of | `string` | `"."` |
| WaitForFinish | Wait until the application finishes executing before continuing | `bool` | `False` |
| StdOutVariable | The variable name to store the stdout stream. Only stored if `WaitForFinish == True` | `string` | `""` |
| StdErrVariable | The variable name to store the stderr stream. Only stored if `WaitForFinish == True` | `string` | `""` |

### **SayText** Action
Plays the configured text through a TTS engine. Allows for completely customized and dynamic responses from JOY!

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Text | The text to use for Text-To-Speech | `string` | `""` |

### **SetSystemVolume** Action
Set the OS system volume to given value.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Volume | Value to set system volume to | `int` | `100` |

### **StopAllSounds** Action
Stop all currently playing audio files.

### **SetVariable** Action
Set a specific value to a given variable.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Value | The value to give `OutputVariable` | `string` | `""` |
| OutputVariable | The name of the variable to store `Value` | `string` | `""` |

### **TextRemovePrefix** Action
Remove the specified prefix from the given text, and store the result in the given variable name

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Text | Text to remove the Prefix from | `string` | `""` |
| Prefix | The suffix to remove from Text | `string` | `""` |
| OutputVariable | Variable name to store the output to | `string` | `""` |

### **TextRemoveSuffix** Action
Remove the specified suffix from the given text, and store the result in the given variable name

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Text | Text to remove the Suffix from | `string` | `""` |
| Suffix | The suffix to remove from Text | `string` | `""` |
| OutputVariable | Variable name to store the output to | `string` | `""` |

### **TextParseNumber** Action
Parse the given text for a number, and store the output to the given variable name

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Text | Text to parse for a number | `string` | `""` |
| OutputVariable | Variable name to store the output to | `string` | `""` |

Example:
"twenty five" -> "25"

### **Timer** Action
Create a timer in units of either seconds, minutes, or hours. Once timer fires off, play specified audio file at given volume.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Offset | How long to set timer to | `int` | `0` |
| Unit | Whether Offset is specified in second(s), minute(s), or hour(s) | `string` | `seconds` |
| AudioFile | Audio file to play once timer fires off | `string` | `""` |
| Volume | Volume to play the given audio file at | `int` | `100` |

### **While** Action
For as long as ANY of the specified condition sets evaluates to true, run each of the specified Actions.
See [Conditional Statements](#Conditional-Statements) for more info on using conditional expressions.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| ConditionSets | List of ConditionSets to evaluate | `List of ConditionSets` | `[]` |
| Actions | List of Actions to execute if ANY of the ConditionSets evaluates to true | `List of Actions` | `[]` |

## Conditional Statements
Certain Actions in JOY will alter their behavior depending on user defined conditional statements.

These conditional statements are composed of one or more `ConditionSet`s. A ConditionSet is composed of one or more `Condition`s. When JOY is evaluating a conditional statement, it iterates through and evaluates each `ConditionSet`. If **ANY** `ConditionSet` evaluates to true, the overall conditional statement also evaluates to true, and evaluation stops. Otherwise, if ALL the `ConditionSet`s evaluates to false, the overall conditional statement evaluates to false.

Note: If a conditional statement contains no `ConditionSet`s, then it automatically evaluates to false.

While this may seem complicated at first, this system of conditional statements allow you to write quite complicated logic in your commands, given your JOY assistant a lot of power and flexibility!

### **ConditionSet**
A `ConditionSet` consists entirely of a list of `Condition`s.

A `ConditionSet` evaluates to true if and only if **ALL** `Condition`s evaluate to true. If any of these `Condition`s evaluate to false, the overall `ConditionSet` evaluates to false, and evaluation stops.

Note: If a `ConditionSet` has no configured `Condition`s, then it automatically evaluates to true.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Conditions | List of Conditions to evaluate | `List of Conditions` | `[]` |

### **Condition**s
A `Condition` will always evaluate to either true or false, and how that evaluation is decided is based on the `Condition`'s Type.

Note: Every `Condition` will always have the implied options:
| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| Negate | Return the opposite of the evaluation | `bool` | `false` |

#### **Equals** Condition
Evaluates to true if `LeftOperand == RightOperand`.
If `Negate == true`, then evaluates to true if `LeftOperand != RightOperand`.

| Option | Description | Type | Default value |
| :----: | :---------: | :--: | :-----------: |
| LeftOperand | Left operand to compare | `string` | `""` |
| RightOperand | Right operand to compare | `string` | `""` |