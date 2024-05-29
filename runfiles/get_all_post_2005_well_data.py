#returns all post 2005 well data
import os
import csv
import collections
import time
from datetime import datetime
import re

from .map_to_drive import map_to_drive #path to Project Data folder



def get_all_post_2005_well_data():

	print('\nGETTING ALL POST 2005 WELL DATA')
	print('The database was exported from geoSCOUT on 25-Feb-2019')

	well_data = collections.OrderedDict()
	well_data_headings = []

	wells_list = []
	array = []
	#file_location = map_to_drive() + "/Project Data/geoSCOUT_data/weyburn-estevan.csv"
	file_location = map_to_drive() + "Project Data/geoSCOUT_data/Post 2005 well_data.csv"


	#Searching for wells
	print('\nSearching For Wells...\n')
	timer = time.time()


	with open(file_location) as f:
		reader = csv.reader(f)
		for row in reader:
			
			if row[0] == 'Sort Format Well ID (Long)':
				well_data_headings = row
				date_index = row.index('Date Drlg Completed')

			if row[0] != 'Sort Format Well ID (Long)':
				
				year = row[date_index][-4:]
				#print year
				wellid = row[well_data_headings.index('CPA Well ID')]
				if wellid not in well_data:
					try:
						if float(row[well_data_headings.index("Last 12 mo. Total GAS (e3m3)")]) > 200:
							#if year == '2017':
							wells_list.append(wellid)
							well_data[wellid] = row
					except:
						continue

				


	print(('Computational Time (s): ' + "%.4f" %(time.time() - timer) + '\n'))

	print((str(len(wells_list)) + ' Wells Found Meeting Criteria\n'))

	return well_data_headings, well_data 


def get_tight_oil_wells():

	from .emissions_sensitivity import get_all_emission_data

	print('\nGETTING TIGHT OIL DATA - ONLY WELLS PROD > 0.1 bbl/day\n')

	well_data = collections.OrderedDict()
	well_data_headings = []

	wells_list = []
	file_location = map_to_drive() + "/Project Data/geoSCOUT_data/Post 2005 Well Data.csv"

	#Searching for wells
	formation = str(input('Enter the tight oil formation of interest or type all;   '))
	print('\nSearching For Wells...\n')
	timer = time.time()

	emissions_headings, tight_oil_wells = get_all_emission_data()

	with open(file_location) as f:
		reader = csv.reader(f)
		for row in reader:
			
			if row[0] == 'Sort Format Well ID (Long)':
				well_data_headings = row
				date_index = row.index('Date Drlg Completed')

			if row[0] != 'Sort Format Well ID (Long)':
				
				year = row[date_index][-4:]
				#print year
				wellid = row[well_data_headings.index('CPA Well ID')]
				if wellid in tight_oil_wells:
					if formation.upper() == 'ALL':
						#if year in ['2017']:
						well_data[wellid] = row
					elif formation == tight_oil_wells[wellid][emissions_headings.index('Formation')]:
						#if year in ['2017']:
						well_data[wellid] = row
				


	print(('Computational Time (s): ' + "%.4f" %(time.time() - timer) + '\n'))

	print((str(len(well_data)) + ' Wells Found Meeting Criteria\n'))

	time.sleep(5)

	return well_data_headings, well_data

if __name__ == '__main__':
	
	#well_data_headings, well_data  = get_all_post_2005_well_data()

	well_data_headings, well_data  = get_tight_oil_wells()
