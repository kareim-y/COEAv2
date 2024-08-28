import numpy as np
import matplotlib.pyplot as plt
import collections
import datetime
import re
import time
from get_BC_water_data import get_BC_water_data
from get_AB_water_data import get_AB_water_use_data, get_AB_water_source_data
import math

def water_data_sum_average_min_max(water_data, water_data_headings, well_data, well_data_headings, data_type, sum_average_max_min, Alberta_or_BC):

	#this should be flexible to AB and BC water data 
	#data_type = a type of data from BC_water_data - eg 'TOTAL FLUID PUMPED (m3)'
	#sum or average = 'sum' or 'average' or 'max' or 'min' depending on what we want to return
	#the function returns a dictionary of wells and the sum or average of the selected data type

	#get WA's from well data for comparison
	UWI_to_WA = dict()
	WA_to_UWI = dict()	
	sum_average_max_min_dictionary = dict()	


	for well in well_data:
		WA_index = well_data_headings.index('Lic/WA/WID/Permit #')
		WA = well_data[well][WA_index]
		UWI_to_WA[well] = WA
		WA_to_UWI[WA] = well

		#depending on if we are looking at AB or BC water data we want to use WA or UWI
		#BC water data needs WA
		#AB water data needs well UWI 

		if Alberta_or_BC[0].upper() == 'A':
			#we are dealing with alberta data and want the UWI
			well_ID = well[1:-2] + well[-1] # we need to shorten transform 100062505526W502 into 00062505526W52

		if Alberta_or_BC[0].upper() == 'B':
			#we are dealing with BC data so we want WA
			well_ID = UWI_to_WA[well]

		#print(well_ID)

		if well_ID in water_data:
			well_data_array = []

			for completion in range(0,len(water_data[well_ID])):
				data_index = water_data_headings.index(data_type)
				data = water_data[well_ID][completion][data_index]
				try:
					data = float(data)
					if np.isnan(data) != True:
						well_data_array.append(float(data))
				except:
					pass

			if sum_average_max_min.upper() == 'SUM':
				well_water_data = sum(well_data_array)
			elif sum_average_max_min.upper() == 'AVERAGE':
				well_water_data = np.mean(well_data_array)
			elif sum_average_max_min.upper() == 'MIN':
				well_water_data= np.min(well_data_array)
			elif sum_average_max_min.upper() == 'MAX':
				well_water_data = np.max(well_data_array)

			#we want to return a dictionary references to UWI
			sum_average_max_min_dictionary[well] = well_water_data


	return sum_average_max_min_dictionary

if __name__ == '__main__':

	from get_BC_water_data import get_BC_water_data
	from well_search import well_search
	from get_all_post_2005_well_data import get_all_post_2005_well_data

	#water_function = get_BC_water_data()
	water_function = get_AB_water_source_data()
	#water_function = get_AB_water_use_data()

	water_data_headings = water_function[0]
	water_data = water_function[1]

	#well_data_function = get_formation_well_data() # MONTNEY
	well_data_function = well_search()
	#well_data_function = get_all_post_2005_well_data()

	well_data_headings = well_data_function[0] # MONTNEY
	well_data = well_data_function[1] # MONTNEY

	#well_water_data = water_data_sum_average_min_max(water_data, water_data_headings, well_data, well_data_headings,'TOTAL FLUID PUMPED (m3)', 'sum','BC')
	well_water_data = water_data_sum_average_min_max(water_data, water_data_headings, well_data, well_data_headings,'Total Water Volume', 'sum','AB')


	array = []

	for well in well_water_data:
		array.append(well_water_data[well])

	plt.scatter(range(0,len(array)),array)
	plt.show()
	print(len(array))
	print(np.mean(array))
