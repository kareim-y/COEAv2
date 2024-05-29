import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import csv
import collections
import pylab
import datetime
import re
#from plot_basemap import plot_basemap
import time
from get_all_post_2005_well_data import get_tight_oil_wells
from map_to_drive import map_to_drive #path to Project Data folder

def get_all_monthly_facility_data(year_month, from_to_facility,facility_connection_dates):

	print('\nImporting All Facility Data for :' + str(year_month))
	timer = time.time()

	#gets data for all facilities in the given year-month
	#taken in ordered dictionary facilty_connections, we want this to update if we assess multiple months

	all_facility_data = collections.OrderedDict() #Getting data from the csv referenced to facilityID

	Battery_FFV_folder = map_to_drive() + "/Project Data/AER/facility_volumetrics/"
	Battery_FFV_File = "Vol_" + year_month + ".csv"

	Battery_FFV = Battery_FFV_folder + Battery_FFV_File + "/" + Battery_FFV_File
	count = 0;
	switch = 0;

	data_start_count = 100 # make this a high number to begin with

	with open(Battery_FFV) as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row) > 0:
				if row[0] == 'ProductionMonth':
					facility_data_headings = row
					for i in range(0,len(row)):
						if row[i] == 'ReportingFacilityID':
							fac_ID_index = i
						if row[i] == 'FromToID':
							fromto_ID_index = i
						if row[i] == 'ReportingFacilitySubTypeDesc':
							subtype_index = i

						data_start_count = count
				
				if count > data_start_count + 1:

					facility_ID = row[fac_ID_index]
					subtype =  row[subtype_index]

					#if subtype not in facility_type_of_interest: #limit to certain facility type

					if facility_ID not in all_facility_data:
						all_facility_data[facility_ID] = [row]
					if facility_ID in all_facility_data:
						all_facility_data[facility_ID].append(row)


					from_ID = row[fromto_ID_index]
					if from_ID[0:4] == 'ABWI':
						from_ID = from_ID[4:]

			
					if from_ID not in from_to_facility:
						from_to_facility[from_ID] = [facility_ID] #well to facility 
					else:
						from_to_facility[from_ID].append(facility_ID)

					# Get dates which facilities are connected
					# key to dict will be facility + ' to ' + well
					dates_key = facility_ID + ' to ' + from_ID
					if dates_key not in facility_connection_dates:
						facility_connection_dates[dates_key] = [year_month]
					elif year_month not in facility_connection_dates[dates_key]: 
						facility_connection_dates[dates_key].append(year_month)



			count = count + 1

	print('Computational Time (s): ' + "%.4f" %(time.time() - timer))

	
	#print(facility_data['ABBT0051211'])
	#print('\n')
	#print(facility_connections['ABBT0051211'])

	return facility_data_headings, all_facility_data, from_to_facility, facility_connection_dates


def AB_formation_facility_list(from_to_facility, well_data, facility_to_well, connected_wells, all_facility_data, facility_data_headings):

	#takes in the from_to_facilities and the formation well data to determing which facilities are connected to project wells


	timer = time.time()
	#facility type index 

	formation_facility_list = []

	#we can limit out search to facilities of a certain type:
	subtype_index = facility_data_headings.index('ReportingFacilitySubTypeDesc')
	
	excluded_facility_type = [] 
	included_facility_type = []
	#excluded_facility_type = ['DRILLING AND COMPLETING '] 
	#included_facility_type = ['CRUDE OIL SINGLE-WELL BATTERY']

	#print('Excluding facility type ' + str(facility_type_of_interest))

	if len(well_data) > 0:

		print('\nGetting facility list for selected wells')

		for well in well_data:

			if well in from_to_facility:

				for facility in from_to_facility[well]:
					
					#comment blow line out for all facilities
					#if 'BATTERY' in all_facility_data[facility][0][subtype_index]: 
					if all_facility_data[facility][0][subtype_index] not in excluded_facility_type:

						if well not in connected_wells:
							connected_wells.append(well)

						if facility not in formation_facility_list:
							formation_facility_list.append(facility)
						
						if facility not in facility_to_well:
							facility_to_well[facility] = []

						if well not in facility_to_well[facility]:
							facility_to_well[facility].append(well)
							


		print('Number of AB facilities connected to project wells (this month):  '+ str(len(formation_facility_list)))
		print('Number of project wells producing to facilities (total):  '+ str(len(connected_wells)))
		if len(excluded_facility_type) > 0:
			print('Excluded facility types - ' + str(excluded_facility_type))
		if len(included_facility_type) > 0:
			print('The following facility types are being assessed - ' + str(included_facility_type))
		print('Computational Time (s): ' + "%.4f" %(time.time() - timer))
		#print('\n')
	
	if len(well_data) == 0:
		print('\nASSESSING ALL ALBERTAN FACILITIES')
		print('Number of Albertan Facilities Opertating (this month); ' + str(len(all_facility_data)))
		print('Computational Time (s): ' + "%.4f" %(time.time() - timer))
		
		formation_facility_list = -1
		#formation_facility_list = ['ABIF0009895']

	return formation_facility_list, facility_to_well, connected_wells


def get_formations_facility_data(all_facility_data, facility_data_headings, formation_facility_list, selected_facility_data):

	#selected_facility_data is an OrderedDict being passed through

	print('\nGetting facility data for selected wells')
	timer = time.time()

	if formation_facility_list == -1:

		#WE ARE LOOKING AT ALL FACILITIES!!

		formation_facility_list = all_facility_data

	if len(formation_facility_list) == 0:

		#WE COULD NOT FIND ANY FACILIIES

		formation_facility_list = []

	for facility in formation_facility_list:

		if facility in selected_facility_data:

			selected_facility_data[facility].extend(all_facility_data[facility])

		if facility not in selected_facility_data:
			
			selected_facility_data[facility] = all_facility_data[facility]


	print('Computational Time (s): ' + "%.4f" %(time.time() - timer))
	#print('\n')


	return selected_facility_data

def gas_plant_from_facility(formation_facility_list, from_to_facility, facility_data_headings, all_facility_data):

	print('Adding GP facilities connected to batteries')

	fac_type_index = facility_data_headings.index('ReportingFacilityType')
	fac_type_index = facility_data_headings.index('ReportingFacilityID')

	checked_facilities = [] #an array of facilities we have checked so we dont repear
	connected_GPs = []

	#finding facilities connected to facilities connected to project wells (E.g gas processing plants and gathering systems)
	for from_facility in formation_facility_list:
		if from_facility in from_to_facility:
			connected_facilities = from_to_facility[from_facility]
			#print(from_facility, connected_facilities)
			for facility in connected_facilities:
				if facility not in checked_facilities:
					checked_facilities.append(facility)
					if ('GP') in facility:
						connected_GPs.append(facility)

	for facility in connected_GPs:
		if facility not in formation_facility_list:
			formation_facility_list.append(facility)

	return connected_GPs #this will just return the secondary connected facilities 
	#return formation_facility_list

def AB_facility_data_summary(facility_data_headings, selected_facility_data, facility_summary):

	
	#takes in the selected facility data and organises it by date and activity_product type

	print('\nCalculating All Facility Summary Data')
	timer = time.time()

	list_of_all_activites = []

	ActivityID_index = facility_data_headings.index('ActivityID')
	ProductID_index = facility_data_headings.index('ProductID')
	ProductionMonth_index = facility_data_headings.index('ProductionMonth')
	Volume_index = facility_data_headings.index('Volume')

	if 'ALL' not in facility_summary:

		#make an entry for the total facility data 

		facility_summary['ALL'] = collections.OrderedDict()

	for facility in selected_facility_data:
		
		for entry in range(0,len(selected_facility_data[facility])):

			#print(selected_facility_data[facility][entry])

			year_month = selected_facility_data[facility][entry][ProductionMonth_index]

			if year_month not in facility_summary['ALL']:

				facility_summary['ALL'][year_month] = collections.OrderedDict()


			Activity_Product = str(selected_facility_data[facility][entry][ActivityID_index]) + ' ' + str(selected_facility_data[facility][entry][ProductID_index])

			try:

				if Activity_Product not in facility_summary['ALL'][year_month]:

					facility_summary['ALL'][year_month][Activity_Product] = float(selected_facility_data[facility][entry][Volume_index])

					list_of_all_activites.append(Activity_Product)

				else:

					facility_summary['ALL'][year_month][Activity_Product] = facility_summary['ALL'][year_month][Activity_Product] + float(selected_facility_data[facility][entry][Volume_index])

			except:

				pass


	print('Computational Time (s): ' + "%.4f" %(time.time() - timer))
	
	#print('\n')
	#print out of all activities 
	#print(list_of_all_activites)

	return facility_summary


def single_facility_OPGEE(facility_summary, OPGEE_data, facility_to_well, geoscout_fac_data, geoscout_fac_data_headings,facility_connection_dates):

	print('\nCollecting OPGEE FFV inputs for wells\n')

	m3_scf = 35.314666
	m3_bbl = 6.2898

	activities = activities = ['PROD GAS', 'FLARE GAS', 'VENT GAS', 'FUEL GAS', 'PROD COND','PROD OIL', 'REC GAS', 'DISP GAS','PURREC GAS']
	wells_with_fac_data = []
	impossible_FFV = [] #wells with FFV rates greater tham 100%
	well_cumulative = collections.OrderedDict()
	well_to_fac_type = collections.OrderedDict()
	well_to_fac_name = collections.OrderedDict()

	for facility in facility_summary:
		#if 'BT' in facility:
		if len(facility_summary[facility]) > 0:
			#only consider batteries 
			period_cumulative = np.zeros(len(activities))
			
			if facility != 'ALL':
				try:
					fac_type = geoscout_fac_data[facility][geoscout_fac_data_headings.index('Sub Type')]
				except:
					fac_type = 'Unknown'

				
				for well in facility_to_well[facility]:
					dates_key = facility + ' to ' + well
					for year_month in facility_summary[facility]:
						if year_month in facility_connection_dates[dates_key]:
							for product in facility_summary[facility][year_month]:
								if product in activities:
									period_cumulative[activities.index(product)] += facility_summary[facility][year_month][product]


					if well in OPGEE_data:
						#print(dates_key,facility_connection_dates[dates_key])
						if well not in well_cumulative:
							well_cumulative[well] = period_cumulative
							well_to_fac_type[well] = [fac_type]
							well_to_fac_name[well] = [facility]
						elif well in well_cumulative:
							well_to_fac_type[well].append(fac_type)
							well_to_fac_name[well].append(facility)
							well_cumulative[well] = [sum(x) for x in zip(well_cumulative[well],period_cumulative)]
	

	for well in well_cumulative:
		if well not in wells_with_fac_data:
			wells_with_fac_data.append(well)

			prod_oil = float(well_cumulative[well][activities.index('PROD OIL')]*m3_bbl)
			prod_cond = float(well_cumulative[well][activities.index('PROD COND')]*m3_bbl)
			fuel_gas = float(well_cumulative[well][activities.index('FUEL GAS')]*1000*m3_scf)
			flare_gas = float(well_cumulative[well][activities.index('FLARE GAS')]*1000*m3_scf)
			vent_gas = float(well_cumulative[well][activities.index('VENT GAS')]*1000*m3_scf)
			prod_gas = float(well_cumulative[well][activities.index('PROD GAS')]*1000*m3_scf)
			rec_gas = float(well_cumulative[well][activities.index('REC GAS')]*1000*m3_scf)
			purrec_gas = float(well_cumulative[well][activities.index('PURREC GAS')]*1000*m3_scf)

			#get well GOR 
			try:
				fac_type = well_to_fac_type[well] 
				fac_name = well_to_fac_name[well]
			except: 
				fac_type = 'UNKNOWN'
				fac_name = 'UNKNOWN'


			well_GOR = OPGEE_data[well][OPGEE_data['headings'].index('Gas-to-oil ratio (GOR)')]
			OPGEE_data[well][OPGEE_data['headings'].index('Facility name')] = str(fac_name)
			OPGEE_data[well][OPGEE_data['headings'].index('Facility type')] = str(fac_type)
			
			if (fuel_gas + flare_gas + vent_gas) > 1.05*(prod_gas + rec_gas + purrec_gas):
				impossible_FFV.append(well)
				OPGEE_data[well][OPGEE_data['headings'].index('Facility flared gas')] = 'FFV>100%, set to 0'
				OPGEE_data[well][OPGEE_data['headings'].index('Facility vented gas')] = 0
				OPGEE_data[well][OPGEE_data['headings'].index('Facility fuel gas')] = 0.001
				OPGEE_data[well][OPGEE_data['headings'].index('Flaring-to-oil ratio')] = 0
				OPGEE_data[well][OPGEE_data['headings'].index('Venting-to-oil ratio')] = 0
				continue

			if (prod_gas + rec_gas) > 0:
				OPGEE_data[well][OPGEE_data['headings'].index('Facility flared gas')] = round(flare_gas/(prod_gas + rec_gas + purrec_gas)*100,4)
				OPGEE_data[well][OPGEE_data['headings'].index('Facility vented gas')] = round(vent_gas/(prod_gas + rec_gas + purrec_gas)*100,4)
				fuel_gas_rate = round(fuel_gas/(prod_gas + rec_gas + purrec_gas)*100,4)
				if fuel_gas_rate == 0:
					fuel_gas_rate = 0.001
				OPGEE_data[well][OPGEE_data['headings'].index('Facility fuel gas')] = fuel_gas_rate
				#update well flare and vent data in terms of scf/bbl
				OPGEE_data[well][OPGEE_data['headings'].index('Flaring-to-oil ratio')] = round(well_GOR*(flare_gas/(prod_gas + rec_gas + purrec_gas))*0.99,4)
				OPGEE_data[well][OPGEE_data['headings'].index('Venting-to-oil ratio')] = round(well_GOR*(vent_gas/(prod_gas + rec_gas + purrec_gas))*0.99,4)

			else:
				OPGEE_data[well][OPGEE_data['headings'].index('Facility flared gas')] = 0
				OPGEE_data[well][OPGEE_data['headings'].index('Facility vented gas')] = 0
				OPGEE_data[well][OPGEE_data['headings'].index('Facility fuel gas')] = 0.001
				#update well flare and vent data in terms of scf/bbl
				OPGEE_data[well][OPGEE_data['headings'].index('Flaring-to-oil ratio')] = 0
				OPGEE_data[well][OPGEE_data['headings'].index('Venting-to-oil ratio')] = 0

			if (prod_oil + prod_cond) > 0:
				OPGEE_data[well][OPGEE_data['headings'].index('Facility gas-to-oil ratio')] = (prod_gas + rec_gas + purrec_gas)/(prod_oil + prod_cond)
			else:
				OPGEE_data[well][OPGEE_data['headings'].index('Facility gas-to-oil ratio')] = 0 

			

	#Do something about wells with impossible FFV rates 								
	print('Unique FFV Data added to ' + str(len(wells_with_fac_data)) + ' wells')
	print('Impossible FFV rates (>100%) were found for ' + str(len(impossible_FFV)) + ' wells')
	print('Fuel, flare and vent rates for these wells have been set to zero')


	#for well in OPGEE_data:
	#	if well in well_to_fac:
	#		print(well,well_to_fac[well])
	#	else:
	#		print(well,0)

	return OPGEE_data	


def AB_single_facility_data_summary(facility_data_headings, selected_facility_data, single_facility_summary):

	
	#takes in the selected facility data and organises it by date and activity_product type for each well

	print('\nCalculating Single Facility Summary Data')
	timer = time.time()


	ActivityID_index = facility_data_headings.index('ActivityID')
	ProductID_index = facility_data_headings.index('ProductID')
	ProductionMonth_index = facility_data_headings.index('ProductionMonth')
	Volume_index = facility_data_headings.index('Volume')



	for facility in selected_facility_data:

		for entry in range(0,len(selected_facility_data[facility])):

			year_month = selected_facility_data[facility][entry][ProductionMonth_index]

			Activity_Product = str(selected_facility_data[facility][entry][ActivityID_index]) + ' ' + str(selected_facility_data[facility][entry][ProductID_index])

			#for a single activity product e.g INJ CO2
			#if Activity_Product in ['INJ CO2']:

			if facility not in single_facility_summary:

				single_facility_summary[facility] = collections.OrderedDict()

			if year_month not in single_facility_summary[facility]:

				single_facility_summary[facility][year_month] = collections.OrderedDict()

			try:

				if Activity_Product not in single_facility_summary[facility][year_month]:


					single_facility_summary[facility][year_month][Activity_Product] = float(selected_facility_data[facility][entry][Volume_index])

				else:

					single_facility_summary[facility][year_month][Activity_Product] = single_facility_summary[facility][year_month][Activity_Product] + float(selected_facility_data[facility][entry][Volume_index])

			except:

					pass


	print('Computational Time (s): ' + "%.4f" %(time.time() - timer))
	#print('\n')

	return single_facility_summary


def geoscout_facility_data(selected_facility_data):

	print('\nImporting AB data from geoSCOUT export\n')

	#only getting the facilities of interest

	geoscout_facility_data = collections.OrderedDict() #Getting data from the csv referenced to facilityID
	
	facility_data_file_location = map_to_drive() + "/Project Data/geoSCOUT_data/AB_all_facilities.csv"
	
	with open(facility_data_file_location) as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == 'Unique Facility ID':
				geoscout_facility_data_headings = row
				fac_ID_index = geoscout_facility_data_headings.index('Unique Facility ID')

			if row[0] != 'Unique Facility ID':
				fac_ID = row[fac_ID_index]
				if fac_ID in selected_facility_data:
					geoscout_facility_data[fac_ID] = row

	return geoscout_facility_data, geoscout_facility_data_headings

def geoscout_facility_info(facility_ID, return_type, geoscout_facility_data, geoscout_facility_data_headings):

	#takes in a facility ID, return_type geoscout_facility_data, geoscout_facility_data_headings
	#return type example - 'Sub Type' (single crude battery) or 'Latitude'

	return_value = geoscout_facility_data[facility_ID][geoscout_facility_data_headings.index(return_type)]

	return return_value

#-----------------plot flare data on a map ----------------------

def facility_summary_print(facility_summary, facility, connected_wells, facility_to_well,geoscout_fac_data, geoscout_fac_data_headings):

	m3_scf = 35.315
	m3_bbl = 6.2898

	#get header data from geoscout for the facility_type_count

	fac_type_index = geoscout_fac_data_headings.index('Sub Type')

	facility_type_count = collections.Counter()

	all_facility_data = facility_summary[facility]

	#count and type of facilty
	for fac in geoscout_fac_data:
		fac_type = geoscout_fac_data[fac][fac_type_index]
		facility_type_count[fac_type] += 1
		if fac == facility:
			#this is the data of the individual facility 
			single_fac = fac

	if facility not in geoscout_fac_data:
		single_fac = 'GeoSCOUT Facility Data Missing'

	activities_of_interest = ['PROD GAS','FLARE GAS','VENT GAS','FUEL GAS','PROD COND','PROD OIL','REC GAS','DISP GAS','PURREC GAS','INJ CO2','INJ WATER']#,'DISP GAS','REC GAS']

	#print out data for all facilities over the assessed period
	date_volumes = collections.OrderedDict()
	for date in all_facility_data:
		date_volumes[date] = []
		for activity in activities_of_interest:
			if activity in all_facility_data[date]:
				date_volumes[date].append(all_facility_data[date][activity])
			elif activity not in all_facility_data[date]:
				date_volumes[date].append(0)

	if facility == 'ALL':
		print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nSummary of All Connected facilities\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
		print('Total Number of Connected Facilities', len(facility_summary) - 1)
		print('\n')
		print('FACILITY TYPE AND COUNT\n')
		for key in sorted(facility_type_count.keys()):
			print(key + '; ' + str(facility_type_count[key]))
		print('\n')
		print('Total Number of Connected Project Wells', len(connected_wells))
		print('\n')
	
	elif facility != 'ALL':
		print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nSummary of facility ' + facility + '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
		print('\n')
		if single_fac != 'GeoSCOUT Facility Data Missing':
			for i in range(0,13):
				print(geoscout_fac_data_headings[i],geoscout_fac_data[single_fac][i]) #just give first 15 headings 
			print('\nCONNECTED WELLS\n')
		else:
			print('\nGeoSCOUT Facility Data Missing\n')
		try:
			print(facility_to_well[single_fac])
		except:
			print('No connected wells could be found')
		print('\n')
	
	print('Year-Month',activities_of_interest)
	print('\n')
	totals = np.zeros(len(activities_of_interest))

	for date in date_volumes:
		print(date + ', ' + str([np.round(x,1) for x in date_volumes[date]]))
		totals = [x + y for x, y in zip(totals,date_volumes[date])]
	print('\n')
	print('Totals',[np.round(x) for x in totals])

	#add a print of GOR at the facility level
	prod_oil = totals[activities_of_interest.index('PROD OIL')] + totals[activities_of_interest.index('PROD COND')]
	inlet_gas = totals[activities_of_interest.index('PROD GAS')] + totals[activities_of_interest.index('REC GAS')]

	if prod_oil == 0:
		fuel_rate = 0
		flare_rate = 0
		vent_rate = 0
		gas_oil_ratio = 0
			
	elif prod_oil != 0:
		fuel_rate = (totals[activities_of_interest.index('FUEL GAS')]*1000*m3_scf)/(totals[activities_of_interest.index('PROD OIL')]*m3_bbl+ totals[activities_of_interest.index('PROD COND')]*m3_bbl)
		flare_rate = (totals[activities_of_interest.index('FLARE GAS')]*1000*m3_scf)/(totals[activities_of_interest.index('PROD OIL')]*m3_bbl+ totals[activities_of_interest.index('PROD COND')]*m3_bbl)
		vent_rate = (totals[activities_of_interest.index('VENT GAS')]*1000*m3_scf)/(totals[activities_of_interest.index('PROD OIL')]*m3_bbl + totals[activities_of_interest.index('PROD COND')]*m3_bbl)
		gas_oil_ratio = (totals[activities_of_interest.index('PROD GAS')]*1000*m3_scf)/(totals[activities_of_interest.index('PROD OIL')]*m3_bbl + totals[activities_of_interest.index('PROD COND')]*m3_bbl)

	if inlet_gas > 0:
		fuel_percentage =  (totals[activities_of_interest.index('FUEL GAS')])/(totals[activities_of_interest.index('PROD GAS')] + totals[activities_of_interest.index('REC GAS')])
		flare_percentage =  (totals[activities_of_interest.index('FLARE GAS')])/(totals[activities_of_interest.index('PROD GAS')] + totals[activities_of_interest.index('REC GAS')])
		vent_percentage =  (totals[activities_of_interest.index('VENT GAS')])/(totals[activities_of_interest.index('PROD GAS')] + totals[activities_of_interest.index('REC GAS')])
	elif inlet_gas == 0:
		fuel_percentage = 0	
		flare_percentage = 0
		vent_percentage = 0	



	print('\nGas Consumption (percent of inlet)')
	print('Fuel Gas ("%"); ' + str(round(fuel_percentage*100,3)))
	print('Flare Gas ("%"); ' + str(round(flare_percentage*100,3)))
	print('Vent Gas ("%"); ' + str(round(vent_percentage*100,3)))

	print('\nFacility Gas Oil Ratio (scf/bbl); ' + str(round(gas_oil_ratio,2)))

	print('\nFuel Flare Vent Rates (scf/bbl)')
	print('Fuel Rate (scf/bbl); ' + str(round(fuel_rate,2)))
	print('Flare Rate (scf/bbl); ' + str(round(flare_rate,2)))
	print('Vent Rate (scf/bbl); ' + str(round(vent_rate,2)))

	print('\n')

	return


def AB_facility_analysis(well_data, well_data_headings, OPGEE_data, dates_array):
	
	print('\n')
	
	if len(well_data) != 0:
		ask_include_GP = str(raw_input('Would you like to include Gas Processing Plants? (Y/N) :    '))
		print('\n')
	else:
		ask_include_GP = 'N'

	facility_summary = collections.OrderedDict()
	single_facility_summary = collections.OrderedDict()
	facility_to_well = collections.OrderedDict()
	facility_connection_dates = collections.OrderedDict() #facility_connection_dates[facility + ' to ' + well] = [month1, month2, month3..]
	connected_wells = []


	for year_month in dates_array:

		selected_facility_data = collections.OrderedDict()
		facility_connections = collections.OrderedDict() #resets every iteration

		facility_data_headings, all_facility_data, from_to_facility,facility_connection_dates = get_all_monthly_facility_data(year_month, facility_connections,facility_connection_dates)

		formation_facility_list, facility_to_well, connected_wells = AB_formation_facility_list(from_to_facility, well_data, facility_to_well, connected_wells, all_facility_data, facility_data_headings)

		#add conected facilities 
		if ask_include_GP[0].upper() == 'Y':
			formation_facility_list = gas_plant_from_facility(formation_facility_list, from_to_facility, facility_data_headings, all_facility_data)

		#Dictionary containing data for facilities in the formation
		selected_facility_data = get_formations_facility_data(all_facility_data, facility_data_headings, formation_facility_list, selected_facility_data)

		#summary of ALL facility data!
		facility_summary = AB_facility_data_summary(facility_data_headings, selected_facility_data, facility_summary)

		#summary of single facility data
		#we can delete this when looking at ALL facilities to save data/time 
		facility_summary = AB_single_facility_data_summary(facility_data_headings, selected_facility_data, facility_summary)

		del all_facility_data #clear from mem

	geoscout_fac_data, geoscout_fac_data_headings = geoscout_facility_data(facility_summary)
	
	facility_summary_print(facility_summary, 'ALL', connected_wells, facility_to_well, geoscout_fac_data, geoscout_fac_data_headings)

	#single faclity print out 
	ask_single_fac_print = str(raw_input('\nWould you like a print out of each facility? (Y/N):   '))

	if ask_single_fac_print[0].upper() == 'Y':

		for facility in facility_summary:
			print('\nFacility ' + str(facility_summary.keys().index(facility)) + ' of ' + str(len(facility_summary)))
			facility_summary_print(facility_summary, facility, connected_wells, facility_to_well, geoscout_fac_data, geoscout_fac_data_headings)

	#print(facility_summary['ALL'])

	if formation_facility_list != -1:

		OPGEE_data = single_facility_OPGEE(facility_summary, OPGEE_data, facility_to_well, geoscout_fac_data, geoscout_fac_data_headings, facility_connection_dates)

	#for well in OPGEE_data:
	#	print(well, OPGEE_data[well][OPGEE_data['headings'].index('Facility flared gas')],OPGEE_data[well][OPGEE_data['headings'].index('Facility vented gas')], OPGEE_data[well][OPGEE_data['headings'].index('Facility fuel gas')])								
						

	return OPGEE_data, facility_summary['ALL'], len(connected_wells), len(facility_summary) - 1


if __name__ == '__main__':

	from well_search import well_search
	from OPGEE_defaults import OPGEE_defaults
	from general_well_data_analysis import OPGEE_well_data, general_well_data_analysis
	from dates_array import dates_array
	from OPGEE_input_sensitivity import OPGEE_input_sensitivity
	#from LNG_well_search import LNG_well_search

	#well_data_function = get_formation_well_data() # MONTNEY
	well_data_function = well_search()
	#well_data_function = get_tight_oil_wells()
	#well_data_function = LNG_well_search()

	well_data_headings = well_data_function[0] 
	well_data = well_data_function[1] 
	#well_data = []

	OPGEE_data = OPGEE_defaults()

	OPGEE_data = OPGEE_well_data(well_data, well_data_headings, OPGEE_data)

	dates_array = dates_array = dates_array('2017-01','2017-12')
	#dates_array = ['2017-06']

	OPGEE_data, province_facility_total, count_AB_wells, count_AB_facilities = AB_facility_analysis(well_data, well_data_headings, OPGEE_data, dates_array)

	#for well in OPGEE_data:
	#print(OPGEE_data['assessed field'][OPGEE_data['headings'].index('Flaring-to-oil ratio')])
	#print(OPGEE_data['defaults'][OPGEE_data['headings'].index('Flaring-to-oil ratio')])

	#OPGEE_input_sensitivity(OPGEE_data, well_data)