from get_AB_water_data import get_AB_water_use_data
from get_BC_water_data import get_BC_water_data
from water_data_functions import water_data_sum_average_min_max
import math
import numpy as np 


def OPGEE_drilling_and_development(OPGEE_data, well_data, well_data_headings):

	m_ft = 3.28084
	m3_gal = 264.172
	Kpam_psift = 0.0442075


	print('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	print('   Getting OPGEE Drilling and Development Data')
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

	#fraction of horizontal wells and length of lateral

	BH_NS_dist_index = well_data_headings.index('BotHole N/S Distance (m)')
	BH_EW_dist_index = well_data_headings.index('BotHole E/W Distance (m)')
	Horizontal_TF_index = well_data_headings.index('Horizontal Hole (T/F)')
	well_depth = well_data_headings.index('TVD (m)')
		 		
	horizontal_length_array = []
	horizontal_TF_count = [0,0] #[true,false]

	for well in well_data:

		try:
			NS_length = float(well_data[well][BH_NS_dist_index])
			EW_length = float(well_data[well][BH_EW_dist_index])
			horizontal_length = math.sqrt(NS_length**2 + EW_length**2)
			OPGEE_data[well][OPGEE_data['headings'].index('Horizontal well fraction')] = 1
			OPGEE_data[well][OPGEE_data['headings'].index('Length of lateral')] = horizontal_length*m_ft
			horizontal_length_array.append(horizontal_length)
		except:
			pass

		horizontal_true_false = well_data[well][Horizontal_TF_index]
		
		if horizontal_true_false == 'T':
			horizontal_TF_count[0] += 1
		elif horizontal_true_false == 'F':
			horizontal_TF_count[1] += 1

	if len(horizontal_length_array) > 0:
		mean_horzontal_length = np.mean(horizontal_length_array)
	elif len(horizontal_length_array) == 0:
		mean_horzontal_length = 0

	fraction_horizontal = float(horizontal_TF_count[0])/(sum(horizontal_TF_count))


	#OPGEE_data[well][OPGEE_data['headings'].index('Horizontal well fraction')] = fraction_horizontal
	#OPGEE_data[well][OPGEE_data['headings'].index('Length of lateral')] = mean_horzontal_length*m_ft

	#fracturing fluid injection volume and gradient

	AB_water_data_headings, AB_water_data = get_AB_water_use_data()
	BC_water_data_headings, BC_water_data = get_BC_water_data()

	#get dictionaries of total water injection volumes for AB and BC
	AB_water_use = water_data_sum_average_min_max(AB_water_data, AB_water_data_headings, well_data, well_data_headings,'Total Water Volume', 'sum','AB')
	BC_water_use = water_data_sum_average_min_max(BC_water_data, BC_water_data_headings, well_data, well_data_headings,'TOTAL FLUID PUMPED (m3)', 'sum','BC')


	AB_water_array = []

	if len(AB_water_use) > 0: #if we have water data

		for well in AB_water_use:
			OPGEE_data[well][OPGEE_data['headings'].index('Fracturing fluid injection volume')] = AB_water_use[well]*m3_gal/1000000
			OPGEE_data[well][OPGEE_data['headings'].index('Fraction of wells fractured')] = 1
			AB_water_array.append(AB_water_use[well])

		average_AB_water_use = np.mean(AB_water_array)
		AB_water_use_count = len(AB_water_array)

	elif len(AB_water_use) == 0: #if we dont have water data 

		average_AB_water_use = 0
		AB_water_use_count = 0

	BC_water_array = []

	if len(BC_water_use) > 0: #if we have water data

		for well in BC_water_use:
			OPGEE_data[well][OPGEE_data['headings'].index('Fracturing fluid injection volume')] = BC_water_use[well]*m3_gal/1000000
			OPGEE_data[well][OPGEE_data['headings'].index('Fraction of wells fractured')] = 1
			BC_water_array.append(BC_water_use[well])

		average_BC_water_use = np.mean(BC_water_array)
		BC_water_use_count = len(BC_water_array)

	elif len(BC_water_use) == 0: #if we dont have water data 

		average_BC_water_use = 0
		BC_water_use_count = 0

	#now we have water data we get the weights average of water injected
	fractured_well_count = AB_water_use_count + BC_water_use_count

	if (fractured_well_count) > 0:
		average_water_injected = float(AB_water_use_count*average_AB_water_use)/fractured_well_count + float(BC_water_use_count*average_BC_water_use)/fractured_well_count
	elif (fractured_well_count) == 0:
		#we will assume the default
		average_water_injected = 0
	
	#-------Fracture Gadient-----------#

	#get dictionary of BC fracture gradients 
	BC_frac_gradient = water_data_sum_average_min_max(BC_water_data, BC_water_data_headings, well_data, well_data_headings,'FRAC GRADIENT (KPa/m)', 'average','BC')

	BC_frac_array = []

	if len(BC_frac_gradient) > 0: #if we have water data

		for well in BC_frac_gradient:
			if np.isnan(BC_frac_gradient[well]) != True:
				if BC_frac_gradient[well]*Kpam_psift > 0.6:
					#this is the minimum OPGEE can run with
					OPGEE_data[well][OPGEE_data['headings'].index('Fracture pressure gradient')] = BC_frac_gradient[well]*Kpam_psift
				BC_frac_array.append(BC_frac_gradient[well])

		average_BC_frac_gradient = np.mean(BC_frac_array)
		BC_frac_gradient_count = len(BC_frac_array)

	if len(BC_frac_gradient) == 0:

		average_BC_frac_gradient = 0
		BC_frac_gradient_count = 0 

	#now we have all data, we add it to OPGEE data

	#print mean_horzontal_length
	#print fraction_horizontal
	#print average_water_injected
	#print average_BC_frac_gradient
	#print fractured_well_count

	if average_water_injected > 0:
		#we want to convert m3 to million gal 
		OPGEE_data['assessed field'][OPGEE_data['headings'].index('Fracturing fluid injection volume')] = round(float(average_water_injected*m3_gal)/1000000,4)

		#assign average to all wells without data
		#the default for fracture wells must be 1 (ie all wells are fractured)

		for well in well_data:
			if OPGEE_data[well][OPGEE_data['headings'].index('Fracturing fluid injection volume')] == OPGEE_data['defaults'][OPGEE_data['headings'].index('Fracturing fluid injection volume')]:
				if OPGEE_data['defaults'][OPGEE_data['headings'].index('Horizontal well fraction')] == 1:
					OPGEE_data[well][OPGEE_data['headings'].index('Fracturing fluid injection volume')] = round(float(average_water_injected*m3_gal)/1000000,4)

	if average_BC_frac_gradient > 0.6:
		#this is the minimum OPGEE can run with
		OPGEE_data['assessed field'][OPGEE_data['headings'].index('Fracture pressure gradient')] = average_BC_frac_gradient*Kpam_psift
	
	OPGEE_data['assessed field'][OPGEE_data['headings'].index('Horizontal well fraction')] = 1

	return OPGEE_data


if __name__ == '__main__':

	from get_well_data import get_formation_well_data
	from OPGEE_defaults import OPGEE_defaults
	from search_production_data import search_production_data
	import collections
	from well_search import well_search
	from general_well_data_analysis import OPGEE_well_data, general_well_data_analysis
	from production_analysis import production_dates, production_summary, OPGEE_production_data, OPGEE_well_production_data
	from OPGEE_input_sensitivity import OPGEE_input_sensitivity

	#well_data_function = get_formation_well_data() # MONTNEY
	well_data_function = well_search()

	well_data_headings = well_data_function[0] # MONTNEY
	well_data = well_data_function[1] # MONTNEY
	field_name = 'Montney'

	OPGEE_data = OPGEE_defaults()

	OPGEE_data = general_well_data_analysis(well_data_headings, well_data, OPGEE_data, field_name)

	OPGEE_data = OPGEE_well_data(well_data, well_data_headings, OPGEE_data)

	#production_data_headings, production_data, well_data_headings, well_header_data = search_production_data(general_well_data)

	#date_array = production_dates()
	
	#production_dict = production_summary(production_data_headings, production_data, date_array)
	
	#OPGEE_data = OPGEE_production_data(OPGEE_data, production_data, production_dict, date_array)

	#OPGEE_data = OPGEE_well_production_data(production_data, production_data_headings, OPGEE_data, date_array)
	
	OPGEE_data = OPGEE_drilling_and_development(OPGEE_data, well_data, well_data_headings)

	OPGEE_input_sensitivity(OPGEE_data, well_data)