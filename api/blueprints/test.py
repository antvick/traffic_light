from flask import Blueprint
test_blueprint = Blueprint('test', __name__)
@test_blueprint.route("/status")
def status():
    return "OK"

