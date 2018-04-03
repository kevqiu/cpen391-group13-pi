import math
import pynmea2
import datetime

from server.models.item_data import ItemData


def parse_gpgga_data(data):
    """
    Converts an NMEA sentence containing GPGGA data
    to a server-consumable ItemData object
    """

    # call pynmea library to convert GPGGA sentence to Python object
    msg = pynmea2.parse(data)

    # replace current timestamp with GPS timestamp
    dt = datetime.datetime.now()\
            .replace(hour=msg.timestamp.hour,
                minute=msg.timestamp.minute,
                second=msg.timestamp.second)

    return ItemData(dt, msg.latitude, msg.longitude)



def find_closest_warehouse(warehouses, latitude, longitude):
    """
    Given a target latitude and longitude,
    find the closest warehouse by distance
    """

    # initialize variables to keep track
    closest_dist = float('inf')
    closest_warehouse = None

    for w in warehouses:
        # find closest warehouse using hypotenuse distance
        dist = math.hypot(w.latitude - latitude, w.longitude - longitude)
        if  dist < closest_dist:
            closest_dist = dist
            closest_warehouse = w

    return closest_warehouse


def convert_dmm_to_dd(coord):
    """
    Converts DMM coordinates to Degree Decimals
    Input: DDMM.MMMM,C or DDDMM.MMMM,C
    """
    (dm, card) = coord.split(',')

    dir = 1 if card == 'N' or card == 'E' else -1
    d = dm[:dm.index('.') - 2]
    m = dm[dm.index('.') - 2:]

    return (int(d) + float(m) / 60) * dir
