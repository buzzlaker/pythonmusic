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
import threading
from subprocess import Popen, PIPE
import json


class MPVRunner:
    mpv = None

    def __init__(self):
        pass

    def start_mpv_thread(self):
        self.mpv = threading.Thread(
            target=self.start_mpv_player, args=(), name="mpv")
        self.mpv.start()

    def start_mpv_player(self):
        default = [
            "mpv",
            "--idle",
            "--no-input-default-bindings",
            "--no-terminal",
            "--input-ipc-server",
            "/tmp/mpvsocket",
        ]
        ret = Popen(default, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        return ret.communicate(b"ret")

    def run_command(self, command):
        """
        dmesg | grep hda
        would be:

        p1 = Popen(["dmesg"], stdout=PIPE)
        p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
        output = p2.communicate()[0]

         | socat - /tmp/mpvsocket
        """
        p1 = Popen(["echo", json.dumps(command)], stdout=PIPE)
        p2 = Popen(["socat", "-", "/tmp/mpvsocket"],
                   stdin=p1.stdout,
                   stdout=PIPE)
        return json.loads(p2.communicate()[0])

    def build_message(self, command):
        if type(command) != list:
            return False
        msg = {"command": command}
        return msg

    def x_bm(self, x, c):
        a = self.build_message(c)
        return self.run_command(a)
