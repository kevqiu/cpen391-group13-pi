import pynmea2
import datetime

from server.models.item_data import ItemData


def parse_gpgga_data(data):
    msg = pynmea2.parse(data)

    d = datetime.datetime.now()\
            .replace(hour=msg.timestamp.hour,
                minute=msg.timestamp.minute,
                second=msg.timestamp.second)

    return ItemData(d, msg.latitude, msg.longitude)


data = parse_gpgga_data("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")
print(data.timedate)
print(data.latitude)
print(data.longitude)