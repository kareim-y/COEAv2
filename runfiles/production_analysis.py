#production_analysis

from datetime import datetime, timedelta
import collections 
from .dates_array import dates_array
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def production_dates():

	print('\nSelect the dates for which you would like to assess production')
	print('The available data set contains monthly production data for wells between Jan-2005 and Dec-2019')
	print('For OPGEE field assessment, adjust start date to be first drill year\n')
	start_date = str(input('Enter the Start Date (YYYY-MM): '))
	end_date = str(input('Enter the End Date (YYYY-MM): '))
	print('\n')

	date_array = dates_array(start_date, end_date)

	return date_array


def sumaverage_production_value(well, production_data, production_data_headings, date_array, variable, sum_or_average):

	#takes in the above data and returns either the sum or average average over that period

	variable_array = []
	
	for year_month in range(0,len(production_data[well])):
		date = production_data[well][year_month][production_data_headings.index('Date')]
		if date in date_array:
			variable_array.append(float(production_data[well][year_month][production_data_headings.index(variable)]))

	if len(variable_array) > 0:
		if sum_or_average.upper() == 'SUM':
			result = sum(variable_array)
		if sum_or_average[0:3].upper() == 'AVE':
			result = np.mean(variable_array)
		return result

	if len(variable_array) == 0:
		return 0



def production_summary(production_data_headings, production_data, well_data, well_data_headings, date_array):

	production_dict = collections.OrderedDict()
	empty_headings_array = []

	print('\n~~~~~~~~~~~~~~~~~~~~~~ PRODUCTION ANALYSIS  ~~~~~~~~~~~~~~~~~~~~~~ ')

	start_date = date_array[0]
	end_date = date_array[1]

	producing_wells = [] #these are the wells producing in the timeframe

	#production data indexing 
	for i in range(0,len(production_data_headings)):
		empty_headings_array.append([])
		if production_data_headings[i] == 'Date':
			date_index = i
		if production_data_headings[i] == 'PRD Ratio: WTR/OIL m3/m3':
			prd_ratio_index = i
		if production_data_headings[i] == 'PRD Percent: OIL Cut %':
			prd_percent_index = i
		if production_data_headings[i] == 'PRD Cumulative GAS e3m3':
			cum_gas_index = i
		if production_data_headings[i] == 'PRD Cumulative HRS hrs':
			cum_hrs_index = i
	
	#well data indexing
	for i in range(0,len(well_data_headings)):
		if well_data_headings[i] == 'Well Status Text':
			well_status_index = i


	#we structure the summary data for all producing wells in a dictionary
	#index of dictionary - dictionary[catagory][year_month] = value
	#NEED TO FIX CUMULATIVES!

	for well in production_data:
		well_type = well_data[well][well_status_index]

		for catagory in range(1,len(production_data_headings)):
			#we exclude the date catagory
			type_ = production_data_headings[catagory] #the data type - eg AVG daily gas
			if type_ not in production_dict:
				#for first well add a dictionary for each catagory  
				production_dict[type_] = dict()
				for date in date_array:
					#get dates of interest from data array
					production_dict[type_][date] = []
			for i in range(0,len(production_data[well])):
				#for each year-month of data 
				year_month = production_data[well][i][date_index]
				if year_month in production_dict[type_]:
					#if the year month is in the dates of interest 
					#append the values to an array  
					production_dict[type_][year_month].append(float(production_data[well][i][catagory]))

	#now we have all values in array form for each date, we need to sum average depending on data type
	for i in range(1,len(production_data_headings)):
		catagory = production_data_headings[i]
		for year_month in production_dict[catagory]:
			if (prd_ratio_index <= i <= prd_percent_index): #average this data
				production_dict[catagory][year_month] = np.mean(production_dict[catagory][year_month])
			else:
				production_dict[catagory][year_month] = sum(production_dict[catagory][year_month])

	#we need to fix the cumulative values - 
	#They dont sum properly. If wells stop producing early, cumulative will not be summed the nect month
	#Thus, we will calculate the cumulatives by summing monthly production volumes

	for catagory in production_data_headings[cum_gas_index:cum_hrs_index+1]:
		#for the cumulative catagories
		for year_month in date_array:
			#instead we will sum the month gas catagories for each catagory
			split = catagory.split(' ') #split PRD Cumulative Gas e3m3 to ['PRD','Cumulative','Gas','e3e3']
			monthly_catagory = split[0] + ' ' + 'Monthly' + ' ' + split[2] + ' ' + split[3] #converts to monthly
			if year_month == date_array[0]:
				#for the first day we just want to equate the month not sum to previous
				production_dict[catagory][year_month] = production_dict[monthly_catagory][year_month]
			elif year_month != date_array[0]:
				#sum current month onto previous month
				prev_month = date_array[date_array.index(year_month) - 1] #set previous month for next iteration
				production_dict[catagory][year_month] = production_dict[catagory][prev_month] + production_dict[monthly_catagory][year_month]
			



	return production_dict

def production_plotter(production_data, production_data_headings, production_dict, date_array):

	start_date = date_array[0] 
	end_date =  date_array[-1]

	print('PLOT OPTIONS\n')
	
	for i in range(1,len(production_data_headings)):
		print((str(i) + ') ' + production_data_headings[i]))

	plot_option = plot_option = int(eval(input('\nWhat would you like to plot? Choose from above options or type 0 to exit:     ')))

	while plot_option != 0:

		catagory = production_data_headings[plot_option]

		dates = []
		values = []

		for i in range(0,len(date_array)):
			try:
				values.append(production_dict[catagory][date_array[i]])
				dates.append(date_array[i])
			except:
				values.append(0)
				dates.append(date_array[i])

		#print(date_array)
		print('\n')
		print((production_data_headings[plot_option] + ' Over the Period: ' + str(start_date) + ' to ' + str(end_date)))
		print('\n')
		for val in values:
			print(val)
		print('\n')

		plt.plot(dates,values)
		plt.title(production_data_headings[plot_option])
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
	print('Number of wells having produced in that period: ' + str(len(production_data)))
	print('\nCUMULATIVES BY END OF PERIOD ASSESSED')
	print('\nAVERAGE RATES OVER PERIOD ASSESSED')
	print('\nFor OPGEE we will consider Oil to be both condensate and oil volumes (C5+)\n')
	'''
	
	return

	#------------------OPGEE DATA-------------------------

def OPGEE_production_data(OPGEE_data, production_data, production_dict, date_array):

	print('\nGathering Project Production Data OPGEE inputs\n')

	start_date = date_array[0] 
	end_date =  date_array[-1]

	m3_scf = 35.315
	m3_bbl = 6.289814

	#--------Field OPGEE Data--------

	for i in range(0, len(OPGEE_data['headings'])):

		if OPGEE_data['headings'][i] == 'Oil production volume':
			ave_oil = []
			ave_cnd = []
			for date in date_array:
				ave_oil.append(production_dict['PRD Calndr-Day Avg OIL m3'][date])
				ave_cnd.append(production_dict['PRD Calndr-Day Avg CND m3'][date])
			ave_c5 = (np.mean(ave_oil) + np.mean(ave_cnd))*m3_bbl #non-weighted avg
			OPGEE_data['assessed field'][i] = round(ave_c5,3)
			#print(OPGEE_data['headings'][i] + '   ' + str(OPGEE_data['assessed field'][i]))

		if OPGEE_data['headings'][i] == 'Number of producing wells':
			OPGEE_data['assessed field'][i] = len(production_data)
			#print(OPGEE_data['headings'][i] + '   ' + str(OPGEE_data['assessed field'][i]))

		if OPGEE_data['headings'][i] == 'Gas-to-oil ratio (GOR)':
			cum_gas = (production_dict['PRD Cumulative GAS e3m3'][date_array[-1]] - production_dict['PRD Cumulative GAS e3m3'][date_array[0]])*1000*m3_scf
			cum_oil = (production_dict['PRD Cumulative OIL m3'][date_array[-1]] - production_dict['PRD Cumulative OIL m3'][date_array[0]])*m3_bbl
			cum_cnd = (production_dict['PRD Cumulative CND m3'][date_array[-1]] - production_dict['PRD Cumulative CND m3'][date_array[0]])*m3_bbl
			OPGEE_data['assessed field'][i] = round(cum_gas/(cum_cnd +cum_oil),3)
			#print(OPGEE_data['headings'][i] + '   ' + str(OPGEE_data['assessed field'][i]))

		if OPGEE_data['headings'][i] == 'Water-to-oil ratio (WOR)':
			cum_water = (production_dict['PRD Cumulative WTR m3'][date_array[-1]] - production_dict['PRD Cumulative WTR m3'][date_array[1]])*m3_bbl
			OPGEE_data['assessed field'][i] = round(cum_water/(cum_oil + cum_cnd),3)
			#print(OPGEE_data['headings'][i] + '   ' + str(OPGEE_data['assessed field'][i]))

	#change field age to how long it has been producing 
	
	field_age_index = OPGEE_data['headings'].index('Field age')
	age = float(len(date_array))/12
	if age > 0:
		OPGEE_data['assessed field'][field_age_index] = round(age,3)	

	return OPGEE_data


def well_production_analysis(production_data, production_data_headings, well_data, well_data_headings):

	print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nFirst Year Production Trend Analysis')
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

	from .well_plotter import  plot_color_label_for_tight_oil

	csv_dict = {}

	#assess first year production from formation by year
	
	yearly_prod_data = collections.OrderedDict()
	yearly_prod_count = collections.OrderedDict()

	#Indexing
	drill_date_index = well_data_headings.index('Date Drlg Completed')
	spud_index_date = drill_date_index = well_data_headings.index('Date Well Spudded')
	operator_index = well_data_headings.index('Cur Operator Name')
	drill_operator_index = well_data_headings.index('Drilling Contractor')
	formation_index = well_data_headings.index('Prod./Inject. Frmtn')
	province_index = well_data_headings.index('Area')
	area_field_index = well_data_headings.index('Producing Field/Area Name')
	pool_index = well_data_headings.index('Producing Pool Name')
	well_UWI_index = well_data_headings.index('CPA Well ID')
	study_formation_index = 'using study labels..'

	#'PRD Ratio: WTR/OIL m3/m3':
	#'PRD Percent: OIL Cut %':

	#selected_index = study_formation_index #this is what we will base our search off of
	selected_index = drill_date_index

	months_assessed = 12

	for well in production_data:
		
		if len(production_data[well]) > months_assessed:
			#if the selected catagory is year, then we only want the year from the date
			if selected_index == drill_date_index:
				catagory = (well_data[well][selected_index][-4:]) #not necissarily the year, whatever the selected_index reprisents
			elif selected_index == study_formation_index:
				color, catagory  = plot_color_label_for_tight_oil(well, well_data, well_data_headings)
			else:
				#otherwise we take the full description
				catagory = str((well_data[well][selected_index]))


			if catagory not in yearly_prod_data:
				#if the catagory isnt in the dictionary yet
				yearly_prod_data[catagory] = []
				for i in range(0,months_assessed):
					#we are doing it for all prod data types - gas prod, oil prod etc. We exclude the date however (hence len(headings) - 1)
					yearly_prod_data[catagory].append(np.zeros(len(production_data_headings) - 1))
				yearly_prod_count[catagory] = 0 # we initilize the count 
			if catagory in yearly_prod_data:
				#dictionary of how many wells fall into each catagory
				yearly_prod_count[catagory] = yearly_prod_count[catagory] + 1 # add the count
			
			for i in range(0,months_assessed):
				#for each month in the months assessed 
				for j in range(1,len(production_data_headings)):
					#monthly data is added based on the catagory 
					#we want to ensure that we have data for the header of interest - Ie well is not an injector and brings the average down
					#NEED TO FIX ABOVE - CURRENTLY AVERAGE IS BEING DRAWN DOWN BY NON PRODUCERS WHICH HAVE MORE THAN 12 MONTHS PROD DATA 
					#j-1 because we want to start at 0, but we ignore the date string in production data 
					yearly_prod_data[catagory][i][j-1] = yearly_prod_data[catagory][i][j-1] + float(production_data[well][i][j])



	#organise dictionary in ascending order (201601, 201602 ...)
	yearly_prod_data = collections.OrderedDict(sorted(list(yearly_prod_data.items()), key=lambda t: t[0]))

	if selected_index == well_UWI_index:
		minimum_well_count = 0
	else:
		minimum_well_count = 2 #we set a minimum criteria for plotting - there must be at least 50 wells in a catagory -eg year - to plot

	for i in range(1,len(production_data_headings)):
		print((str(i) + ') ' + production_data_headings[i]))

	plot_option = plot_option = int(eval(input('\nWhat would you like to plot? Choose from above options or type 0 to exit:     ')))

	while plot_option != 0:
		for catagory in yearly_prod_data:
			if int(yearly_prod_count[catagory]) >= minimum_well_count:
				#if we have more than the minimum wells in the catagory 
				catagory_data = []
				for i in range(0,months_assessed):
					#plot option -1 because we ignore the dates 
					catagory_data.append(float(yearly_prod_data[catagory][i][plot_option-1])/int(yearly_prod_count[catagory]))

				if catagory == study_formation_index:
					label = 'Formation :' + str(yearly_prod_count[catagory])
				else:
					label = str(catagory) + ' : ' + str(yearly_prod_count[catagory]) + ' wells'
				
				plt.plot(list(range(0,months_assessed)),catagory_data, label = label)
				print((label + ';' + str(np.around(catagory_data,decimals=1))))

		
		if selected_index == study_formation_index:
			plot_title = 'Formation'
		else:
			plot_title = well_data_headings[selected_index]

		plt.legend(loc = 'upper right', title = plot_title, fontsize='xx-small')
		plt.ylabel(production_data_headings[plot_option])
		plt.xlabel('Month')
		plt.xticks(list(range(0,months_assessed)),list(range(1,months_assessed+1)))
		plt.title('First ' + str(months_assessed) + ' Month Average From Wells: ' + production_data_headings[plot_option])
		plt.show()

		
		plot_option = int(eval(input('\nWhat would you like to plot? Choose from above options or type 0 to exit:     ')))

	return


def OPGEE_well_production_data(production_data, production_data_headings, OPGEE_data, date_array):

	print('\nGathering Individual Well Production Data OPGEE inputs\n')

	m3_scf = 35.315
	m3_bbl = 6.289814
	m3m3_scfbbl = 5.614583

	#at the moment it looks at the complete well production, and not within the date range specified

	for well in production_data:

			#print(well + '\n')

			well_producing_months = []

			for year_month in range(0,len(production_data[well])):
				date = production_data[well][year_month][production_data_headings.index('Date')]
				if date in date_array:
					well_producing_months.append(date)

			well_age = float(len(well_producing_months)) / 12 #number of years it has been porducing

			#get cum oil gas condensate and water volumes over period
			cum_oil = sumaverage_production_value(well, production_data, production_data_headings, date_array, 'PRD Monthly OIL m3', 'SUM')*m3_bbl
			cum_cnd = sumaverage_production_value(well, production_data, production_data_headings, date_array, 'PRD Monthly CND m3', 'SUM')*m3_bbl
			cum_gas = sumaverage_production_value(well, production_data, production_data_headings, date_array, 'PRD Monthly GAS e3m3', 'SUM')*1000*m3_scf
			cum_water = sumaverage_production_value(well, production_data, production_data_headings, date_array, 'PRD Monthly WTR m3', 'SUM')*m3_bbl
			cum_c5_plus = cum_oil + cum_cnd

			#average per day
			if well_age > 0:
				avg_c5_plus = cum_c5_plus/(well_age*365)
			elif well_age <= 0:
				avg_c5_plus = 0

			for i in range(0, len(OPGEE_data['headings'])):

				if OPGEE_data['headings'][i] == 'Field age':
					OPGEE_data[well][i] = round(float(well_age),3) 

				if OPGEE_data['headings'][i] == 'Oil production volume':
					OPGEE_data[well][i] = round(float(avg_c5_plus),3)

				if OPGEE_data['headings'][i] == 'Number of producing wells':
					OPGEE_data[well][i] = 1
					
				if OPGEE_data['headings'][i] == 'Gas-to-oil ratio (GOR)':
					if cum_c5_plus != 0:
						GOR = cum_gas/cum_c5_plus
						OPGEE_data[well][i] = round(float(GOR),3)
					elif cum_c5_plus == 0:
						OPGEE_data[well][i] = 0

				if OPGEE_data['headings'][i] == 'Water-to-oil ratio (WOR)':
					if cum_c5_plus > 0:
						OPGEE_data[well][i] = round(float(cum_water/cum_c5_plus),3)
					elif cum_c5_plus == 0:
						OPGEE_data[well][i] = 0
			
			#Change field age to producing length

			

	#some wells dont have production date 

	return OPGEE_data

def production_analysis(well_data, well_data_headings, production_data, production_data_headings, OPGEE_data):

	well_production_analysis(production_data, production_data_headings, well_data, well_data_headings)
	
	date_array = production_dates()
	#date_array = ['2005-01', '2005-02', '2005-03', '2005-04', '2005-05', '2005-06', '2005-07', '2005-08', '2005-09', '2005-10', '2005-11', '2005-12', '2006-01', '2006-02', '2006-03', '2006-04', '2006-05', '2006-06', '2006-07', '2006-08', '2006-09', '2006-10', '2006-11', '2006-12', '2007-01', '2007-02', '2007-03', '2007-04', '2007-05', '2007-06', '2007-07', '2007-08', '2007-09', '2007-10', '2007-11', '2007-12', '2008-01', '2008-02', '2008-03', '2008-04', '2008-05', '2008-06', '2008-07', '2008-08', '2008-09', '2008-10', '2008-11', '2008-12', '2009-01', '2009-02', '2009-03', '2009-04', '2009-05', '2009-06', '2009-07', '2009-08', '2009-09', '2009-10', '2009-11', '2009-12', '2010-01', '2010-02', '2010-03', '2010-04', '2010-05', '2010-06', '2010-07', '2010-08', '2010-09', '2010-10', '2010-11', '2010-12', '2011-01', '2011-02', '2011-03', '2011-04', '2011-05', '2011-06', '2011-07', '2011-08', '2011-09', '2011-10', '2011-11', '2011-12', '2012-01', '2012-02', '2012-03', '2012-04', '2012-05', '2012-06', '2012-07', '2012-08', '2012-09', '2012-10', '2012-11', '2012-12', '2013-01', '2013-02', '2013-03', '2013-04', '2013-05', '2013-06', '2013-07', '2013-08', '2013-09', '2013-10', '2013-11', '2013-12', '2014-01', '2014-02', '2014-03', '2014-04', '2014-05', '2014-06', '2014-07', '2014-08', '2014-09', '2014-10', '2014-11', '2014-12', '2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06', '2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12', '2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12', '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09', '2017-10', '2017-11', '2017-12']
	production_dict = production_summary(production_data_headings, production_data, well_data, well_data_headings, date_array)
	production_plotter(production_data, production_data_headings, production_dict, date_array)
	OPGEE_data = OPGEE_production_data(OPGEE_data, production_data, production_dict, date_array)

	OPGEE_data = OPGEE_well_production_data(production_data, production_data_headings, OPGEE_data, date_array)
	

	#print(OPGEE_data['assessed field'])
	#print(OPGEE_data['202d005E094G0800'])
	

	return OPGEE_data


if __name__ == '__main__':

	from .OPGEE_defaults import OPGEE_defaults
	from .search_production_data import search_production_data
	import collections
	from .well_search import well_search
	from .general_well_data_analysis import OPGEE_well_data, general_well_data_analysis
	from .OPGEE_input_sensitivity import OPGEE_input_sensitivity
	from .get_all_post_2005_well_data import get_tight_oil_wells, get_all_post_2005_well_data

	#from LNG_well_search import LNG_well_search

	print('Importing General Well Data') #MONTN1EY
	#well_data_function = get_formation_well_data() # MONTNEY
	#well_data_function = get_tight_oil_wells()
	#well_data_function = LNG_well_search()
	well_data_function = well_search()
	#well_data_function = get_all_post_2005_well_data()

	general_well_data_headings = well_data_function[0] # MONTNEY
	general_well_data = well_data_function[1] # MONTNEY
	field_name = 'Montney'

	OPGEE_data = OPGEE_defaults()

	OPGEE_data = OPGEE_well_data(general_well_data, general_well_data_headings, OPGEE_data)

	production_data_headings, production_data, well_data_headings, well_header_data = search_production_data(general_well_data)

	production_analysis(general_well_data, general_well_data_headings, production_data, production_data_headings, OPGEE_data)
	
	#value = sumaverage_production_value('100141503010W500', production_data, production_data_headings, ['2016-01','2016-02'], 'PRD Monthly WTR m3', 'AVERAGE')
	#print(value)
	OPGEE_input_sensitivity(OPGEE_data, general_well_data)

	#for heading in range(0,len(OPGEE_data['100131108118W600'])):
	#	print(OPGEE_data['headings'][heading], OPGEE_data['100131108118W600'][heading], OPGEE_data['assessed field'][heading])

