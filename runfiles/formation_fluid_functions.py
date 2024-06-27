#formation_fluid_functions

import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import collections
import pylab
import datetime
import re
import time

from model_inputs import ModelInputs
import pickle

from .return_statistics import histogram, return_statistics, boxplot
from .map_to_drive import map_to_drive #path to Project Data folder

'''
def sum_average_min_max(well_data, well_data_headings, fluid_data, fluid_data_headings, data_type, sum_avg_min_max):

	#fluid data can either be oil or gas data
	#data type eg ''
	#sum average min max returns w

	for well in well data:
		if well in 
'''

def get_fluid_data(fluid_type,well_data,):

	#function will read the data from the fluid analysis extracted from geoSCOUT for formation wells
	#formation must be entered in the following format 'Montney'. 'Viking' etc
	#enter either water, gas or oil for fluid type

	#get appropriate file for 
	if fluid_type.upper() == 'GAS':
		# Kareem Edits
		# file_location = map_to_drive() + "/Project Data/geoSCOUT_data/post 2005 gas_analysis.csv"
		file_location = 'Project Data/geoSCOUT_data/post 2005 gas_analysis.csv'
	#if fluid_type.upper() == 'WATER':
	#	file = formation + '_' + fluid_type + '_analysis.csv' 
	if fluid_type.upper() == 'OIL':
		# Kareem Edits
		# file_location = map_to_drive() + "/Project Data/geoSCOUT_data/post 2005 oil_analysis.csv"
		file_location = 'Project Data/geoSCOUT_data/post 2005 oil_analysis.csv'

	count = 0;
	fluid_data = collections.OrderedDict() #Getting data from the csv referenced to well
	remove_characters = ['/', '-', ' ']
	data_start_count = 100

	# Kareem Edits: added ("r", encoding='windows-1252')
	with open(file_location, "r", encoding='windows-1252') as f:
		reader = csv.reader(f)
		for row in reader:
			if count == 0:
				fluid_data_headings = row
				for i in range(0,len(row)):
					if row[i] == 'Well Identifier':
						well_UWI_index = i 

					data_start_count = count
			
			if count > 0:
				well_ID = re.sub("|".join(remove_characters), "", row[well_UWI_index]) 
				if well_ID in well_data:	
					if well_ID not in fluid_data:
						fluid_data[well_ID] = {} 
					fluid_data[well_ID][row[0]] = row

			count = count + 1


	return fluid_data_headings, fluid_data


def OPGEE_well_gas_data(well_data, gas_header_data, gas_data, OPGEE_data):

	#for now we will use the air free - no idea what the difference is 
	
	index_array = [] 

	for i in range(0,len(gas_header_data)):

		if gas_header_data[i] == 'H2 Air Free':
			H2_index = i
		if gas_header_data[i] == 'He Air Free':
			He_index = i
		if gas_header_data[i] == 'iC4 Air Free':
			ic4_index = i
		if gas_header_data[i] == 'C10 Air Free':
			c10_index = i

	ic4t10_index = list(range(ic4_index, c10_index+2, 2))

	index_array = ic4t10_index

	OPGEE_headings = OPGEE_data['headings']

	for i in range(0,len(OPGEE_headings)):
		
		if OPGEE_headings[i] == 'Gas composition C1':
			C1_index = i

	h2s = []

	for well in gas_data:
		
		sum_check = 0 

		OPGEE_data[well][OPGEE_headings.index('Gas composition C4+')] = 0

		#append with the most recent test data

		recent_test = list(gas_data[well].keys())[-1]
		recent_test_data = gas_data[well][recent_test]

		OPGEE_inputs = []
		gas_data_headings = ['N2 Air Free', 'CO2 Air Free', 'C1 Air Free', 'C2 Air Free', 'C3 Air Free', 'H2S Air Free']
		OPGEE_input_headings = ['Gas composition N2', 'Gas composition CO2', 'Gas composition C1','Gas composition C2','Gas composition C3','Gas composition H2S']

		for i in range(0,len(OPGEE_input_headings)):
			try:
				OPGEE_data[well][OPGEE_headings.index(OPGEE_input_headings[i])] = float(recent_test_data[gas_header_data.index(gas_data_headings[i])])*100
				#print(OPGEE_input_headings[i])
				#print(recent_test_data[gas_header_data.index(gas_data_headings[i])])
			except:
				OPGEE_data[well][OPGEE_headings.index(OPGEE_input_headings[i])] = 0

		#HE and H2 are assumed to be C1

		try:
			#adjust C1 composition to include hydrogen 
			H2 = float(recent_test_data[H2_index])*100
			if H2 > 0:
				OPGEE_data[well][C1_index] = OPGEE_data[well][C1_index] + H2
		except:
			pass

		try:
			#adjust C1 composition to include helium 
			He = float(recent_test_data[He_index])*100
			if He > 0:
				OPGEE_data[well][C1_index] = OPGEE_data[well][C1_index] + He
		except:
			pass

		#c4+

		c4_plus = 0

		for i in range(0,len(index_array)):
			try:
				c4_plus = c4_plus + float(recent_test_data[index_array[i]])*100
			except:
				pass

		OPGEE_data[well][OPGEE_headings.index('Gas composition C4+')] = c4_plus
	

	#for wells without gas data, we want to assign the field average
	for well in well_data:
		if well not in gas_data:
			for i in range(OPGEE_headings.index('Gas composition N2'), OPGEE_headings.index('Gas composition H2S') + 1):
				OPGEE_data[well][i] = OPGEE_data['assessed field'][i]
				#print(well)
				#print(OPGEE_headings[i] + '  ' + str(OPGEE_data['assessed field'][i]))

	#sum check
	for well in well_data:
		sum_ = 0
		for i in range(OPGEE_headings.index('Gas composition N2'), OPGEE_headings.index('Gas composition H2S') + 1):
			sum_ = sum_ + OPGEE_data[well][i]
			#sum check
			#print(well)
			#print(OPGEE_headings[i] + '  ' + str(OPGEE_data[well][i]))
		if sum_ != float(100):
			#some wells are still 0.01 off
			#print(sum_)
			C1 = OPGEE_data[well][OPGEE_headings.index('Gas composition C1')]
			#print(C1)
			C1 = C1 + (100 - sum_)
			#print(C1)
			OPGEE_data[well][OPGEE_headings.index('Gas composition C1')] = C1


		#print(str(sum_) + '\n')


	return OPGEE_data


def OPGEE_well_oil_data(well_data, oil_header_data, oil_data, OPGEE_data):


	api_index = oil_header_data.index('API Reported')
	OPGEE_api_index = OPGEE_data['headings'].index('API gravity')			 

	api_average = OPGEE_data['assessed field'][OPGEE_api_index]

	for well in well_data:

		if well in oil_data:

			well_apis = []

			for test in oil_data[well]:
				api = float(oil_data[well][test][api_index])
				if api > 0:
					well_apis.append(api)

			if len(well_apis) > 0:
				#we have tests with an api reading - we take the average
				OPGEE_data[well][OPGEE_api_index] = np.mean(well_apis)
			elif len(well_apis) == 0:
				#no tests have an api reading - we use the field average 
				OPGEE_data[well][OPGEE_api_index] = api_average
		
			# we will only get the most recent analysis done for each well
			# Note not actually the most recent, just the last added to the gas_data file (e.g could be 3/5 test) 

		if well not in oil_data:
		
			OPGEE_data[well][OPGEE_api_index] = api_average


	return OPGEE_data

def oil_analysis_summary(oil_header_data, oil_data, OPGEE_data):

	# Kareem Edit
	with open('model_input_instance.pkl', 'rb') as f:
		inputs_instance = pickle.load(f)

	index_array = []

	for i in range(0,len(oil_header_data)):
		if oil_header_data[i] == 'API Reported':
			api_index = i
		if oil_header_data[i] == 'Oil Analysis #':
			test_num_index = i


	well_apis = []
	multiple_api_count = 0
	wells_with_oil_data = []

	for well in oil_data:

		test_num = []
		reported_api = []

		for test in oil_data[well]:
			api = float(oil_data[well][test][api_index])
			test = int(test)
			if api > 0: #some are references as zero
				test_num.append(test)
				reported_api.append(api)
				well_apis.append(np.mean(reported_api))
				if well not in wells_with_oil_data:
					wells_with_oil_data.append(well)
		
		if len(test_num) > 1:
			multiple_api_count = multiple_api_count + 1

	print('\n\n ~~~~~~~~~~~~~ OIL DATA ANALYSIS ~~~~~~~~~~~~~~~~\n')
	print(('Number of wells with API measurements; ' + str(len(wells_with_oil_data))))
	print(('Number of Wells with follow-up APIs; ' + str(multiple_api_count)))
	return_statistics(well_apis, 'OIL API GRAVITY')
	print('\n')
	
	# Kareem Edits
	# ask_boxplot = str(input('\n\nWould you like an API boxplot (Y/N)?:   '))
	ask_boxplot = inputs_instance.fluid_boxplot
	print("Chosen input for \'Would you like an API boxplot (Y/N)?\' is", ask_boxplot)

	if ask_boxplot == True:
		boxplot(well_apis, 'OIL API GRAVITY')

	#------------------OPGEE DATA-------------------

	for i in range(0, len(OPGEE_data['headings'])):
		if OPGEE_data['headings'][i] == 'API gravity':
			OPGEE_data['assessed field'][i] = np.mean(well_apis)

	
	#time.sleep(5)

	return OPGEE_data

def gas_analysis_summary(gas_header_data, gas_data, OPGEE_data):
	
	index_array = [] 
	headings = []
	average_gas_data = []

	for i in range(0,len(gas_header_data)):

		if gas_header_data[i] == 'Gas Analysis #':
			test_num_index = i
			index_array.append(i)
		if gas_header_data[i] == 'Gross Heating Value(MJ/m3)':
			HHV_index = i
			index_array.append(i)
		if gas_header_data[i] == 'Net Heating Value(MJ/m3)':
			LHV_index = i 
			index_array.append(i)
		if gas_header_data[i] == 'Relative Density':
			dens_index = i
			index_array.append(i)
		if gas_header_data[i] == 'N2 Air Free':
			N2_index = i
			index_array.append(i)
		if gas_header_data[i] == 'CO2 Air Free':
			h2s_index = i
			index_array.append(i)
		if gas_header_data[i] == 'H2S Air Free':
			co2_index = i
			index_array.append(i)
		if gas_header_data[i] == 'C1 Air Free':
			c1_index = i
			index_array.append(i)
		if gas_header_data[i] == 'C2 Air Free':
			c2_index = i
			index_array.append(i)
		if gas_header_data[i] == 'C3 Air Free':
			c3_index = i
			index_array.append(i)
		if gas_header_data[i] == 'iC4 Air Free':
			ic4_index = i
			index_array.append(i)
		if gas_header_data[i] == 'nC4 Air Free':
			nc4_index = i
			index_array.append(i)
		if gas_header_data[i] == 'iC5 Air Free':
			ic5_index = i
			index_array.append(i)
		if gas_header_data[i] == 'nC5 Air Free':
			nc5_index = i
			index_array.append(i)
		if gas_header_data[i] == 'C6 Air Free':
			c6_index = i
		if gas_header_data[i] == 'C10 Air Free':
			c10_index = i

	c6t10_index = list(range(c6_index, c10_index+2, 2))

	for i in range(0,len(c6t10_index)):
		index_array.append(c6t10_index[i])

	for i in range(0,len(index_array)):
		headings.append(gas_header_data[index_array[i]]) #headings for the reported data we are interested in
		average_gas_data.append([])  # we make an array for each for each of the variables which we will fill with the average from each well 

	multipe_test_count = 0 # count of wells with multiple gas tests 

	for well in gas_data:
		well_data = [] # new array for each well iteration
		for i in range(0,len(headings)):
			well_data.append([]) #wells have multiple entries (follow up reports), we want to calculate the average for each well
		for test in gas_data[well]: #go through all gas data but only get values from out index_array
			for k in range(0,len(index_array)): #each variable of interest index_arrray[k]
				try:
					well_data[k].append(float(gas_data[well][test][index_array[k]]))
				except:
					well_data[k].append(0) #if there is no reported value we put a zero - Note no recorded value doesnt mean that a measurement want taken, just that the composition was zero
		if len(well_data[0]) > 1:
			multipe_test_count = multipe_test_count + 1
		

		for i in range(0, len(well_data)):
			#if np.mean(well_data[i]) != 0: #un-comment this to get a count of non-zero data entries
			average_gas_data[i].append(np.around(np.mean(well_data[i]),decimals=5)) #the average of multiple tests for the same well

	print('\n\n~~~~~~~~~~~~~~ GAS DATA ANALYSIS ~~~~~~~~~~~~~~\n')

	print(('Number of wells with gas analysis data; ' + str(len(average_gas_data[0]))))
	print(('Number of wells with follow-up gas analysis reports; ' + str(multipe_test_count)))
	print('\nAVERAGE OF WELLS\n')

	sum_composition = 0 #sum of the constituents (should be 1 for a single well but will differ for all wells)

	for i in range(0, len(headings)):
		'''
		print('Count of ' + headings[i] + ' = ' + str(len(average_gas_data[i])))
		print('Average of ' + headings[i] + ' = ' + str("%.5f" %np.mean(average_gas_data[i])))
		print('\n')
		'''
		print((headings[i] + ', ' + str("%.5f" %np.mean(average_gas_data[i]))))

		if i > 3:
			sum_composition = sum_composition + np.mean(average_gas_data[i])

	print('\n\n')

	#-------------OPGEE Data-----------
	
	#first calculate c4+

	for i in range(0,len(headings)):
		if headings[i] == 'iC4 Air Free':
			ic4_index = i
		if headings[i] == 'N2 Air Free':
			N2_index = i
		if headings[i] == 'CO2 Air Free':
			co2_index = i
		if headings[i] == 'H2S Air Free':
			H2S_index = i
		if headings[i] == 'C1 Air Free':
			C1_index = i
		if headings[i] == 'C2 Air Free':
			C2_index = i
		if headings[i] == 'C3 Air Free':
			C3_index = i

	c4_plus = 0
	sum_composition2 = 0

	for i in range(ic4_index, len(headings)):
		c4_plus = c4_plus + np.mean(average_gas_data[i])


	#filling in the OPGEE Data

	for i in range(0, len(OPGEE_data['headings'])):
		
		if OPGEE_data['headings'][i] == 'Gas composition N2':
			average_N2 = np.mean(average_gas_data[N2_index])*100
			OPGEE_data['assessed field'][i] = round(average_N2,5)
			sum_composition2 = sum_composition2 + OPGEE_data['assessed field'][i]
		
		if OPGEE_data['headings'][i] == 'Gas composition CO2':
			average_CO2 = np.mean(average_gas_data[co2_index])*100
			OPGEE_data['assessed field'][i] = round(average_CO2,5)
			sum_composition2 = sum_composition2 + OPGEE_data['assessed field'][i]

		if OPGEE_data['headings'][i] == 'Gas composition C2':
			average_C2 = np.mean(average_gas_data[C2_index])*100
			OPGEE_data['assessed field'][i] = round(average_C2,5)
			sum_composition2 = sum_composition2 + OPGEE_data['assessed field'][i]

		if OPGEE_data['headings'][i] == 'Gas composition C3':
			average_C3 = np.mean(average_gas_data[C3_index])*100
			OPGEE_data['assessed field'][i] = round(average_C3,5)
			sum_composition2 = sum_composition2 + OPGEE_data['assessed field'][i]

		if OPGEE_data['headings'][i] == 'Gas composition C4+':
			average_C4 = c4_plus*100
			OPGEE_data['assessed field'][i] = round(average_C4,5)
			sum_composition2 = sum_composition2 + OPGEE_data['assessed field'][i]

		if OPGEE_data['headings'][i] == 'Gas composition H2S':
			average_H2S = np.mean(average_gas_data[H2S_index])*100
			OPGEE_data['assessed field'][i] = round(average_H2S,5)
			sum_composition2 = sum_composition2 + OPGEE_data['assessed field'][i]


	#we need to adjust the methane content to be exactly 1

	#Getting new methane content value
	average_C1 = np.mean(average_gas_data[C1_index])*100
	methane = round(average_C1,5)
	sum_composition2 = sum_composition2 + methane

	if sum_composition2 != 100:
		new_methane = methane + (100 - sum_composition2)


	for i in range(0,len(OPGEE_data['headings'])):
		if OPGEE_data['headings'][i] == 'Gas composition C1':
				OPGEE_data['assessed field'][i] = new_methane
	
	print('OPGEE Requires Gas Components to Sum to Exactly 100%')
	print('We Adjust the Average Field Methane Content to ensure sum is 100%')
	print(('Average C1 content;  ' + str(methane)))
	print(('Adjusted C1 content;  ' + str(new_methane)))
	print(('OPGEE Composition Sum Check;  ' + str(sum_composition2 - methane + new_methane)))

	print('\n\n')

	time.sleep(5)

	return OPGEE_data


if __name__ == '__main__':
	
	from .OPGEE_defaults import OPGEE_defaults
	from .search_production_data import search_production_data
	import collections
	from .well_search import well_search
	from .general_well_data_analysis import OPGEE_well_data, general_well_data_analysis
	from .get_all_post_2005_well_data import get_all_post_2005_well_data
	from .OPGEE_input_sensitivity import OPGEE_input_sensitivity
	from .get_all_post_2005_well_data import get_tight_oil_wells

	#well_data_function = get_montney_trial_well_data() # MONTNEY
	#well_data_function = well_search()
	well_data_function = get_tight_oil_wells()
	#well_data_function = get_all_post_2005_well_data()

	general_well_data_headings = well_data_function[0] # MONTNEY
	general_well_data = well_data_function[1] # MONTNEY
	field_name = 'Montney'

	OPGEE_data = OPGEE_defaults()

	gas_analysis_headings, gas_data  = get_fluid_data('gas', general_well_data)
	oil_analysis_headings, oil_data  = get_fluid_data('oil', general_well_data)

	#OPGEE_data = general_well_data_analysis(general_well_data_headings, general_well_data, OPGEE_data, field_name)

	OPGEE_data = OPGEE_well_data(general_well_data, general_well_data_headings, OPGEE_data)

	OPGEE_data = gas_analysis_summary(gas_analysis_headings, gas_data, OPGEE_data)

	OPGEE_data = oil_analysis_summary(oil_analysis_headings, oil_data, OPGEE_data)

	OPGEE_data = OPGEE_well_gas_data(general_well_data, gas_analysis_headings, gas_data, OPGEE_data)

	OPGEE_data = OPGEE_well_oil_data(general_well_data, oil_analysis_headings, oil_data, OPGEE_data)

	OPGEE_input_sensitivity(OPGEE_data, general_well_data)