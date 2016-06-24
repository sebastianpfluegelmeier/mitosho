#!/bin/env python3
"""midi to shortcut utility"""

from pykeyboard import PyKeyboard
import mido

def process_message(in_msg):
    """ processes message """
    keyboard = PyKeyboard()
    print(in_msg)
    try:
        """ this are the available key commands:
        a s d f h g z x c v b q w e r y t 1 2 3 4 6 5 = 9 7 - 8 0 ] o u [ i p l j \
                ' k ; \\ , / n m . ` \r \t \n return  tab  space  delete  escape
                command  shift  capslock  option  alternate  control rightshift
                rightoption  rightcontrol  function  """

        # presses command shift v on note 60 on channel 0
        if in_msg.note is 60 and in_msg.channel is 0 and in_msg.type is 'note_on':

            keyboard.press_key('command')
            keyboard.press_key('shift')
            keyboard.press_key('v')
            keyboard.release_key('command')
            keyboard.release_key('shift')
            keyboard.release_key('v')

        # presses tap on note 59, channel 0 
        if in_msg.note is 59 and in_msg.channel is 0 and in_msg.type is 'note_on':

            keyboard.tap_key('tab')

    except AttributeError:
        print('note not recognized')

def main():
    """main function"""
    print(mido.get_input_names())
    # input the name off your Midi device here.
    with mido.open_input('IAC-Treiber IAC Bus 1') as input:
        for message in input:
            process_message(message)


if __name__ == '__main__':
    main()
