#!/bin/env python3
"""midi to shortcut utility. takes midi notes from one device and generates virtual keyboard events.
there should be a config file containing information about the midi notes and the corresponding
shortcuts"""

import sys
from pykeyboard import PyKeyboard
import mido

def read_conf():
    """reads the config file and returns all midi notes an corresponding shortcuts and the device"""
    # the name of the device inside the config file
    device = ''
    # dict with key: midi note, value: list containing strings with key identifiers
    midi_to_shortcut = {}
    try:
        with open('config') as config:
            for line in config:
                if len(line.strip()) == 0 or line[0] == '#' or line[0] == '/n':
                    pass
                elif len(line) > 6 and line[0:7] == 'device:':
                    device = line[8:-1]
                else:

                    print('else: ', line)
                    if line is 'n':
                        print('empty: ', line)
                    midi, shortcut = line.split(':')
                    midi = midi.split(' ')
                    shortcut = shortcut.split(' ')
                    for key in shortcut:
                        if key[-1:] == '\n':
                            shortcut.remove(key)
                            shortcut.append(key[:-1])

                    message = (int(midi[0]), int(midi[1]))
                    for key in shortcut:
                        if len(key) < 1:
                            shortcut.remove(key)
                    midi_to_shortcut[message] = shortcut

        if device is "":
            print("no device specified")
            sys.exit()

        return (device, midi_to_shortcut)
    except OSError:
        print('Error reading config')

def process_message(in_msg, midi_to_shortcut):
    """ processes message """
    keyboard = PyKeyboard()
    print(in_msg)
    try:
        if (in_msg.note, in_msg.channel) in midi_to_shortcut and in_msg.type != 'note_off':
            shortcut = midi_to_shortcut[(in_msg.note, in_msg.channel)]
            print('shortcut: ', shortcut)
            for key in shortcut:
                keyboard.press_key(key)
            for key in shortcut:
                keyboard.release_key(key)

    except OSError:
        print('note not recognized')

def main():
    """reads the config file first, then opens the midi input and waits for commands"""
    device, midi_to_shortcut = read_conf()

    print(mido.get_input_names())
    # input the name off your Midi device here.
    with mido.open_input(device) as inp:
        for message in inp:
            process_message(message, midi_to_shortcut)


if __name__ == '__main__':
    main()
