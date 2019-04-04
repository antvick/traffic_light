import time
import requests

url = 'http://traffic-light/api/lamps/set'
delay = 0.5
sequence = ['r', 'ra', 'g', 'g', 'a', 'r']
lamp_names = {'r': 'red', 'a': 'amber', 'g': 'green'}

def switch_off(colour):
    params = {'lamp': lamp_names[colour], 'state': 'off'}
    requests.get(url, params=params)

def switch_on(colour):
    params = {'lamp': lamp_names[colour], 'state': 'on'}
    requests.get(url, params=params)

def main():
    shifted_sequence = [sequence[-1]] + sequence[:-1]
    while True:
        for state, prev_state in zip(sequence, shifted_sequence):
            off_colours = [c for c in prev_state if c not in state]
            on_colours = [c for c in state if c not in prev_state]
            list(map(switch_off, off_colours))
            list(map(switch_on, on_colours))
            time.sleep(delay)

if __name__ == '__main__':
    main()
