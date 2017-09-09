from gmaps import Geocoding
import math
import stops

import warnings
import requests
import contextlib

try:
    from functools import partialmethod
except ImportError:
    # Python 2 fallback: https://gist.github.com/carymrobbins/8940382
    from functools import partial

    class partialmethod(partial):
        def __get__(self, instance, owner):
            if instance is None:
                return self

            return partial(self.func, instance, *(self.args or ()), **(self.keywords or {}))

@contextlib.contextmanager
def no_ssl_verification():
    old_request = requests.Session.request
    requests.Session.request = partialmethod(old_request, verify=False)

    warnings.filterwarnings('ignore', 'Unverified HTTPS request')
    yield
    warnings.resetwarnings()

    requests.Session.request = old_request

api = Geocoding()
bus_stops = None

def load_bus_stops():
    stops_lines = stops.data.split("\n")
    stops_data = {d[2] : (float(d[3]), float(d[4])) for d in [l.split(',') for l in stops_lines if l is not None and ',' in l and 'stop_name' not in l]}
    global bus_stops
    bus_stops = stops_data

def address_to_coord(address):
    coord = None
    try:
        location = api.geocode(address)
        coords = [(p['lat'], p['lng']) for p in [a['geometry']['location'] for a in location]]
        coord = coords[0]
    except Exception as e:
        coord = str(e)
    return coord

def distance(a, b):
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))

def closest_stop_coord(coord):
    global bus_stops
    if bus_stops is None:
        load_bus_stops()
    return sorted(list(bus_stops.keys()), key=lambda x : distance(coord, bus_stops[x]))[0]

def closest_stop(address):
    a_coord = "test"
    try:
        with no_ssl_verification:
            a_coord = address_to_coord(address)
    except Exception as e:
        a_coord = str(e)
    return str(a_coord)
    # if a_coord is None:
#        return None 
    #     return str(len(bus_stops))
    # return closest_stop_coord(a_coord)
