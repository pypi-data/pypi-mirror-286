# import numpy as np
# import os
# import requests
# import pickle
# import json
# import numpy as np
# from datetime import datetime, timezone
# # from datetime import time as tm
# from datetime import timedelta, date
# import time
# from astropy import units as u
# from astropy.time import Time
# from sgp4.api import Satrec
# from sgp4.api import SatrecArray
# from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation
# from astropy.coordinates import SkyCoord
# from astropy import units as u
# from astropy.coordinates import ITRS
from satdatagen.sizes import object_sizes
from satdatagen.helpers import *
from satdatagen.TimeRange import *
from satdatagen.GroundLocation import *
from satdatagen.Satellite import *
# import openmeteo_requests



# '''
# ########################################################################
# ************************************************************************
# WEB QUERY methods
# ************************************************************************
# ########################################################################
# '''

# def space_track_login(space_track_credentials):
# 	'''
# 	logs user into space-track.org

# 	@param space_track_credentials: path to credentials.json file containing the user's login info to space-track.org
# 	@returns: login cookies

# 	'''
# 	with open(space_track_credentials) as json_file:
# 		credentials = json.load(json_file)

# 	url = "https://www.space-track.org/ajaxauth/login"
# 	x = requests.post(url, data = credentials)
# 	if x.status_code == 200:

# 		return x.cookies
# 	else:
# 		print("Login failed with code:",x.status_code)
# 		return None


# def get_cookie(space_track_credentials):
# 	'''
# 		@param space_track_credentials: path to credentials.json file containing the user's login info to space-track.org
# 	    @returns: an existing cookie if there is one, otherwise, get a new one.
# 	    @returns: None if can't get cookies
#     '''

# 	cookie_path = "./cookie.pkl"
# 	try:
# 		auth_cookie = pickle.load(open(cookie_path, "rb"))
# 	except:
# 		auth_cookie = None
# 	if type(auth_cookie) == requests.cookies.RequestsCookieJar:
# 		auth_cookie.clear_expired_cookies()
# 	else:
# 		auth_cookie = None
# 	# log in if needed
# 	if auth_cookie == None or len(auth_cookie) == 0:
# 		auth_cookie = space_track_login(space_track_credentials)
# 		pickle.dump(auth_cookie, open(cookie_path, "wb"))

# 	#return none if failed
# 	if auth_cookie == None:
# 		return None
		
# 	return auth_cookie

# def get_unique_entries(sat_list, day):
# 	'''
# 		finds only the TLE for each object that is closest (but not after) the desired time of observation
# 		@param sat_list: list of dictionaries, 1 for each TLE returned by space-track.org, sorted in order of NORAD ID
# 		@param day: datetime.datetime object representing the day/time of observation

# 		@returns: list of dictionaries, 1 for each RSO observed on day
# 	'''
	
# 	idx = 1
# 	unique_sats = []
	
# 	while (idx < len(sat_list)):
# 		#go through indices of sat_list, find the other TLEs for the same NORAD ID, put them in temp_list
# 		temp_list = []
# 		while(sat_list[idx]['NORAD_CAT_ID'] == sat_list[idx-1]['NORAD_CAT_ID']):

# 			temp_list.append((idx-1, sat_list[idx-1]['EPOCH']))
# 			idx+=1

# 		temp_list.append((idx-1, sat_list[idx-1]['EPOCH']))

# 		#go through temp_list to find the TLE that has the epoch closest to desired time, add that to unique_sats list
# 		closest_ep = 1000000000 #ridiculous number for initial comparison
# 		closest_idx = idx
# 		for ix,ep in temp_list:
# 			epoch = datetime.fromisoformat(ep)
# 			delta = day - epoch

# 			if delta.total_seconds() > 0 and delta.total_seconds() <= closest_ep:
# 				closest_ep = delta.total_seconds()
# 				closest_idx = ix
# 		unique_sats.append(sat_list[closest_idx])
# 		idx+=1
		

# 	return unique_sats


# def get_all_objects(space_track_credentials, day = None): 
# 	'''
# 	@param space_track_credentials: path to credentials.json file containing the user's login info to space-track.org
# 	@param day type: datetime.datetime object representing desired observation day (including time)
# 	@returns: the data that is received as response of the request to star-tracker as list of python dictionaries for each object
# 	'''

# 	auth_cookie = get_cookie(space_track_credentials)
# 	#query space-track for observation day
# 	if day is not None:
# 		#note that if the desired time is early on a day the closest TLE might be from the day before, set threshold to be 8 hours as most TLEs are reported on an 8-hourly basis
# 		if day.hour < 8:
# 			qdate = day.date() - timedelta(days=1)
# 		else:
# 			qdate = day.date()
# 		next_qdate = qdate + timedelta(days=1)
# 		url = f'https://www.space-track.org/basicspacedata/query/class/gp_history/EPOCH/{qdate.isoformat()}--{next_qdate.isoformat()}/orderby/NORAD_CAT_ID%20asc/emptyresult/show'

# 	#if no day specified then queries for current day
# 	else:
# 		url = f'https://www.space-track.org/basicspacedata/query/class/gp/decay_date/null-val/epoch/%3Enow-30/orderby/norad_cat_id/format/json'
# 	response_data = requests.get(url, allow_redirects=True, cookies=auth_cookie)
	
# 	all_objects = []
	
# 	#create list of all objects returned
# 	for i in response_data.json():
# 		all_objects.append(dict(i))

# 	#only return closest TLEs that were recorded BEFORE time of obs.
# 	unique_objs = get_unique_entries(all_objects, day)
# 	return unique_objs
	

# def get_sat_tle(space_track_credentials, sat_id, day):
# 	'''
# 		@param space_track_credentials: path to credentials.json file containing the user's login info to space-track.org
# 		@param sat_id: NORAD ID of RSO for which you'd like the TLEs
# 		@param day type: datetime.datetime object representing desired observation day (including time)

# 		@returns: python dictionary containing the TLE for that satellite which is closest to day
# 	'''
# 	auth_cookie = get_cookie(space_track_credentials)
# 	if day.hour < 8:
# 		qdate = day.date() - timedelta(days=1)
# 	else:
# 		qdate = day.date()
# 	next_qdate = qdate + timedelta(days=1)
		
# 	url = f'https://www.space-track.org/basicspacedata/query/class/gp_history/NORAD_CAT_ID/{sat_id}/EPOCH/{qdate.isoformat()}--{next_qdate.isoformat()}/emptyresult/show'
# 	response_data = requests.get(url, allow_redirects=True, cookies=auth_cookie)
	
# 	all_objects = []
	
# 	#create list of all objects returned
# 	closest_ep = 1000000000
# 	closest_tle = {}
# 	tle = {}
# 	for i in response_data.json():
# 		tle = dict(i)
# 		try:
# 			epoch = datetime.fromisoformat(tle['EPOCH'])
# 		except KeyError:
# 			return None
# 		else:
# 			delta = day - epoch
# 			if delta.total_seconds() > 0 and delta.total_seconds() <= closest_ep:
# 				closest_ep = delta.total_seconds()
# 				closest_tle = tle

# 	return tle


# def propagate_sats(sats, time_list):
# 	'''
# 		propagates each object in sats to its position at the desired observation time(s)

# 		@param sats: list of dictionaries representing the TLEs returned from space-track after filtering for uniqueness
# 		@param time_list: list of datetime.datetime objects representing the desired observation time(s)

# 		@returns: tuple of ndarray numpy arrays.  error codes [e], TEME position coordinates [r], and TEME velocity coordinates [v], with each TLE passed in representing a row in each numpy array

# 	'''
# 	sat_arr = []
# 	for sat in sats:
# 		sat_arr.append(Satrec.twoline2rv(sat['TLE_LINE1'], sat['TLE_LINE2']))
# 	prop_sats = SatrecArray(sat_arr)

# 	times = Time(time_list, scale='utc')
# 	# print(times.jd1)
# 	# print(times.jd2)
# 	time_jd1 = 0
# 	time_jd2 = 0
# 	if type(times.jd1) == float:
# 		time_jd1 = np.array([times.jd1])
# 		time_jd2 = np.array([times.jd2])
# 	else:
# 		time_jd1 = times.jd1
# 		time_jd2 = times.jd2
# 	e,r,v = prop_sats.sgp4(time_jd1, time_jd2)
# 	return e,r,v



# def get_alt_az(observ_loc, sat_teme, sat_teme_v, observ_time):
# 	'''
# 	returns the altitude and azimuth of the given RSO at the given time as observed from the observation location on ground

# 	@param observ_loc: astropy EarthLocation object representing the point on the ground we are observing from
# 	@param sat_teme: numpy array containing the TEME position coordinates of the sat as returned from propagate_sats(...)
# 	@param sat_teme_v: numpy array containing the TEME velocity coordinates of the sat as returned from propagate_sats(...)
# 	@param observ_time: datetime.datetime object representing time of observation

# 	@returns tuple of (altitude, azimuth)
# 	'''

# 	itrs_sat = get_sat_itrs(sat_teme, sat_teme_v, observ_time)

# 	topo_itrs_sat = itrs_sat.cartesian.without_differentials() - observ_loc.get_itrs(np.array(observ_time)).cartesian
# 	sat_itrs_topo = ITRS(topo_itrs_sat, obstime=observ_time, location=observ_loc)
# 	altaz = sat_itrs_topo.transform_to(AltAz(obstime=observ_time, location=observ_loc))

# 	return altaz.alt, altaz.az


# def _find_all_overhead_sats(space_track_credentials, lon, lat, obs_time, periods = 25, delta = 5, eclipsed = False):
# 	'''
# 	returns a json/python dictionary of all the satellites overhead with keys of satellite NORAD ID as given by space-track and values the altitude/azimuth of the satellite at the observation time

# 	@param lat: (geodetic) latitude of ground location
# 	@param lon: longitude of ground location
# 	@param obs_time: datetime object of desired time of observation
# 	[@param periods]: the number of periods to extend the observation time (default 25)
# 	[@param delta]: the delta in minutes between each period (default 5mins)
# 	[@param eclipsed]: boolean that controls whether to include satellites that are eclipsed by the earth (default False)

# 	'''

# 	overhead_sats = {}
# 	observ_loc = EarthLocation(lat = lat * u.deg, lon = lon * u.deg)
# 	time_delta = timedelta(minutes=delta)
# 	time_list = []
# 	for i in range(periods):
# 		time_list.append(obs_time + time_delta*i)

# 	all_sats_for_obs_time = get_all_objects(space_track_credentials, obs_time)

# 	e, r, v = propagate_sats(all_sats_for_obs_time, time_list)
# 	v_x = v[:,:,0] * u.km / u.s
# 	v_y = v[:,:,1] * u.km / u.s
# 	v_z = v[:,:,2] * u.km / u.s

# 	r_x = r[:,:,0] * u.km
# 	r_y = r[:,:,1] * u.km
# 	r_z = r[:,:,2] * u.km

# 	r_cartesian = CartesianRepresentation(x=r_x, y = r_y, z = r_z)
# 	v_cartesian = CartesianDifferential(d_x = v_x, d_y = v_y, d_z = v_z)
# 	teme = TEME(r_cartesian.with_differentials(v_cartesian), obstime=time_list)

# 	obstime = Time(time_list, scale = 'utc')
# 	itrs_sat = teme.transform_to(ITRS(obstime=time_list))

# 	topo_itrs_sat = itrs_sat.cartesian.without_differentials() - observ_loc.get_itrs(obstime).cartesian
# 	sat_itrs_topo = ITRS(topo_itrs_sat, obstime=obstime, location=observ_loc)
# 	altaz = sat_itrs_topo.transform_to(AltAz(obstime=obstime, location=observ_loc))

# 	alt_degs = altaz.alt.dms[0]

# 	# is_over = np.where(alt_degs>10, alt_degs, 0)
# 	# print(is_over.shape)
# 	over_indices = np.nonzero(alt_degs>10)


# 	for i in range(len(over_indices[0])):
# 		s = over_indices[0][i]
# 		t = over_indices[1][i]
# 		sat = all_sats_for_obs_time[s]
# 		sat_area = get_object_area(sat['NORAD_CAT_ID'])
# 		avm = 0
# 		try:
# 			avm = get_avm(observ_loc, itrs_sat[s,t], sat_area, time_list[t])
# 		except:
# 			avm = None
# 		finally:
# 			if sat['NORAD_CAT_ID'] in overhead_sats:
				
# 				overhead_sats[sat['NORAD_CAT_ID']].append({'name':sat['OBJECT_NAME'],'time': time_list[t].isoformat(), 'alt':altaz[s,t].alt.dms, 'az':altaz[s,t].az.dms, 'TLE_LINE1':sat['TLE_LINE1'], 'TLE_LINE2':sat['TLE_LINE2'], 'AVM' : avm})
# 			else:
# 				overhead_sats[sat['NORAD_CAT_ID']] = [{'name':sat['OBJECT_NAME'],'time': time_list[t].isoformat(), 'alt':altaz[s,t].alt.dms, 'az':altaz[s,t].az.dms, 'TLE_LINE1':sat['TLE_LINE1'], 'TLE_LINE2':sat['TLE_LINE2'], 'AVM' : avm}]


# 	return overhead_sats

# def get_sat_itrs(sat_teme, sat_teme_v, observ_time):
# 	'''
# 	@param sat_teme: numpy array containing the TEME position coordinates of the sat as returned from propagate_sats(...)
# 	@param sat_teme_v: numpy array containing the TEME velocity coordinates of the sat as returned from propagate_sats(...)
# 	@param observ_time: datetime.datetime object representing time of observation or astropy Time object
# 	'''

# 	teme_p = CartesianRepresentation(sat_teme*u.km)
# 	teme_v = CartesianDifferential(sat_teme_v*u.km/u.s)
# 	teme = TEME(teme_p.with_differentials(teme_v), obstime=observ_time)
# 	itrs_sat = teme.transform_to(ITRS(obstime=observ_time))

# 	return itrs_sat


# def is_eclipsed(sat_itrs, obs_time):
# 	sat_gcrs = sat_itrs.transform_to(GCRS(obstime=obs_time)).cartesian.without_differentials().xyz.value

# 	solar_system_ephemeris.set('builtin')
# 	sun_gcrs = get_sun(obs_time).cartesian.xyz.to(u.km).value

# 	sat_mag = np.sqrt(np.sum(np.square(sat_gcrs)))
# 	sun_mag = np.sqrt(np.sum(np.square(sun_gcrs)))

# 	sun_sat_angle = np.rad2deg(np.arccos((np.dot(sat_gcrs, sun_gcrs))/(sat_mag * sun_mag)))

# 	sat_earth_vec = sat_itrs.cartesian.without_differentials().xyz.value
# 	sat_earth_mag = np.sqrt(np.sum(np.square(sat_earth_vec)))
# 	earth_radius = 6371.0088
	
# 	max_sat_earth_angle = np.rad2deg(np.arccos(earth_radius/sat_earth_mag)) + 90
# 	print(f'sun sat angle: {sun_sat_angle}, max_sat_earth_angle: {max_sat_earth_angle}')
		
# 	return sun_sat_angle > max_sat_earth_angle

# # def get_cloud_cover(ground_loc, obs_date, periods, delta):
# # 	'''
# # 	@param ground_loc: astropy EarthLocation object representing ground observatory location
# # 	@param obs_date: datetime object of the day of observation (starting time)
# # 	@param periods: the number of time periods to increase the time by delta minutes
# # 	@param delta: the number of minutes in each time period during the desired time range

# # 	@returns: list of percentages by area for cloud cover, for ALL hours in ALL days in the range
# # 	'''

# # 	end_time = obs_date + timedelta(minutes = (periods*delta))
# # 	end_date = end_time.date()
# # 	url = "https://archive-api.open-meteo.com/v1/archive"
# # 	params = {
# # 		"latitude": 42.58,
# # 		"longitude": -71.44,
# # 		"start_date": f'{obs_date.date().isoformat()}',
# # 		"end_date": f'{end_date.isoformat()}',
# # 		"hourly": ["cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"],
# # 		"timezone": "auto"
# # 	}
# # 	responses = openmeteo.weather_api(url, params=params)

# # 	# Process first location. Add a for-loop for multiple locations or weather models
# # 	response = responses[0]
# # 	# Process hourly data. The order of variables needs to be the same as requested.
# # 	hourly = response.Hourly()
# # 	hourly_cloud_cover = hourly.Variables(0).ValuesAsNumpy()
# # 	hourly_cloud_cover_low = hourly.Variables(1).ValuesAsNumpy()
# # 	hourly_cloud_cover_mid = hourly.Variables(2).ValuesAsNumpy()
# # 	hourly_cloud_cover_high = hourly.Variables(3).ValuesAsNumpy()

# # 	return hourly_cloud_cover

# '''
# ########################################################################
# ************************************************************************
# AVM methods
# ************************************************************************
# ########################################################################
# '''
# def get_phase_angle(ground_loc, sat_coords, t):
# 	'''
# 	calculates the phase angle between the sun, observer, and satellite

# 	@param ground_loc: astropy EarthLocation object of the observer's location on earth
# 	@param sat_coords: coordinates of the satellite in ITRS as astropy ITRS object
# 	@param t: datetime time object

# 	@returns: phase angle at observed time in radians
# 	'''
# 	obs_time = Time(t, scale='utc')
# 	#the following are all 1x3 numpy arrays
# 	sat_gcrs = sat_coords.transform_to(GCRS(obstime=obs_time)).cartesian.without_differentials().xyz.value
# 	ground_gcrs = ground_loc.get_gcrs(obs_time).cartesian.without_differentials().xyz.to(u.km).value
# 	solar_system_ephemeris.set('builtin')
# 	sun_gcrs = get_sun(obs_time).cartesian.xyz.to(u.km).value
	
# 	sun_sat_vec = sun_gcrs - sat_gcrs
# 	ground_sat_vec = ground_gcrs - sat_gcrs

# 	sun_sat_mag = np.sqrt(np.sum(np.square(sun_sat_vec)))
# 	ground_sat_mag = np.sqrt(np.sum(np.square(ground_sat_vec)))

# 	sun_sat_unit = sun_sat_vec / sun_sat_mag
# 	ground_sat_unit = ground_sat_vec / ground_sat_mag

# 	phase_angle = (np.arccos(np.dot(sun_sat_unit, ground_sat_unit)))

# 	return phase_angle

# def get_range(ground_loc, sat_coords, observ_time):
# 	'''
# 	calculates the range between the satellite and the observer for the given satellite coordinates

# 	@param ground_loc: astropy EarthLocation object of the observer's location on earth
# 	@param sat_coords: coordinates of the satellite in ITRS as astropy ITRS object
# 	@param observ_time: datetime object of the time of observation

# 	@returns float of the range between observer and sat
# 	'''
# 	o_time = Time(observ_time, scale = 'utc', location = ground_loc)
# 	sat_topo = sat_coords.cartesian.without_differentials() - ground_loc.get_itrs(o_time).cartesian
# 	sat_itrs = ITRS(sat_topo, obstime=observ_time, location=ground_loc)

# 	return np.sqrt(np.sum(np.square(sat_itrs.cartesian.xyz.value)))

# def orientation_correction(phase_angle):
# 	'''
# 	calculates the orientation correction component of apparent visual magnitude
# 	uses the phase factor according to the Molczan method which defines the intrinsic brightness at a 90deg phase angle and 1000km range_los

# 	@param phase_angle: phase angle between sun, observer, and satellite in radians
# 	@returns: float of correction value
# 	'''
# 	pi = np.pi
# 	return -2.5 * np.log10(((pi - phase_angle) * np.cos(phase_angle) + np.sin(phase_angle)))

# def mccant_orientation_correction(phase_angle):
# 	'''
# 	calculates the orientation correction component of apparent visual magnitude
# 	uses the phase factor according to the McCant method which defines the intrinsic brightness at a 0deg phase angle and 1000km range_los

# 	@param phase_angle: phase angle between sun, observer, and satellite in radians
# 	@returns: float of correction value
# 	'''
# 	pi = np.pi
# 	return -2.5 * np.log10((1/pi) * (np.sin(phase_angle) + (pi - phase_angle)*np.cos(phase_angle)))


# def range_correction(range_los):
# 	'''
# 	calculates the range_los correction component of apparent visual magnitude
# 	since intrinsic magnitude is calculated for an object at 1000km range_los, this function is required to adjust its brightness to its actual range_los from the observer

# 	@param range_los: the range_los in km from the observer to the object
# 	@returns: float of correction value
# 	'''

# 	return 5 * np.log10(range_los) - 15

# def get_avm(intrinsic_mag, sat_diameter, range_los, phase_angle):
# 	'''

# 	@param intrinsic_mag: the value of the intrinsic magnitude of the object, M_90 as according to Molczan's method of determining AVM (90deg phase angle 1000km away)
# 	@param sat_diameter: estimated spherical diameter in ???meters???
# 	@param range_los: range_los from the observer to the RSO
# 	@param phase_angle: angle between the sun, RSO, and observer

# 	@returns: the AVM of the RSO
# 	'''
# 	# reflectivity = 0.1 #assumption from the IADC simplification
# 	or_cor = orientation_correction(phase_angle)
# 	range_cor = range_correction(range_los)

# 	return intrinsic_mag + or_cor + range_cor


# def get_mccant_avm(intrinsic_mag, sat_diameter, range_los, phase_angle):
# 	'''
# 	@param intrinsic_mag: the value of the intrinsic magnitude of the object, M_0 as according to McCant's method of determining AVM (0deg phase angle 1000km away)
# 	@param sat_diameter: estimated spherical diameter in ???meters???
# 	@param range_los: range_los from the observer to the RSO
# 	@param phase_angle: angle between the sun, RSO, and observer

# 	@returns: the AVM of the RSO
# 	'''
# 	# reflectivity = 0.1 #assumption from the IADC simplification
# 	or_cor = mccant_orientation_correction(phase_angle)
# 	range_cor = range_correction(range_los)

# 	return intrinsic_mag + or_cor + range_cor


# def sphere_spectral_correction(phase_angle):
# 	'''
# 	calculates correction for the spectral component of reflection off a spherical objct

# 	@param phase_angle: @param phase_angle: angle between the sun, RSO, and observer in radians
# 	@returns: spectral correction value to be used in Hejduk AVM calcs
# 	'''
# 	return (1/(4*np.pi))

# def sphere_diffuse_correction(phase_angle):
# 	'''
# 	calculates correction for the diffuse component of reflection off a spherical objct

# 	@param phase_angle: @param phase_angle: angle between the sun, RSO, and observer in radians
# 	@returns: diffuse correction value to be used in Hejduk AVM calcs
# 	'''
# 	pi = np.pi
# 	# p_rad = np.deg2rad(phase)
# 	term1 = 2.0/(3 * pi**2)
# 	term2 = ((pi - phase_angle) * np.cos(phase_angle)) + np.sin(phase_angle)
# 	return term1 * term2



# def cyl_diffuse_correction(phase_angle):
# 	'''
# 	calculates correction for the diffuse component of reflection off a cylindrical object.  we assume that all cylinders only have diffuse reflection components, and assume that the observation is not during the flash that occurs from their spectral reflectivity 

# 	@param phase_angle: @param phase_angle: angle between the sun, RSO, and observer in radians
# 	@returns: diffuse correction value to be used in Hejduk AVM calcs
# 	'''
# 	pi = np.pi
# 	# p_rad = np.deg2rad(phase)
# 	term1 = 1.0/4.0
# 	term2 = (np.cos(phase_angle/2.0))**2
# 	return term1 * term2

# def plate_diffuse_correction(phase_angle):
# 	'''
# 	calculates correction for the diffuse component of reflection off a flat object.  we assume that all cylinders only have diffuse reflection components, and assume that the observation is not during the flash that occurs from their spectral reflectivity 

# 	@param phase_angle: @param phase_angle: angle between the sun, RSO, and observer in radians
# 	@returns: diffuse correction value to be used in Hejduk AVM calcs
# 	'''
# 	pi = np.pi
# 	# p_rad = np.deg2rad(phase)
# 	term1 = 1.0/pi
# 	term2 = (np.cos(phase_angle/2.0))**2
# 	return term1 * term2

# def get_hejduk_avm(beta_val, sat_area, range_los, phase_angle):
# 	'''
# 	calculates AVM according to Hejduk's model of specular and diffuse components

# 	@param beta_val: float in [0,1] that represents the percent diffuse reflection of the object
# 	@param sat_area: float representing product of object area and albedo/reflectivity
# 	@param range_los: range_los from the observer to the RSO
# 	@param phase_angle: angle between the sun, RSO, and observer in radians

# 	@returns: AVM value
# 	'''
# 	beta_correction = (beta_val * sphere_diffuse_correction(phase_angle)) + ((1 - beta_val) * sphere_spectral_correction(phase_angle))
# 	return -26.74 + (-2.5 * np.log10(sat_area*beta_correction)) + (5 * np.log10(range_los))


# def get_krag_avm(sat_area, range_los, phase_angle):
# 	'''
# 	calculates AVM for the satellite based on Krag (1974) formulations
	
# 	@param sat_area: float representing product of object area and albedo/reflectivity
# 	@param range_los: range_los from the observer to the RSO
# 	@param phase_angle: angle between the sun, RSO, and observer in radians

# 	@returns: AVM value
# 	'''
# 	phase_func = sphere_diffuse_correction(phase_angle)
# 	return -26.78 - 2.5 * np.log10((sat_area * phase_func)/(range_los**2))


# def get_object_area(sat_id):
# 	'''
# 	gets the cross sectional areas of the objects from the DISCOs database.  If the cross sectional area is unavailable, then we assume a size based on object type
# 	'''
# 	try:
# 		return object_sizes[sat_id]['xSectAvg']
# 	except:
# 		return None

# def get_avm(ground_loc, sat_coords, sat_area, obstime, method = 'krag'):
# 	'''
# 	performs calculations to get the brightness (AVM) of the satellite at the desired obstime
# 	@param sat_area: float representing product of object area and albedo/reflectivity
# 	@param ground_loc: astropy EarthLocation object of the observer's location on earth
# 	@param sat_coords: coordinates of the satellite in ITRS as astropy ITRS object
# 	'''

# 	range_los = get_range(ground_loc, sat_coords, obstime)
# 	phase_angle = get_phase_angle(ground_loc, sat_coords, obstime)

# 	if sat_area:
# 		return get_krag_avm(sat_area, range_los, phase_angle)
# 	else:
# 		return None

# 	