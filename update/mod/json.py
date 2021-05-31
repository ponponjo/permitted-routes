'''
Functions to process data in downloads folder to create json
'''

import re
import os
import json


def get_filename(file_regex: re.Pattern) -> str:
    '''
    Searches in fownload dir for filename matching regex, and returns that filename
    '''
    files = os.listdir('../.download')
    for file in files:
        if re.search(pattern=file_regex, string=file):
            return file
    return None


def update_station_to_routing_point_json() -> None:
    '''
    Updates from the downloads folder to a file named output/station_to_routing_point.json,
    json to convert station to routing point(s)
    '''
    stations_file = get_filename(r'RJRG.*\.RGS')
    if not stations_file:
        print("Generating Stations File failed - File not found")
        return

    stations_dict = {}
    with open('../.download/'+stations_file, 'r') as open_file:
        for line in open_file:
            if line[0:3] == '/!!':
                continue
            if line[0:2] == '/ ':
                station_name = line[2:].strip()
                rps = next(open_file).strip()
                stations_dict[station_name] = [
                    rp for rp in rps.split(',') if rp]

    with open('../.output/station_to_routing_point.json', 'w') as json_file:
        json.dump(stations_dict, json_file)


def update_crs_to_station_name_json() -> None:
    '''
    Updates from the downloads folder to a file named output/crs_to_station_name.json,
    json to convert RP Identifier to station name
    '''
    crs_file = get_filename(r'RJRG.*\.RGN')
    if not crs_file:
        print("Generating crs File failed - File not found")
        return

    crs_dict = {}
    with open('../.download/'+crs_file, 'r') as open_file:
        for line in open_file:
            if line[0:3] == '/!!':
                continue
            if line[0:2] == '/ ':
                station_name = line[2:].strip()
                crs = next(open_file).strip()
                crs_dict[crs] = station_name

    with open('../.output/crs_to_station_name.json', 'w') as json_file:
        json.dump(crs_dict, json_file)


def update_rp_to_rp_to_maps_json() -> None:
    '''
    Updates from the downloads folder to a file named output/route_to_maps.json,
    json to convert a route to which maps it appears on
    '''
    routes_file = get_filename(r'RJRG.*\.RGR')
    if not routes_file:
        print("Generating routes File failed - File not found")
        return

    routes_dict = {}
    with open('../.download/'+routes_file, 'r') as open_file:
        for line in open_file:
            if line[0:3] == '/!!':
                continue
            if line[0:2] == '/ ':
                route = line[2:].strip()
                routes_dict[route] = []
            else:
                rps = line.strip()
                routes_dict[route].append(
                    [rp for rp in rps.split(',') if rp][2:])
    with open('../.output/route_to_maps.json', 'w') as json_file:
        json.dump(routes_dict, json_file)


def update_map_to_links_json() -> None:
    '''
    Updates from the downloads folder to a file named output/map_to_links.json,
    json to convert a map to the links contained on that map
    '''
    maps_file = get_filename(r'RJRG.*\.RGM')
    if not maps_file:
        print("Generating links File failed - File not found")
        return

    links_dict = {}

    with open('../.download/'+maps_file, 'r') as open_file:
        for line in open_file:
            if line[0:3] == '/!!':
                continue
            if line[0:2] != '/ ':
                links_dict[line.strip()] = []

    links_file = get_filename(r'RJRG.*\.RGL')
    if not links_file:
        print("Generating links File failed - File not found")
        return

    with open('../.download/'+links_file, 'r') as open_file:
        for line in open_file:
            if line[0:3] == '/!!':
                continue
            if line[0:2] != '/ ':
                clean_line = line.strip().split(',')
                links_dict[clean_line[2]].append(
                    (clean_line[0], clean_line[1]))
    with open('../.output/map_to_links.json', 'w') as json_file:
        json.dump(links_dict, json_file)


def update_data() -> None:
    '''
    Function to update each json in turn
    '''
    try:
        os.mkdir('../.output')
    except FileExistsError:
        pass
    update_station_to_routing_point_json()
    update_crs_to_station_name_json()
    update_rp_to_rp_to_maps_json()
    update_map_to_links_json()
