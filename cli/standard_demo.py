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
import os
import sys
import subprocess
import json
import argparse
import logging
from subprocess import Popen, PIPE



def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    if args.spotify:
        # TODO port bash script to python.
        print("Including spotify & dbus settings later")
        sys.exit(2)
        return 1

    def sub_loop(chosen=None):
        clear_screen()
        print("Make sure you have started mpv like this:")
        print("mpv --idle --log-file=~/tmp/mpv_log.txt --input-ipc-server=/tmp/mpvsocket")
        print("\n")
        media_title = run_mpv_command(['get_property', 'media-title'])
        print(json.loads(media_title[0].decode("utf-8")))

        choice = None
        if chosen == 'q':
            sys.exit(0)
        elif chosen == '2':
            pass
        elif chosen == '4':
            pass
        elif chosen == '5':
            playlist = input("Enter path to playlist: ").strip()
            # TODO error checking....
            if playlist:
                ret = run_mpv_command(['loadlist', playlist])
                # TODO do something on success/fail
        elif chosen == 'n':
            ret = run_mpv_command(["playlist-next", "weak"])
            # TODO do something on success/fail
        elif chosen == 'p':
            ret = run_mpv_command(["playlist-prev", "weak"])
            # TODO do something on success/fail
        elif chosen == 's':
            ret = run_mpv_command(["playlist-shuffle"])
            # TODO do something on success/fail
        else:
            choice = input("h Help or enter command: ").strip()
            if choice == 'h':
                print(" ".join(get_menu()))
                choice = input("User Choice: ").strip()
        sub_loop(choice)
    sub_loop()

"""
"""

def clear_screen():
    # TODO add multi OS support
    return subprocess.call('clear', shell=True)


def get_menu():
    return [
        "2)Play/Pause",
        "4)Play File",
        "5)Load List",
        "n)Next",
        "p)Prev",
        "s)Shuffle Playlist",
        "q)Quit",
    ]


def run_mpv_command(command):
    msg = {"command": command}
    p1 = Popen(["echo", json.dumps(msg)], stdout=PIPE)
    p2 = Popen(["socat", "-", "/tmp/mpvsocket"],
               stdin=p1.stdout,
               stdout=PIPE)

    return p2.communicate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python - MPV Player",
        epilog="Control MPV player with python + do more. Removing cli controls",
        fromfile_prefix_chars="@",
    )
    parser.add_argument(
        "-s",
        "--spotify",
        action="store_true",
        dest="spotify",
        help="Use spotify instead of mpv.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity.",
        action="store_true")
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
