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

def get_BC_water_data():

	count = 0;
	BC_hydraulic_fracture = map_to_drive() + "/Project Data/BCOGC/hydraulic_fracture/hydraulic_fracture.csv"
	water_data_headings = []

	timer = time.time()

	print('\n\n========Importing B.C Water Data========')
	print('File Location: ' + BC_hydraulic_fracture)

	water_data = collections.OrderedDict() #Getting data from the csv referenced to well


	with open(BC_hydraulic_fracture) as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == 'WA NUM':
				for i in range(0,len(row)):
					water_data_headings.append(row[i])
					if row[i] == 'UWI':
						well_UWI_index = i 
					WA_NUM_index = row.index('WA NUM')
					
					data_start_count = count
			if count > data_start_count + 1:
				water_data_array = []
				well_WA = row[WA_NUM_index]
				for j in range(0,len(water_data_headings)):
					water_data_array.append(row[j])
				try:
					water_data[well_WA].append(water_data_array)
				except:
					water_data[well_WA] = [water_data_array]

			count = count + 1

	
	print('\n\n====================  Data available   ====================\n')
	print(water_data_headings)
	print('\n')
	print('Computational Time (s): ' + "%.4f" %(time.time() - timer))
	print('\n')

	return water_data_headings, water_data
'''
well_data_headings = get_BC_water_data()[0]
water_data = get_BC_water_data()[1]
count = get_BC_water_data()[2]

BC_well_UWIs = [] 

for well in water_data:
	BC_well_UWIs.append(well)

'''