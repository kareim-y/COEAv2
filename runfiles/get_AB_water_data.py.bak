import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import csv
import collections
import pylab
import datetime
#from mpl_toolkits.basemap import Basemap
import re
from distance_between_coordinates import distance_between_coordinates
#from plot_basemap import plot_basemap
import time 
from map_to_drive import map_to_drive #path to Project Data folder

def get_AB_water_source_data():
	
	AB_HF_WaterSourceData = map_to_drive() +"/Project Data/AER/HF_WaterSourceData.csv"

	timer = time.time()
	print('\n\n========Importing Alberta Water Source Data========')
	print('File Location: ' + str(AB_HF_WaterSourceData))

	count = 0;	
	water_data = collections.OrderedDict() #Getting data from the csv referenced to well
	water_data_headings = []
	remove_characters = ['/', '-', ' ']
	data_start_count = 100

	with open(AB_HF_WaterSourceData) as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == 'Submitter Licencee BA ID':
				for i in range(0,len(row)):
					water_data_headings.append(row[i])
					if row[i] == 'Submitted UWI':
						well_UWI_index = i 

					data_start_count = count
			if count > data_start_count + 1:
				water_data_array = []
				well_ID = re.sub("|".join(remove_characters), "", row[well_UWI_index]) 
				for j in range(0,len(water_data_headings)):
					water_data_array.append(row[j])
				try:
					water_data[well_ID].append(water_data_array)
				except:
					water_data[well_ID] = [water_data_array]

			count = count + 1

	print('\n\n====================  Data available   ====================\n')
	print(water_data_headings)
	print('\n\n') 
	print('Computational Time (s): ' + "%.4f" %(time.time() - timer))


	return water_data_headings, water_data


def get_AB_water_use_data():

	AB_HF_WaterUseData = map_to_drive() +"/Project Data/AER/HF_WaterUseData.csv"

	timer = time.time()
	print('\n\nImporting Alberta Water Use Data')
	print('File Location: ' + AB_HF_WaterUseData)

	water_data = collections.OrderedDict() #Getting data from the csv referenced to well
	remove_characters = ['/', '-', ' ']
	switch = 0
	water_use_data = collections.OrderedDict()

	with open(AB_HF_WaterUseData) as f:
		reader = csv.reader(f)

		for row in reader:
			
			if row[0] == 'Well Licence Number':
				water_use_headings = row
				UWI_index = row.index('UWI')
			
			if switch == 1:
				UWI = re.sub("|".join(remove_characters), "", row[UWI_index])
				if UWI not in water_use_data:
					water_use_data[UWI] = []
				water_use_data[UWI].append(row)

			if row[0] == '-------------------':
				#our data starts on the next rown
				switch = 1
				
	print('\n\n====================  Data available   ====================\n')
	print(water_use_headings)
	print('\n\n') 
	print('Computational Time (s): ' + "%.4f" %(time.time() - timer))
	

	return water_use_headings, water_use_data


def AB_water_source_plotter(water_data_headings, water_data, formation_well_headings, formation_well_data):


	m = plot_basemap()
	
	plotted_well_count = 0
	water_source_count = 0
	count = 0
	distances = [] 

	for i in range(0,len(formation_well_headings)):
		if formation_well_headings[i] == 'Surf-Hole Latitude (NAD83)':
			well_latitude_index = i
		if formation_well_headings[i] == 'Surf-Hole Longitude (NAD83)':
			well_longitude_index = i

	for i in range(0,len(water_data_headings)):
		if water_data_headings[i] == 'Water Source Latitude':
			water_latitude_index = i
		if water_data_headings[i] == 'Water Source Longitude':
			water_longitude_index = i
		if water_data_headings[i] == 'Water Source Type':
			water_type_index = i

	for well in formation_well_data:
		adj_well = str(well[1:-1])
		try:	#not all formation wells have water data, only want those that do
			water_use = water_data[adj_well]	
			plotted_well_count = plotted_well_count + 1
			for i in range(0,len(water_use)):
				water_latitude = float(water_use[i][water_latitude_index])
				water_longitude = float(water_use[i][water_longitude_index])
				well_latitude = float(formation_well_data[well][well_latitude_index][0:-1])
				well_longitude = -float(formation_well_data[well][well_longitude_index][0:-1])
				x1, y1 = [water_longitude,water_latitude]
				x2, y2 = [well_longitude,well_latitude]
				water_location = [water_longitude,water_latitude]
				well_location = [well_longitude,well_latitude]
				water_colour = 'red'
				well_colour = 'blue'
				plt.plot(x1, y1, 'ok', markersize=0.2, color=water_colour)
				plt.plot(x2, y2, 'ok', markersize=0.2, color=well_colour)
				water_source_count = water_source_count + 1
				#calculating distances between the water source and well
				#THHIS IS WRONG!!! USE MPU!!
				distance = distance_between_coordinates(water_location, well_location)
				distances.append(distance)

		except:
			pass

	print('\n')
	print('Number of Albertan Montney Wells Plotted: ' + str(plotted_well_count))
	print('Number of different water sources: ' + str(water_source_count))
	print('Mean distance from water source to well: ' + str("%2f" %np.mean(distances)))
	print('Meadian distance from water source to well: ' + str("%2f" %np.median(distances)))
	print('Std dev of distance from water source to well: ' + str("%2f" %np.std(distances)))
	print('Maximum distance from water source to well: ' + str("%2f" %np.max(distances)))
	plt.show()
	
	return



'''
well_data_headings = get_AB_water_data()[0]
water_data = get_AB_water_data()[1]
count = get_AB_water_data()[2]

#---------------------------General Info about data------------------------------

Alberta_well_UWIs = [] 

for well in water_data:
	Alberta_well_UWIs.append(well)

'''

if __name__ == '__main__':

	AB_water_use_headings, AB_water_use_data =  get_AB_water_use_data()
	print(AB_water_use_headings)
	print(len(AB_water_use_data))