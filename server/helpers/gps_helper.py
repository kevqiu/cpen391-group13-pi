import math
import pynmea2
import datetime

from server.models.item_data import ItemData


"""
Converts an NMEA sentence containing GPGGA data
to a server-consumable ItemData object
"""
def parse_gpgga_data(data):
    msg = pynmea2.parse(data)

    dt = datetime.datetime.now()\
            .replace(hour=msg.timestamp.hour,
                minute=msg.timestamp.minute,
                second=msg.timestamp.second)

    return ItemData(dt, msg.latitude, msg.longitude)


"""
Given a target latitude and longitude,
find the closest warehouse by distance
"""
def find_closest_warehouse(warehouses, latitude, longitude):
    closest_dist = float('inf')
    closest_warehouse = None

    for w in warehouses:
        dist = math.hypot(w.latitude - latitude, w.longitude - longitude)
        if  dist < closest_dist:
            closest_dist = dist
            closest_warehouse = w

    return closest_warehouse