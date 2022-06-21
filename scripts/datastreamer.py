#!/usr/bin/env python3
import click
import gpxpy
import gpxpy.gpx
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json

ENDPOINT = "Endpoint=sb://eh-zcamprivage2022.servicebus.windows.net/;SharedAccessKeyName=rootManagedAccessKey;SharedAccessKey=duPp8T82aGyMSgO+hQ5zoJuxZCLUreQ6yyVYo39DoqM=;EntityPath=eventhub-zcamprivage2022"
EVENT_HUBNAME = "eventhub-zcamprivage2022"
POINTS_ITER = None
DELAY_SECONDS = 1

@click.command()
@click.argument('input', type=click.File("rb"))
def main(input):
    """Simple program that processes gpx data."""
    print("Process input file %s".format(input))
    global POINTS_ITER
    POINTS_ITER = readfile(input)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(publish_events())

def readfile(input):
    print("Process input file %s".format(input))
    points = []
    gpx = gpxpy.parse(input)
    for count, track in enumerate(gpx.tracks):
        print("Process track {}".format(count))
        for segment in track.segments:
            for point in segment.points:
                print("{} - Point at ({}, {}) -> {}".format(point.time, point.latitude, point.longitude, point.elevation))
                points.append({
                    'ti': str(point.time),
                    'la': point.latitude,
                    'lo': point.longitude,
                    'el': point.elevation,
                })
    return iter(points)

async def publish_events():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(conn_str=ENDPOINT, eventhub_name=EVENT_HUBNAME)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        for point in POINTS_ITER:
            json_data = json.dumps(point)
            # Send the event to the event hub
            await asyncio.sleep(DELAY_SECONDS)
            event_data = EventData(json_data)
            print("Publish event data {}".format(str(event_data)))
            await producer.send_event(event_data)

if __name__ == '__main__':
    main()