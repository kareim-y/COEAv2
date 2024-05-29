import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import csv
import collections
import pylab
from scipy import stats
import time
from datetime import datetime
import re
from map_to_drive import map_to_drive #path to Project Data folder
	
def get_injection_data(well_data):

	print('\n==========================\n  INJECTION DATA SEARCH \n==========================\n')
	print('Getting injection Data For Selected Wells')
	print('\nData is Loading, May Take a Minute.....\n')

	start_time = time.time()

	injection_data = collections.OrderedDict()
	well_header_data = collections.OrderedDict()
	well_data_headings = []

	count = 0
	count2 = 0;
	init = 0
	switch = 0
	wells_list = []
	file_location = map_to_drive() +"/Project Data/geoSCOUT_data/post 2005 injection.csv"
	remove_characters = ['/', '-', ' ']

	with open(file_location) as f:
		reader = csv.reader(f)
		#row_count = sum(1 for row in reader)
		
		#bar = progressbar.ProgressBar(maxval=row_count).start()

		for row in reader:

			#bar.update(count)
			#count += 1

			if row[0] == 'Unique Well ID':
				well_ID = re.sub("|".join(remove_characters), "", row[1])
				if well_ID[-1] == ')':
					well_ID = well_ID[0:-6] #this is for SK wells which have (0000) on the end for some reason
				in_well = 'no' # we start with each well not being in set until it has been proven
				if well_ID in well_data:
					in_well = 'yes'
					switch = 0
					#injection_data[well_ID].append(well_ID)
					well_header_data[well_ID] = [row[1]]

			if (init == 0 and in_well == 'yes'):
				well_data_headings.append(row[0])

			if (switch == 0 and in_well == 'yes'):
				well_header_data[well_ID].append(row[1])

			if (switch == 1 and in_well == 'yes'):
				try:
					injection_data[well_ID].append(row)
				except:
					injection_data[well_ID] = [row]

			if (row[0] == 'Date' and in_well == 'yes'):
				switch = 1
				init = 1
				injection_data_headings = row 


	print('Computational Time (s): ' + "%.4f" %(time.time() - start_time) + '\n')
	
	for well in injection_data:
		count2 = count2 + 1

	print(str(count2) + ' Of The Selected Wells Have Been Found With Injection Data')
	print('\n')
	#print(get_size(injection_data))
	#print(get_size(well_data))

	time.sleep(5)

	return injection_data_headings, injection_data, well_data_headings, well_header_data 

if __name__ == '__main__':
	
	from well_search import well_search

	well_data_function = well_search()

	well_data_headings = well_data_function[0] 
	well_data = well_data_function[1] 
	#well_data = []

	injection_data_headings, injection_data, well_data_headings, well_header_data = get_injection_data(well_data)

	print(injection_data_headings)