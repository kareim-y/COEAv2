#returns all post 2005 well data
import os
import csv
import collections
import time
from datetime import datetime
import re
from map_to_drive import map_to_drive #path to Project Data folder


def get_well_data_from_WA(WA_array):

	print('\nGETTING WELL DATA FROM LIST OF WAs')

	well_data = collections.OrderedDict()
	well_data_headings = []

	wells_list = []
	file_location = map_to_drive() + "Project Data/geoSCOUT_data/post 2005 well data.csv"

	#Searching for wells
	print('\nSearching For Wells...\n')
	timer = time.time()


	with open(file_location) as f:
		reader = csv.reader(f)
		for row in reader:
			
			if row[0] == 'Sort Format Well ID (Long)':
				well_data_headings = row
			if row[0] == 'Lic/WA/WID/Permit #':
				WA_index = i

			if row[0] != 'Sort Format Well ID (Long)':
				
				wellid = row[well_data_headings.index('CPA Well ID')]
				wellWA = row[well_data_headings.index('Lic/WA/WID/Permit #')]
				if wellWA in WA_array:
					wells_list.append(wellid)
					well_data[wellid] = row
				


	print('Computational Time (s): ' + "%.4f" %(time.time() - timer) + '\n')

	print(str(len(wells_list)) + ' Wells Found Meeting Criteria\n')

	return(well_data_headings, well_data)
