#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2020 Bitcraze AB
#
#  AI-deck demo
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  this program; if not, write to the Free Software Foundation, Inc., 51
#  Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#  Demo for showing streamed JPEG images from the AI-deck example.
#
#  By default this demo connects to the IP of the AI-deck example when in
#  Access point mode.
#
#  The demo works by opening a socket to the AI-deck, downloads a stream of
#  JPEG images and looks for start/end-of-frame for the streamed JPEG images.
#  Once an image has been fully downloaded it's rendered in the UI.
#
#  Note that the demo firmware is continously streaming JPEG files so a single
#  JPEG image is taken from the stream using the JPEG start-of-frame (0xFF 0xD8)
#  and the end-of-frame (0xFF 0xD9).

import argparse
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import threading
import time, datetime
import socket,os,struct
from PIL import Image

deck_ip = None
deck_port = None

class ImgThread(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self, daemon=True)
        self._callback = callback

    def run(self):
        print("Connecting to socket on {}:{}...".format(deck_ip, deck_port))
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((deck_ip, deck_port))
        print("Socket connected")

        imgdata = None

        while(1):
            strng = client_socket.recv(512)

            # Look for start-of-frame and end-of-frame
            start_idx = strng.find(b"\xff\xd8")
            end_idx = strng.find(b"\xff\xd9")

            # Concatenate image data, once finished send it to the UI
            if start_idx >= 0:
                imgdata = strng[start_idx:len(strng)] # Does not support start and end in same package
            elif end_idx >= 0 and imgdata:
                imgdata += strng[0:end_idx]
                try:
                    self._callback(imgdata)
                except gi.repository.GLib.Error:
                    pass
                imgdata = strng[end_idx:len(strng)]
            elif imgdata:
                imgdata += strng

# UI for showing frames from AI-deck example
class FrameViewer(Gtk.Window):

    def __init__(self):
        super(FrameViewer, self).__init__()
        self.frame = None
        self.init_ui()
        self._start = None
        self.set_default_size(374, 294)

        self.img_frame_count = 0

    def init_ui(self):            
        self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0, 0, 0, 1))
        self.set_border_width(20)
        self.set_title("Connecting...")
        self.frame = Gtk.Image()
        f = Gtk.Fixed()
        f.put(self.frame, 10, 10)
        self.add(f)
        self.connect("destroy", Gtk.main_quit)
        self._thread = ImgThread(self._showframe)
        self._thread.start()

    def _update_image(self, pix):
        self.frame.set_from_pixbuf(pix)

    def _showframe(self, imgdata):
        # Add FPS/img size to window title
        if (self._start != None):
            fps = 1 / (time.time() - self._start)
            GLib.idle_add(self.set_title, "{:.1f} fps / {:.1f} kb".format(fps, len(imgdata)/1000))
        self._start = time.time()
        img_loader = GdkPixbuf.PixbufLoader.new()

        # Try to decode JPEG from the data sent from the stream
        try:
            img_loader.write(imgdata)
            pix = img_loader.get_pixbuf()
            
            if pix is not None:
                data = pix.get_pixels()
                w = pix.props.width
                h = pix.props.height
                stride =  pix.props.rowstride
                mode = "L"
                im = Image.frombytes(mode, (w, h), data)
        
                dt_date = datetime.datetime.now()
                time_stamp = dt_date.strftime("%d%m%Y%H%M%S%f")

                #print("In specified format:", time_stamp)
                file_to_stream = "stream_" + str(self.img_frame_count) + "_" + time_stamp + ".jpeg"
                im.save(file_to_stream)

            GLib.idle_add(self._update_image, pix)

        except gi.repository.GLib.Error:
            print("Could not set image!")
        img_loader.close()

# Args for setting IP/port of AI-deck. Default settings are for when
# AI-deck is in AP mode.
parser = argparse.ArgumentParser(description='Connect to AI-deck JPEG streamer example')
parser.add_argument("-n",  default="192.168.4.1", metavar="ip", help="AI-deck IP")
parser.add_argument("-p", type=int, default='5000', metavar="port", help="AI-deck port")
args = parser.parse_args()

deck_port = args.p
deck_ip = args.n

fw = FrameViewer()
fw.show_all()
Gtk.main()


