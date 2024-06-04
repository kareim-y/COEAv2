#well search
#the file searches through the general well data from the file post 2005 well data
#and returns data based on search criteria 

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
import webbrowser
import subprocess
from .map_to_drive import map_to_drive #path to Project Data folder

import chardet


def introduction():

	#explaination of module:
	print('\n=========================\n WELL SELECTION MODULE \n=========================\n')
	print('Begin by selecting the set of wells for assessment')
	print('The database was exported from geoSCOUT in Jan-2020')
	print('Some of the most recent data may be missing through confidentiality. For example see;')
	print('https://geologicsystems.wordpress.com/2011/03/28/when-data-is-released-on-confidential-wells/\n')
	print('Current Available Search Criteria for Selecting Wells: \n')
	print('Drilled Between (Start and End Date)')
	print('Production/Injection Formation Name')
	print('Horizontal Well (True/False)')
	print('Gas oil ratio (GOR) range (m3/m3)\n')



def well_search():
	
	introduction()

	project_name = str(input('Firstly, what would you like to name the Project?   '))
	print('\n')

	start_time = time.time()


	well_data = collections.OrderedDict()
	well_data_headings = []

	count = 0;
	wells_list = []

	#file_location = map_to_drive() + "Project Data/geoSCOUT_data/Canadian_LNG_well_data.csv"
	#The main one

	#Kareem Edit
	#old code
	# file_location = map_to_drive() + "Project Data/geoSCOUT_data/post 2005 well_data.csv" 

	#new code
	file_location = "Project Data/geoSCOUT_data/post 2005 well_data.csv"
	#end

	with open(file_location, "r", encoding='windows-1252') as f:
		# Kareem edit
		# result = chardet.detect(f.read())
		# print(result['encoding'])
		reader = csv.reader(f)
		for row in reader:
			if row[0] == 'Sort Format Well ID (Long)':
				well_data_headings = row
				break

			count = count + 1

	#this is a list of potential search parameters 
	#print(well_data_headings)

	#start with three selection criteria

	#Get date limits
	date_min = str(input('Enter a Drilled After Date (DD/MM/YYYY): '))
	date_min = datetime.strptime(date_min, '%d/%m/%Y')
	date_max = str(input('Enter a Drilled Before Date (DD/MM/YYYY): '))
	date_max = datetime.strptime(date_max, '%d/%m/%Y')

	#get province of interest
	provinces =  str(input('Enter provinces of Interest (separate by , ). AB,BC and SK available;  '))
	provinces = re.sub(' ', '', provinces)
	provinces = provinces.split(',')
	#Get formations of Interest
	
	tight_formations = ['Mbakken_M', 'Dtorquay', 'D3_forks', 'Dbvrhl_lk', 'Dswan_hl', 'Kcard_ss', 'TRchly_lk', 'TRbndrylk', 'Kdunvegan', 'Dduvernay', 'Jshaunv_L', 'TRmontney', 'TRdoig', 'Mpekisko', 'Dslave_pt', 'Kvik_ss'] #, 'Kbelly_rv'

	#formations
	formations = 'SEARCH'
	while formations.upper() == 'SEARCH':
		formations = str(input('Enter formations of Interest (separate by , ). Type "Search" for a complete list of formations;  '))
		if formations.upper() == 'SEARCH':
			# Kareem Edits
			# webbrowser.open("runfiles/list_of_producing_formations.txt")
			subprocess.run(["open", "runfiles/list_of_producing_formations.txt"])


	formations = re.sub(' ', '', formations)
	formations = formations.split(',')

	if formations[0].upper() == 'TIGHTOIL':
		formations = tight_formations

	#Horizontal Well? Condition for tight oil
	
	horizontal_TF = str(input('Horizontal Well? (True, False or Both): '))
	horizontal_TF = horizontal_TF[0].upper()
	if horizontal_TF == 'B':
		horizontal_TF = ['T','F']
	else:
		horizontal_TF = [horizontal_TF]

	#GOR Conditions

	min_GOR= float(input('Enter a Minimum First 12 month Ave GOR (m3/m3):  '))
	max_GOR= float(input('Enter a Maximum First 12 month Ave GOR (m3/m3):  '))

	if len(str(max_GOR)) == 0:
		max_GOR = 100000000000

	if len(str(min_GOR)) == 0:
		min_GOR = 0

	all_formations = [] #used temporarily to get a list of all formations
	



	#Searching for wells
	print('\nSearching For Wells...\n')
	timer = time.time()
	temporary_dict = collections.Counter()

	# Kareem Edits: changed the open() function, adding, ("r", encoding='windows-1252')
	with open(file_location, "r", encoding='windows-1252') as f:
		reader = csv.reader(f)
		for row in reader:
			
			if row[0] == 'Sort Format Well ID (Long)':
				well_data_headings = row

			if row[0] != 'Sort Format Well ID (Long)':
				
				#date = row[well_data_headings.index('Date Drlg Completed')]
				date = row[well_data_headings.index('Date Well Spudded')]
				horizontal = row[well_data_headings.index('Horizontal Hole (T/F)')]
				wellid = row[well_data_headings.index('CPA Well ID')]
				formation = row[well_data_headings.index('Prod./Inject. Frmtn')]
				province = row[well_data_headings.index('Area')]
				company = row[well_data_headings.index('Cur Operator Name')]
				producing_unit = row[well_data_headings.index('Producing Unit Name')] #producing unit name
				field_name = row[well_data_headings.index('Producing Field/Area Name')]
				most_recent_GOR = row[well_data_headings.index('Most Recent 12 mo. Ave GOR (m3/m3)')]
				first_12_gas = row[well_data_headings.index('First 12 mo. Total GAS (e3m3)')]
				#formation = field_name # this will search the companies entered as fomrations

				'''
				#select from list
				if wellid in ['100013403924W400','102113603924W400','102060104024W400','103160204024W400','100010304024W400']:
					wells_list.append(wellid)
					well_data[wellid] = row
				'''

				try:
					GOR = float(row[well_data_headings.index('First 12 mo. Ave GOR (m3/m3)')])
					#if GOR == 0:
					#	if float(first_12_gas) == 0:
					#		GOR = float(most_recent_GOR)
				except:
					GOR = -1
				
				#(field_name in ['NORTHERN MONTNEY']) and \
				#(field_name in ['HERITAGE']) and \
				#(field_name in ['WASKAHIGAN']) and \
				#date_format = '%Y/%m/%d'
				date_format = '%m/%d/%Y'
				if len(date) > 1:
					if (date_min < datetime.strptime(date, date_format) < date_max) and \
						(horizontal in horizontal_TF) and \
						(min_GOR <= GOR <= max_GOR) and \
						(province in provinces):
						for wanted_formation in formations:
							if wanted_formation in formation:
								if wellid not in wells_list:
									wells_list.append(wellid)
									well_data[wellid] = row
									#temporary_dict[formation] += 1
									temporary_dict[field_name] +=1
									#print(wellid)
									#print(len(wells_list))



	print(('Computational Time (s): ' + "%.4f" %(time.time() - timer) + '\n'))

	print(('Project Name: ' + project_name))
	print((str(len(wells_list)) + ' Project Wells Found Meeting Criteria\n\n'))
	

	time.sleep(5)

	for key in temporary_dict:
		print((key, temporary_dict[key]))

	return well_data_headings, well_data, project_name 


if __name__ == '__main__':

	well_data_headings, well_data, project_name = well_search()

	