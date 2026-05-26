"""Geocode subject + all comps via U.S. Census Bureau geocoder (free, no API key).
Falls back to Nominatim if Census misses. Also outputs Google Maps URLs."""
import urllib.request, urllib.parse, json, time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ADDRESSES = [
    ("Subject",          "3607 Pacific Ave, Marina Del Rey, CA 90292"),
    ("A 440 Howland",    "440 Howland Canal, Venice, CA 90291"),
    ("B 124 Catamaran",  "124 Catamaran St, Marina Del Rey, CA 90292"),
    ("C 101 Catamaran",  "101 Catamaran St, Marina Del Rey, CA 90292"),
    ("D 16 Fleet",       "16 Fleet St, Marina Del Rey, CA 90292"),
    ("E 1426 Main",      "1426 Main St, Venice, CA 90291"),
    ("F 2201 Ocean Ave", "2201 Ocean Ave, Venice, CA 90291"),
    ("G 315 Vernon",     "315 Vernon Ave, Venice, CA 90291"),
    ("R1 3900 Pacific",  "3900 Pacific Ave, Marina Del Rey, CA 90292"),
    ("R2 3512 Pacific",  "3512 Pacific Ave, Marina Del Rey, CA 90292"),
    ("R3 3003 OFW",      "3003 Ocean Front Walk, Venice, CA 90291"),
]

HEADERS = {'User-Agent': 'LAAA-OM-Builder/1.0'}

def census(addr):
    q = urllib.parse.quote(addr)
    url = f'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={q}&benchmark=Public_AR_Current&format=json'
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
        matches = data.get('result',{}).get('addressMatches',[])
        if matches:
            c = matches[0]['coordinates']
            return float(c['y']), float(c['x']), matches[0].get('matchedAddress','')
    return None

def nominatim(addr):
    q = urllib.parse.quote(addr)
    url = f'https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1&countrycodes=us'
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
        if data:
            return float(data[0]['lat']), float(data[0]['lon']), data[0].get('display_name','')
    return None

print(f"{'Label':<20} {'Lat':>11}  {'Lng':>12}  Source   Matched")
print('-'*120)

results = []
for label, addr in ADDRESSES:
    r = None
    src = ''
    try:
        r = census(addr)
        src = 'CENSUS'
    except Exception as e:
        print(f"  Census error: {e}")
    time.sleep(0.4)
    if not r:
        try:
            r = nominatim(addr)
            src = 'NOMINATIM'
        except Exception as e:
            print(f"  Nominatim error: {e}")
        time.sleep(1.1)
    if r:
        lat, lng, name = r
        gmap_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(addr)}"
        print(f"{label:<20} {lat:>11.6f}, {lng:>12.6f}  {src:<9} {name[:70]}")
        results.append((label, addr, lat, lng, gmap_url))
    else:
        print(f"{label:<20} {'NOT FOUND':>26}")
        results.append((label, addr, None, None, None))

print('\n=== JS-ready coordinates ===\n')
for label, addr, lat, lng, gmap in results:
    if lat:
        print(f"  // {label} - {addr}")
        print(f"  [{lat:.6f}, {lng:.6f}, '{gmap}'],")
