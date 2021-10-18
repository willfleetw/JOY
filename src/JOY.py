#!/usr/bin/env python3

import Command
import JOYConfig
from SpeechRecognition import init_input_stream, speech_recognition_loop

import argparse
import os
import sounddevice as sd
import sys

class JOY(object):

    def parse_args() -> argparse.Namespace:
        def int_or_str(arg):
            """Helper function for argument parsing."""
            try:
                return int(arg)
            except ValueError:
                return arg

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            '-l', '--list-devices', action='store_true',
            help='show list of audio devices and exit')
        args, remaining = parser.parse_known_args()
        if args.list_devices:
            print(sd.query_devices())
            parser.exit(0)
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[parser])
        parser.add_argument(
            '-f', '--filename', type=str, metavar='FILENAME',
            help='audio file to store recording to')
        parser.add_argument(
            '-m', '--model', type=str, metavar='MODEL_PATH',
            help='Path to the model', default="model")
        parser.add_argument(
            '-d', '--device', type=int_or_str,
            help='input device (numeric ID or substring)')
        parser.add_argument(
            '-r', '--samplerate', type=int, help='sampling rate')
        parser.add_argument(
            '-c', '--config_path', type=str, help='Path to YAML configuration file', default="JOY.yml")
        args = parser.parse_args(remaining)

        try:
            if not os.path.exists(args.model):
                print ("Please download a model for your language from https://alphacephei.com/vosk/models")
                print ("and unpack as 'model' in the current folder.")
                parser.exit(0)
            if args.samplerate is None:
                device_info = sd.query_devices(args.device, 'input')
                # soundfile expects an int, sounddevice provides a float:
                args.samplerate = int(device_info['default_samplerate'])
        except Exception as e:
            parser.exit(type(e).__name__ + ': ' + str(e))

        return args

    def handle_speech(speech) -> None:
        if speech == "":
            return

        Command.LastHeardSpeech = speech

        print(f"Heard: {speech}")
        for command in Command.Commands.values():
            if command.matches(speech):
                command.execute(speech)

    def main() -> None:
        args = JOY.parse_args()

        try:
            JOYConfig.load_config(args.config_path)

            init_input_stream(args.device)

            speech_recognition_loop(
                callback=JOY.handle_speech,
                model=args.model,
                samplerate=args.samplerate)

        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    JOY.main()