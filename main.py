import serial

from client.httprequests import change_state
from client.urls import LIGHT_ID_1, LIGHT_ID_2, LIGHT_ID_3, LIGHT_ID_4, LIGHT_ID_5, LIGHT_ID_6

ser = serial.Serial('COM5', 9600)

lights = [LIGHT_ID_1, LIGHT_ID_2, LIGHT_ID_3, LIGHT_ID_4, LIGHT_ID_5, LIGHT_ID_6]
NR_OF_LIGHTS = len(lights)
states = [True, True, True, True, True, True]
ALL_LIGHTS_OFF = False


def reset(light_id):  # PINK WITH 0 SAT => WHITE
    change_state(light_id, "on", True)
    change_state(light_id, "hue", 60000)
    change_state(light_id, "sat", 0)
    change_state(light_id, "bri", 120)
    change_state(light_id, "alert", "none")


def reset_all():
    for light_id in lights:
        reset(light_id)


def turn_off(light_id):
    change_state(light_id, "on", False)


def turn_off_all():
    for light_id in lights:
        turn_off(light_id)


def alarm(on, caller):
    if on:
        for light in lights:
            if light != lights[caller]:
                change_state(light, "alert", "lselect")
    else:
        for light in lights:
            change_state(light, "alert", "none")


def alarm_color(caller):
    for light in lights:
        if light != lights[caller]:
            change_state(light, "hue", 0)
            change_state(light, "sat", 254)


def default_color(selected):
    print(f"selected {selected}: updating colors")
    for i in range(0, NR_OF_LIGHTS):
        light = lights[i]
        if ALL_LIGHTS_OFF:
            change_state(light, "on", False)
        elif states[i]:
            if light != lights[selected]:  # TURNED ON & UNSELECTED
                change_state(light, "sat", 0)
            else:  # TURNED ON & SELECTED
                change_state(light, "sat", 254)
            change_state(light, "hue", 60000)
            change_state(light, "on", True)
        else:
            if light != lights[selected]:  # TURNED OFF & UNSELECTED
                change_state(light, "on", False)
            else:  # TURNED OFF & SELECTED
                change_state(light, "hue", 0)
                change_state(light, "sat", 254)
                change_state(light, "on", True)


def check_if_all_lights_off():
    global ALL_LIGHTS_OFF
    for i in range(0, NR_OF_LIGHTS):
        if states[i]:
            ALL_LIGHTS_OFF = False
            return
    ALL_LIGHTS_OFF = True
    print("all lights have been turned off")


def toggle(selected):
    global ALL_LIGHTS_OFF
    if states[selected]:
        states[selected] = False
        check_if_all_lights_off()
        print(f"turned {selected} off")
    else:
        states[selected] = True
        ALL_LIGHTS_OFF = False
        print(f"turned {selected} on")


# MAIN

reset_all()
previous_x = 0
default_color(0)
try:
    while True:
        if ser.in_waiting > 0:
            try:
                arduino_data = int(ser.readline().decode('utf-8', errors='ignore').rstrip())

                c = arduino_data
                if c >= 1000000:  # ALARM

                    x = (c - 1000000) % NR_OF_LIGHTS
                    if previous_x < 1000000:  # UPDATE COLORS
                        alarm_color(x)
                        alarm(True, x)  # TURN ON ALARM
                        print("turn on alarms")
                    previous_x = c

                elif c <= -1000000:  # TOGGLED ON/OFF

                    x = ((c * -1) - 1000000) % NR_OF_LIGHTS
                    toggle(x)  # TOGGLE LIGHT
                    previous_x = c

                else:  # SELECTED

                    x = c % NR_OF_LIGHTS
                    if previous_x >= 1000000:  # TURN OFF ALARM
                        alarm(False, x)
                        default_color(x)
                        print("turn off alarms")
                    elif previous_x != x:  # SELECTED DIFFERENT LIGHT
                        default_color(x)  # UPDATE COLORS
                    previous_x = x

            except ValueError:
                continue


except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
