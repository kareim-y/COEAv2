
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas
from scipy import stats

from model_inputs import ModelInputs
import pickle

def DST_analysis(well_data, well_data_headings, DST_data, DST_headings, OPGEE_data):

	# Kareem Edits
	# Import Model Inputs from .pkl file
	with open('model_input_instance.pkl', 'rb') as f:
		inputs_instance = pickle.load(f)

	print('\n\n======================\n Analysis of DST Data\n======================')

	wells_with_DST = []
	wells_with_multiple_DST = []
	DST_data_array = [] #an array of all the available DST data - we can average this 
	date_differences = [] #array of the number of days between well completion and DST


	#indexs

	test_date_index = DST_headings.index('Test Date')
	res_temp_index = DST_headings.index('Rsrvr Temp.(degC)')
	max_pressure_index = DST_headings.index('Max Pressure(kPa)')
	recorder_depth_index = DST_headings.index('Recorder Depth(m)')
	#DST_headings.index('')

	#conversions
	kpam_psift = 0.0442075
	kpa_psi = 0.145038
	m_ft = 3.28084

	#date format
	date_format1 = '%m/%d/%Y'
	date_format2 = '%Y/%m/%d'

	DST_well_data = dict() 
	DST_test_dates = dict()
	pressure_time_dict = dict() #a dictionary of pressures and dates after drilling to assess pressure decline, [well][[press_data][days_data]]

	for well in well_data:
		
		#print(well)

		if well in DST_data:
			
			#dates
			well_drill_date = well_data[well][well_data_headings.index('Date Drlg Completed')]
			well_drill_date = well_data[well][well_data_headings.index('Date Well Spudded')]
			try:
				well_drill_date = datetime.strptime(well_drill_date, date_format1)
			except:
				well_drill_date = datetime.strptime(well_drill_date, date_format2)


			well_test_data = [] #array of the test data for each well 
			well_dateoftest = []
			wells_with_DST.append(well)
			
			#check for multiple tests
			if len(DST_data[well]) > 1:
				wells_with_multiple_DST.append(well)

			for test in range(0,len(DST_data[well])):

				#test dates
				DST_test_date =  DST_data[well][test][DST_headings.index('Test Date')]
				DST_test_date = datetime.strptime(DST_test_date, date_format1)
				date_diff = (DST_test_date - well_drill_date)
				date_diff =  date_diff.days
				#print(well, test, date_diff)
				


				#change this for different data ie test depth 
				index_of_interest = max_pressure_index

				try:
					#we have to try for pressures becuase some data is empty
					data = float(DST_data[well][test][index_of_interest])
					well_test_data.append(data) #*kpa_psi
					well_dateoftest.append(int(date_diff))
				
				except:

					pass

			#-------selecting which pressure and time data 

			if len(well_test_data) > 0: #make sure we have data
				#average_data = np.mean(well_test_data) #if we want the average of all tests 
				#test_date_well = np.mean(well_dateoftest) #if we want the average of all tests 

				average_data = min(well_test_data) #if we want the most recent pressure
				test_date_well = np.max(well_dateoftest)  #if we want the most recent pressure

				#average_data = max(well_test_data) #if we want the initial pressure
				#test_date_well = np.min(well_dateoftest)  #if we want the initial pressure
				
				#------------

				#average data keyed by well 
				DST_well_data[well] = average_data
				DST_test_dates[well] = test_date_well
				DST_data_array.append(average_data)
				date_differences.append(test_date_well)

				#pressure and test date in dict
				pressure_time_dict[well] = [well_test_data,well_dateoftest]


	#well heading of interest - ie what we will plot the data against
	well_depth_index = well_data_headings.index('TVD (m)')

	press_array = []
	depth_array = []

	if len(wells_with_DST) > 0:

		for well in DST_well_data:
			try:
				plt.scatter(float(well_data[well][well_depth_index])*m_ft,DST_well_data[well]*kpa_psi)
				press_array.append(float(DST_well_data[well])*kpa_psi)
				depth_array.append(float(well_data[well][well_depth_index])*m_ft)
			except:
				pass
		
		#print out data
		print(('Number of wells with DST Data',len(wells_with_DST)))
		print(('Number of wells with multiple DSTs',len(wells_with_multiple_DST)))
		#print('The average' + DST_headings[index_of_interest], np.mean(DST_data_array))
		print(('Average max pressure (psi) ', np.mean(DST_data_array)*kpa_psi))
		print(('Average max pressure (kpa) ', np.mean(DST_data_array)))
		print(('Average well depth for test wells (ft)', np.mean(depth_array)))
		print(('Average well depth for test wells (m)', np.mean(depth_array)*(float(1)/m_ft)))
		print(('Average days between drilling and test', np.mean(date_differences)))
		#print('The average number of days between drilling completion and DST; ', np.mean(date_differences))


		#line fitting
		#print(len(press_array),len(depth_array))
		linear = np.polyfit(depth_array,press_array,1)
		print(('\nLinear Equation of best fit; Pressure (psi) = ' + str("%.5f" %linear[0]) + '*TVD (ft) + ' + str("%.2f" %linear[1]) + ' psi'))
		stat = stats.linregress(depth_array, press_array)
		#slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
		slope = stat[0]
		intercept = stat[1]
		print(('Slope; ' + str(stat[0])))
		print(('Intercept; ' + str(stat[1])))
		print(('r_square_value; ' + str(stat[2])))
		print(('p_value; ' + str(stat[3])))
		print(('std_err; ' + str(stat[4])))
		print('\n')

		#pressure gradient
		gradient_array = []
		for i in range(0,len(press_array)):
			gradient_array.append(press_array[i]/depth_array[i])
		pressure_gradient = np.mean(gradient_array)
		print(('Average Pressure Gradient (psi/ft)', pressure_gradient))

		# Kareem edits
		if inputs_instance.pressure_plot == True:
			#plot of pressure vs depth
			plt.xlabel('TVD (ft)')
			plt.ylabel('Max Pressure (psi)')
			plt.ylim(0,np.max(press_array))
			plt.xlim(0,np.max(depth_array))
			proj_name =  OPGEE_data['assessed field'][OPGEE_data['headings'].index('Field name')]
			plt.title(proj_name + ' - Max Pressure (psi)' + '  ' + '(count ' + str(len(wells_with_DST)) + ')')
			plt.show()
			plt.clf()

		count = 0 

		#pressure decline analysis
		'''
		for well in pressure_time_dict:
			if len(pressure_time_dict[well][0]) > 1:
				plt.plot(pressure_time_dict[well][1], pressure_time_dict[well][0])
				count += 1

		plt.xlim(left = 0)
		plt.title('Pressure (kpa) vs Days after Drilling Completed (Count ' + str(count) + ')' )
		plt.show()
		'''	

		#---------OPGEE field Data----------------

		OPGEE_pressure_index = OPGEE_data['headings'].index('Reservoir pressure')
		# The average of recorded pressures 
		OPGEE_data['assessed field'][OPGEE_pressure_index] = np.mean(DST_data_array)*kpa_psi

		print('\n~~~Collecting OPGEE pressure inputs~~~')
		print('\nThe most recent DST data is used (if over 100 psi)\n')

		# Kareem edits
		# ask_pressure_value = str(input('Would you like to use the calculated pressure gradient (' + str(round(pressure_gradient,3)) + 'psi/ft) ? \nIf no the default pressure gradient is assumed (0.45 psi/ft)\n\nYes/No?   '))
		ask_pressure_value = str(inputs_instance.pressure_gradient)
		print("Chosen option for using the calculated pressure gradient is", ask_pressure_value)

		#-----------OPGEE well data--------
		for well in well_data:
			if well in DST_data:
				try:
					most_recent_pressure = float(DST_data[well][-1][max_pressure_index])*kpa_psi
					#if it is less that 100 psi likely an error
					if most_recent_pressure > 100:
						OPGEE_data[well][OPGEE_pressure_index] = most_recent_pressure
					else:
						depth = float(well_data[well][well_depth_index])
						OPGEE_data[well][OPGEE_pressure_index] = depth*m_ft*pressure_gradient
					#print(well, most_recent_pressure, 'from DST',depth)
				except:
					try:
						if ask_pressure_value[0].upper() == 'Y':
							depth = float(well_data[well][well_depth_index])
							pressure_from_gradient = depth*m_ft*pressure_gradient 
							OPGEE_data[well][OPGEE_pressure_index] = pressure_from_gradient
						else:
							#print('using default')
							#we keep the default 0.45psi/ft
							pass
					except:
						#print(well,'missing depth data but has DST')
						pass
				#print(well,most_recent_pressure, 'from DST',depth)
			if well not in DST_data:
				try:
					if ask_pressure_value[0].upper() == 'Y':
						#calculayes pressure based on gradient 
						depth = float(well_data[well][well_depth_index])
						pressure_from_gradient = depth*m_ft*pressure_gradient 
						OPGEE_data[well][OPGEE_pressure_index] = pressure_from_gradient
						#print(well, pressure_from_equation, 'from equation', depth*m_ft)
					else:
						#print('using default')
						pass
				except:
					#we keep the default 0.45psi/ft
					#print(well,'missing depth data')
					pass
	
	if len(wells_with_DST) == 0:

		print('\n\nNo project wells have DST data\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

	print('\n')
	return OPGEE_data

if __name__ == '__main__':
	
	from .get_DST_data import get_DST_data
	from .OPGEE_defaults import OPGEE_defaults
	from .well_search import well_search
	from .general_well_data_analysis import OPGEE_well_data, general_well_data_analysis
	from .get_all_post_2005_well_data import get_all_post_2005_well_data
	from .OPGEE_input_sensitivity import OPGEE_input_sensitivity
	
	well_data_headings, well_data, project_name = well_search()
	#well_data_headings, well_data = get_all_post_2005_well_data()
	#well_data_headings, well_data = get_formation_well_data()

	OPGEE_data = OPGEE_defaults()

	field_name = 'poop'

	OPGEE_data = general_well_data_analysis(well_data_headings, well_data, OPGEE_data, field_name)

	OPGEE_data = OPGEE_well_data(well_data, well_data_headings, OPGEE_data)

	DST_data, DST_headings = get_DST_data()

	OPGEE_data = DST_analysis(well_data, well_data_headings, DST_data, DST_headings, OPGEE_data)

	OPGEE_input_sensitivity(OPGEE_data, well_data)


