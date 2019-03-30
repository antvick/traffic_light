import RPi.GPIO as GPIO
from flask import Blueprint, request, jsonify, make_response
from typing import Dict
from collections import namedtuple
light_blueprint = Blueprint('light', __name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lamp = namedtuple('lamp', 'gpio colour')
green = lamp(gpio=4, colour='green')
amber = lamp(gpio=3, colour='amber')
red = lamp(gpio=2, colour='red')
spare = lamp(gpio=17, colour=None)
lamps = [green, amber, red]
GPIO.setup(spare.gpio, GPIO.OUT)
GPIO.output(spare.gpio, GPIO.LOW)
for lamp in lamps:
    GPIO.setup(lamp.gpio, GPIO.OUT)


def lamp_status() -> str:
    return {lamp.colour:not(GPIO.input(lamp.gpio)) for lamp in lamps}


@light_blueprint.route("/lamps/status")
def status() -> None:
    return make_response(jsonify({'status':'OK', 'lamp_state': lamp_status()}), 200)


@light_blueprint.route("/lamps/set")
def set_state() -> str:
    if not request.args.get('lamp'):
        return make_response(jsonify('Failed, no lamp requested'), 400)
    if not request.args.get('state'):
        return make_response(jsonify('Failed, no state requested'), 400)
    requested_lamp = request.args.get('lamp')
    requested_state = request.args.get('state')
    if requested_state == 'on':
        actuate = GPIO.HIGH
    elif requested_state == 'off':
        actuate = GPIO.LOW
    else:
        return make_response(jsonify('Failed, no matching state'), 400)
    if requested_lamp == 'green':
        GPIO.output(green.gpio, actuate)
    elif requested_lamp == 'amber':
        GPIO.output(amber.gpio, actuate)
    elif requested_lamp == 'red':
        GPIO.output(red.gpio, actuate)
    elif requested_lamp == 'all':
        for lamp in lamps:
            GPIO.output(lamp.gpio, actuate)
    else:
       return make_response(jsonify('Failed, no matching lamp'), 400)
    return make_response(jsonify({'status':'OK', 'lamp_state': lamp_status()}), 200)

