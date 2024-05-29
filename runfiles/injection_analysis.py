
from datetime import datetime, timedelta
import collections 

from .dates_array import dates_array

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def injection_dates():

	print('\nSelect the dates for which you would like to assess injection')
	print('The available data set contains monthly injection data for wells between Jan-2005 and Dec-2019')
	print('For OPGEE field assessment, adjust start date to be first drill year\n')
	start_date = str(input('Enter the Start Date (YYYY-MM): '))
	end_date = str(input('Enter the End Date (YYYY-MM): '))
	print('\n')

	date_array = dates_array(start_date, end_date)

	return date_array



def injection_summary(injection_data_headings, injection_data, well_data, well_data_headings, date_array):

	injection_dict = collections.OrderedDict()
	empty_headings_array = []

	print('\n~~~~~~~~~~~~~~~~~~~~~~ INJECTION ANALYSIS  ~~~~~~~~~~~~~~~~~~~~~~ ')

	start_date = date_array[0]
	end_date = date_array[1]

	producing_wells = [] #these are the wells producing in the timeframe

	#injection data indexing 
	for i in range(0,len(injection_data_headings)):
		empty_headings_array.append([])
		if injection_data_headings[i] == 'Date':
			date_index = i
		if injection_data_headings[i] == 'INJ Pressure kPa':
			inj_press_index = i
	
	#well data indexing
	#well_status_index = well_data_headings.index('Well Status Text')


	#we structure the summary data for all producing wells in a dictionary
	#index of dictionary - dictionary[catagory][year_month] = value
	#NEED TO FIX CUMULATIVES!

	for well in injection_data:
		#well_type = well_data[well][well_status_index]

		for catagory in range(1,len(injection_data_headings)):
			#we exclude the date catagory
			type_ = injection_data_headings[catagory] #the data type - eg AVG daily gas
			if type_ not in injection_dict:
				#for first well add a dictionary for each catagory  
				injection_dict[type_] = dict()
				for date in date_array:
					#get dates of interest from data array
					injection_dict[type_][date] = []
			for i in range(0,len(injection_data[well])):
				#for each year-month of data 
				year_month = injection_data[well][i][date_index]
				if year_month in injection_dict[type_]:
					#if the year month is in the dates of interest 
					#append the values to an array  
					injection_dict[type_][year_month].append(float(injection_data[well][i][catagory]))

	#now we have all values in array form for each date, we need to sum average depending on data type
	for i in range(1,len(injection_data_headings)):
		catagory = injection_data_headings[i]
		for year_month in injection_dict[catagory]:
			if i == inj_press_index: #average this data
				injection_dict[catagory][year_month] = np.mean(injection_dict[catagory][year_month])
			else:
				injection_dict[catagory][year_month] = sum(injection_dict[catagory][year_month])

	#we need to fix the cumulative values - 
	#They dont sum properly. If wells stop producing early, cumulative will not be summed the nect month
	#Thus, we will calculate the cumulatives by summing monthly injection volumes

	for catagory in injection_data_headings:
		if 'Cum' in catagory:
			#for the cumulative catagories
			for year_month in date_array:
				#instead we will sum the month gas catagories for each catagory
				split = catagory.split(' ') #split PRD Cumulative Gas e3m3 to ['PRD','Cumulative','Gas','e3e3']
				monthly_catagory = split[0] + ' ' + 'Monthly'
				#we have labels of variying length
				for i in range(2, len(split)):
					monthly_catagory = monthly_catagory + ' ' + split[i]
				if year_month == date_array[0]:
					#for the first day we just want to equate the month not sum to previous
					injection_dict[catagory][year_month] = injection_dict[monthly_catagory][year_month]
				elif year_month != date_array[0]:
					#sum current month onto previous month
					prev_month = date_array[date_array.index(year_month) - 1] #set previous month for next iteration
					injection_dict[catagory][year_month] = injection_dict[catagory][prev_month] + injection_dict[monthly_catagory][year_month]
				



	return injection_dict

def injection_plotter(injection_data, injection_data_headings, injection_dict, date_array):

	start_date = date_array[0] 
	end_date =  date_array[-1]

	print('PLOT OPTIONS\n')
	
	for i in range(1,len(injection_data_headings)):
		print((str(i) + ') ' + injection_data_headings[i]))

	plot_option = plot_option = int(eval(input('\nWhat would you like to plot? Choose from above options or type 0 to exit:     ')))

	while plot_option != 0:

		catagory = injection_data_headings[plot_option]

		dates = []
		values = []

		for i in range(0,len(date_array)):
			try:
				values.append(injection_dict[catagory][date_array[i]])
				dates.append(date_array[i])
			except:
				values.append(0)
				dates.append(date_array[i])

		#print(date_array)
		print('\n')
		print((injection_data_headings[plot_option] + ' Over the Period: ' + str(start_date) + ' to ' + str(end_date)))
		print('\n')
		print(values)
		print('\n')

		plt.plot(dates,values)
		plt.title(injection_data_headings[plot_option])
		plt.xlabel('Date')
		xtick_frequency = 3
		#plt.xticks(rotation = 90)
		plt.xticks(dates[::xtick_frequency], dates[::xtick_frequency], rotation = 90)
		plt.show()

		plot_option = int(eval(input('\nWhat would you like to plot? Choose from above options or type 0 to exit:     ')))

	#Summary Statistics across period

	'''
	print('\n\n ~~~~~~~~~~~~ SUMMARY STATISTICS ~~~~~~~~~~~~ \n')
	print('Period Assessed: ' + str(start_date) + ' to ' + str(end_date))
	print('Number of wells having produced in that period: ' + str(len(injection_data)))
	print('\nCUMULATIVES BY END OF PERIOD ASSESSED')
	print('\nAVERAGE RATES OVER PERIOD ASSESSED')
	print('\nFor OPGEE we will consider Oil to be both condensate and oil volumes (C5+)\n')
	'''
	
	return

def injection_analysis(date_array, well_data, well_data_headings):

	from .get_injection_data import get_injection_data

	injection_data_headings, injection_data, prod_well_data_headings, prod_well_header_data = get_injection_data(well_data)

	injection_dict = injection_summary(injection_data_headings, injection_data, well_data, well_data_headings, date_array)
	injection_plotter(injection_data, injection_data_headings, injection_dict, date_array)

	return


if __name__ == '__main__':

	from .well_search import well_search
	from .get_injection_data import get_injection_data

	well_data_function = well_search()

	well_data_headings = well_data_function[0] 
	well_data = well_data_function[1] 
	#well_data = []

	date_array = injection_dates()
	
	injection_analysis(date_array)
