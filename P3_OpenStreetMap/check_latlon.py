import xml.etree.cElementTree as ET
import math

osm_file = 'guiyang_china.osm'

# number of nodes whose latitude is out of bounds
count_of_error_lat = 0
# number of nodes whose longitude is out of bounds
count_of_error_lon = 0
# the maximum difference of latitude
max_abs_lat_diff = -1
# the maximum difference of longitude
max_abs_lon_diff = -1
# the minimum difference of latitude
min_abs_lat_diff = float('inf')
# the minimum difference of longitude
min_abs_lon_diff = float('inf')

for event, element in ET.iterparse(osm_file, events=("start",)):
    # retrieve the latitude and longitude range from <bounds .../>
    if element.tag == 'bounds':
        minlat = float(element.attrib['minlat'])
        minlon = float(element.attrib['minlon'])
        maxlat = float(element.attrib['maxlat'])
        maxlon = float(element.attrib['maxlon'])

    # only node elements have latitude and longitude information
    if element.tag == 'node':
        lat = float(element.attrib['lat'])
        lon = float(element.attrib['lon'])
        if not (minlat <= lat <= maxlat):
            diff = min(math.fabs(lat-minlat), math.fabs(lat-maxlat))
            # print('node {} latitude {} out of bounds [{}, {}], diff {}'.format(element.attrib['id'], lat, minlat, maxlat, diff))
            count_of_error_lat += 1
            if diff > max_abs_lat_diff:
                max_abs_lat_diff = diff
            if diff < min_abs_lat_diff:
                min_abs_lat_diff = diff
        if not (minlon <= lon <= maxlon):
            diff = min(math.fabs(lat - minlat), math.fabs(lat - maxlat))
            # print('node {} longitude {} out of bounds [{}, {}], diff {}'.format(element.attrib['id'], lon, minlon, maxlon, diff))
            count_of_error_lon += 1
            if diff > max_abs_lon_diff:
                max_abs_lon_diff = diff
            if diff < min_abs_lon_diff:
                min_abs_lon_diff = diff

print('total number of error lat {}, lon {}'.format(count_of_error_lat, count_of_error_lon))
print('latitude diff range [{}, {}], longitude diff range [{}, {}]'.format(min_abs_lat_diff, max_abs_lat_diff, min_abs_lon_diff, max_abs_lon_diff))