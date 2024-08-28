import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import csv
import collections
import pylab
import datetime
import re
import math
import time
from datetime import datetime
from return_statistics import return_statistics, histogram
from get_AB_water_data import get_AB_water_use_data, get_AB_water_source_data
from get_all_post_2005_well_data import get_tight_oil_wells

def AB_water_source_analysis(well_data_headings, well_data):

	m_ft = 3.28084

	#importing water data

	AB_water_data_headings, AB_water_data = get_AB_water_source_data()

	#for analysis of all albera, let well_data = []

	water_data = AB_water_data

	if len(well_data) == 0:
		wells_assessed = [] 
		shorten_UWI = 'NO' #we are looking at all wells in alberta meaning we dont need to shorten the UWI
		for well in water_data:
			wells_assessed.append(well)

	else:
		wells_assessed = well_data
		shorten_UWI = 'YES' #we have to shorten the UWI because the one in formation well data is to long


	print('\n\n~~~~~~~~~~~~~~~~~~~WATER SOURCE ANALYSIS OF ALBERTAN WELLS~~~~~~~~~~~~~~~~~~~\n')
	print('data reprisents the volume of water "sourced" for treatments. Hence, it does not reprisent the')
	print('volume of water being injected. This data is in a different AER dataset (Water use).\n')
	print('Total number of AB wells with water data entries: ' + str(len(water_data)))

	#------------------------------ WATER Analysis-----------------------------

	total_water_volume = [] #total water volume by type eg municipal water
	well_water_volume = collections.OrderedDict()
	year_water_volume = collections.OrderedDict()
	well_proppant_mass = collections.OrderedDict()
	drilled_year_count = collections.Counter()
	HZ_lengths = []
	TVDs = []
	MDs = [] 
	water_types = []
	water_sources = []
	drilled_year = []
	well_count = 0
	count_miss_well = 0
	formation_wells_with_water_data = []

	for j in range(0,len(AB_water_data_headings)):
		if AB_water_data_headings[j] == 'Water Source Type':
			water_type_index = j
		if AB_water_data_headings[j] == 'Total Water Volume':
			water_vol_index = j
		
	TVD_index = well_data_headings.index('TVD (m)')
	MD_index = well_data_headings.index('MD (All Wells) (m)')
	HZNS_index = well_data_headings.index('BotHole N/S Distance (m)')
	HZEW_index = well_data_headings.index('BotHole E/W Distance (m)')
	drill_year_index = well_data_headings.index('Date Drlg Completed')

	for well in wells_assessed:

		if shorten_UWI == 'YES':
			well_long = well
			well = well[1:-2] + well[-1] #transform 100062505526W502 into 00062505526W52

		#arrays for each well volume and type 
		well_water_types = []
		well_water_volume_array = []
		
		if well in water_data:
			well_count = well_count + 1
			well_water_volume[well] = []
			well_proppant_mass[well] = []

			for i in range(0,len(water_data[well])):
				well_water_vol = 0
				water_type = water_data[well][i][water_type_index]
				try:
					water_vol = float(water_data[well][i][water_vol_index])
				except:
					water_vol = 0
				
				#totals 
				if water_type not in water_types: #Getting only different water types 
					water_types.append(water_type)
					total_water_volume.append(0)
				for j in range(0,len(water_types)):
					if water_type == water_types[j]:
						total_water_volume[j] = total_water_volume[j] + water_vol

				#Individual Wells
				if water_type not in well_water_types:
					well_water_types.append(water_type)
					well_water_volume_array.append(0)
				for j in range(0,len(well_water_types)):
					if water_type == well_water_types[j]:
						well_water_volume_array[j] = well_water_volume_array[j] + water_vol

			well_water_volume[well].append(well_water_types)
			well_water_volume[well].append(well_water_volume_array)

			#we also want to get the average TVD, TD and Horizontal length of the wells

			try:
				try:
					year = int(well_data[well_long][drill_year_index][0:4])
					
					drilled_year_count[year] += 1
					if year not in year_water_volume:
						year_water_volume[year] = 0
					year_water_volume[year] += sum(well_water_volume[well][1])
				except:
					pass
				TVDs.append(float(well_data[well_long][TVD_index]))
				MDs.append(float(well_data[well_long][MD_index]))
				NS_length =float(well_data[well_long][HZNS_index])
				EW_length = float(well_data[well_long][HZEW_index])
				horizontal_length = math.sqrt(NS_length**2 + EW_length**2)
				HZ_lengths.append(horizontal_length)
			except:
				count_miss_well += 1

	#return if no wells have been fracced in alberta
	if well_count == 0:
		print('\nNo Wells Have Reported Albertan Hydraulic Fracture Data\n')
		return

	#--------------------------Plot of total water and type ----------------------------------

	#sort in aplhabetical order
	total_water_volume = [x for _, x in sorted(zip(water_types, total_water_volume))]
	water_types.sort()

	print('\nCount of Completed Wells; ' + str(well_count))

	print('\nWater Source Type and Total Volume (m3)\n')
	
	for i in range(0,len(water_types)):
		print(water_types[i] + ' (m3);  '+ str(total_water_volume[i]))
	print('Total Volume (m3); ' + str(sum(total_water_volume)))

	x = np.arange(len(water_types));
	fig, ax = plt.subplots()
	plt.bar(x, total_water_volume)
	plt.xticks(x, water_types, fontsize=5, rotation=85) #
	plt.ylabel('Water Volume (m3)', fontsize=12)
	plt.title('Total water usage in Alberta (' + str(well_count) + ' wells)' ,fontsize=12)
	plt.tight_layout()


	#---------------------------Data analysis of water use in alberta wells------------------------

	water_vol_array = [] #array of water injection volumes
	high_count = 0
	zero_count = 0
	max_volume = 1000000 # These wells are excluded as extremes 

	for well in well_water_volume:
		if len(well_water_volume[well][1]) == 0:
			water_volume = 0
		else:
			water_volume = sum(well_water_volume[well][1])
		if water_volume > max_volume:
			high_count = high_count + 1
		if water_volume == 0:
			zero_count = zero_count + 1
		if (0 < water_volume < max_volume):
				water_vol_array.append(water_volume)

	print('\nAnalysis of the ' + str(well_count) + ' wells that have been fractured in Alberta:\n')
	print('Number of wells above the ' + str(max_volume) + ' m3 of injected water limit; ' + str(high_count))
	print('Number of zero volume injected wells; ' + str(zero_count))
	print('Mean volume injected (m3); ' + str("%.2f" %np.mean(water_vol_array)))
	print('Number of wells assessed; ' + str(len(water_vol_array)))
	print('Median volume injected (m3); ' + str("%.2f" %np.median(water_vol_array)))
	print('Standard Deviation of volume injected (m3); ' + str("%.2f" %np.std(water_vol_array)))
	print('Variance of volume injected (m3); ' + str("%.2f" %np.var(water_vol_array)))
	print('Max of volume injected (m3); ' + str("%.2f" %np.max(water_vol_array)))
	print('Min of volume injected (m3); ' + str("%.2f" %np.min(water_vol_array)))
	print('25th percentaile of volume injected (m3); ' + str("%.2f" %np.percentile(water_vol_array,25)))
	print('75th percentile of volume injected (m3); ' + str("%.2f" %np.percentile(water_vol_array,75)))

	print('\nAnalysis of Completed Well Lengths\n')
	print('Count TVDs; ' + str(len(TVDs)))
	print('Count Measured Depths; ' + str(len(TVDs)))
	print('Count Horizontal Lengths; ' + str(len(HZ_lengths)))
	print('Count Missing Length Data; ' + str(count_miss_well))
	print('\n')
	print('Mean TVD (m); ' + str(np.mean(TVDs)))
	print('Mean TVD (ft); ' + str(np.mean(TVDs)*m_ft))
	print('Mean Measured Depth (m); ' + str(np.mean(MDs)))
	print('Mean Measured Depth (ft); ' + str(np.mean(MDs)*m_ft))
	print('Mean Horizontal Length (m); ' + str(np.mean(HZ_lengths)))
	print('Mean Horizontal Length (ft); ' + str(np.mean(HZ_lengths)*m_ft))

	print('\nAnalysis of Well Drill Year\n')
	
	for key in sorted(drilled_year_count.keys()):
		print(str(key) + '; ' + str(drilled_year_count[key]))

	print('\nAnalysis of Volume Sourced By Well Drill Year\n')

	for key in sorted(year_water_volume.keys()):
		print(str(key) + '; ' + str(year_water_volume[key]))


	plt.show()
	
	return

def AB_water_use_analysis(AB_water_use_headings, AB_water_use_data, well_data_headings, well_data):

	#indexings
	stage_index = AB_water_use_headings.index('Number of Stages')
	BH_lat_index = AB_water_use_headings.index('Bottom Hole Latitude')
	BH_lon_index = AB_water_use_headings.index('Bottom Hole Longitude')
	prod_fluid_type_index = AB_water_use_headings.index('Production Fluid Type')
	TVD_index = AB_water_use_headings.index('Max True Vertical Depth')	
	water_vol_index = AB_water_use_headings.index('Total Water Volume')
	start_date_index = AB_water_use_headings.index('Start Date')
	end_date_index = AB_water_use_headings.index('End Date')
	comp_type_index = AB_water_use_headings.index('Component Type')
	comp_name_index = AB_water_use_headings.index('Component Trade Name')
	additive_purpose_index = AB_water_use_headings.index('Additive Purpose')
	ingredient_index = AB_water_use_headings.index('Ingredient Name')
	comp_concentration_index = AB_water_use_headings.index('Concentration Component ')	
	total_conc_index = AB_water_use_headings.index('Concentration HFF') #concentration by mass

	date_format =  '%m/%d/%Y'

	metric_water_density = 998 
	m3_gal = 264.172052
	zeros = 0
	well_count = 0
	wells_w_data = []

	water_volume_array = [] #an array of the volume injected for each well
	stages_array = []

	for well in well_data:

		well = well[1:-2] + well[-1] #transform 100062505526W502 into 00062505526W52

		if well in AB_water_use_data:

			if well not in wells_w_data:
				wells_w_data.append(well)

			well_count = well_count + 1
			water_volume = 0 #well water volume
			proppant_mass = 0 
			max_stage = 0

			start_date = AB_water_use_data[well][0][start_date_index]
			start_date = datetime.strptime(start_date, date_format)

			#calculate total water injection volume and get max stage number
			for entry in range(0,len(AB_water_use_data[well])):
				water_volume = water_volume + float(AB_water_use_data[well][entry][water_vol_index])
				stage_number = float(AB_water_use_data[well][entry][stage_index])
				if stage_number > max_stage:
					max_stage = stage_number
			
			if water_volume == 0:
				zeros = zeros + 1

			water_volume_array.append(water_volume)
			stages_array.append(max_stage)


	histogram(water_volume_array, 'HF Water Volumes (m3)')

	return_statistics(water_volume_array, 'HF Water Volumes (m3)')
	print('zeros: ' + str(zeros))
	print('total: ' + str(len(water_volume_array)))
	plt.scatter(stages_array,water_volume_array)
	plt.show()




if __name__ == '__main__':

	from OPGEE_defaults import OPGEE_defaults
	import collections
	from well_search import well_search
	from general_well_data_analysis import OPGEE_well_data, general_well_data_analysis
	from get_AB_water_data import get_AB_water_use_data, get_AB_water_source_data
	from get_all_post_2005_well_data import get_all_post_2005_well_data
	from water_data_functions import water_data_sum_average_min_max

	print('Importing General Well Data') #MONTN1EY
	#well_data_function = get_formation_well_data() # MONTNEY
	#well_data_function = well_search()
	well_data_function = get_tight_oil_wells()
	#well_data_function = get_all_post_2005_well_data()

	well_data_headings = well_data_function[0] # MONTNEY
	well_data = well_data_function[1] # MONTNEY
	field_name = 'Montney'

	AB_water_source_data_headings, AB_water_source_data = get_AB_water_source_data()

	AB_water_source_analysis(well_data_headings, well_data)

	#AB_water_use_data_headings, AB_water_use_data = get_AB_water_use_data()

	#AB_water_use_analysis(AB_water_use_data_headings, AB_water_use_data, well_data_headings, well_data)

