import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import csv
import collections
import pylab
from scipy import stats
import math

from .return_statistics import return_statistics, histogram
from .well_plotter import well_plotter, get_well_coordinates

#def data_type_and_count()


def general_well_data_analysis(header_data, well_data, OPGEE_data, field_name):


	well_count = 0

	for i in range(0,len(header_data)):
		if header_data[i] == 'CPA Well ID':
			ID_index = i
		if header_data[i] == 'Area':
			area_index = i
		#if header_data[i] == 'Date Drlg Completed':
		if header_data[i] == 'Date Well Spudded':
			date_index = i
		if header_data[i] == 'TVD (m)':
			TVD_index = i
		if header_data[i] == 'Prod./Inject. Frmtn':
			formation_index = i
		if header_data[i] == 'Production-Casing Size (mm)':
			prod_casing_index = i
		if header_data[i] == 'Intermediate-Casing Size (mm)':
			int_casing_index = i
		if header_data[i] == 'Liner-Casing Size (mm)':
			liner_casing_index = i
		if header_data[i] == 'BH Temp. (degC)':
			temp_index = i
		if header_data[i] == 'First Prod YYYY/MM':
			start_prod_index = i
		if header_data[i] == 'Last Prod. YYYY/MM':
			last_prod_index = i
		if header_data[i] == 'BotHole N/S Distance (m)':
			BH_NS_dist_index = i
		if header_data[i] == 'BotHole E/W Distance (m)':
			BH_EW_dist_index = i
		if header_data[i] == 'Horizontal Hole (T/F)':
			Horizontal_TF_index = i
		if header_data[i] == 'Well Status Text':
			well_status_index = i
		if header_data[i] == 'First 12 mo. Ave GOR (m3/m3)':
			GOR_index = i

	#initially set OPGEE to defaults

	# Area, Year and Formation Count

	drill_year_counter = collections.Counter()
	province_counter = collections.Counter()
	zone_wells = collections.Counter()
	producing_wells = []
	formations = []
	formation_counter = collections.Counter()
	well_depths = [] # an array of well depths 
	min_casing = [] #an array of the smallest casing sizes for each well 
	formation_temps = [] #array of formation temperatures
	formation_temp_depths = [] #array of depths for each temperature 
	well_type_counter = collections.Counter()
	no_data_count = 0
	horizontal_length_array = [] #array of ho
	count = 0

	for well in well_data:
		
		#province count
		province = well_data[well][area_index]
		province_counter[province] += 1

		#producing formation count
		formation = well_data[well][formation_index]
		formation_counter[formation] += 1

		#year count
		try:
			year = int(well_data[well][date_index][-4:])
			#print(well_data[well][date_index], well)
		except:
			#print(well_data[well][date_index], well)
			year = int(well_data[well][date_index][0:4])
		
		drill_year_counter[year] += 1

		#Well type and count - eg Pump Gas
		well_type = well_data[well][well_status_index]
		well_type_counter[well_type] += 1

		#well zonation count
		zone_criteria = ['GOR = 0 or > 17800 ', '1780 < GOR =< 17800','267 < GOR =< 1780', 'GOR =< 267']
		
		try:
			GOR = float(well_data[well][GOR_index])
		except:
			GOR = 'NA'
		#GOR = 1

		if (GOR == 0 or GOR > 17800):
			zone_wells['Dry Gas'] += 1
		elif (1780 < GOR <= 17800):
			zone_wells['Condensate'] += 1
		elif (267 < GOR <= 1780):
			zone_wells['Volitile Oil'] += 1
		elif (0 < GOR <= 267):
			zone_wells['Black Oil'] += 1
		else:
			zone_wells['NA'] += 1
		# Formation Depths
		try:
			well_depths.append(float(well_data[well][TVD_index]))
		except:
			pass

		# Producing Wells
		if len(well_data[well][start_prod_index]) > 0:
			producing_wells.append(well)
		
		# Horizontal length
		
		if well_data[well][Horizontal_TF_index] == 'T':
			try:
				NS_length =float(well_data[well][BH_NS_dist_index])
				EW_length = float(well_data[well][BH_EW_dist_index])
				horizontal_length = math.sqrt(NS_length**2 + EW_length**2)
				horizontal_length_array.append(horizontal_length)
			except:
				pass


		#--------------formation Temperatures------------------
		min_temp = 0 # remove temps under this number for imporved fit, set to zero to include all

		try:
			temp = float(well_data[well][temp_index])
			depth = well_data[well][TVD_index]
			if (temp > min_temp and len(depth) >0): #this will only include wells with both a temperature and a depth
				formation_temps.append(temp) #get temp data if it exists
				formation_temp_depths.append(float(depth))
		
		except:
			pass

		
		#-----------Casing size ----------------------
		#gets the smallest casing for every well comparing - production, liner, inermedaite
		min_size = 100000
		casing_data = 'NO' #if the well hs casing data change to yes 
		casing_array = [] #array of sizes for each casing 
		casing_array.append(well_data[well][prod_casing_index])
		casing_array.append(well_data[well][int_casing_index])
		casing_array.append(well_data[well][liner_casing_index])
		count = count + 1
		
		for i in range(0, len(casing_array)):
			try:
				casing_array[i] = float(casing_array[i])
				if casing_array[i] < min_size:
					min_size = casing_array[i]
			except:
				pass
		if min_size < 100000:
			min_casing.append(min_size)
		if casing_array.count('') == 3:
			no_data_count = no_data_count + 1



	
	#--------------------Summary Print------------------

	print('\n~~~~~~~~ GENERAL DATA SUMMARY ~~~~~~~~~\n')
	print('General Data Taken from GeoScout')
	print(('Number of wells drilled in target formation: ' + str(well_count)))
	print(('The Number of Wells Having Produced in Some Period: ' + str(len(producing_wells))))
	print(('The average well depth (m) for the ' + str(len(well_depths)) + ' wells with reported TVD data: ' + str("%.2f" %np.mean(well_depths))))
	print('\n')
	print('Provinces wells are drilled in and the count')
	for prov in sorted(province_counter.keys()):
		print((prov + ';' + str(province_counter[prov])))
	print('\n')
	print('Producing formation and producing formation count')
	for form in sorted(formation_counter.keys()):
		print((form + ';' + str(formation_counter[form])))
	print('\n')
	print('Year wells have been drilled and count')
	for year in sorted(drill_year_counter.keys()):
		print((str(year) + ';' + str(drill_year_counter[year])))
	print('\n')
	print('Well Type/Status and Count')
	for well_type in sorted(well_type_counter.keys()):
		print((well_type + ';' + str(well_type_counter[well_type])))
	print('\n')
	print('Zoning By First Year Average GOR (m3m3)')
	print(zone_criteria)
	for zone in sorted(zone_wells.keys()):
		print((zone + ';' + str(zone_wells[zone])))

	#---------------------TVD Statistics--------------
	#print(well_depths)
	return_statistics(well_depths, 'True Vertical Depth')
	#histogram(well_depths, 'True Vertical Depth')

	#3D plot in future would look sick
	#https://stackoverflow.com/questions/37478460/add-background-image-to-3d-plot
	#https://stackoverflow.com/questions/23785408/3d-cartopy-similar-to-matplotlib-basemap
	
	#-----------------Plot of TVD's-----------------
	'''
	x = range(0,len(well_depths))
	plt.scatter(x,well_depths, s = 0.5)
	plt.xlabel('Well Count')
	plt.ylabel('TVD (m)')
	plt.ylim(ymin = 0)
	plt.title('Distribution of TVD for Formation Wells')
	plt.show()
	'''
	#------------------Horizontal Lenght------------------
	#print('\nHorizontal Well Length')
	return_statistics(horizontal_length_array, 'Horizontal Well Length')
	#print([round(x,1) for x in horizontal_length_array])
	#histogram(horizontal_length_array, 'Horizontal Well Length')


	#---------------------Casing Statistics--------------
	
	return_statistics(min_casing, 'Prod Casing')
	#histogram(min_casing, 'Prod Casing')

	print(('The number of wells with either intermediate liner or production casing data; ' + str(len(min_casing))))
	print(('The number of wells with no casing data; ' + str(no_data_count)))
	print(('Total count check; ' + str(len(min_casing) + no_data_count)))
	print('\n')

	#---------------------Temperature Data --------------	
	return_statistics(formation_temps, 'Formation Temperature')
	#histogram(formation_temps, 'Formation Temperature')


	if min_temp > 21:
		print(('Outliers have been removed - temperatures under ' + str(min_temp) + ' degrees'))

	#--------------------Plot of Temp vs Depth--------------
	if len(formation_temps) > 0:

		#we want to add 15 degrees at a depth of 0 ft
		#formation_temps.append(15)
		#formation_temp_depths.append(0)
		'''

		plt.scatter(formation_temp_depths, formation_temps, s = 1, color = 'r')
		plt.ylabel('Temperature (Celcius)')
		plt.ylim(ymin = 0)
		plt.xlim(xmin = 0)
		plt.xlabel('TVD (m)')
		plt.title('Temperature vs Depth')
		'''
		
		#----------------Linear Trendline and Fit ---------------------
		linear = np.polyfit(formation_temp_depths,formation_temps,1)
		print(('Linear Equation; Temperature (C) = ' + str("%.5f" %linear[0]) + '*TVD (m) + ' + str("%.2f" %linear[1])))
		stat = stats.linregress(formation_temp_depths, formation_temps)
		#slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
		
		slope = stat[0]
		intercept = stat[1]
		r_value = stat[2]

		print(('Slope; ' + str(stat[0])))
		print(('Intercept; ' + str(stat[1])))
		print(('r_value; ' + str(stat[2])))
		print(('p_value; ' + str(stat[3])))
		print(('std_err; ' + str(stat[4])))
		print('\n')

	if len(formation_temps) == 0:
		#we have no correlation for temp
		r_value = 0
	#plt.show()

	#-------------OPGEE Field Averages-----------------

	mtoft = 3.28084
	mm_inch = 0.0393701

	#we want to fill in the data for the whole field of interest (assessed field)


	for i in range(0, len(OPGEE_data['headings'])):

		if OPGEE_data['headings'][i] == 'Field name':
			OPGEE_data['assessed field'][i] = field_name

		#if OPGEE_data['headings'][i] == 'Field age':
			#OPGEE_data['assessed field'][i] = end_year - start_year 
			#we adjust this in the production_analysis sheet to be the 'producing age'

		if OPGEE_data['headings'][i] == 'Field depth':
			OPGEE_data['assessed field'][i] = np.around(np.mean(well_depths)*mtoft, decimals = 3)

		if OPGEE_data['headings'][i] == 'Production tubing diameter':
			OPGEE_data['assessed field'][i] = round(np.median(min_casing)*mm_inch,1)

		if OPGEE_data['headings'][i] == 'Reservoir pressure':
			#For now assume water gradient
			OPGEE_data['assessed field'][i] = np.around(np.mean(well_depths)*mtoft*0.45,decimals = 3)
		
		if OPGEE_data['headings'][i] == 'Reservoir temperature':
			#using the equation if r^2 > 0.75
			if r_value >= 0.75:
				OPGEE_data['assessed field'][i] = np.around((float(9)/5)*(slope*(np.mean(well_depths)) + intercept) + 32,decimals = 3)
			if r_value < 0.75:
				OPGEE_data['assessed field'][i] = np.around((float(9)/5)*np.mean(formation_temps) + 32,2)
			if r_value == 0:
				#assume 15 F/1000 ft normal temp gradient
				OPGEE_data['assessed field'][i] = np.mean(well_depths)*mtoft*(float(15)/1000) + 60

		if OPGEE_data['headings'][i] == 'Length of lateral':
			OPGEE_data['assessed field'][i] = np.mean(horizontal_length_array)*mtoft

		if OPGEE_data['headings'][i] == 'Fraction of wells fractured':
			OPGEE_data['assessed field'][i] = 1

	return OPGEE_data	

def OPGEE_well_data(well_data, well_data_headings, OPGEE_data):

	mtoft = 3.28084
	mm_inch = 0.0393701


	for well in well_data:
	
		OPGEE_data[well] = [] #initialize well_data
		OPGEE_headings = OPGEE_data['headings']

		#add coordinated of wells 
		lat_lon = get_well_coordinates(well_data, well_data_headings, well)
		#OPGEE_data[well][OPGEE_data['headings'].index('Coordinates')] = str(lat_lon)
		
		for i in range(0,len(OPGEE_headings)):
			field_av = OPGEE_data['assessed field'][i]
			OPGEE_data[well].append(field_av)

			if OPGEE_headings[i] == 'Field name':
				OPGEE_data[well][i] = well

			if OPGEE_headings[i] == 'Field age':
				
				try:
					start_year = int(well_data[well][well_data_headings.index('First Prod YYYY/MM')][0:4])
					start_month = int(well_data[well][well_data_headings.index('First Prod YYYY/MM')][-2:])
					end_year = int(well_data[well][well_data_headings.index('Last Prod. YYYY/MM')][0:4])
					end_month = int(well_data[well][well_data_headings.index('Last Prod. YYYY/MM')][-2:])
					years_between = float(end_year - start_year) + (float(end_month - start_month))/12
					OPGEE_data[well][i] = years_between
				except:
					pass

			if OPGEE_headings[i] == 'Field depth':
				try:
					OPGEE_data[well][i] = float(well_data[well][well_data_headings.index('TVD (m)')])*mtoft
				except:
					pass

			if OPGEE_headings[i] == 'Production tubing diameter':
				#just look for prod casing
				try:
					OPGEE_data[well][i] = round(float(well_data[well][well_data_headings.index('Production-Casing Size (mm)')])*mm_inch,1)
				except:
					pass

			if OPGEE_headings[i] == 'Reservoir pressure':
				#For now assume water gradient
				try:
					OPGEE_data[well][i] = float(well_data[well][well_data_headings.index('TVD (m)')])*mtoft*0.45
				except:
					pass

			if OPGEE_headings[i] == 'Reservoir temperature':
				#using the equation
				try:
					OPGEE_data[well][i] = (float(9)/5)*float(well_data[well][well_data_headings.index('BH Temp. (degC)')]) + 32
				except:
					try:
						OPGEE_data[well][i] = round(float(well_data[well][well_data_headings.index('TVD (m)')])*mtoft*(float(15)/1000) + 60,2) 
						#print(OPGEE_data[well][i])
					except:
						pass

			if OPGEE_headings[i] == 'Formation':
				OPGEE_data[well][i] = well_data[well][well_data_headings.index('Prod./Inject. Frmtn')]

			if OPGEE_headings[i] == 'Province':
				OPGEE_data[well][i] = well_data[well][well_data_headings.index('Area')]

			if OPGEE_headings[i] == 'Area':
				OPGEE_data[well][i] = OPGEE_data[well][i] = well_data[well][well_data_headings.index('Producing Field/Area Name')]
						
					
					
	return OPGEE_data
	
	



if __name__ == '__main__':


	from .well_search import well_search
	from .OPGEE_defaults import OPGEE_defaults

	#MONTNEYY ONLY!!!!!
	print('Importing General Well Data') #MONTNEY
	#well_data_function = get_montney_trial_well_data() # MONTNEY
	well_data_function = well_search()
	well_data_headings = well_data_function[0] # MONTNEY
	well_data = well_data_function[1] # MONTNEY
	field_name = 'Montney'

	OPGEE_data = OPGEE_defaults()

	#-------------------------General Data Analysis------------------------

	OPGEE_data = general_well_data_analysis(well_data_headings, well_data, OPGEE_data, field_name)
	OPGEE_data = OPGEE_well_data(well_data, well_data_headings, OPGEE_data)

	'''

	print(OPGEE_data['headings'])
	print('\n')
	print(OPGEE_data['defaults'])
	print('\n')
	for well in OPGEE_data:

		print well
	
	for i in range(0,len(OPGEE_data['200a041J094H0802'])):
		print(str(OPGEE_data['200a041J094H0802'][i]) + '   ' + OPGEE_data['headings'][i])
		


	print(OPGEE_data['200a041J094H0802'])

	'''