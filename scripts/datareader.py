#!/usr/bin/env python3
import click
import gpxpy
import gpxpy.gpx

@click.command()
@click.argument('input', type=click.File("rb"))
def read(input):
    """Simple program that processes gpx data."""
    print("Process input file %s".format(input))

    gpx = gpxpy.parse(input)
    for count, track in enumerate(gpx.tracks):
        print("Process track {}".format(count))

        for segment in track.segments:
            for point in segment.points:
                print("{} - Point at ({}, {}) -> {}".format(point.time, point.latitude, point.longitude, point.elevation))


if __name__ == '__main__':
    read()