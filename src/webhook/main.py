from flask import Flask, request
import requests
import json
app = Flask(__name__)

url = 'http://traffic-light/api/lamps/set'

status_colours = {
    'running': {'off': ['red', 'green'], 'on': ['amber']},
    'pending': {'off': [], 'on': ['amber']},
    'success': {'off': ['red', 'amber'], 'on': ['green']},
    'failed': {'off': ['amber', 'green'], 'on': ['red']}
}


def _setColours(colours):
    for colour in colours['off']:
        params = {'lamp': colour, 'state': 'off'}
        requests.get(url, params=params)
    for colour in colours['on']:
        params = {'lamp': colour, 'state': 'on'}
        requests.get(url, params=params)


def _requestFilter(reqData):
    if reqData['object_kind'] != 'pipeline':
        return False
    if reqData['project']['name'] != 'exmouth-stats':
        return False
    if reqData['object_attributes']['ref'] != 'master':
        return False
    return True


@app.route("/", methods=['POST', 'GET'])
def hello():
    reqData = json.loads(request.data)
    if not _requestFilter(reqData):
        return 'Filtered'
    status = reqData['object_attributes']['status']
    if status not in status_colours:
        print(f'WARNING: ignored status {status}.')
    else:
        print(f'Status={status}, colours={status_colours[status]}.')
        _setColours(status_colours[status])
    return 'OK'
