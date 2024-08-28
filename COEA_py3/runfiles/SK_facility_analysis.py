
import collections
import time
import csv
import re
import numpy as np
from datetime import datetime, timedelta

from .map_to_drive import map_to_drive #path to Project Data folder

def get_SK_facility_links(date_array):

	print('Getting SK Facility Well Links')

	#returns two dictionaries, 
	#1. well to facility, 
	#2. facility to well

	well_to_facility = collections.OrderedDict()
	facility_to_well = collections.OrderedDict()
	facility_connection_dates = collections.OrderedDict() #facility_connection_dates[facility + ' to ' + well] = [month1, month2, month3..]

	# Kareem Edits:
	# SK_FFV_file =  map_to_drive() + "Project Data/SK_gov/SK Well to BT Links.csv"
	SK_FFV_file = "Project Data/SK_gov/SK Well to BT Links.csv"

	# Kareem edits: ("r", encoding='windows-1252')
	with open(SK_FFV_file, "r", encoding='windows-1252') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == 'Facility ID':
				headings = row
				fac_index = headings.index('Facility ID')
				well_index = headings.index('Well ID')
				start_index = headings.index('Start Date')
				end_index = headings.index('End Date')
				#print(row)

			elif row[0] != 'Facility ID':
				long_fac_ID = row[fac_index] # SK BT S1H3996
				long_well_ID = row[well_index] #SK WI 191011204823W300
				start_date = row[start_index]
				end_date = row[end_index]
				last_day_we_care_about = datetime.strptime(date_array[-1], '%Y-%m')
				first_day_we_care_about = datetime.strptime(date_array[0], '%Y-%m')

				#we need to shorten these for matching
				fac_ID = long_fac_ID.split(' ')[-1] #S1H3996
				well_ID = long_well_ID.split(' ')[-1] #191011204823W300
				
				if fac_ID not in facility_to_well:
					facility_to_well[fac_ID] = []
				if fac_ID in facility_to_well:
					if well_ID not in facility_to_well[fac_ID]:
						facility_to_well[fac_ID].append(well_ID)

				if well_ID not in well_to_facility:
					well_to_facility[well_ID] = []
				if well_ID in well_to_facility:
					if fac_ID not in well_to_facility[well_ID]:
						well_to_facility[well_ID].append(fac_ID)

				
				#get arrays of when wells are connected to facilities
				
				date_key = fac_ID + ' to ' + well_ID
				start_date = datetime.strptime(start_date, '%Y-%m-%d') #.strftime('%Y-%m')
				if start_date <= first_day_we_care_about:
					start_date = date_array[0]
				else:
					start_date = start_date.strftime('%Y-%m')

				if len(end_date) == 0:
					end_date = date_array[-1]
				else:
					#print(end_date)
					end_date = datetime.strptime(end_date, '%Y-%m-%d') #.strftime('%Y-%m')
					if end_date >= last_day_we_care_about:
						end_date = date_array[-1]
					else:
						end_date = end_date.strftime('%Y-%m')


				if date_key not in facility_connection_dates:
					#print(start_date,end_date)
					try:
						if start_date == end_date:
							facility_connection_dates[date_key] = [start_date]
						else:
							facility_connection_dates[date_key] = date_array[date_array.index(start_date):date_array.index(end_date)]
					except:
						facility_connection_dates[date_key] = ['pass']
						#start date is greater than what we care about therefore skip
						continue

				#print(start_date)
				#print(end_date)

	return well_to_facility, facility_to_well, facility_connection_dates

def SK_facility_list(well_data, well_data_headings, well_to_facility):

	#returns a list of the connected facilities
	#if an empty well list is passed through, connected_facilities = -1 (we collect all in get_SK_facility_data)

	connected_facilities = []
	connected_wells = []

	if len(well_data) > 0:
		print('\nGetting SK Facilities Connected to Project Wells')
		for well in well_data:
			if well in well_to_facility:
				if well not in connected_wells:
					connected_wells.append(well)
				for facility in well_to_facility[well]:
					if facility not in connected_facilities:
						connected_facilities.append(facility)

	if len(well_data) == 0:
		print('\nGetting ALL SK facility Data')
		connected_facilities = -1
		#for well in well_to_facility:
		#	[connected_facilites.append(facility) for facility in well_to_facility[well]]

	try:
		print(('Total Number of SK Facilities Connected to Project Wells (All Time)',len(connected_facilities)))
		print(('Total Number of Project Wells Connected to SK Facilities (All Time)', len(connected_wells)))
	except:
		pass

	return connected_facilities

def get_SK_facility_data(connected_facilities, date_array):

	#collects facility data for the connected facilites over the date_range
	#returns a summary dictionary of format = SK_facility_data[facility][date][activity product] = volume
	#also returns a facility_info dictionary = SK_facility_info[facility] and SK_facility_info_headings for the data
	#data is organised into yearly files, first we get the years we need to open

	SK_facility_data = collections.OrderedDict()
	SK_facility_data_headings = [] #this will be an array of the activity products 
	SK_facility_info = collections.OrderedDict()
	SK_facility_info_headings = collections.OrderedDict()

	selected_facilites = connected_facilities

	#included_facility_type = ['CRUDE OIL SINGLE-WELL BATTERY']
	#excluded_facility_type = ['DRILLING AND COMPLETING ']

	years_array = [] #an array of the year files we will search
	
	for year_month in date_array:
		year = year_month[0:4]
		if year not in years_array:
			years_array.append(year)

	#gas is measured in 1000m3

	for year in years_array:

		start_time = time.time()

		print(('\nGetting SK facility Data for ' + str(year)))

		# Kareem Edits
		# SK_data_path = map_to_drive() + "Project Data/SK_gov/SK FFV (Nov 22)/" + year + ".csv"
		SK_data_path = "Project Data/SK_gov/SK FFV (Nov 22)/" + year + ".csv"

		included_facility_type = []
		excluded_facility_type = []
		#included_facility_type = ['CRUDE OIL SINGLE-WELL BATTERY']

		switch = 0
		# Kareem edits: ("r", encoding='windows-1252')
		with open(SK_data_path, "r", encoding='windows-1252') as f:
			
			reader = csv.reader(f)
			
			for row in reader:
		
				if row[0] == 'Production Month':
					headings = row
					date_index = headings.index('Production Month')
					fac_index = headings.index('Facility BID')
					sub_type_index = headings.index('Facility Sub Type')
					surface_loc_index = headings.index('Facility Surface Location')
					product_index = headings.index('Prod Accounting Product Type Code')
					activity_index = headings.index('Volumetric Activity Type Code')
					volume_index = headings.index('Reported Volume')
					SK_facility_info_headings = row[1:activity_index]

				elif row[0] != 'Production Month':
					long_fac_ID = row[fac_index]  # SK BT S1H3996
					fac_ID = long_fac_ID.split(' ')[-1] #S1H3996
					

					#if we have a set of selected facilities
					if connected_facilities == -1:
						selected_facilites = [fac_ID]

					if fac_ID in selected_facilites:
						
						year_month = row[date_index][0:4] + '-' + row[date_index][4:7] # convert 201012 to 2010-12
						fac_type = row[sub_type_index]
						
						#comment in below for certain sub types
						#if fac_type in included_facility_type:

						#print(year_month)
						if fac_ID not in SK_facility_data:
							SK_facility_data[fac_ID] = collections.OrderedDict()
							SK_facility_info[fac_ID] = row[1:activity_index] #get info for facilites	
						if year_month in date_array:
							product = row[product_index].upper()
							if year_month not in SK_facility_data[fac_ID]:
								SK_facility_data[fac_ID][year_month] = collections.OrderedDict()
							if len(product) > 0:
								#we have some missing data 
								product = row[product_index].upper()
								activity = row[activity_index]
								activity_product = activity + ' ' + product 
								volume = float(re.sub("|".join([',']), "",row[volume_index]))
	
								if activity_product not in SK_facility_data[fac_ID][year_month]:
									#print(year_month,activity_product, fac_ID)
									SK_facility_data[fac_ID][year_month][activity_product] = 0
								if activity_product in SK_facility_data[fac_ID][year_month]:
									#sum the totl volume for each activity at the facilities 
									SK_facility_data[fac_ID][year_month][activity_product] += volume

		


		if len(excluded_facility_type) > 0:
			print(('Excluded facility types - ' + str(excluded_facility_type)))
		if len(included_facility_type) > 0:
			print(('The following facility types are being assessed - ' + str(included_facility_type)))
		print(('Computational Time(s): ' + str(time.time() - start_time)))
	
	print('\n')
	
	return SK_facility_data, SK_facility_info, SK_facility_info_headings

def SK_facility_period_summary(SK_facility_data,date_array):

	#summarizes the volumes for each facility over the period
	#also calculates a summary of ALL facilities over the period
	#structure will be facility[activity_prod] = vol

	SK_facility_data['ALL'] = collections.OrderedDict()

	for fac_ID in SK_facility_data:
		if fac_ID != 'ALL':
			for year_month in date_array:
				if year_month not in SK_facility_data['ALL']:
					SK_facility_data['ALL'][year_month] = collections.OrderedDict()
				if year_month in  SK_facility_data[fac_ID]:
					for activity_product in SK_facility_data[fac_ID][year_month]:
						if activity_product not in SK_facility_data['ALL'][year_month]:
							SK_facility_data['ALL'][year_month][activity_product] = 0
						if activity_product in SK_facility_data['ALL'][year_month]:
							SK_facility_data['ALL'][year_month][activity_product] += SK_facility_data[fac_ID][year_month][activity_product]
		
	return SK_facility_data

def print_SK_facility_data(facility_printed, SK_facility_data, SK_facility_info, SK_facility_info_headings, facility_to_well, well_data):

	#facility_printed reprisents the facility that will be proted out e.g 'ALL'

	#conversion factors
	m3_scf = 35.314666
	m3_bbl = 6.2898

	facility_type_count = collections.Counter()

	#summary of ALL facilities 
	print(('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n    Summary of Facility; ' + facility_printed + ' \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'))
	
	if facility_printed == 'ALL':
		proj_wells_connected = []
		print(('Total Number of Connected Facilities Over Period Assessed', len(SK_facility_data) - 1))
		print('\n')
		try: #we try because if well data = [], we get an error
			print('FACILITY TYPE AND COUNT\n')
			for facility in SK_facility_info:
				fac_type = SK_facility_info[facility][SK_facility_info_headings.index('Facility Sub Type')]
				facility_type_count[fac_type] += 1
				for well in facility_to_well[facility]:
					if well in well_data:
						if well not in proj_wells_connected:
							proj_wells_connected.append(well)
			for key in sorted(facility_type_count.keys()):
					print((key + '; ' + str(facility_type_count[key])))
			print(('\nNumber of project wells connected over period; ' + str(len(proj_wells_connected))))
			print('\n')
		except:
			print(('COUNT of All SK Facilities; ' + str(len(SK_facility_data)-1) + '\n'))
			print()
	
	if facility_printed != 'ALL':
		proj_wells_connected = []
		for i in range(0,len(SK_facility_info_headings)):
			print((SK_facility_info_headings[i] + '; ' + SK_facility_info[facility_printed][i]))
		print('\n')
		print(('Number of Connected Wells; ' + str(len(facility_to_well[facility_printed]))))
		for well in facility_to_well[facility_printed]:
			if well in well_data:
				if well not in proj_wells_connected:
					proj_wells_connected.append(well)
		print(('Project Wells Connected (count = ' + str(len(proj_wells_connected)) + ')'))
		print(proj_wells_connected)

	print('\nSUMMARY OF VOLUMES\n')

	activity_product_array = []
	for date in SK_facility_data[facility_printed]:
		for activity_product in SK_facility_data[facility_printed][date]:
			if activity_product not in activity_product_array:
				#get list of all activity_products 
				activity_product_array.append(activity_product)
	
	activity_product_array = ['PROD GAS', 'FLARE GAS', 'VENT GAS', 'FUEL GAS', 'PROD COND', 'PROD OIL','REC GAS','DISP GAS','PURREC GAS']

	print(('Year-month, ' + str(activity_product_array)))
	#print('Total Number of Connected Project Wells', len(connected_wells))
	
	period_total = np.zeros(len(activity_product_array))


	for year_month in SK_facility_data[facility_printed]:
		act_value = []
		for activity_product in activity_product_array:
			#some months may flare while others dont
			if activity_product in SK_facility_data[facility_printed][year_month]:
				act_value.append(round(SK_facility_data[facility_printed][year_month][activity_product],2))
			elif activity_product not in SK_facility_data[facility_printed][year_month]:
				act_value.append(0)
		
		print((year_month + ', ' + str(act_value)))
		period_total = [x + y for x,y in zip(period_total,act_value)]

	print('\nPeriod Totals\n')
	print([round(x,2) for x in period_total])

	activity_product_array = activity_product_array

	if 'PROD OIL' in activity_product_array:
		prod_oil = period_total[activity_product_array.index('PROD OIL')]
	if 'PROD OIL' not in activity_product_array:
		prod_oil = 0

	inlet_gas = period_total[activity_product_array.index('PROD GAS')] + period_total[activity_product_array.index('REC GAS')]

	if prod_oil == 0:
		fuel_rate = 0
		flare_rate = 0
		vent_rate = 0
		gas_oil_ratio = 0
			
	elif prod_oil != 0:
		fuel_rate = (period_total[activity_product_array.index('FUEL GAS')]*1000*m3_scf)/(period_total[activity_product_array.index('PROD OIL')]*m3_bbl)
		flare_rate = (period_total[activity_product_array.index('FLARE GAS')]*1000*m3_scf)/(period_total[activity_product_array.index('PROD OIL')]*m3_bbl)
		vent_rate = (period_total[activity_product_array.index('VENT GAS')]*1000*m3_scf)/(period_total[activity_product_array.index('PROD OIL')]*m3_bbl)
		gas_oil_ratio = (period_total[activity_product_array.index('PROD GAS')]*1000*m3_scf)/(period_total[activity_product_array.index('PROD OIL')]*m3_bbl)

	if inlet_gas > 0:
		fuel_percentage =  (period_total[activity_product_array.index('FUEL GAS')])/(period_total[activity_product_array.index('PROD GAS')] + period_total[activity_product_array.index('REC GAS')])
		flare_percentage =  (period_total[activity_product_array.index('FLARE GAS')])/(period_total[activity_product_array.index('PROD GAS')] + period_total[activity_product_array.index('REC GAS')])
		vent_percentage =  (period_total[activity_product_array.index('VENT GAS')])/(period_total[activity_product_array.index('PROD GAS')] + period_total[activity_product_array.index('REC GAS')])
	elif inlet_gas == 0:
		fuel_percentage = 0	
		flare_percentage = 0
		vent_percentage = 0

	print('\nGas Consumption (percent of inlet)')
	print(('Fuel Gas ("%"); ' + str(round(fuel_percentage*100,3))))
	print(('Flare Gas ("%"); ' + str(round(flare_percentage*100,3))))
	print(('Vent Gas ("%"); ' + str(round(vent_percentage*100,3))))

	print(('\nFacility Gas Oil Ratio (scf/bbl); ' + str(round(gas_oil_ratio,2))))

	print('\nFuel Flare Vent Rates (scf/bbl)')
	print(('Fuel Rate (scf/bbl); ' + str(round(fuel_rate,2))))
	print(('Flare Rate (scf/bbl); ' + str(round(flare_rate,2))))
	print(('Vent Rate (scf/bbl); ' + str(round(vent_rate,2))))

	print('\n')


	return proj_wells_connected

def single_facility_OPGEE(well_data, well_data_headings, SK_facility_data, OPGEE_data, facility_to_well, SK_facility_info, SK_facility_info_headings,facility_connection_dates):

	print('\nCollecting OPGEE FFV inputs for wells\n')

	m3_scf = 35.314666
	m3_bbl = 6.2898

	wells_with_fac_data = []
	impossible_FFV = [] #wells with FFV rates greater tham 100%
	well_cumulative = collections.OrderedDict()
	well_to_fac = collections.OrderedDict()

	activities = ['PROD GAS', 'FLARE GAS', 'VENT GAS', 'FUEL GAS', 'PROD OIL','REC GAS','DISP GAS', 'PURREC GAS']

	for facility in SK_facility_data:
		period_cumulative = np.zeros(len(activities))
		
		if facility != 'ALL':
			if len(SK_facility_data[facility]) > 0:
				fac_type = SK_facility_info[facility][SK_facility_info_headings.index('Facility Sub Type')]
				
				
				for well in facility_to_well[facility]:
					date_key = facility + ' to ' + well
					for year_month in SK_facility_data[facility]:
						if year_month in facility_connection_dates[date_key]:
							for product in SK_facility_data[facility][year_month]:
								period_cumulative[activities.index(product)] += SK_facility_data[facility][year_month][product]

				
					if well in OPGEE_data:
						if well not in well_cumulative:
							well_cumulative[well] = period_cumulative
							well_to_fac[well] = [facility]
						elif well in well_cumulative:
							well_to_fac[well].append(facility)
							well_cumulative[well] = [sum(x) for x in zip(well_cumulative[well],period_cumulative)]
		
	for well in well_cumulative:
		if well not in wells_with_fac_data:
			wells_with_fac_data.append(well)


		prod_oil = float(well_cumulative[well][activities.index('PROD OIL')]*m3_bbl)
		fuel_gas = float(well_cumulative[well][activities.index('FUEL GAS')]*1000*m3_scf)
		flare_gas = float(well_cumulative[well][activities.index('FLARE GAS')]*1000*m3_scf)
		vent_gas = float(well_cumulative[well][activities.index('VENT GAS')]*1000*m3_scf)
		prod_gas = float(well_cumulative[well][activities.index('PROD GAS')]*1000*m3_scf)
		rec_gas = float(well_cumulative[well][activities.index('REC GAS')]*1000*m3_scf)


		well_GOR = OPGEE_data[well][OPGEE_data['headings'].index('Gas-to-oil ratio (GOR)')]
		OPGEE_data[well][OPGEE_data['headings'].index('Facility name')] = str(facility) 
		OPGEE_data[well][OPGEE_data['headings'].index('Facility type')] = str(fac_type) 

					
		if (fuel_gas + flare_gas + vent_gas) > 1.05*(prod_gas + rec_gas):
			impossible_FFV.append(well)
			OPGEE_data[well][OPGEE_data['headings'].index('Facility flared gas')] = 'FFV>100%, set to 0'
			OPGEE_data[well][OPGEE_data['headings'].index('Facility vented gas')] = 0
			OPGEE_data[well][OPGEE_data['headings'].index('Facility fuel gas')] = 0.001
			OPGEE_data[well][OPGEE_data['headings'].index('Flaring-to-oil ratio')] = 0
			OPGEE_data[well][OPGEE_data['headings'].index('Venting-to-oil ratio')] = 0
			continue


		if (prod_gas + rec_gas) > 0:
			OPGEE_data[well][OPGEE_data['headings'].index('Facility flared gas')] = round(flare_gas/(prod_gas + rec_gas)*100,4)
			OPGEE_data[well][OPGEE_data['headings'].index('Facility vented gas')] = round(vent_gas/(prod_gas + rec_gas)*100,4)
			fuel_gas_rate = round(fuel_gas/(prod_gas + rec_gas)*100,4)
			if fuel_gas_rate == 0:
				fuel_gas_rate = 0.001
			OPGEE_data[well][OPGEE_data['headings'].index('Facility fuel gas')] = fuel_gas_rate
			#update well flare and vent data in terms of scf/bbl
			OPGEE_data[well][OPGEE_data['headings'].index('Flaring-to-oil ratio')] = round(well_GOR*(flare_gas/(prod_gas + rec_gas))*0.99,4)
			OPGEE_data[well][OPGEE_data['headings'].index('Venting-to-oil ratio')] = round(well_GOR*(vent_gas/(prod_gas + rec_gas))*0.99,4)

		else:
			OPGEE_data[well][OPGEE_data['headings'].index('Facility flared gas')] = 0
			OPGEE_data[well][OPGEE_data['headings'].index('Facility vented gas')] = 0
			OPGEE_data[well][OPGEE_data['headings'].index('Facility fuel gas')] = 0.001
			#update well flare and vent data in terms of scf/bbl
			OPGEE_data[well][OPGEE_data['headings'].index('Flaring-to-oil ratio')] = 0
			OPGEE_data[well][OPGEE_data['headings'].index('Venting-to-oil ratio')] = 0


		try:
			OPGEE_data[well][OPGEE_data['headings'].index('Facility gas-to-oil ratio')] = (prod_gas + rec_gas)/prod_oil
		except:
			OPGEE_data[well][OPGEE_data['headings'].index('Facility gas-to-oil ratio')] = 0 



	print(('\nUnique FFV Data added to ' + str(len(wells_with_fac_data)) + ' wells'))
	print(('Impossible FFV rates (>100%) were found for ' + str(len(impossible_FFV)) + ' wells'))
	print('Fuel, flare and vent rates for these wells have been set to zero')

	#for well in OPGEE_data:
	#	if well in well_to_fac:
	#		print(well,well_to_fac[well])
	#	else:
	#		print(well,0)


	return OPGEE_data


def SK_facility_analysis(well_data, well_data_headings, OPGEE_data, date_array):

	print('\n\n======================= \nSK FACILITY ANALYSIS\n=======================\n ')

	well_to_facility, facility_to_well, facility_connection_dates = get_SK_facility_links(date_array)

	connected_facilities = SK_facility_list(well_data, well_data_headings, well_to_facility)

	SK_facility_data, SK_facility_info, SK_facility_info_headings = get_SK_facility_data(connected_facilities, date_array)

	if len(SK_facility_data) == 0:
		print('\nNo Saskatchewan Facility Data\n')
		return OPGEE_data, SK_facility_data, 0, 0

	well = list(well_to_facility.keys())[0]
	#fac = connected_facilities[10]
	#print(fac, facility_to_well[fac])
	#print(well, well_to_facility[well])
	
	SK_facility_data = SK_facility_period_summary(SK_facility_data, date_array)
	
	#print(SK_facility_data['ALL'])

	#print(SK_facility_data['B2L0185']['2017-01'])
	#print(SK_facility_data['ALL']['2017-01'])

	connected_wells = print_SK_facility_data('ALL',SK_facility_data, SK_facility_info, SK_facility_info_headings, facility_to_well, well_data)	

	if connected_facilities != -1:
		OPGEE_data = single_facility_OPGEE(well_data, well_data_headings, SK_facility_data, OPGEE_data, facility_to_well, SK_facility_info, SK_facility_info_headings,facility_connection_dates)

	ask_for_single_print = str(input('\nPrint Individual Facility? (Y/N):  '))

	if ask_for_single_print.upper() == 'Y':

		for facility in SK_facility_data:

			print_SK_facility_data(facility,SK_facility_data, SK_facility_info, SK_facility_info_headings, facility_to_well, well_data)

	#for well in OPGEE_data:
	#	print(well, OPGEE_data[well][OPGEE_data['headings'].index('Facility flared gas')],OPGEE_data[well][OPGEE_data['headings'].index('Facility vented gas')], OPGEE_data[well][OPGEE_data['headings'].index('Facility fuel gas')])								
					

	return OPGEE_data, SK_facility_data['ALL'], len(connected_wells), len(SK_facility_data)-1


if __name__ == '__main__':
		
	from .well_search import well_search
	from .dates_array import dates_array
	from .OPGEE_defaults import OPGEE_defaults
	from .general_well_data_analysis import OPGEE_well_data
	from .OPGEE_input_sensitivity import OPGEE_input_sensitivity
	from .get_all_post_2005_well_data import get_all_post_2005_well_data, get_tight_oil_wells

	#well_data_headings, well_data, project_name = well_search()
	#well_data_headings, well_data = get_all_post_2005_well_data()
	#well_data_headings, well_data = get_formation_well_data() # MONTNEY
	#well_data = [] #collec all facility data
	well_data_headings, well_data = get_tight_oil_wells()
	well_data = []

	date_array = dates_array('2015-01','2015-12')

	OPGEE_data = OPGEE_defaults()

	OPGEE_data = OPGEE_well_data(well_data, well_data_headings, OPGEE_data)

	OPGEE_data, province_facility_total, count_SK_wells, count_SK_facilities = SK_facility_analysis(well_data, well_data_headings, OPGEE_data, date_array)

	OPGEE_input_sensitivity(OPGEE_data, well_data)