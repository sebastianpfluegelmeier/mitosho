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
                if len(line) < 1 or line[0] == '#':
                    pass
                elif len(line) > 5 and line[0:7] == 'device:':
                    device = line[9:]
                else:
                    midi, shortcut = line.split(':')
                    midi = line.split(' ')
                    shortcut = line.split(' ')
                    message = mido.Message('note_on', note=midi[0], channel=midi[1])
                    midi_to_shortcut[message] = shortcut

        if device is "":
            print("no device specified")
            sys.exit()

        return (device, midi_to_shortcut)
    except TypeError:
        print('Error reading config')

def process_message(in_msg, midi_to_shortcut):
    """ processes message """
    keyboard = PyKeyboard()
    print(in_msg)
    try:
        if mido.Note(in_msg.type, note=in_msg.note, channel=in_msg.channel) in midi_to_shortcut:
            shortcut = midi_to_shortcut(mido.Note.type, note=in_msg.note, channel=in_msg.channel)
            keyboard.press_key(shortcut)
            keyboard.release_key(shortcut)

    except AttributeError:
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
