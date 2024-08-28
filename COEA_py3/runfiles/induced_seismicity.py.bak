#induced Seismicity 
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.basemap import Basemap 
import matplotlib as mpl
import os
import csv
import collections
import pylab
import datetime
import re
from get_AB_water_data import get_AB_water_source_data, get_AB_water_use_data
from get_BC_water_data import get_BC_water_data
from get_seismic_data import get_NRC_seismic_data, get_CISC_seismic_data, get_updated_NRC_seismic_data
from get_well_data import get_formation_well_data
from water_data_functions import water_data_sum_average_min_max 
import mpu
from datetime import datetime
from map_plotter import map_plotter
from plot_basemap import plot_basemap
from shapefile_reader import formation_shapefile_plotter, plot_infrastructure
from well_plotter import well_plotter, get_well_coordinates
from Spatial_impact_plotting import plot_water_shapefiles
import csv

def save_full_screen_figure():

	save_name = 'Seismic_Map.png'

	print('Saving Figure as.....' + str(save_name))

	manager = plt.get_current_fig_manager()
	manager.resize(*manager.window.maxsize())

	plt.savefig(save_name, dpi=500)


def induced_seismic_assessment(well_data_headings, well_data):

	print('\n========================\n Induced Seismic Module \n========================\n\n')

	#get earthquake and frac data
	#seismic_data_headings, seismic_data = get_NRC_seismic_data()
	#seismic_data_headings, seismic_data = get_updated_NRC_seismic_data()
	seismic_data_headings, seismic_data = get_CISC_seismic_data()
	AB_water_headings, AB_water_data = get_AB_water_use_data()
	#AB_water_headings, AB_water_data = get_AB_water_source_data()
	BC_water_headings, BC_water_data = get_BC_water_data()

	wells_of_interest = []

	for well in well_data:
		wells_of_interest.append(well)

	#### Machine lerning stuff ###
	data_of_interest_dict = collections.OrderedDict() #data containing things for ML
	headings_of_interest = ['Completion Date','Related Event','Event Mag'] #the data we are collecting in this fucntion

	#dicts for end stuff
	coordinates = collections.OrderedDict() #collection of coordinates [well][well lat, well lon][sei]
	well_drill_date_type = collections.Counter()
	formation_well_counter = collections.Counter()
	formation_event_counter = collections.OrderedDict()
	field_event_counter = collections.OrderedDict()
	sesmic_events_dict = collections.OrderedDict() #disctionary contain the well data, seismic event data and HF data for wells with 'Induced Seismicity'
	event_well_field_locations = collections.Counter() #dictionary of which field wells found with seismic events are located 
	comp_well_field_locations = collections.Counter() #dictionary of the number of wells completed in each formation

	#indexing
	for i in range(0, len(BC_water_headings)):
		if BC_water_headings[i] == 'COMPLTN DATE':
			BC_compl_date_index = i

	for i in range(0, len(AB_water_headings)):
		if AB_water_headings[i] == 'Water Diversion End Date':
			#water source data
			AB_compl_date_index = i
		if AB_water_headings[i] == 'End Date':
			#water us data
			AB_compl_date_index = i


	for i in range(0,len(well_data_headings)):
		if well_data_headings[i] == 'Date Drlg Completed':
			all_compl_date_index = i #No fracture data, this will have to do
		if well_data_headings[i] == 'Surf-Hole Latitude (NAD83)': 
			well_lat_index = i
		if well_data_headings[i] == 'Surf-Hole Longitude (NAD83)': 
			well_lon_index = i
		if well_data_headings[i] == 'Well Status Abrv': 
			well_type_index = i
		if well_data_headings[i] == 'TVD (m)':
			TVD_index = i

		WA_index = well_data_headings.index('Lic/WA/WID/Permit #')
		formation_index = well_data_headings.index('Prod./Inject. Frmtn')
		field_name_index = well_data_headings.index('Producing Field/Area Name')
		prov_index =   well_data_headings.index('Area')

	if seismic_data_headings[0] == 'Date':
		#we are dealing with the old NRC data
		EQ_set = 'NRC'
		for i in range(0,len(seismic_data_headings)):
			if seismic_data_headings[i] == 'Date': 
				event_date_index = i
			if seismic_data_headings[i] == 'Lat': 
				event_lat_index = i
			if seismic_data_headings[i] == 'Long': 
				event_long_index = i
			if seismic_data_headings[i] == 'Mag': 
				event_mag_index = i

	elif seismic_data_headings[0] == 'yr':
		#we are dealing with the SISC data 
		EQ_set = 'SISC'
		for i in range(0,len(seismic_data_headings)):
			if seismic_data_headings[i] == 'lat': 
				event_lat_index = i
			if seismic_data_headings[i] == 'lon': 
				event_long_index = i
			if seismic_data_headings[i] == 'MwAsg': 
				event_mag_index = i
	

	elif seismic_data_headings[0] == '#EventID':
			#we are dealing with new NRC data
			EQ_set = 'NRC_new'
			for i in range(0,len(seismic_data_headings)):
				if seismic_data_headings[i] == 'Time': 
					event_date_index = i
				if seismic_data_headings[i] == 'Latitude': 
					event_lat_index = i
				if seismic_data_headings[i] == 'Longitude': 
					event_long_index = i
				if seismic_data_headings[i] == 'Magnitude': 
					event_mag_index = i



	count = 0
	max_dist = float(raw_input('What is the maximum distance of investigation (km)? (Distance between well and seismic event):   '))
	min_mag = float(raw_input('What is the minimum magnitude of the event?   '))
	max_days_between = float(raw_input('The maximum amount of time between completion date and event (days):   '))
	negative_days =  str(raw_input('Include Seismic Events that Happen in an Area Prior to Drilling (Yes/No)?  :   '))

	print('\nFinding induced events...\n')

	if negative_days[0].upper() == 'Y':
		date_min = -10000
	else:
		date_min = -1 


	#max_dist = 5 #the maximum distance we are interested in between events
	#min_mag = 2.5 #the minimum magnitude for events we are interested in
	#max_days_between = 200 #we are only inderested in events with < 200 days between
	days_between_array = []
	distance_array = []
	iteration_count = 0
	unique_events = [] #array of unique seismic events
	unique_events_form = collections.OrderedDict() #well formations relating to an event - i.e mutliple formations / wells can be associated with a single event
	unique_events_well_UWI = collections.OrderedDict()
	unique_events_field = []
	unique_mag = [] #array of magnitudes for unique events 
	unique_wells = [] #array of wells being affectd by seimsic
	well_locations = [] #an array of affected well locations which have met conditions
	event_locations = [] #an array of event locations which have met conditions
	magnitude_array = []
	wells_with_HF_data = []
	non_associated_wells = []

	start_time = time.time()

	for well in wells_of_interest:
		
		#for AB water data search 
		well_short = well[1:-2] + well[-1] #transform 100062505526W502 into 00062505526W52

		WA = well_data[well][WA_index]

		#we want to see how many calculations are left for the well_set
		iteration_count = iteration_count + 1
		if iteration_count % 1000 == 0:
			print('\n' + str(iteration_count) + ' Wells of ' + str(len(wells_of_interest))+' Wells Searched' + ' (Computational Time (s): ' + "%.4f" %(time.time() - start_time) + ')')

		well_found = 'no' #if we cant find the HF data, we will use drilling date 

		#try:

		#get the approprate completion date from file
		if WA in BC_water_data:
			compl_date = str(BC_water_data[WA][0][BC_compl_date_index])
			well_date_format = '%d-%b-%y'
			well_found = 'BC Completion Date'
			wells_with_HF_data.append(well)

		if well_short in AB_water_data:
			compl_date = str(AB_water_data[well_short][0][AB_compl_date_index]) #just take the 0th entry for now
			well_date_format = '%m/%d/%Y'
			well_found = 'AB Completion Date'
			wells_with_HF_data.append(well)

		if well_found == 'no':
			compl_date = str(well_data[well][all_compl_date_index])
			#if __name__ == "__main__": #this is the format for that dataset
			well_date_format = '%m/%d/%Y'
			#else:
			#well_date_format = '%Y/%m/%d'
			
			well_found = 'Well Drilled Date'

		try:
			try:
				compl_date = datetime.strptime(compl_date, well_date_format)
			except:
				compl_date = datetime.strptime(compl_date, '%Y/%m/%d')
			
			well_lat = float(well_data[well][well_lat_index][:-1])
			well_lon = float(well_data[well][well_lon_index][:-1])
			well_type = well_data[well][well_type_index]
			formation = well_data[well][formation_index] + ' (' + well_data[well][prov_index] +')'
			field_name = well_data[well][field_name_index]
		except:
			print('Missing well data',well)
			#print(compl_date, well_date_format)
			#print('well_lat',well_data[well][well_lat_index][:-1])
			#print('well_lon', well_data[well][well_lon_index][:-1])
			#print('well_type',well_data[well][well_type_index])
			continue
		
		######## add params to dict ##########
		if well_found in ['AB Completion Date','BC Completion Date']:
			data_of_interest_dict[well] = [compl_date,0,0]
			comp_well_field_locations[field_name] += 1

		event_counter = 0 
		events_per_well_count = 0
		date_skip  = 'skip'

		for event in seismic_data:
			
			event_counter +=1

			if seismic_data_headings[0] == 'Date':
				#Dealing with NRC data, need to convert date
				try:
					event_date = seismic_data[event][event_date_index]
					event_date = datetime.strptime(event_date, '%m/%d/%Y')
					event_mag = float(seismic_data[event][event_mag_index][:-3])
					event_lat = float(seismic_data[event][event_lat_index])
					event_lon = -float(seismic_data[event][event_long_index])
				except:
					print('Missing Earthquake Data', well, event_counter)
					continue
			
			elif seismic_data_headings[0] == 'yr':
				# we are dealing with CISC data
				event_date = event
				try:
					event_mag = float(seismic_data[event][event_mag_index])
					event_lat = float(seismic_data[event][event_lat_index])
					event_lon = -float(seismic_data[event][event_long_index])
				except:
					print('Missing Earthquake Data', well, event_counter)
					continue
			
			if seismic_data_headings[0] == '#EventID':
				#Dealing with new NRC data, need to convert date
				event_date = seismic_data[event][event_date_index].split('T')[0]
				event_date = datetime.strptime(event_date, '%Y-%m-%d')
				event_mag = float(seismic_data[event][event_mag_index])
				event_lat = float(seismic_data[event][event_lat_index])
				event_lon = -float(seismic_data[event][event_long_index])
	

				#print((well_lat,well_lon),(event_lat, event_lon))
			#print(mpu.haversine_distance((well_lat,well_lon),(event_lat, event_lon)))
			distance = mpu.haversine_distance((well_lat,well_lon),(event_lat, event_lon))
			try:
				date_difference = str(event_date - compl_date)
			except:
				print(event_date, compl_date, well)
			if 'day' in date_difference:
				#pull the day as an integer
				days_between = int(date_difference[:(date_difference.find('d')-1)])#get the number of days
			elif 'day' not in date_difference:
				#we are looking at same day events
				days_between = 0
			if distance < max_dist:
				if event_mag >= min_mag:
					if (date_min < days_between <= max_days_between):
					#if date_skip == 'skip':
						#exclude well drill dates 
						if well_found not in ['Well Drilled Date']:
							
							print('\n')
							print('Well UWI: ' + str(well))
							print('Distance Between Recorded Event and Completed Well (km): ' + str(distance))
							print('Event Field: ' + str(field_name))
							print('Well Formation:  ' + str(formation))
							print('Magnitude of Event: ' + str(event_mag))
							print('Well Completion Date: ' + str(compl_date))
							print('Seismic Event Date: ' + str(event_date))
							print('Days Between Completion and Event: ' + date_difference)
							print('Distance Between Completion and Event; ' + str(round(distance,2)))
							print('Event Number: ' + str(event) + ' of ' + str(len(seismic_data)) + ' in Data File')
							print('Type of Well: ' + str(well_type))
							print('Well Depth (m): ' + str(well_data[well][TVD_index]))
							print(well_found)
	

							days_between_array.append(days_between)
							count = count + 1
							if event not in unique_events:
								unique_events.append(event)
								unique_events_field.append(field_name)
								unique_events_form[event] = [formation + ' ' + str(date_difference).split(',')[0]]
								unique_events_well_UWI[event] = [well]
								unique_mag.append(event_mag)
								event_locations.append([event_lat,-event_lon])
								magnitude_array.append(event_mag)
							elif event in unique_events:
								#add the second completion to the unique event if multiple wells are flagged for same event
								unique_events_form[event].append(formation+ ' ' + str(date_difference).split(',')[0])
								unique_events_well_UWI[event].append(well)

							if well not in unique_wells:
								unique_wells.append(well)
							
							distance_array.append(float(distance))
							well_locations.append([well_lat,-well_lon])
							well_drill_date_type[well_found] += 1
							formation_well_counter[formation] += 1
							event_well_field_locations[field_name] += 1

							if formation not in formation_event_counter:
								formation_event_counter[formation] = []
							if field_name not in field_event_counter:
								field_event_counter[field_name] = []
							if event not in formation_event_counter[formation]:
								formation_event_counter[formation].append(event)
							if event not in field_event_counter[field_name]:
								field_event_counter[field_name].append(event)

							#replace the event mag of zero with the induced mag
							data_of_interest_dict[well][1] = 1
							data_of_interest_dict[well][2] = event_mag
							events_per_well_count += 1
		
		if well not in unique_wells:
			non_associated_wells.append(well)


	print('\n\nInduced Seismic Assessment Results')
	#print('Analysis of 5255 Seismic Events in Western Canada B.C Between 2008 and 2018')
	print('Maximum Distance Between Completion and Seismic Event (km); ' + str(max_dist)) 
	print('Minimum Magnitude of Event; ' + str(min_mag)) 
	print('Maximum Time Between Completion and Seismic Event (days); ' + str(max_days_between))
	print('Number Events Meeting Conditions; ' + str(count))
	print('The Number of Unique Seismic Events;  ' + str(len(unique_events)))
	print('The number of Unique wells affected;  ' + str(len(unique_wells)))
	print('The number of wells with AB or BC completion data;  ' + str(len(wells_with_HF_data)))
	print('Percentage of wells with HF data related to an induced event; ' + str(round(100*(float(len(unique_wells))/len(wells_with_HF_data)),2)) + str('%'))
	try:
		print('Mean Days Between Events; ' + str(np.mean(days_between_array)))
		print('Max Days Between Events; ' + str(np.max(days_between_array)))
		print('Min Days Between Events; ' + str(np.min(days_between_array)))
		print('Average Distance Between Event and Well;  ' + str(np.mean(distance_array)))
	except:
		pass

	print('\nWell Date Used')
	for key in well_drill_date_type:
		print(key, well_drill_date_type[key])
	print('\nFormations Wells are Completed in')
	for key in formation_well_counter:
		print(key,formation_well_counter[key])
	print('\nField Wells are Completed in')
	for key in comp_well_field_locations:
		print(key,comp_well_field_locations[key])
	print('\nField Wells with Events are Completed in')
	for key in event_well_field_locations:
		print(key,event_well_field_locations[key])
	print('\nNumber of unique events by formation')
	for key in formation_event_counter:
		print(key,len(formation_event_counter[key]))
	print('\nNumber of unique events by Field')
	for key in field_event_counter:
		print(key,len(field_event_counter[key]))
	print('\nEvent Summary')
	for event in range(0,len(unique_mag)):
		event_name = unique_events[event]
		print('Event ' + str(event))
		print(str(unique_events[event]),unique_mag[event],unique_events_field[event])
		print(unique_events_well_UWI[event_name])
		print(unique_events_form[event_name])
		print('\n')

	print('\n\n')

	plot_YN = raw_input('Would you like to plot the events (Yes/No)?   ')


	if plot_YN[0].upper() == 'Y':

		#mpl.rcParams['figure.dpi'] = 500

		#plot wells
		unique_well_dict = collections.OrderedDict()
		non_associated_dict = collections.OrderedDict()

		for well in unique_wells:
			data = well_data[well]
			unique_well_dict[well] = data

		for well in non_associated_wells:
			data = well_data[well]
			non_associated_dict[well] = data

		#plot water heat mapping
		plot_water_shapefiles()

		#plot formation and area shapes
		#formation_shapefile_plotter()

		#Plot Associated Completions
		#well_plotter(unique_well_dict, well_data_headings)

		#Plot Non Associated Completions 
		#for well in non_associated_dict:
		for well in well_data:
			x,y = get_well_coordinates(well_data, well_data_headings, well)
			#plt.plot(x, y, 'ok', markersize = 0.2, color='black', label = 'Completed Tight Oil Well')

	
		#handles, labels = plt.gca().get_legend_handles_labels()
		#by_label = collections.OrderedDict(zip(labels, handles))
		#leg = plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(0.93, 0.95), fontsize=12, markerscale=8)
		#leg.set_title('      Completed Well      ', prop = {'size': 12})
	

		#plot_infrastructure()

		plt.title('Seismic Events Occuring Within 7.5km and 30 Days of a Tight Oil Hydraulic Fracture Treatment (2012 - 2017)', fontsize = 16)
	
		plot_seismic_events(event_locations,magnitude_array)

		#save_full_screen_figure()

		plt.show()

	#get ML completion and well data
	ML_data, ML_headings =  get_well_comp_data(well_data, well_data_headings)
	ML_headings.extend(headings_of_interest)
	for well in ML_data:
		ML_data[well].extend(data_of_interest_dict[well])
		#print(ML_data[well])

	return ML_data, ML_headings

def plot_seismic_events(event_locations,magnitude_array):

		print('\nPlotting The Induced Seismic Event Locations\n')

		for i in range(0,len(event_locations)):
			if magnitude_array[i] < 3:
				color = 'blue'
				#color = 'darkorange'
				size = 8
				label = '2 < $M_W$ < 3'
				mew = 1.5
			if (3 <= magnitude_array[i] < 4):
				color = 'green'
				#color = 'red'
				size = 10
				label = '3 <= $M_W$ < 4'
				mew = 2.5
			if (magnitude_array[i] >= 4):
				color = 'white'
				#color = 'black'
				size = 12
				label = '$M_W$ >= 4'
				mew = 3
			
			plt.plot(event_locations[i][1], event_locations[i][0], marker = 'x', markersize=size, color=color, mew = mew, label = label)
		
		
		#Only Show Unique Labels Not Doubles 
		'''
		handles, labels = plt.gca().get_legend_handles_labels()
		by_label = collections.OrderedDict(zip(labels, handles))

		#organise labels
		keys = by_label.keys()
		organised_keys =  [keys[0],keys[2],keys[1]]
		new_by_label = collections.OrderedDict()
		for key in organised_keys:
			value = by_label[key]
			new_by_label[key] = value
		by_label = new_by_label	

		leg = plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(0.93, 0.95), fontsize=12)
		leg.set_title('Earthquake Magnitude ' + '($M_W$)', prop = {'size': 12})
		'''

def get_well_comp_data(well_data, well_data_headings):

	####Get water data#####
	AB_water_use_headings, AB_water_use_data = get_AB_water_use_data()
	AB_water_source_headings, AB_water_source_data = get_AB_water_source_data()
	BC_water_headings, BC_water_data = get_BC_water_data()


	#dictionary for data were vcollecting
	well_and_comp_data_dict = collections.OrderedDict()

	well_params = ['Well UWI','Date Drlg Completed','Surf-Hole Latitude (NAD83)','Surf-Hole Longitude (NAD83)',
		'Well Status Abrv','TVD (m)','Prod./Inject. Frmtn','Producing Field/Area Name']

	############ get dictionaries of completion data for wells ##############
	BC_injection_vol = water_data_sum_average_min_max(BC_water_data, BC_water_headings, well_data, well_data_headings, 'TOTAL FLUID PUMPED (m3)', 'SUM', "BC")
	BC_stage_count = water_data_sum_average_min_max(BC_water_data, BC_water_headings, well_data, well_data_headings, 'FRAC STAGE NUM', 'MAX', "BC")
	AB_injection_vol = water_data_sum_average_min_max(AB_water_source_data, AB_water_source_headings, well_data, well_data_headings, 'Total Water Volume', 'SUM', "AB")
	AB_stage_count = water_data_sum_average_min_max(AB_water_use_data, AB_water_use_headings, well_data, well_data_headings, 'Number of Stages', 'MAX', "AB")

	well_params.extend(['Injected Volume','Number of Stages'])

	for dict_ in [BC_injection_vol,AB_injection_vol]:
		for well in dict_.keys():
			if well not in well_and_comp_data_dict:
				well_and_comp_data_dict[well] = [well]
				for param in well_params[1:-2]:
					if param in ['Surf-Hole Latitude (NAD83)','Surf-Hole Longitude (NAD83)']:
						well_and_comp_data_dict[well].append(well_data[well][well_data_headings.index(param)][:-1])
					else:
						well_and_comp_data_dict[well].append(well_data[well][well_data_headings.index(param)])
				well_and_comp_data_dict[well].append(dict_[well])

	#add stage numbers
	for dict_ in [BC_stage_count,AB_stage_count]:
		for well in dict_:
			if well in well_and_comp_data_dict:
				well_and_comp_data_dict[well].append(dict_[well])
			else:
				continue

	return well_and_comp_data_dict, well_params

def write_to_csv(ML_data, ML_headings):


	with open('Trial.csv' , 'wb') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(ML_headings)
		for well in ML_data:
			writer.writerow(ML_data[well])


if __name__ == "__main__":
	
	from well_search import well_search
	from get_all_post_2005_well_data import get_tight_oil_wells


	#well_data_headings, well_data = get_formation_well_data() #actually all horizontal wells from geoscout

	well_data_headings, well_data, project_name = well_search()
	#well_data_headings, well_data, project_name = get_tight_oil_wells()

	ML_data, ML_headings = induced_seismic_assessment(well_data_headings, well_data)
	
	#write_to_csv(ML_data,ML_headings)

	#get_well_comp_data(well_data, well_data_headings)
	
	