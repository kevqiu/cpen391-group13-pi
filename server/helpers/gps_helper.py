import math
import pynmea2
import datetime

from server.models.item_data import ItemData


def parse_gpgga_data(data):
    msg = pynmea2.parse(data)

    dt = datetime.datetime.now()\
            .replace(hour=msg.timestamp.hour,
                minute=msg.timestamp.minute,
                second=msg.timestamp.second)

    return ItemData(dt, msg.latitude, msg.longitude)


def find_closest_warehouse(warehouses, item_data):
    closest_dist = float('inf')
    closest_warehouse = None

    for w in warehouses:
        dist = math.hypot(w.latitude - item_data.latitude, w.longitude - item_data.longitude)
        if  dist < closest_dist:
            closest_dist = dist
            closest_warehouse = w

    return closest_warehouse