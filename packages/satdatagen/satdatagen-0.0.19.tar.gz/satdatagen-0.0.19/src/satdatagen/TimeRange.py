from astropy.time import Time
from datetime import datetime, date, timedelta
import numpy as np
class TimeRange:
	def __init__(self, start_date, end_date = None, periods = 0, delta = 0):
		'''
		@param start_date: can be string in ISO format, datetime object, or list of strings/datetime objects
		'''
		self.periods = periods
		self.delta = delta

		if isinstance(start_date, str):
			temp = datetime.fromisoformat(start_date)
			self.start = Time(start_date, scale='utc', format='isot')
			if isinstance(end_date, str):
				self.end = Time(end_date, scale = 'utc', format = 'isot')
				self.times = np.linspace(self.start, self.end, periods)
				self.delta = None
			elif isinstance(end_date, datetime):
				self.end = Time(end_date, scale = 'utc')
				self.times = np.linspace(self.start, self.end, periods)
				self.delta = None

			elif not end_date:
				times_temp = [temp + timedelta(minutes=i*delta) for i in range(periods)]
				self.times = Time(times_temp, scale='utc', format='isot')
				self.end = Time(times_temp[-1], scale='utc', format='isot')

		elif isinstance(start_date, list) or isinstance(start_date, tuple) or isinstance(start_date, np.ndarray):
			if isinstance(start_date[0], str):
				self.start = Time(start_date[0], scale='utc', format='isot')
				self.end = Time(start_date[-1], scale='utc', format='isot')
				self.times = Time(start_date, scale='utc', format='isot')

			elif isinstance(start_date[0], datetime):
				self.start = Time(start_date[0], scale='utc')
				self.end = Time(start_date[-1], scale='utc')
				self.times = Time(start_date, scale='utc')

		elif isinstance(start_date, datetime):
			self.start = Time(start_date, scale='utc')

			if isinstance(end_date, str):
				self.end = Time(end_date, scale = 'utc', format = 'isot')
				self.times = np.linspace(self.start, self.end, periods)
				self.delta = None
			elif isinstance(end_date, datetime):
				self.end = Time(end_date, scale = 'utc')
				self.times = np.linspace(self.start, self.end, periods)
				self.delta = None

			elif not end_date:
				times_temp = [start_date + timedelta(minutes=i*delta) for i in range(periods)]
				self.times = Time(times_temp, scale='utc')
				self.end = Time(times_temp[-1], scale='utc')

		self.jd1 = self.times.jd1
		self.jd2 = self.times.jd2

	def __len__(self):
		return len(self.times)

	def __getitem__(self, i):
		return self.times[i]

	def __str__(self):

		return '\n'.join(self.times.utc.iso)
	def get_start(self):
		return self.start

	def get_end(self):
		return self.end


if __name__ == '__main__':
	temp = datetime(2024, 6, 10, hour=14, minute=30)
	time_range = TimeRange(temp, periods = 5, delta = 2)
	print(type(time_range[0].datetime))

	print((time_range.start) - time_range.end)

