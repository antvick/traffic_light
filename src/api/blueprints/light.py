import RPi.GPIO as GPIO
from flask import Blueprint, request, jsonify
from typing import Dict
from collections import namedtuple
light_blueprint = Blueprint('light', __name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lamp = namedtuple('lamp', 'gpio colour')
green = lamp(gpio=2, colour='green')
amber = lamp(gpio=3, colour='amber')
red = lamp(gpio=4, colour='red')
lamps = [green, amber, red]

@light_blueprint.route("/status")
def status() -> None:
    return jsonify({lamp.colour:GPIO.input(lamp.gpio) for lamp in lamps})

