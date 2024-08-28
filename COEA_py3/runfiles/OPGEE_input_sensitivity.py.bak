
from return_statistics import histogram, boxplot, return_statistics
import collections

def checkEqual1(iterator):
	#returns true if all elements of iterator are the same
	#this will stop producing a histogram of an array with equal values  
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)


def OPGEE_input_sensitivity(OPGEE_data, well_data):

	print('\n~~~~~~~~~~~~~~~ OPGEE SENSITIVITY ~~~~~~~~~~~~~~~\n')

	OPGEE_array = collections.OrderedDict()
	OPGEE_array_wells = collections.OrderedDict()

	proj_name =  OPGEE_data['assessed field'][OPGEE_data['headings'].index('Field name')]

	for i in range(0,len(OPGEE_data['headings'])):
		OPGEE_array[proj_name + ' - ' + OPGEE_data['headings'][i] + ' (' + OPGEE_data['units'][i] + ')'] = []
		OPGEE_array_wells[proj_name + ' - ' + OPGEE_data['headings'][i] + ' (' + OPGEE_data['units'][i] + ')'] = []


	for well in OPGEE_data:
		if well in well_data:
			for i in range(0,len(OPGEE_data[well])):
				try:
					data = float(OPGEE_data[well][i]) # ensure they are numbers
					round_average_data = round(float(OPGEE_data['assessed field'][i]),3) # need this for C1 composition
					if data not in [float(0), float(OPGEE_data['assessed field'][i]), float(OPGEE_data['defaults'][i]), round_average_data]:
						#print(OPGEE_data['headings'][i])
						#print(str(OPGEE_data[well][i]) + '   ' + str(OPGEE_data['assessed field'][i]) + '   ' + str(OPGEE_data['defaults'][i]))
						OPGEE_array[proj_name + ' - ' + OPGEE_data['headings'][i] + ' (' + OPGEE_data['units'][i] + ')'].append(data) 
						OPGEE_array_wells[proj_name + ' - ' + OPGEE_data['headings'][i] + ' (' + OPGEE_data['units'][i] + ')'].append(well)
				except:
					pass
	
	for heading in OPGEE_array:
		array = OPGEE_array[heading]
		if len(array) > 0:
			if isinstance(array[0], (int, float)):
				return_statistics(array, heading)
				histogram(array, heading)


	return


if __name__ == '__main__':

	from get_well_data import get_formation_well_data
	from OPGEE_defaults import OPGEE_defaults
	from search_production_data import search_production_data
	import collections
	from well_search import well_search
	from general_well_data_analysis import OPGEE_well_data, general_well_data_analysis
	from production_analysis import production_dates, production_summary, OPGEE_production_data,  production_analysis
	from get_all_post_2005_well_data import get_tight_oil_wells

	print('Importing General Well Data') #MONTN1EY
	#well_data_function = get_formation_well_data() # MONTNEY
	#well_data_function = well_search()
	well_data_function = get_tight_oil_wells()

	well_data_headings = well_data_function[0] # MONTNEY
	well_data = well_data_function[1] # MONTNEY
	field_name = 'Montney'

	OPGEE_data = OPGEE_defaults()

	OPGEE_data = general_well_data_analysis(well_data_headings, well_data, OPGEE_data, field_name)

	OPGEE_data = OPGEE_well_data(well_data, well_data_headings, OPGEE_data)

	production_data_headings, production_data, production_well_data, production_well_data_headings = search_production_data(well_data)

	OPGEE_data = production_analysis(well_data, well_data_headings, production_data, production_data_headings, OPGEE_data)

	OPGEE_input_sensitivity(OPGEE_data, well_data)

