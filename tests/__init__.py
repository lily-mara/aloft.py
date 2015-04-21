from unittest import TestCase, main
import os

from aloft import _find_station_line, _parse_station_line
from aloft import _airport_codes_from_data_block

BASE_DIR = os.path.dirname(__file__)


class TestAirportCodes(TestCase):
	def setUp(self):
		with open(os.path.join(BASE_DIR, 'example_data.txt'), 'r') as data_file:
			self.data = data_file.readlines()

	def test_all_codes(self):
		codes = {
			'ABI', 'ABQ', 'ABR', 'ACK', 'ACY', 'AGC', 'ALB', 'ALS', 'AMA',
			'AST', 'ATL', 'AVP', 'AXN', 'BAM', 'BCE', 'BDL', 'BFF', 'BGR',
			'BHM', 'BIH', 'BIL', 'BLH', 'BML', 'BNA', 'BOI', 'BOS', 'BRL',
			'BRO', 'BUF', 'CAE', 'CAR', 'CGI', 'CHS', 'CLE', 'CLL', 'CMH',
			'COU', 'CRP', 'CRW', 'CSG', 'CVG', 'CZI', 'DAL', 'DBQ', 'DEN',
			'DIK', 'DLH', 'DLN', 'DRT', 'DSM', 'ECK', 'EKN', 'ELP', 'ELY',
			'EMI', 'EVV', 'EYW', 'FAT', 'GPI', 'FLO', 'FMN', 'FOT', 'FSD',
			'FSM', 'FWA', 'GAG', 'GCK', 'GEG', 'GFK', 'GGW', 'GJT', 'GLD',
			'GRB', 'GRI', 'GSP', 'GTF', 'H51', 'H52', 'H61', 'HAT', 'HOU',
			'HSV', 'ICT', 'ILM', 'IMB', 'IND', 'INK', 'INL', 'JAN', 'JAX',
			'JFK', 'JOT', 'LAS', 'LBB', 'LCH', 'LIT', 'LKV', 'LND', 'LOU',
			'LRD', 'LSE', 'LWS', 'MBW', 'MCW', 'MEM', 'MGM', 'MIA', 'MKC',
			'MKG', 'MLB', 'MLS', 'MOB', 'MOT', 'MQT', 'MRF', 'MSP', 'MSY',
			'OKC', 'OMA', 'ONL', 'ONT', 'ORF', 'OTH', 'PDX', 'PFN', 'PHX',
			'PIE', 'PIH', 'PIR', 'PLB', 'PRC', 'PSB', 'PSX', 'PUB', 'PWM',
			'RAP', 'RBL', 'RDM', 'RDU', 'RIC', 'RKS', 'RNO', 'ROA', 'ROW',
			'SAC', 'SAN', 'SAT', 'SAV', 'SBA', 'SEA', 'SFO', 'SGF', 'SHV',
			'SIY', 'SLC', 'SLN', 'SPI', 'SPS', 'SSM', 'STL', 'SYR', 'T01',
			'T06', 'T07', 'TCC', 'TLH', 'TRI', 'TUL', 'TUS', 'TVC', 'TYS',
			'WJF', 'YKM', 'ZUN', '2XG', '4J3'
		}

		self.assertEqual(_airport_codes_from_data_block(self.data), codes)


class TestWindsAloftDictAllGood(TestCase):
	def setUp(self):
		with open(os.path.join(BASE_DIR, 'example_data.txt'), 'r') as data_file:
			self.data = data_file.readlines()
		self.line = _find_station_line('CVG', self.data)
		self.winds = _parse_station_line(self.line)
		self.winds_dict = self.winds.dict()

	def test_3k_winds(self):
		self.assertEqual(self.winds_dict['winds'][3000]['direction'], 190)
		self.assertEqual(self.winds_dict['winds'][3000]['speed'], 30)

	def test_6k_winds(self):
		self.assertEqual(self.winds_dict['winds'][6000]['direction'], 220)
		self.assertEqual(self.winds_dict['winds'][6000]['speed'], 36)

	def test_9k_winds(self):
		self.assertEqual(self.winds_dict['winds'][9000]['direction'], 210)
		self.assertEqual(self.winds_dict['winds'][9000]['speed'], 35)


class TestWindsAloftDictSomeNone(TestCase):
	def setUp(self):
		with open(os.path.join(BASE_DIR, 'example_data.txt'), 'r') as data_file:
			self.data = data_file.readlines()
		self.line = _find_station_line('DEN', self.data)
		self.winds = _parse_station_line(self.line)
		self.winds_dict = self.winds.dict()

	def test_3k_winds(self):
		self.assertEqual(self.winds_dict['winds'][3000]['direction'], 0)
		self.assertEqual(self.winds_dict['winds'][3000]['speed'], 0)

	def test_6k_winds(self):
		self.assertEqual(self.winds_dict['winds'][6000]['direction'], 0)
		self.assertEqual(self.winds_dict['winds'][6000]['speed'], 0)

	def test_9k_winds(self):
		self.assertEqual(self.winds_dict['winds'][9000]['direction'], 360)
		self.assertEqual(self.winds_dict['winds'][9000]['speed'], 8)



class TestParseStationLine(TestCase):
	def setUp(self):
		with open(os.path.join(BASE_DIR, 'example_data.txt'), 'r') as data_file:
			self.data = data_file.readlines()
		self.line = _find_station_line('CVG', self.data)
		self.winds = _parse_station_line(self.line)

	def test_6k_winds(self):
		winds = self.winds.winds[6000]
		self.assertEqual(winds.direction, 220)
		self.assertEqual(winds.speed, 36)

	def test_3k_winds(self):
		winds = self.winds.winds[3000]
		self.assertEqual(winds.direction, 190)
		self.assertEqual(winds.speed, 30)

	def test_9k_winds(self):
		winds = self.winds.winds[9000]
		self.assertEqual(winds.direction, 210)
		self.assertEqual(winds.speed, 35)


class TestParseStationLineSomeNone(TestCase):
	def setUp(self):
		with open(os.path.join(BASE_DIR, 'example_data.txt'), 'r') as data_file:
			self.data = data_file.readlines()
		self.line = _find_station_line('DEN', self.data)
		self.winds = _parse_station_line(self.line)

	def test_6k_winds(self):
		winds = self.winds.winds[6000]
		self.assertIsNone(winds)

	def test_3k_winds(self):
		winds = self.winds.winds[3000]
		self.assertIsNone(winds)

	def test_9k_winds(self):
		winds = self.winds.winds[9000]
		self.assertEqual(winds.direction, 360)
		self.assertEqual(winds.speed, 8)


class TestFindStationLine(TestCase):
	def setUp(self):
		with open(os.path.join(BASE_DIR, 'example_data.txt'), 'r') as data_file:
			self.data = data_file.readlines()

	def test_cvg_lowercase_airport_code(self):
		station_line = _find_station_line('cvg', self.data)
		self.assertIn('CVG', station_line)

	def test_cvg_uppercase_airport_code(self):
		station_line = _find_station_line('CVG', self.data)
		self.assertIn('CVG', station_line)

	def test_cvg_leading_spaces_airport_code(self):
		station_line = _find_station_line('      CVG', self.data)
		self.assertIn('CVG', station_line)

	def test_cvg_trailing_spaces_airport_code(self):
		station_line = _find_station_line('CVG      ', self.data)
		self.assertIn('CVG', station_line)

	def test_cvg_leading_and_trailing_spaces_airport_code(self):
		station_line = _find_station_line('   CVG   ', self.data)
		self.assertIn('CVG', station_line)

	def test_bogus_airport_code(self):
		with self.assertRaises(ValueError):
			_find_station_line('fjaksdlf', self.data)



if __name__ == '__main__':
	main()
