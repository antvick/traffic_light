from flask import Blueprint, request
from typing import Dict
light_blueprint = Blueprint('light', __name__)

gpiolightmap = {
    "green": "1",
    "yellow": "3", 
    "red": "5"
}

@light_blueprint.route("/flash")
def flash() -> None:
    colour = request.args.get('colour')
    return gpiolightmap[colour]

