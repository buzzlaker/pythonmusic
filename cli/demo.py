#!/usr/bin/env python
# vim:set et sw=4 ts=4 foldmethod=manual foldlevel=99:
# ===============================================================================#
# MIT License                                                                    #
#                                                                                #
# Copyright (c) [2019] [John Petrilli]                                           #
#                                                                                #
# Permission is hereby granted, free of charge, to any person obtaining a copy   #
# of this software and associated documentation files (the "Software"), to deal  #
# in the Software without restriction, including without limitation the rights   #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      #
# copies of the Software, and to permit persons to whom the Software is          #
# furnished to do so, subject to the following conditions:                       #
#                                                                                #
# The above copyright notice and this permission notice shall be included in all #
# copies or substantial portions of the Software.                                #
#                                                                                #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  #
# SOFTWARE.                                                                      #
#   __       __                       ___ __            __          __ __        #
#  |__.-----|  |--.-----.-----.--.--.'  _|__.----.-----|  |--.---.-|  |  |       #
#  |  |  _  |     |     |     |  |  |   _|  |   _|  -__|  _  |  _  |  |  |       #
#  |  |_____|__|__|__|__|__|__|___  |__| |__|__| |_____|_____|___._|__|__|       #
# |___| johnny@techsystems.io |_____|https://www.github.com/johnnyfireball       #
# ===============================================================================#
import sys
import os
import curses

from mpvcontrol import MPVControl


class PythonPlayer:
    def __init__(self):
        pass

mpv = None
gstdscr = None
width = None
height = None


def start_screen(stdscr):
    global gstdscr
    global width
    global height
    gstdscr = stdscr

    # Clear and refresh the screen for a blank canvas
    gstdscr.clear()
    gstdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    draw_screen()


def draw_center_content(key_pressed):
    global gstdscr
    global width
    global height

    title = "Curses example" [:width - 1]
    subtitle = "Written by Clay McLeod" [:width - 1]
    keystr = "Last key pressed: {}".format(key_pressed)[:width - 1]
    if key_pressed == 0:
        keystr = "No key press detected..." [:width - 1]

    # Centering calculations
    start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
    start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
    start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
    start_y = int((height // 2) - 2)
    # Rendering title
    gstdscr.addstr(start_y, start_x_title, title)

    # Turning off attributes for title
    gstdscr.attroff(curses.color_pair(2))
    gstdscr.attroff(curses.A_BOLD)

    # Print rest of text
    gstdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
    gstdscr.addstr(start_y + 3, (width // 2) - 2, "-" * 4)
    gstdscr.addstr(start_y + 5, start_x_keystr, keystr)


def draw_screen():
    global gstdscr
    global width
    global height
    global mpv

    mpv = MPVControl(False)
    # mpv.start_mpv()

    key_pressed = None
    mpv_launched = False
    # TODO clean up this menu its a disaster
    user_commands = {
        "Launch MPV": ["set_property", "pause", False],
        "Play/Pause": ["set_property", "pause", False],
        "Pause": ["set_property", "pause", True],
        "Play File": ["loadfile"],
        "Load List": ["loadlist"],
        "Next": ["playlist-next", "weak"],
        "Prev": ["playlist-prev", "weak"],
        "Quit": ["quit"],
    }
    while key_pressed != ord("q"):
        """
        n = 110
        p = 112
        s = 115
        l = 108
        o = 111
        y = 121
        r = 114
        """
        if key_pressed == 49 and not mpv_launched:
            mpv.start_mpv()
            pass

        # Initialization
        gstdscr.clear()
        height, width = gstdscr.getmaxyx()

        # Declaration of strings
        # msg = []
        statusbarstr = ""
        # for idx, i in enumerate(user_commands):
        #     statusbarstr += str(idx + 1) + ") " + i + " "
        # if not mpv_launched:
        #     statusbarstr = f"Options 1 launch MPV {statusbarstr}"

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        gstdscr.addstr(0, 0, whstr, curses.color_pair(1))
        for idx, i in enumerate(user_commands):
            line = str(idx + 1) + ") " + i + " "
            gstdscr.addstr(int(int(idx) + 1), 0, line)

        # Render status bar
        gstdscr.attron(curses.color_pair(3))
        gstdscr.addstr(height - 1, 0, statusbarstr)
        gstdscr.addstr(height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        gstdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        gstdscr.attron(curses.color_pair(2))
        gstdscr.attron(curses.A_BOLD)

        # Center window content
        draw_center_content(key_pressed)

        # Refresh the screen
        gstdscr.refresh()

        # Wait for next input
        key_pressed = gstdscr.getch()


def main():
    curses.wrapper(start_screen)


if __name__ == "__main__":
    main()
