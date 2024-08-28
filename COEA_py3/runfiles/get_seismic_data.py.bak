import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import csv
import collections
import pylab
import datetime
from mpl_toolkits.basemap import Basemap
import re
import time
from map_to_drive import map_to_drive #path to Project Data folder 

def get_NRC_seismic_data():

	count = 0;
	seismic_file = map_to_drive() +"/Project Data/NRC (EarthQuakes)/EarthQuakes (2008-2018).csv"
	
	timer = time.time()
	print('\n========Importing Seismic Data========')
	print('Getting Seismic Data from Natural Resources Canada\n')
	print('File Location: ' + str(seismic_file))


	seismic_data = collections.OrderedDict() #Getting data from the csv referenced to well
	seismic_data_headings = []
	remove_characters = ['/', '-', ' ']
	data_start_count = 100
	index_count = 0 #all events will be references to a count variable (we dont have a well name or anything)



	with open(seismic_file) as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == 'Date':
				for i in range(0,len(row)):
					seismic_data_headings.append(row[i])

					data_start_count = count
			if count > data_start_count + 1:
				seismic_data[index_count] = row
				index_count = index_count + 1
			
			count = count + 1
			

	print('\n====================  Data available   ====================\n')
	print(seismic_data_headings)
	print('\n\n') 
	print('Computational Time (s): ' + "%.4f" %(time.time() - timer))

	return seismic_data_headings, seismic_data

def get_CISC_seismic_data():

	file_location = map_to_drive() +"/Project Data/Canadian_Induced_Seismicity_Collaboration/AlbertaCompCat2018-09.txt"

	print('\n========Importing Seismic Data========')
	print('Getting Seismic Data from the Canadian Induced Seismicity Collaboration\n')
	print('File Location: ' + str(file_location))
	print('\n')

	from datetime import datetime

	seismic_data = collections.OrderedDict()

	with open(file_location, 'r') as myfile:
		data = myfile.readlines()
		
		count = 0

		for row in data:
			#print(row.split(' '))
			row_data = [x for x in row.split() if len(x) > 0] #remove spaces 
			if count == 0:
				seismic_data_headings = row_data
			if count != 0:
				event_date = row_data[0]+ ' ' +row_data[1] + ' ' + row_data[2] #YYYY MM DD
				event_date =  datetime.strptime(event_date, '%Y %m %d')
				seismic_data[event_date] = row_data

			#if count == 2:
			#	print(seismic_data_headings)
			#	print(seismic_data)
			#	break 

			count += 1

	#print(count)

	return seismic_data_headings , seismic_data 

def get_updated_NRC_seismic_data():

	count = 0;
	seismic_file = map_to_drive() +"/Project Data/NRC (EarthQuakes)/EarthQuakes_new (2008-2018).csv"
	
	timer = time.time()
	print('\n========Importing Seismic Data========')
	print('Getting Seismic Data from Natural Resources Canada (updated version 20-June-19)')
	print('Events with Mag > 2 over the period 2008-2018')
	print('File Location: ' + str(seismic_file))


	seismic_data = collections.OrderedDict() #Getting data from the csv referenced to well
	seismic_data_headings = []
	remove_characters = ['/', '-', ' ']
	data_start_count = 100
	index_count = 0 #all events will be references to a count variable (we dont have a well name or anything)



	with open(seismic_file) as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == '#EventID':
				seismic_data_headings = row		
			elif row[0] != '#EventID':
				seismic_data[index_count] = row
				index_count = index_count + 1
			
			count = count + 1
			

	print('\n====================  Data available   ====================\n')
	print('Number of Seismic Events in database: ' + str(index_count))
	print('\n') 
	print(seismic_data_headings)
	print('\n') 
	print('Computational Time (s): ' + "%.4f" %(time.time() - timer))

	return seismic_data_headings, seismic_data



if __name__ == '__main__':
	
	get_CISC_seismic_data()
