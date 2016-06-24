#!/bin/env python3
"""midi to shortcut utility"""

import sys
from pykeyboard import PyKeyboard
import mido

def read_conf():
    """reads the config file and returns all substitutions and the device"""
    device = ''
    midi_to_shortcut = {}
    try:
        with open('config') as config:
            for line in config:
                if len(line) is 0 or line[0] == '#':
                    pass
                elif len(line) > 5 and line[0:7] == 'device:':
                    device = line[8:-1]
                else:
                    midi, shortcut = line.split(':')
                    midi = midi.split(' ')
                    shortcut = shortcut.split(' ')
                    for key in shortcut:
                        if key[-1:] == '\n':
                            shortcut.remove(key)
                            shortcut.append(key[:-1])

                    message = (int(midi[0]), int(midi[1]))
                    for sh in shortcut:
                        if len(sh) < 1:
                            shortcut.remove(sh)
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
        if (in_msg.note, in_msg.channel) in midi_to_shortcut:
            shortcut = midi_to_shortcut[(in_msg.note, in_msg.channel)]
            print('shortcut: ', shortcut)
            for sh in shortcut:
                keyboard.press_key(sh)
            for sh in shortcut:
                keyboard.release_key(sh)

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
