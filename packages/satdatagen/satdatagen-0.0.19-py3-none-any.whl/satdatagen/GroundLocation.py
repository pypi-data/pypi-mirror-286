from astropy.coordinates import EarthLocation
from astropy import units as u
import openmeteo_requests
from datetime import datetime
from satdatagen.TimeRange import TimeRange
import satdatagen.helpers as hel

		
class GroundLocation:
	'''
	this class acts as a wrapper for the astropy EarthLocation class, and is also how the user creates their dataset using the create_dataset class method.

	users create a GroundLocation instance with the latitude/longitude of a location on earth, a TimeRange object that determines the period of observation, and the path to their space-track.org login credentials
	'''
	def __init__(self, space_track_credentials, lat, lon, time_range):
		self.lon = lon
		self.lat = lat
		self.el = EarthLocation(lat = lat*u.deg, lon = lon*u.deg)
		self.time_range = time_range
		self.credentials = space_track_credentials

	def set_latlon(self, lat, lon):
		self.lat = lat
		self.lon = lon

	def get_latlon(self):
		return lat,lon

	def EarthLocation(self):
		return self.el

	def set_time_range(self, time_range):
		self.time_range = time_range

	def get_time_range(self):
		return self.time_range

	def generate_dataset(self, timing = False):

		return hel._generate_dataset(self.credentials, self.el, self.time_range.times, timing = timing)

	def __str__(self):
		return f'Latitude: {self.lat}, Longitude: {self.lon}, Time range: {self.time_range}'




# if __name__ == '__main__':
# 	lat = 48.78 #degrees north
# 	lon = 9.18 #degrees west

# 	temp = datetime(2024, 6, 10, hour=23, minute=30)
# 	temp2 = datetime(2024, 6, 12)
# 	td = temp2.date() - temp.date()
# 	print((td.days))
# 	time_range = TimeRange(temp, periods = 25, delta = 500)
# 	credentials = '/Users/adinagolden/Documents/MIT/Thesis/thesis/code/credentials.json'
# 	haystack = GroundLocation(credentials, lat, lon, time_range = time_range)
# 	print(haystack.find_all_overhead_sats())

# 	# print(clouds)