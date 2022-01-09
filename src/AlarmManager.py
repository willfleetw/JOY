import Audio

from datetime import datetime, timedelta
import threading
import time

class AlarmContext(object):
    _end_time: datetime
    _duration: timedelta
    _audio_file: str
    _volume: float
    _is_timer: bool

    def __init__(self, duration: timedelta, audio_file: str, volume: float, is_timer: bool) -> None:
        self._end_time = datetime.now() + duration
        self._duration = duration
        self._audio_file = audio_file
        self._volume = volume
        self._is_timer = is_timer

    def is_expired(self) -> bool:
        return datetime.now() >= self._end_time

    def _format_datetime(timestamp: datetime) -> str:
        val = ""
        times = f"{timestamp}".split(":")
        if times[0] != "0":
            val += f"{times[0]} hour"
            if times[0] == "1":
                val += " "
            else:
                val += "s "
        if times[1] != "00":
            time_val = times[1].removeprefix("0")
            val += f"{time_val} minute"
            if times[1] == "1":
                val += " "
            else:
                val += "s "
        if times[2] != "00":
            time_val = times[2].removeprefix("0")
            val += f"{round(float(time_val))} second"
            if times[2] == "1":
                val += " "
            else:
                val += "s "
        return val

    def __str__(self) -> str:
        return AlarmContext._format_datetime(self._end_time - datetime.now())

_alarms_lock = threading.Lock()
_alarms: list[AlarmContext] = []
def _monitor_alarms() -> None:
    loop_delay = 1.0
    while True:
        with _alarms_lock:
            for alarm in _alarms[:]:
                if alarm.is_expired():
                    _alarms.remove(alarm)
                    Audio.play_audio_file(alarm._audio_file, alarm._volume, wait_for_finish=False)
        time.sleep(loop_delay)
threading.Thread(target=_monitor_alarms, daemon=True).start()

def add_alarm(Duration: timedelta, AudioFile: str, Volume: float, is_timer: bool = False) -> None:
    with _alarms_lock:
        _alarms.append(AlarmContext(Duration, AudioFile, Volume, is_timer))

def num_alarms() -> int:
    with _alarms_lock:
        return len(_alarms)

def get_alarms_copy() -> list[AlarmContext]:
    with _alarms_lock:
        return _alarms.copy()

def get_alarms_strings() -> list[str]:
    alarm_strings = []
    with _alarms_lock:
        for alarm in _alarms:
            alarm_strings.append(str(alarm))
    return alarm_strings

def clear_all_alarms() -> None:
    with _alarms_lock:
        _alarms.clear()

def clear_all_timers() -> None:
    with _alarms_lock:
        for alarm in _alarms[:]:
            if alarm._is_timer:
                _alarms.remove(alarm)