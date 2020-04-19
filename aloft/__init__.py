#!/usr/bin/env python
import requests
from collections import namedtuple, OrderedDict
from bs4 import BeautifulSoup
import re
import json


class WindsAloft(namedtuple('WindsAloft', 'station winds')):
	def json(self):
		return json.dumps(self.dict())

	def dict(self):
		d = {'station': self.station, 'winds': []}

		for altitude, wind in self.winds.items():
			if wind:
				wind_dict = wind.dict()
			else:
				wind_dict = Wind(0, 0).dict()
			wind_dict['altitude'] = altitude

			d['winds'].append(wind_dict)

		return d


class Wind(namedtuple('Wind', 'direction speed temp')):
	def json(self):
		return json.dumps(self.dict())

	def dict(self):
		return {'direction': self.direction, 'speed': self.speed, 'temp': self.temp}


URL = 'https://www.aviationweather.gov/windtemp/data?region=all&level=low&fcst=24&layout=off'
LINE_PATTERN = re.compile(
        r"""
	(?P<code>\w+)\s               # Airport code
	(?P<three_K>.{4})\s           # Winds aloft at 3,000'
	(?P<six_K>.{7})\s             # Winds aloft at 6,000'
	(?P<nine_K>.{7})\s            # Winds aloft at 9,000'
	(?P<twelve_K>.{7})\s          # Winds aloft at 12,000'
	(?P<eighteen_K>.{7})\s        # Winds aloft at 18,000'
	(?P<twenty_four_K>.{7})\s     # Winds aloft at 24,000'
	(?P<thirty_K>.{6})\s          # Winds aloft at 30,000'
	(?P<thirty_four_K>.{6})\s     # Winds aloft at 34,000'
	(?P<thirty_nine_K>.{6})     # Winds aloft at 39,000'
	""",
	re.VERBOSE
)


def airport_codes():
	"""
	Returns the set of airport codes that is available to be requested.
	"""
	html = requests.get(URL).text
	data_block = _find_data_block(html)

	return _airport_codes_from_data_block(data_block)


def winds_aloft(airport_code):
    wahtml = requests.get(URL).text
    data_block = _find_data_block(wahtml)
    station_line = _find_station_line(airport_code, data_block)
    return _parse_station_line(station_line)


def _airport_codes_from_data_block(data_block):
	codes = set()

	for line in data_block:
		match = LINE_PATTERN.match(line)
		if match:
			codes.add(match.group('code'))

	return codes


def _find_data_block(wahtml):
	soup = BeautifulSoup(wahtml, 'html.parser')
	data_block = soup.find('pre').text

	block = [i for i in data_block.split('\n') if i]
	return block


def _find_station_line(airport_code, data_block):
    airport_code = airport_code.strip().upper()
    for line in data_block:
        match = LINE_PATTERN.match(line)
        print(match)
        if match:
            print(match.group('code').strip())
            if match.group('code').strip() == airport_code:
                return line
            #raise ValueError('The given airport code is not indexed by NOAA')


def _parse_station_line(station_line):
    print(station_line)
    match = LINE_PATTERN.match(station_line)
    winds = OrderedDict()
    
    winds[3000] = _parse_3k(match.group('three_K'))
    winds[6000] = _parse_6k_24k(match.group('six_K'))
    winds[9000] = _parse_6k_24k(match.group('nine_K'))
    winds[12000] = _parse_6k_24k(match.group('twelve_K'))
    winds[18000] = _parse_6k_24k(match.group('eighteen_K'))
    winds[24000] = _parse_6k_24k(match.group('twenty_four_K'))
    winds[30000] = _parse_30k_39k(match.group('thirty_K'))
    winds[34000] = _parse_30k_39k(match.group('thirty_four_K'))
    winds[39000] = _parse_30k_39k(match.group('thirty_nine_K'))
    
    winds_aloft = WindsAloft(match.group('code'), winds)
    return winds_aloft


def _parse_3k(three_k):
    if re.match(r'\w+', three_k):
        direction = int(three_k[:2] + '0')
        speed = int(three_k[2:])
        temp = 000
        return Wind(direction, speed, temp)
    else:
        return None


def _parse_6k_24k(group):
    if re.match(r'\w+', group):
        direction = int(group[:2] + '0')
        speed = int(group[2:4])
        temp = int(group[4:])
        return Wind(direction, speed, temp)
    else:
        return None
    
def _parse_30k_39k(group):
    if re.match(r'\w+', group):
        direction = int(group[:2] + '0')
        if direction >= 400:
            direction = direction - 500
            speed = int(group[2:4]) + 100
        else:
            speed = int(group[2:4])
        temp = int(group[4:])*-1
        return Wind(direction, speed, temp)
    else:
        return None
