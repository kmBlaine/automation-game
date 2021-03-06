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


import utm
import sys

"""
Returns the UTM coordinates described a lat long string in format:
    "longitude,latitude,altitude"

As a tuple in format:
    (easting, northing, altitude, zone #, zone letter)
"""
def lonlat_to_utm(coords_str):
    coords_strs = coords_str.split(",")

    lon = float(coords_strs[0])
    lat = float(coords_strs[1])
    alt = float(coords_strs[2])

    utm_coords = utm.from_latlon(lat, lon)
    utm_coords_full = (utm_coords[0], utm_coords[1], alt, utm_coords[2], utm_coords[3])

    return utm_coords_full

"""
Gets the UTM coordinate described by a single-point placemark in Google Earth.
Input line should be the coordinates line with format:
    "<coordinates>-122.6797019415874,47.30797394101634,69</coordinates>"

i.e. longitude, latitude, altitude

Returns a tuple in format:
    (easting, northing, altitude)
"""
def get_ctl_point(line):
    # <coordinates>-122.6797019415874,47.30797394101634,69</coordinates>

    coords_str = line.lstrip("<coordinates>").rstrip("</coordinates>")
    utm_coords = lonlat_to_utm(coords_str)

    return (utm_coords[0],
            utm_coords[1],
            utm_coords[2])

"""
Gets the list of UTM coordinates describing a LineString placemark in Google
Earth. Input line should be the series of coordinates with format:
    -122.6797019415874,47.30797394101634,69 ...

i.e. longitude,latitude,altitude [longitude,latitude,altitude] ...

Returns a list of tuples in format:
    {
        (easting northing altitude),
        [(easting northing altitude)],
        ...
    }
"""
def get_ref_points(line):
    # -122.6797019415874,47.30797394101634,69

    coords_strs = line.split(" ")
    coords_all = []

    for coords_str in coords_strs:
        coords = lonlat_to_utm(coords_str)
        coords_all.append((coords[0],
                           coords[1],
                           coords[2]))

    return coords_all

"""
Writes an ASCII point cloud file in format:
    easting northing altitude
    [easting northing altitude]
    ...

Essentially a CSV using spaces instead of commas. data is a list of points as
tuples in format (easting northing altitude). name is the filename
"""
def write_output(data, name):
    output = open(name, "w")

    for coords in data:
        output.write("{} {} {}\n".format(coords[0],
                                       coords[1],
                                       coords[2]))

    output.close()

"""
Because UTM coordinates are based at an origin of 500000, 500000, they need to
be rebased to be imported as a sensible point cloud. This method adjusts all
coordinates given a list of point tuples in format (easting northing altitude)
to be in reference to the given origin point.
"""
def rebase_points(points, origin):
    for (index, point) in enumerate(points):
        points[index] = (point[0] - origin[0],
                         point[1] - origin[1],
                         point[2])

"""
Rips a Google Earth KML consisting of LineStrings and single point Placemarks
into a ASCII point cloud files. Files are called "refpoints.asc" which are the
LineStrings and "ctlpoints.asc" which are the Placemarks. Files created in current
working directory.
"""
def main(args):
    kml = open(args[0], "r")
    ref_points = []
    ctl_points = []

    # Constants for FSM which figures out what to do with each KML line
    RESET = 0           # look for next <Placmark> tag
    REF_LINE = 1        # <Placemark> tag found. look for <LineString> tag
    CTL_POINT = 2       # <LineString> tag not found. get coordinates for a single point Placemark
    GET_REF_POINTS = 3  # <LineString> tag found. look for <coordinates> tag to rip points from

    # tracks FSM state
    state = RESET

    # get all LineStrings and Placemarks in UTM coordinates
    for line in kml:
        line = line.strip()
        if line.startswith("<Placemark>"):
            state = CTL_POINT

        if state == RESET:
            continue

        if state == CTL_POINT:
            if line.startswith("<LineString>"):
                state = REF_LINE
            if line.startswith("<coordinates>"):
                ctl_points.append(get_ctl_point(line))
                state = RESET

        if state == GET_REF_POINTS:
            ref_points.extend(get_ref_points(line))
            state = RESET

        if state == REF_LINE:
            if line.startswith("<coordinates>"):
                state = GET_REF_POINTS

    # print all points for debugging
    origin = ctl_points[0]
    print(ref_points)
    print(ctl_points)

    # rebase points around a more sensible origin
    rebase_points(ref_points, origin)
    rebase_points(ctl_points, origin)

    # write points out to files
    write_output(ref_points, "refpoints.asc")
    write_output(ctl_points, "ctlpoints.asc")

if __name__ == "__main__":
    main(sys.argv[1:])
