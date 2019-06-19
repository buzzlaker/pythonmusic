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
import json

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

    gstdscr.addstr(height - 3, 0, "Lyrics will go here")


def ask_user(msg):
    curses.echo()
    nstdscr = curses.initscr()
    nstdscr.clear()
    choice = my_raw_input(nstdscr, 2, 3, msg).decode("utf-8")
    gstdscr.clear()
    return choice.strip()


def get_paused():
    paused = mpv.execute_cmd(['get_property', 'pause'])
    # TODO I cant get json to read this. I did simple paused[0].decode('utf-8')
    # json.loads wont work. Silly because this should work, something going on.
    # this paused needs to be corrected. hacked together for now
    # statusbar += f"{paused[0]}"
    paused = str(paused[0].strip()).strip("'<>() ").replace('\'', '\"').replace('b"', '')
    if paused == '{"data":false,"error":"success"}':
        return False
    else:
        return True
        mpv.execute_cmd(["set_property", "pause", False])


def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo()
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    inp = stdscr.getstr(r + 1, c, 200)
    return inp


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
        "1) Launch MPV": ["set_property", "pause", False],
    }
    playing = ""
    # Initialization
    while key_pressed != ord("q"):
        stdscr = curses.initscr()
        gstdscr.clear()
        height, width = gstdscr.getmaxyx()
        gstdscr.clear()
        if key_pressed == ord("1") and not mpv_launched:
            # TODO fix what a bad way, not even using this as a dict.
            user_commands = {
                "2) Play/Pause": ["set_property", "pause", False],
                "3) Pause": ["set_property", "pause", True],
                "4) Play File": ["loadfile"],
                "5) Load List": ["loadlist"],
                "n) Next": ["playlist-next", "weak"],
                "p) Prev": ["playlist-prev", "weak"],
                "s) Shuffle Playlist": ["quit"],
                "c) Launch Cava": ["quit"],
                "q) Quit": ["quit"],
            }
            mpv.start_mpv()
            mpv_launched = True

        statusbar = " "
        media_title = None
        if mpv_launched:
            statusbar = "MPV Started"
            paused = mpv.execute_cmd(['get_property', 'pause'])
            # TODO I cant get json to read this. I did simple paused[0].decode('utf-8')
            # json.loads wont work. Silly because this should work, something going on.
            # this paused needs to be corrected. hacked together for now
            if key_pressed == ord("1"):
                pass
            if key_pressed in [ord("3"), ord("2")]:
                if get_paused():
                    mpv.execute_cmd(["set_property", "pause", False])
                else:
                    mpv.execute_cmd(["set_property", "pause", True])

            paused = get_paused()
            if paused:
                statusbar += " - Paused"
            else:
                statusbar += " - Playing"

            if key_pressed == ord("4"):
                # TODO error checking
                choice = ask_user("Enter File or Youtube URL")
                if choice:
                    mpv.execute_cmd(['loadfile', choice, 'append-play'])

            if key_pressed == ord("5"):
                # TODO error checking
                choice = ask_user("Enter File")
                if choice:
                    mpv.execute_cmd(['loadlist', choice])

            if key_pressed == ord("n"):
                # TODO show response
                mpv.execute_cmd(["playlist-next", "weak"])
            if key_pressed == ord("p"):
                # TODO show response
                mpv.execute_cmd(["playlist-prev", "weak"])
            if key_pressed == ord("s"):
                # TODO show response
                mpv.execute_cmd(["playlist-shuffle"])

            # TODO hacked up example
            # TODO Handle media_title properly.
            media_title = mpv.execute_cmd(['get_property', 'media-title'])
            media_title = str(media_title[0].decode("utf-8")).strip("'<>() ").replace('\'', '\"').replace('b"', '').replace('","error":"success"}', '')
            # media_title = str(media_title[0].strip())
            media_title = media_title.replace('{"data":"', '')

            # TODO Handle statusbar properly.
            gstdscr.addstr(height - 1, 0, statusbar)
            try:
                gstdscr.addstr(height - 2, 0, media_title)
            except:
                pass


        # Rendering some text
        # whstr = "Width: {}, Height: {}".format(width, height)
        # gstdscr.addstr(0, 0, whstr, curses.color_pair(1))
        for idx, i in enumerate(user_commands):
            gstdscr.addstr(idx, 0, i)

        # Turning on attributes for title

        # Center window content
        # TODO fix same json.loads issue

        draw_center_content(key_pressed)

        # Refresh the screen
        gstdscr.refresh()

        # Wait for next input
        key_pressed = gstdscr.getch()
    mpv.execute_cmd(['quit'])


def main():
    curses.wrapper(start_screen)


if __name__ == "__main__":
    main()
