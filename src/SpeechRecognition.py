import Variables

import queue
import json
import sounddevice as sd
import sys
import vosk

data_queue = queue.Queue()
def data_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    data_queue.put(bytes(indata))

_sound_input_stream: sd.RawInputStream = None
def init_input_stream(device):
    global _sound_input_stream
    if _sound_input_stream == None:
        _sound_input_stream = sd.RawInputStream(samplerate=44100, blocksize = 8000, device=device, dtype='int16',
                            channels=1, callback=data_callback)
    _sound_input_stream.start()

def speech_recognition_loop(callback, model, samplerate) -> None:
    vosk.SetLogLevel(-1)
    model = vosk.Model(model)

    prompt = f"Hello {Variables.Variables['UserName']}, press Ctrl-C to exit"
    print("#" * len(prompt))
    print(prompt)
    print("#" * len(prompt))

    rec = vosk.KaldiRecognizer(model, samplerate)
    while True:
        data = data_queue.get()

        if rec.AcceptWaveform(data):
            speech = json.loads(rec.Result())["text"].strip()
            callback(speech)
            rec.Reset()