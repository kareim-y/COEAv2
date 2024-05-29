#environmental_reports

import collections
import csv
from map_to_drive import map_to_drive #path to Project Data folder

def environmental_reports(well_data_headings, well_data):

	print('\n================= Environmental Report Module =================\n')
	print('The module outputs all the environmental incidents associated with the selected wells and facilities')

	well_environmental_reports = collections.OrderedDict() # a dictionary filled with report data registered to each well environmental_reports[well]
	facility_environmental_reports = collections.OrderedDict()
	selected_environmental_reports = collections.OrderedDict()

	file_location = map_to_drive() + "/Project Data/geoSCOUT_data/post 2005 environmental_reports.csv"

	with open(file_location) as f:
		reader = csv.reader(f)
		for row in reader:
			
			well_indexs = []
			facility_indexs = []

			if row[0] == 'Release Number':
				environmental_data_headings = row
				
				for i in range(0,len(environmental_data_headings)):
					if environmental_data_headings[i] == 'License Number':
						env_license_index = i
					if environmental_data_headings[i] == 'License Type':
						type_index = i
					if environmental_data_headings[i] == 'Incident Date':
						date_index = i
					if environmental_data_headings[i] == 'Injury Number':
						injury_index = i
					if environmental_data_headings[i] == 'Fatality Number':
						fatality_index = i


			else: 
				
				#we need to split the licenses for each 'released number' which contains multiple licenses
				license_types = row[type_index].split(';')
				licenses = row[env_license_index].replace(' ', '').split(';')
				dates = row[date_index].split(';')
				
				#print(license_types)
				#print(licenses)
				
				#of the licenses we are only interested in well license currently
				for i in range(0,len(license_types)):
					if license_types[i] == 'Well Licence':
						well_indexs.append(i)
					if license_types[i] == 'Facility Licence':
						facility_indexs.append(i)
					#print(license_types)
					#print(indexs)
				
				#Look through all the well licenses and append them to a dict
				for i in range(0,len(well_indexs)):
					try:
						well_environmental_reports[licenses[well_indexs[i]]].append(row)
					except:
						well_environmental_reports[licenses[well_indexs[i]]] = [row]
				
				for i in range(0,len(facility_indexs)):
					try:
						facility_environmental_reports[licenses[facility_indexs[i]]].append(row)
					except:
						facility_environmental_reports[licenses[facility_indexs[i]]] = [row]

		'''
		for license in well_environmental_reports:
			print('\n')
			print(license)
			print(well_environmental_reports[license])
			print('\n')
		'''
	
	print('\n~~~~~~~~~~~~~~ Report Data Available ~~~~~~~~~~~~~~\n')
	print(environmental_data_headings)
	
	#now looking through the well liceenses from the general well data
	for i in range(0,len(well_data_headings)):
		if well_data_headings[i] == 'Lic/WA/WID/Permit #':
			well_license_index = i
	
	wells_with_reports = []
	injury_array = []
	fatality_array = []

	for well in well_data:

		#license number varies depending on which source of wells, 
		#we need to ad a zero for the montney well set
	
		if __name__ == '__main__':
			license = '0' + well_data[well][well_license_index]
		else:
			license =  well_data[well][well_license_index]

		#if the well license matches and environmental report license
		if license in well_environmental_reports:
			selected_environmental_reports[well] = well_environmental_reports[license]
			wells_with_reports.append(well)
			
			
			#print('\n')
			print(well)
			print(license)
			print('\n')
			#print(well_environmental_reports[license])
			#print('\n')
			
			
			for i in range(0, len(well_environmental_reports[license])):
				injuries = well_environmental_reports[license][i][injury_index]
				fatalities = well_environmental_reports[license][i][fatality_index]
				print('Injuries:  ' +str(injuries))
				print('Fatalities:  ' + str(fatalities))
				for j in range(0,len(injuries.split(';'))):
					injury_array.append(int(injuries.split(';')[j]))
					fatality_array.append(int(fatalities.split(';')[j]))

	#print indicent type and indicent value for the slected wells next to eachother
	'''
	for well in selected_environmental_reports:
		print('\n')
		for i in range(0,len(selected_environmental_reports[well])):
			for j in range(0,len(environmental_data_headings)):
				print(environmental_data_headings[j] + '   ' + selected_environmental_reports[well][i][j])
	'''

	print('\n~~~~~~~~~~~ SUMMARY ~~~~~~~~~~~')
	print('\nWells/facilities with associated environmental reports:  ' + str(len(wells_with_reports)))
	print('Total number of Injeries Associated With Wells:  ' + str(sum(injury_array)))
	print('Total number of Fatalities Associated With Wells:  ' + str(sum(fatality_array)))
	print('Note - Ensure they are associated with well and not something else')
	
	return selected_environmental_reports




if __name__ == "__main__":

	from get_well_data import get_formation_well_data


	#MONTNEYY ONLY!!!!!
	print('\nImporting Montney Well Data\n') #MONTNEY
	well_data_function = get_formation_well_data() # MONTNEY
	well_data_headings = well_data_function[0] # MONTNEY
	well_data = well_data_function[1] # MONTNEY

	environmental_reports(well_data_headings, well_data)