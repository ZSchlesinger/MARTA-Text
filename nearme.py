from gmaps import Geocoding
import math
import stops

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
    except:
        pass
    return coord

def distance(a, b):
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))

def closest_stop_coord(coord):
    global bus_stops
    if bus_stops is None:
        load_bus_stops()
    return sorted(list(bus_stops.keys()), key=lambda x : distance(coord, bus_stops[x]))[0]

def closest_stop(address):
    return str(address)
    # a_coord = address_to_coord(address)
    # if a_coord is None:
#        return None 
    #     return str(len(bus_stops))
    # return closest_stop_coord(a_coord)
