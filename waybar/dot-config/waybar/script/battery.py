#! /usr/bin/python
import json
import psutil
import time
import sys


def write(text, tooltip, state):
    output = {
        "text": text,
        "tooltip": tooltip,
        "class": "custom-battery-" + state,
        "alt": ""
    }

    sys.stdout.write(json.dumps(output) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    battery = psutil.sensors_battery()
    while True:
        if battery is None:
            write("", "none")
            continue
        precent = (battery.percent//20) * 20
        if precent == 0:
            state = "empty"
        elif precent == 100:
            state = "full"
        else:
            state = str(precent)
        if battery.power_plugged:
            state += "-charging"
        left = battery.secsleft // 60
        if not left >= 0:
            left = "?"
        write(
            " "*3, 
            str(battery.percent) + "%" 
                + " / " + str(left) 
                + " mins left", 
            state
        )
        time.sleep(60)