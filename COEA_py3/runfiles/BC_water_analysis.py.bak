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
from get_BC_water_data import get_BC_water_data
import math

def BC_water_analysis(well_data_headings, well_data):

	#Getting BC water data 

	m_ft = 3.28084

	BC_water_data_headings,  BC_water_data = get_BC_water_data()

	#for analysis of all BC let well_data = [] bugs need to fixed
	#well_data = []

	water_data = BC_water_data

	count = 0
	count2 = 0 #this counts the number of formation wells with BC data
	count_miss_well = 0
	are_wells = 'yes'
	UWI_to_WA = collections.OrderedDict()
	WA_to_UWI = collections.OrderedDict()
	drilled_year_count = collections.Counter()


	#all of BC
	if len(well_data) == 0:
		wells_assessed = [] 
		for well in water_data:
			wells_assessed.append(well)
	
	#selected wells
	elif len(well_data) != 0:
		wells_assessed = well_data
		for well in wells_assessed:
			WA_index = well_data_headings.index('Lic/WA/WID/Permit #')
			WA = wells_assessed[well][WA_index]
			UWI_to_WA[well] = WA
			WA_to_UWI[WA] = well
			if UWI_to_WA[well] in water_data:
				count2 = count2 + 1	


	#count of total water data 
	for well in water_data:
		count = count + 1


	print('\n~~~~~~~~~~~~~~~~~~~WATER ANALYSIS OF BC WELLS~~~~~~~~~~~~~~~~~~~')
	print('\n')
	print('Total number of BC wells with water data entries: ' + str(count))

	if (count2 == 0 and wells_assessed == well_data): # we want to exit if no wells have BC water data
		print('\nNo Formation Wells Have BC Water Data\n')
		return
	#------------------------------ WATER Analysis-----------------------------

	total_water_volume = [] #total water volume by type eg municipal water
	well_water_volume = collections.OrderedDict()
	well_proppant_mass = collections.OrderedDict()
	drilled_year_count = collections.Counter()
	water_types = []
	water_sources = []
	well_count = 0
	formation_wells_with_water_data = []
	HZ_lengths = []
	TVDs = []
	MDs = [] 

	for j in range(0,len(BC_water_data_headings)):
		if BC_water_data_headings[j] == 'BASE FLUID':
			water_type_index = j
		if BC_water_data_headings[j] == 'TOTAL FLUID PUMPED (m3)':
			water_vol_index = j
		


	TVD_index = well_data_headings.index('TVD (m)')
	MD_index = well_data_headings.index('MD (All Wells) (m)')
	HZNS_index = well_data_headings.index('BotHole N/S Distance (m)')
	HZEW_index = well_data_headings.index('BotHole E/W Distance (m)')
	drill_year_index = well_data_headings.index('Date Drlg Completed')

	well_WAs = []

	for well in wells_assessed:

		#arrays for each well volume and type 
		well_water_types = []
		well_water_volume_array = []
		
		if UWI_to_WA[well] in water_data:

			WA = UWI_to_WA[well]
			#well_WAs = ['a']

			if WA not in well_WAs:
				
				well_WAs.append(WA)

				well_count = well_count + 1
				well_water_volume[well] = []
				well_proppant_mass[well] = []

				for i in range(0,len(water_data[WA])):
					well_water_vol = 0
					water_type = water_data[WA][i][water_type_index].upper()
					try:
						water_vol = float(water_data[WA][i][water_vol_index])
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
						drilled_year_count[int(well_data[well][drill_year_index][0:4])] += 1
					except:
						#print(well_data[well][drill_year_index][0:4])
						pass
					TVDs.append(float(well_data[well][TVD_index]))
					MDs.append(float(well_data[well][MD_index]))
					NS_length =float(well_data[well][HZNS_index])
					EW_length = float(well_data[well][HZEW_index])
					horizontal_length = math.sqrt(NS_length**2 + EW_length**2)
					HZ_lengths.append(horizontal_length)
				except:
					count_miss_well += 1


	#--------------------------Plot of total water and type ----------------------------------

	total_water_volume = [x for _, x in sorted(zip(water_types, total_water_volume))]
	water_types.sort()

	print('\nCount of Completed Wells; ' + str(well_count))
	#print('Count of unique WAs; ' + str(len(well_WAs)))
	print('\nWater Type Injected and Total Volume (m3)\n')

	for i in range(0,len(water_types)):
		print(water_types[i] + ' (m3) ; ' + str(total_water_volume[i]))
	print('Total Volume (m3); ' + str(sum(total_water_volume)))
	print('\n')


	x = np.arange(len(water_types));
	fig, ax = plt.subplots()
	plt.bar(x, total_water_volume)
	plt.xticks(x, water_types, fontsize=10, rotation=85) #
	plt.ylabel('Water Volume (m3)', fontsize=12)
	plt.title('Total water usage in B.C (' + str(well_count) + ' wells)' ,fontsize=12)
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


	print('\nAnalysis of the ' + str(well_count) + ' wells that have been fractured in B.C;\n')
	print('Number of wells above the ' + str(max_volume) + ' m3 of injected water limit; ' + str(high_count))
	print('Number of zero volume injected wells; ' + str(zero_count))
	print('Mean volume injected (m3); ' + str("%.2f" %np.mean(water_vol_array)))
	print('Number of wells assessed; ' + str(len(water_vol_array)))
	print('Median volume injected (m3); ' + str("%.2f" %np.median(water_vol_array)))
	print('Standard Deviation of volume injected (m3); ' + str("%.2f" %np.std(water_vol_array)))
	print('Variance of volume injected (m3); ' + str("%.2f" %np.var(water_vol_array)))
	print('Max of volume injected (m3); ' + str("%.2f" %np.max(water_vol_array)))
	print('Min of volume injected (m3); ' + str("%.2f" %np.min(water_vol_array)))
	print('25th percentile of volume injected (m3); ' + str("%.2f" %np.percentile(water_vol_array,25)))
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
	
	time.sleep(5)

	plt.show()
	return


if __name__ == '__main__':

	from get_BC_water_data import get_BC_water_data
	from well_search import well_search
	from get_all_post_2005_well_data import get_all_post_2005_well_data, get_tight_oil_wells

	BC_function = get_BC_water_data()
	BC_water_data_headings = BC_function[0]
	BC_water_data = BC_function[1]

	print('Importing General Well Data') #MONTNEY
	#well_data_function = get_formation_well_data() # MONTNEY
	#well_data_function = well_search()
	well_data_function = get_tight_oil_wells()
	#well_data_function = get_all_post_2005_well_data()

	well_data_headings = well_data_function[0] # MONTNEY
	well_data = well_data_function[1] # MONTNEY

	BC_water_analysis(well_data_headings, well_data)

	'''
	well_water_data = water_data_sum_average_min_max(BC_water_data, BC_water_data_headings, well_data, well_data_headings,'PROPPANT TYPE1 PUMPED (t)', 'sum','BC')

	array = []

	for well in well_water_data:
		array.append(well_water_data[well])

	plt.plot(range(0,len(array)),array)
	plt.show()
	print(len(array))
	print(np.mean(array))
	'''