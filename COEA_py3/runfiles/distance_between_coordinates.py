#distance_between_coordinates

from math import sin, cos, sqrt, atan2, radians

def distance_between_coordinates(location1, location2):	

	#takes in [lon,lat],[lon,lat]
	# approximate radius of earth in km
	R = 6373.0

	lon1 = radians(location1[0])
	lat1 = radians(location1[1])
	lon2 = radians(location2[0])
	lat2 = radians(location2[1])
	

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

	return distance 


