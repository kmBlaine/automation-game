#!/usr/bin/python
#
# BSD 3-Clause License
#
# Copyright (c) 2018, Blaine Murphy
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import pandas
import math

def main(args):
    cadcsv = pandas.read_csv(args[0])

    straights = cadcsv[cadcsv["type"] == "s"]
    curves = cadcsv[cadcsv["type"] != "s"]

    curve_height_diffs = curves["endaltitude"] - curves["startaltitude"]
    curve_lengths = curves["length"] / 180.0 * math.pi * curves["radius"]
    curves["slope"] = curve_height_diffs / curve_lengths * 100.0

    straight_height_diffs = straights["endaltitude"] - straights["startaltitude"]
    straights["slope"] = straight_height_diffs / straights["length"] * 100.0

    track_csv = pandas.concat([straights, curves])
    track_csv = track_csv.sort_values(by="index")

    layout_str = "Layout = {"
    layoutinf_str = "LayoutInfo = {"
    radius_str = "CornerRadius = {"
    slope_str = "Slope = {"
    sport_str = "Sportiness = {"
    camber_str = "Camber = {"

    for (direction, length, radius, slope, sport, camber) in zip(track_csv["type"],
                                                                 track_csv["length"],
                                                                 track_csv["radius"],
                                                                 track_csv["slope"],
                                                                 track_csv["sport"],
                                                                 track_csv["camber"]):
        layout_str += direction + ","
        layoutinf_str += str(length) + ","
        radius_str += str(radius) + ","
        slope_str += str(slope) + ","
        sport_str += str(int(sport)) + ","
        camber_str += str(camber) + ","

    layout_str = layout_str.rstrip(",") + "}"
    layoutinf_str = layoutinf_str.rstrip(",") + "}"
    radius_str = radius_str.rstrip(",") + "}"
    slope_str = slope_str.rstrip(",") + "}"
    sport_str = sport_str.rstrip(",") + "}"
    camber_str = camber_str.rstrip(",") + "}"

    track_file = open("track.lua.new", "w")
    track_file.write("local s = 0\r\n"
                     "local l = 1\r\n"
                     "local r = -1\r\n"
                     "\r\n"
                     "Track =\r\n"
                     "{\r\n"
                     "    Name = \"New Test Track\",\r\n"
                     "\r\n"
                     "    --Track Image Info\r\n"
                     "    --Track Image must be 1280 x 720\r\n"
                     "    --Start Position on the Image x,y from Top Left\r\n"
                     "    Start = { 640, 360 },\r\n"
                     "\r\n"
                     "    --How many pixels per meter ( Pixels / Length )\r\n"
                     "    --Measure a long straight and then manipulate from there\r\n"
                     "    Scale = 0.1,\r\n"
                     "\r\n")
    track_file.write("    " + layout_str + ",\r\n")
    track_file.write("    " + layoutinf_str + ",\r\n")
    track_file.write("    " + radius_str + ",\r\n")
    track_file.write("    " + slope_str + ",\r\n")
    track_file.write("    " + sport_str + ",\r\n")
    track_file.write("    " + camber_str + ",\r\n")
    track_file.write("    Split1 = 500,\r\n"
                     "    Split2 = 1000,\r\n"
                     "}\r\n")

    track_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
