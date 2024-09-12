# uncompyle6 version 3.9.2

# Python bytecode version base 3.8.0 (3413)

# Decompiled from: Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:37:02) [MSC v.1924 64 bit (AMD64)]

# Embedded file name: 1.py

import time, os, re, base64, datetime, requests, threading

from queue import Queue

from datetime import datetime



def txt_to_m3u(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:

        lines = f.readlines()

    with open(output_file, "w", encoding="utf-8") as f:

        f.write('#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml" catchup="append" catchup-source="?playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"\n')

        genre = ""

        for line in lines:

            line = line.strip()

            if "," in line:

                channel_name, channel_url = line.split(",", 1)

                if channel_url == "#genre#":

                    genre = channel_name

                    print(genre)

                else:

                    f.write(f'#EXTINF:-1 tvg-logo="https://raw.githubusercontent.com/linitfor/epg/main/logo/{channel_name}.png" group-title="{genre}",{channel_name}\n')

                    f.write(f"{channel_url}\n")





txt_to_m3u("ceshi.txt", "ceshi.m3u")
