import os
import csv
import collections
import numpy as np
#from plot_basemap import plot_basemap, montney_shape_plot
#from map_plotter import map_plotter
from well_plotter import get_well_coordinates
import matplotlib.pyplot as plt
#import shapefile
#from shapely.geometry import Point
#from shapely.geometry.polygon import Polygon
import re
from OPGEE_input_sensitivity import OPGEE_input_sensitivity
import datetime
from map_to_drive import map_to_drive #path to Project Data folder


def get_BC_facility_links():

	print('\nGetting BC Facility to Well Connections')
	facility_links_location = map_to_drive() + "/Project Data/BCOGC/BC_facility_linkage.csv"
	BC_facility_links = collections.OrderedDict()
	

	#A switch for when we want to start storing csv data
	switch = 0

	with open(facility_links_location) as f:
		reader = csv.reader(f)
		for row in reader:

			if switch == 1:
				#we will index the dictionary with well WA numbers
				if row[FROMWANUM_index] != 'NULL':
					if row[fac_subtype] == 'GP': #excludein include certain facility types 
						if row[FROMWANUM_index] not in BC_facility_links:
							BC_facility_links[row[FROMWANUM_index]] = [row]
						else:
							BC_facility_links[row[FROMWANUM_index]].append(row)

			if row[0] == 'FACILITYID':
				BC_facility_links_headers = row
				FACILITYID_index = row.index("FACILITYID")
				FROMWANUM_index = row.index("FROMWANUM")
				fac_subtype = row.index('FACILITYTYPE_CODE')

				switch = 1

	#print('\nFacility Link Data Obtained\n')
	print('Available Data - Indexed by well WA')
	print(BC_facility_links_headers)
	print('\n')

	return BC_facility_links, BC_facility_links_headers

def get_BC_facility_list(well_data, well_data_headers, BC_facility_links, BC_facility_links_headers, BC_facility_index, BC_facility_index_headings):
	
	
	print('\nGetting List of BC facilities Connected to Project Wells')

	fac_type_index = BC_facility_index_headings.index('Facility Type')

	WA_to_UWI = collections.OrderedDict()
	facility_to_WA = collections.OrderedDict()

	FACILITYID_index = BC_facility_links_headers.index("FACILITYID")

	BC_facility_list = []
	connected_WA = []

	# if we have a set of wells we want to assess
	#selected_facility_type = 'Dehydrator' #Gas Processing Plant
	#selected_facility_type = 'Processing Plant' #Gas Processing Plant
	selected_facility_type = 'Battery'


	if len(well_data) > 0:

		WA_num = well_data_headers.index("Lic/WA/WID/Permit #")

		#get the WA numbers for each well
		for well in well_data:
			well_WA = well_data[well][WA_num]
			WA_to_UWI[well_WA] = well

		for WA in WA_to_UWI:
			
			#check if the wells in our list are connected to BC facilities

			if WA in BC_facility_links:
				
				connected_WA.append(WA) #append to connected WA list
				
				#we also want a list of the connected facilities
				for i in range(0,len(BC_facility_links[WA])):
					facility = BC_facility_links[WA][i][FACILITYID_index]
					fac_type = fac_type = BC_facility_index[facility][0][fac_type_index]
					#if selected_facility_type in fac_type:
					if facility not in BC_facility_list:
						BC_facility_list.append(facility) #list of facilities

				#we want to know which facilities connect to which WA's

					if facility not in facility_to_WA:
						facility_to_WA[facility] = [WA]
					if facility in facility_to_WA:
						if WA not in facility_to_WA[facility]:
							facility_to_WA[facility].append(WA)

# if we are assessing all wells/facilities 

	if len(well_data) == 0:

		print('We are assessing ALL BC facilities!!')


		for WA in BC_facility_links:
				
			if WA not in connected_WA:
				connected_WA.append(WA) #append to connected WA list
				
			#we also want a list of the connected facilities
			for i in range(0,len(BC_facility_links[WA])):
				facility = BC_facility_links[WA][i][FACILITYID_index]
				if facility not in BC_facility_list:
					BC_facility_list.append(facility) #list of facilities

				#we want to know which facilities connect to which WA's
				if facility not in facility_to_WA:
					facility_to_WA[facility] = [WA]
				if facility in facility_to_WA:
					if WA not in facility_to_WA[facility]:
						facility_to_WA[facility].append(WA)

	#print outs

	if len(well_data) > 0:
		print('Total Number of Connected Wells in Our Dataset:  ' + str(len(connected_WA)))
	if len(well_data) == 0:
		print('Total Number of Connected Wells/Facilites to Facilities (Facilities can connect to facilites):  ' + str(len(connected_WA)))
	print('Total Number of Connected facilities:  ' + str(len(BC_facility_list)))

	#print('WA - 27043')
	#print(BC_facility_links['27043'])

	return connected_WA, BC_facility_list, WA_to_UWI, facility_to_WA


def get_BC_facility_data(date_array, BC_facility_list):

	#date array is of the form [2016-01, 2016-02..... 2017-03]
	#given BC facility data is stored in yearly files, we want the year files we should search


	years_array = [] #an array of the year files we will search
	
	for year_month in date_array:
		year = year_month[0:4]
		if year not in years_array:
			years_array.append(year)

	#first we need to change our facility code format to match --123 goes to 00000123
	#BC_facility_list = convert_facility_code(BC_facility_list)

	BC_facility_data = collections.OrderedDict()

	for year in years_array:

		print('Getting BC facility Data for ' + str(year))

		BC_facility_data_path = map_to_drive() + "/Project Data/BCOGC/facility_volumetrics/" + year + ".csv"

		switch = 0

		with open(BC_facility_data_path) as f:
			
			reader = csv.reader(f)
			
			for row in reader:

				if switch == 1:
					
					FAC_ID_CODE = row[FAC_ID_CODE_index]
					#Format Date
					year_month = row[date_index][:4] + '-' + row[date_index][-2:]
	
					if FAC_ID_CODE in BC_facility_list: #comment this for ALL facilites?
						#select by FAC Type
						if FAC_ID_CODE not in BC_facility_data:
							BC_facility_data[FAC_ID_CODE] = collections.OrderedDict()
						if year_month in date_array:
							if year_month not in BC_facility_data[FAC_ID_CODE]:
								BC_facility_data[FAC_ID_CODE][year_month] = collections.OrderedDict()
							#iterate through products excluding facID and date
							for volume in range(1,len(row) -1):
								activity_product = BC_facility_data_headings[volume]
								if activity_product not in BC_facility_data[FAC_ID_CODE][year_month]:
									BC_facility_data[FAC_ID_CODE][year_month][activity_product] = 0
								if row[volume] == 'NULL':
									row[volume] = 0
								BC_facility_data[FAC_ID_CODE][year_month][activity_product] += float(row[volume])

				if row[0] == "FAC_ID_CODE":
					BC_facility_data_headings = row
					#rename 'TOT RECPTS GAS' 'REC GAS'
					BC_facility_data_headings[BC_facility_data_headings.index('TOT RECPTS GAS')] = 'REC GAS'
					BC_facility_data_headings[BC_facility_data_headings.index('TOT DELVRS GAS')] = 'DISP GAS'
					FAC_ID_CODE_index = row.index("FAC_ID_CODE")
					date_index = row.index('PROD_PERIOD')
					switch = 1


	#print data 

	print('\nAvailable Data - Indexed by well FAC_ID_CODE\n')
	print(BC_facility_data_headings)
	#print('\nExample data for facility 7743\n')
	#print(BC_facility_data['7743'])


	return BC_facility_data, BC_facility_data_headings

def BC_facility_data_summary(BC_facility_data, BC_facility_data_headings, date_array):

	if len(BC_facility_data) > 1:
		print('\nSummarizing BC Facility Data....\n')

	#search is based on BC_facility_list
	#check if out facility is connected and active in the facility data
	#returnss Ordered dict summarizing over the period by year month

	activities_of_interest = BC_facility_data_headings[1:-1]

	#we must first convert the dates in date_array from 2016-01 to 201601

	#initialize empty summary dicitionary
	BC_facility_data['ALL'] = collections.OrderedDict()
	for year_month in date_array:
		BC_facility_data['ALL'][year_month] = collections.OrderedDict()
		for activity in activities_of_interest:
			BC_facility_data['ALL'][year_month][activity] = 0

	#fill summary with data from facilities
	for facility in BC_facility_data:
		if facility != 'ALL': #dont want to double count
			for year_month in BC_facility_data[facility]:
				if year_month in date_array:
					for activity_product in BC_facility_data[facility][year_month]:
						BC_facility_data['ALL'][year_month][activity_product] += BC_facility_data[facility][year_month][activity_product]

	#reorganise by dates ascending
	sorted_BC_facility_data = collections.OrderedDict()
	for facility in BC_facility_data:
		sorted_BC_facility_data[facility] = collections.OrderedDict()
		for year_month in date_array:
			if year_month in BC_facility_data[facility]:
				sorted_BC_facility_data[facility][year_month] = BC_facility_data[facility][year_month]

	del BC_facility_data

	return sorted_BC_facility_data


def print_facility_summary(facility_name, well_data, BC_facility_data, BC_facility_data_headings, WA_to_UWI, facility_to_WA, BC_facility_index, BC_facility_index_headings):

	m3_scf = 35.314666
	m3_bbl = 6.2898

	facility = facility_name

	print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	print('  BC FACILITY SUMMARY : ' + str(facility_name) )
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	
	#connected wells - different for All Facilities vs Single Facility

	connected_wells = []
	connected_wells_UWI = [] 
	project_connected_wells = []

	#facility information indexing

	fac_type_index = BC_facility_index_headings.index('Facility Type')
	fac_type_count = collections.Counter()
	
	if facility == 'ALL':
		try: #this does not work when we get all facilites
			for key in facility_to_WA:
				for WA in facility_to_WA[key]:
					
					if WA not in connected_wells: #total connected wells
						connected_wells.append(WA)
					
					if WA_to_UWI[WA] in well_data: #project connected wells
						if WA_to_UWI[WA] not in project_connected_wells:
							project_connected_wells.append(WA_to_UWI[WA])
				
				fac_type = BC_facility_index[key][0][fac_type_index]
				fac_type_count[fac_type] += 1

			print('\nFACILITY TYPE AND COUNT\n')
			fac_count = 0
			for key in sorted(fac_type_count.keys()):
				print(key + '; ' + str(fac_type_count[key]))
				fac_count += fac_type_count[key]
			print('Total; ' + str(fac_count)) #total of all facilities 
		except:
			pass

	if facility != 'ALL':
		connected_wells = facility_to_WA[facility]
		for WA in facility_to_WA[facility]:
			if WA_to_UWI[WA] in well_data: #project connected wells
				if WA_to_UWI[WA] not in project_connected_wells:
					project_connected_wells.append(WA_to_UWI[WA])

	print('\nCONNECTED WELLS')
	print('Total Number of Project Wells Connected;   ' + str(len(project_connected_wells)))
	if facility != 'ALL':
		#print(connected_wells)
		for j in range(0,len(connected_wells)): # we also want to print the well UWI's
			connected_wells_UWI.append(WA_to_UWI[connected_wells[j]])
		#print(connected_wells_UWI)

	#printout

	if facility != 'ALL':
		print('\nFACILITY INFORMATION\n')
		for i in range(0,len(BC_facility_index_headings)):
			print(BC_facility_index_headings[i]	 +  ';   ' + BC_facility_index[facility][0][i])
	
	#print facility total
	print('\n\nFacility Totals Over Period\n')
	activity_headings = ['PROD GAS', 'FLARE GAS', 'VENT GAS', 'FUEL GAS', 'PROD COND', 'PROD OIL', 'REC GAS','DISP GAS','PURREC GAS']
	#activity_headings = BC_facility_data_headings[1:-1]
	total_vol = np.zeros(len(activity_headings))
	print('Date, ' + str(activity_headings) + '\n')

	for year_month in BC_facility_data[facility]:
		monthly_volumes = []
		for activity in activity_headings:
			if activity in BC_facility_data[facility][year_month]:
				monthly_volumes.append(round(BC_facility_data[facility][year_month][activity],1))
				total_vol[activity_headings.index(activity)] += BC_facility_data[facility][year_month][activity]
			elif activity not in BC_facility_data[facility][year_month]:
				monthly_volumes.append(float(0))
		print(year_month + ', ' + str(monthly_volumes))

	print('\n')
	print('Total Over Period\n')
	print([round(x,1) for x in total_vol])

	prod_oil = total_vol[activity_headings.index('PROD OIL')]
	inlet_gas = (total_vol[activity_headings.index('PROD GAS')] + total_vol[activity_headings.index('REC GAS')])

	if prod_oil == 0:
		fuel_rate = 0
		flare_rate = 0
		vent_rate = 0
		gas_oil_ratio = 0
			
	elif prod_oil != 0:
		fuel_rate = (total_vol[activity_headings.index('FUEL GAS')]*1000*m3_scf)/(total_vol[activity_headings.index('PROD OIL')]*m3_bbl)
		flare_rate = (total_vol[activity_headings.index('FLARE GAS')]*1000*m3_scf)/(total_vol[activity_headings.index('PROD OIL')]*m3_bbl)
		vent_rate = (total_vol[activity_headings.index('VENT GAS')]*1000*m3_scf)/(total_vol[activity_headings.index('PROD OIL')]*m3_bbl)
		gas_oil_ratio = (total_vol[activity_headings.index('PROD GAS')]*1000*m3_scf)/(total_vol[activity_headings.index('PROD OIL')]*m3_bbl)

	if inlet_gas > 0:
		fuel_percentage =  (total_vol[activity_headings.index('FUEL GAS')])/(total_vol[activity_headings.index('PROD GAS')] + total_vol[activity_headings.index('REC GAS')])
		flare_percentage =  (total_vol[activity_headings.index('FLARE GAS')])/(total_vol[activity_headings.index('PROD GAS')] + total_vol[activity_headings.index('REC GAS')])
		vent_percentage =  (total_vol[activity_headings.index('VENT GAS')])/(total_vol[activity_headings.index('PROD GAS')] + total_vol[activity_headings.index('REC GAS')])
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

def get_BC_facility_index():

	print('Getting BC Facility Information (e.g Type etc)')

	#function acessesthe facindex file and gets facility data - eg type

	facility_index_location = map_to_drive() + "/Project Data/BCOGC/facindex.csv"
	BC_facility_index = collections.OrderedDict()

	#A switch for when we want to start storing csv data
	switch = 0

	with open(facility_index_location) as f:
		reader = csv.reader(f)
		for row in reader:

			if switch == 1:
				FAC_ID = row[FAC_ID_CODE_index]
				if FAC_ID not in BC_facility_index:
					BC_facility_index[FAC_ID] = [row]
				else:
					BC_facility_index[FAC_ID].append(row)

			if row[0] == 'Facility Code':
				headers = row
				FAC_ID_CODE_index = headers.index('Facility Code')
				switch = 1

	return BC_facility_index, headers


def BC_facility_plotter(well_data, well_data_headers, facility_period_summary, facility_period_summary_headings, facility_to_WA, WA_to_UWI, shape_file,shapefile_facility_list):

	print('\nPlotting BC Facility Data...\n')

	FLARE_index = facility_period_summary_headings.index("FLARED_GAS SUM")
	UWIs = []
	
	for facility in facility_period_summary:
		if facility != 'ALL':	
			FLARED_GAS = facility_period_summary[facility][FLARE_index]
			if (0 < float(FLARED_GAS) < 500):
				color = 'yellow'
			if (500 < float(FLARED_GAS) < 1000):
				color = 'orange'
			if float(FLARED_GAS) > 1000:
				color = 'red'
			if (float(FLARED_GAS) <= 0):
				color = 'no_plot'
		
			
			WAs = facility_to_WA[facility]
			for WA in WAs:
				UWIs.append(WA_to_UWI[WA])
				
			#we will just plot to the location of the first well

			if color != 'no_plot':
				x,y = get_well_coordinates(well_data, well_data_headers, UWIs[0])
				print(x,y)
				plt.plot(x, y, 'ok', markersize=1, color=color, label = None)

				#get the facilities in the shapefile
				if len(shape_file.points) > 0:
					facility_points = Point(x,y)
					shape_polygon = Polygon(shape_file.points)
					if shape_polygon.contains(facility_points) is True: #if the point is in the polygon
						shapefile_facility_list.append(facility)

		return shapefile_facility_list

def facility_OPGEE_data(well_data, well_data_headings, OPGEE_data, BC_facility_data, facility_to_WA, WA_to_UWI, BC_facility_index, BC_facility_index_headings):

	print('\nCollecting OPGEE FFV inputs for wells\n')

	m3_scf = 35.314666
	m3_bbl = 6.2898
	wells_with_fac_data = []
	impossible_FFV = [] #WELLS WITH FFV RATES > 100%
	well_cumulative = collections.OrderedDict()
	well_to_fac = collections.OrderedDict()

	activities = activities = ['PROD GAS', 'FLARE GAS', 'VENT GAS', 'FUEL GAS', 'PROD OIL', 'REC GAS', 'DISP GAS','PURREC GAS']

	for facility in BC_facility_data:
		period_cumulative = np.zeros(len(activities))
		
		if facility != 'ALL':
			if len(BC_facility_data[facility]) > 0:
				fac_type_index = BC_facility_index_headings.index('Facility Type')
				fac_type = BC_facility_index[facility][0][fac_type_index]

				for year_month in BC_facility_data[facility]:
					for product in BC_facility_data[facility][year_month]:
						if product in activities:
							period_cumulative[activities.index(product)] += BC_facility_data[facility][year_month][product]

				for well in facility_to_WA[facility]:
					well = WA_to_UWI[well]
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

	

	print('\nUnique FFV Data added to ' + str(len(wells_with_fac_data)) + ' wells')
	print('Impossible FFV rates (>100%) were found for ' + str(len(impossible_FFV)) + ' wells')
	print('Fuel, flare and vent rates for these wells have been set to zero')

	#for well in OPGEE_data:
	#	if well in well_to_fac:
	#		print(well,well_to_fac[well])
	#	else:
	#		print(well,0)


	return OPGEE_data


def BC_facility_well_production_data(connected_WAs):

	#this function takes in the list of all connected wells to BC facilities
	#it then gets the production data for all of these wells

	print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	print(' Getting All BC Facility Well Production Data To Calculate FFV Rates')
	print(' -We get all well data to ensure we select ALL wells connected to ')
	print(' -BC facilities - this insures we get all well production data for ')
	print(' -Comparison with what they have reported at the facility level')
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	
	well_list = [] #this is a list of all wells connected to BC facilities
	WA_to_UWI = collections.OrderedDict() # dictionary of UWI keyed by WA

	# get all well data so we can make a WA_to_UWI for all connected wells
	from get_well_data_from_WA import get_well_data_from_WA

	well_data_headings, well_data = get_well_data_from_WA(connected_WAs)

	for well in well_data:
		well_list.append(well)
		WA_to_UWI[well_data[well][well_data_headings.index('Lic/WA/WID/Permit #')]] = well

	del well_data

	print(str(len(well_list)) + '  Wells connected found from well data (we will serch production for these wells)')

	from search_production_data import search_production_data

	BC_fac_production_data_headings, BC_fac_production_data, well_data_headings, well_header_data = search_production_data(well_list)

	del well_data_headings 

	del well_header_data


	return BC_fac_production_data, BC_fac_production_data_headings, WA_to_UWI 

def BC_facility_well_prod_comparison(production_data, production_data_headings, fac_period_summary, facility_summary_headings, facility_to_WA, WA_to_UWI, date_array):

	#takes in production data for all wells connected to facilities
	#takes in the period summary for each individual facility and the headings 
	#takes in date_array and conection data (ie Facility_to_WA)

	#we are comparing the production data for the wells registered
	#as connected to the facility, to the production recored at the facility level
	#it seems as there are some discrepancies!

	for key in fac_period_summary:
		facility = key

	if (len(production_data) > 0 and facility == 'ALL'):
		#ensures that we have production data for facilities and that it is not the summary of all facilities
		return

	print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	print('CALCULATING FFV AND EXPORTING TO OPGEE FAC_ID: ' + str(facility) )
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

	from production_analysis import sumaverage_production_value

	well_volume_type = ['PRD Monthly GAS e3m3', 'PRD Monthly OIL m3','PRD Monthly CND m3']
	facility_volume = [0,0,0]
	wells_with_prd = []
	wells_missing_prd = []

	#we have to shorten WAs from 012345 to 12345

	for well in facility_to_WA[facility]:

		if well in WA_to_UWI:
			well = WA_to_UWI[well]

			if well in production_data: # first check that the connected well has prod data
				wells_with_prd.append(well)
				for i in range(0,len(well_volume_type)): #we now sum the data for each type
					facility_volume[i] = facility_volume[i] + sumaverage_production_value(well, production_data, production_data_headings, date_array, well_volume_type[i], 'SUM')
			if well not in production_data:
				wells_missing_prd.append(well)


	print('Production data from wells\n') 
	#summed production data from well over period
	print(well_volume_type)
	print(facility_volume)
	print('\nProduction Data from Facilities\n')
	#Summary of volumes at the facility level
	print(facility_summary_headings)
	print(fac_period_summary[facility])
	#How many wells have been accounted for 
	print('\nNumber of Wells with prod data: ' + str(len(wells_with_prd)))
	print(wells_with_prd)
	print('\nNumber of Wells missing prod data: ' + str(len(wells_missing_prd)))
	print(wells_missing_prd)
	


def BC_facility_analysis(well_data, well_data_headings, OPGEE_data, date_array):

	print('\n=============================')
	print(' BC FACILITY ANALYSIS')
	print('=============================\n')

	print(date_array)

	facility_links, facility_link_headings = get_BC_facility_links()

	BC_facility_index, BC_facility_index_headings = get_BC_facility_index()

	connected_WA, BC_facility_list, WA_to_UWI, facility_to_WA = get_BC_facility_list(well_data, well_data_headings, facility_links, facility_link_headings, BC_facility_index, BC_facility_index_headings)

	BC_facility_data, BC_facility_data_headings = get_BC_facility_data(date_array, BC_facility_list)

	BC_facility_data = BC_facility_data_summary(BC_facility_data, BC_facility_data_headings, date_array)

	print_facility_summary('ALL', well_data, BC_facility_data, BC_facility_data_headings, WA_to_UWI, facility_to_WA, BC_facility_index, BC_facility_index_headings)

	if len(well_data) > 0:

		OPGEE_data = facility_OPGEE_data(well_data, well_data_headings, OPGEE_data, BC_facility_data, facility_to_WA, WA_to_UWI, BC_facility_index, BC_facility_index_headings)

	ask_print_single_fac = str(raw_input('\nWould you like to print each single facility (Y/N)? :    '))

	count = 1

	for facility in BC_facility_data:

		if ask_print_single_fac.upper() == 'Y':

			print('==== Facility ' + str(count) + ' of ' + str(len(BC_facility_data)) + ' ====\n')

			count += 1

			print_facility_summary(facility, well_data, BC_facility_data, BC_facility_data_headings, WA_to_UWI, facility_to_WA, BC_facility_index, BC_facility_index_headings)

	#for well in OPGEE_data:
	#	print(well, OPGEE_data[well][OPGEE_data['headings'].index('Facility flared gas')],OPGEE_data[well][OPGEE_data['headings'].index('Facility vented gas')], OPGEE_data[well][OPGEE_data['headings'].index('Facility fuel gas')])								
			

	return OPGEE_data, BC_facility_data['ALL'], len(connected_WA), len(BC_facility_data) - 1



def BC_facility_shapefile_analyis(well_data, well_data_headings, date_array, shapefile):

	#ensure that well_data is ALL WELL DATA!!

	facility_links, facility_link_headings = get_BC_facility_links()

	BC_facility_index, BC_facility_index_headings = BC_facility_index()

	connected_WA, BC_facility_list, WA_to_UWI, facility_to_WA = get_BC_facility_list(well_data, well_data_headings, facility_links, facility_link_headings)

	BC_facility_data, BC_facility_data_headings = get_BC_facility_data(date_array)

	active_facility_list, facility_summary, facility_summary_headings = BC_facility_data_summary(BC_facility_data, BC_facility_data_headings, facility_to_WA, BC_facility_list, WA_to_UWI, date_array)

	shapefile_facility_list = []
	
	#single facility analysis
	for facility in active_facility_list:
		
		single_facility_data = single_BC_facility_data(BC_facility_data, facility)
		
		active_facility, facility_summary, facility_summary_headings = BC_facility_data_summary(single_facility_data, BC_facility_data_headings, facility_to_WA, BC_facility_list, WA_to_UWI, date_array)

		fac_period_summary = facility_period_summary(single_facility_data, facility_summary, facility_summary_headings)

		#print_facility_summary(facility_summary, fac_period_summary, facility_summary_headings, WA_to_UWI, facility_to_WA, BC_facility_index_, BC_facility_index_headings)
		
		print('\n-------------------------------------------------\n')
		
		shapefile_facility_list = BC_facility_plotter(well_data, well_data_headings, fac_period_summary, facility_summary_headings, facility_to_WA, WA_to_UWI, montney_shape, shapefile_facility_list)

	active_facility_list, facility_summary, facility_summary_headings = BC_facility_data_summary(BC_facility_data, BC_facility_data_headings, facility_to_WA, shapefile_facility_list, WA_to_UWI, date_array)

	fac_period_summary = facility_period_summary(BC_facility_data, facility_summary, facility_summary_headings)

	print_facility_summary(facility_summary, fac_period_summary, facility_summary_headings, WA_to_UWI, facility_to_WA, BC_facility_index_, BC_facility_index_headings)

	plt.show()
	
	return


	return
	

if __name__ == '__main__':

	from well_search import well_search
	from dates_array import dates_array
	from get_all_post_2005_well_data import get_all_post_2005_well_data,get_tight_oil_wells
	from OPGEE_defaults import OPGEE_defaults
	from general_well_data_analysis import general_well_data_analysis, OPGEE_well_data
	from OPGEE_input_sensitivity import OPGEE_input_sensitivity
	#from LNG_well_search import LNG_well_search
	import time

	#well_data_function = get_formation_well_data() # MONTNEY
	well_data_function = well_search()
	#well_data_function = LNG_well_search()
	#well_data_function = get_all_post_2005_well_data()
	#well_data_function = get_tight_oil_wells()


	well_data_headings = well_data_function[0] 
	well_data = well_data_function[1] 
	#well_data = []

	date_array = dates_array('2017-01','2017-12')
	field_name = 'poop'

	#date_array = ['2016-01']
	
	OPGEE_data = OPGEE_defaults()

	#OPGEE_data = general_well_data_analysis(well_data_headings, well_data, OPGEE_data, field_name)
	OPGEE_data = OPGEE_well_data(well_data, well_data_headings, OPGEE_data)

	BC_facility_analysis(well_data, well_data_headings, OPGEE_data, date_array)

	OPGEE_input_sensitivity(OPGEE_data, well_data)

	#print('\nSleeping\n')
	#time.sleep(5)

	#print('\nSleeping\n')
	#time.sleep(5)

	#OPGEE_input_sensitivity(OPGEE_data)

	'''
	m = plot_basemap()
	montney_shape = montney_shape_plot(m)[1]

	BC_facility_shapefile_analyis(well_data, well_data_headings, date_array, montney_shape)

	print('\nSleeping\n')
	time.sleep(5)

	#OPGEE_data = OPGEE_defaults()

	'''