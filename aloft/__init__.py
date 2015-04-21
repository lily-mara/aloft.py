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
		return {
			'station': self.station, 'winds': {
				altitude: wind.dict() if wind else Wind(0, 0).dict()
				for altitude, wind in self.winds.items()
			}
		}


class Wind(namedtuple('Wind', 'direction speed')):
	def json(self):
		return json.dumps(self.dict())

	def dict(self):
		return {'direction': self.direction, 'speed': self.speed}


URL = 'http://aviationweather.gov/products/nws/all'
LINE_PATTERN = re.compile(r"""
	(?P<code>\w+)\s               # Airport code
	(?P<three_K>.{4})\s           # Winds aloft at 3,000'
	(?P<six_K>.{7})\s             # Winds aloft at 6,000'
	(?P<nine_K>.{7})\s            # Winds aloft at 9,000'
	(?P<twelve_K>.{7})\s          # Winds aloft at 12,000'
	(?P<eighteen_K>.{7})\s        # Winds aloft at 18,000'
	(?P<twenty_four_K>.{7})\s     # Winds aloft at 24,000'
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
	html = requests.get(URL).text

	data_block = _find_data_block(html)
	station_line = _find_station_line(airport_code, data_block)
	return _parse_station_line(station_line)


def _airport_codes_from_data_block(data_block):
	codes = set()

	for line in data_block:
		match = LINE_PATTERN.match(line)
		if match:
			codes.add(match.group('code'))

	return codes


def _find_data_block(html):
	soup = BeautifulSoup(html)
	data_block = soup.find('pre').text

	block = [i for i in data_block.split('\n') if i]
	return block


def _find_station_line(airport_code, data_block):
	airport_code = airport_code.strip().upper()
	for line in data_block:
		match = LINE_PATTERN.match(line)
		if match:
			if match.group('code').strip() == airport_code:
				return line
	raise ValueError('The given airport code is not indexed by NOAA')


def _parse_station_line(station_line):
	match = LINE_PATTERN.match(station_line)
	winds = OrderedDict()

	winds[3000] = _parse_3k(match.group('three_K'))
	winds[6000] = _parse_6k_24k(match.group('six_K'))
	winds[9000] = _parse_6k_24k(match.group('nine_K'))
	winds[12000] = _parse_6k_24k(match.group('twelve_K'))
	winds[18000] = _parse_6k_24k(match.group('eighteen_K'))
	winds[24000] = _parse_6k_24k(match.group('twenty_four_K'))

	winds_aloft = WindsAloft(match.group('code'), winds)
	return winds_aloft


def _parse_3k(three_k):
	if re.match(r'\w+', three_k):
		direction = int(three_k[:2] + '0')
		speed = int(three_k[2:])
		return Wind(direction, speed)
	else:
		return None


def _parse_6k_24k(group):
	if re.match(r'\w+', group):
		direction = int(group[:2] + '0')
		speed = int(group[2:4])
		return Wind(direction, speed)
	else:
		return None
