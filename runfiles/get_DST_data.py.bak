import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import csv
import collections
import pylab
import datetime
import re
import time
from map_to_drive import map_to_drive #path to Project Data folder

def get_DST_data():

	count = 0;
	DST_csv = map_to_drive() +"/Project Data/geoSCOUT_data/post 2005 DST data.csv"

	timer = time.time()

	print('\n\n~~~~~~~~~~~~~~~~~~~~~~\n  IMPORTING DST DATA\n~~~~~~~~~~~~~~~~~~~~~~')
	print('\nFile Location: ' + DST_csv)

	DST_data = collections.OrderedDict() #Getting data from the csv referenced to well
	remove_characters = ['/', '-', ' ']

	count = 0

	with open(DST_csv) as f:
		reader = csv.reader(f)
		for row in reader:
			
			if row[0] == 'Well ID':
				UWI_index = row.index('Well ID')
				DST_headings = row
					
			if row[0] != 'Well ID':
				#well_ID = row[UWI_index]
				well_ID = re.sub("|".join(remove_characters), "", row[UWI_index]) 
				if well_ID not in DST_data:
					DST_data[well_ID] = []
				if well_ID in DST_data:
					DST_data[well_ID].append(row)

			count += 1
			

	
	print('\n\n====================  Data available   ====================\n')
	print('File length; ', count)
	print('Number of wells with DST data; ', len(DST_data))
	print('\n')
	print(DST_headings)
	print('\n')
	print('Computational Time (s): ' + "%.4f" %(time.time() - timer))
	print('\n')

	#for well in DST_data:
	#	print(DST_data[well])

	return DST_data, DST_headings

if __name__ == '__main__':

	from well_search import well_search
	from get_all_post_2005_well_data import get_all_post_2005_well_data
	from DST_analysis import DST_analysis
	from OPGEE_defaults import OPGEE_defaults
	from OPGEE_input_sensitivity import OPGEE_input_sensitivity
	from general_well_data_analysis import OPGEE_well_data

	well_data_headings, well_data, project_name = well_search()
	#well_data_headings, well_data = get_all_post_2005_well_data()

	OPGEE_data = OPGEE_defaults()

	OPGEE_data = OPGEE_well_data(well_data, well_data_headings, OPGEE_data)
	
	DST_data, DST_headings = get_DST_data()

	OPGEE_data = DST_analysis(well_data, well_data_headings, DST_data, DST_headings, OPGEE_data)


	OPGEE_input_sensitivity(OPGEE_data)



