#all_province_facility_summary
import collections
import numpy as np

def all_province_facility_summary(well_data, well_data_headings, province_facility_total, connected_project_wells, connected_facilites, OPGEE_data, date_array):

	m3_scf = 35.314666
	m3_bbl = 6.2898

	print('\n=====================================\n  ALL PROVINCE FACILITY ASSESSMENT\n=====================================\n')
	print('calculating FFV rates for the formation from all facility data\n')

	print(str(connected_project_wells) + ' wells have been found connected to ' + str(connected_facilites) + ' facilites')
	print('Period assessed; ' + str(date_array[0]) + ' to ' + str(date_array[-1]))
	print('\n')

	activities = ['PROD GAS', 'FLARE GAS', 'VENT GAS', 'FUEL GAS', 'PROD COND', 'PROD OIL','REC GAS','DISP GAS']

	period_total = collections.OrderedDict()

	for province in province_facility_total:
		for year_month in date_array:
			if year_month not in period_total:
				period_total[year_month] = np.zeros(len(activities))
			if year_month in province_facility_total[province]:
				for activity in activities:
					if activity in province_facility_total[province][year_month]:
						period_total[year_month][activities.index(activity)] += province_facility_total[province][year_month][activity]


	print('year_month' + ', ' + str(activities))
	period_cumulative = np.zeros(len(activities))
	for year_month in period_total:
		print(year_month, [round(x,2) for x in period_total[year_month]])
		period_cumulative = [x + y for x, y in zip(period_cumulative, period_total[year_month])]

	print('\nTotals; ' + str(date_array[0]) + ' to ' + str(date_array[-1]))
	for i in range(0,len(activities)):
		print(activities[i] + ' , ' + str(round(period_cumulative[i],2)))

	prod_oil = period_cumulative[activities.index('PROD OIL')] + period_cumulative[activities.index('PROD COND')]

	if prod_oil == 0:
		fuel_rate = 0
		flare_rate = 0
		vent_rate = 0
		gas_oil_ratio = 0
			
	elif prod_oil != 0:
		fuel_rate = (period_cumulative[activities.index('FUEL GAS')]*1000*m3_scf)/(period_cumulative[activities.index('PROD OIL')]*m3_bbl)
		flare_rate = (period_cumulative[activities.index('FLARE GAS')]*1000*m3_scf)/(period_cumulative[activities.index('PROD OIL')]*m3_bbl)
		vent_rate = (period_cumulative[activities.index('VENT GAS')]*1000*m3_scf)/(period_cumulative[activities.index('PROD OIL')]*m3_bbl)
		gas_oil_ratio = (period_cumulative[activities.index('PROD GAS')]*1000*m3_scf)/(period_cumulative[activities.index('PROD OIL')]*m3_bbl)


	fuel_percentage =  (period_cumulative[activities.index('FUEL GAS')])/(period_cumulative[activities.index('PROD GAS')] + period_cumulative[activities.index('REC GAS')])
	flare_percentage =  (period_cumulative[activities.index('FLARE GAS')])/(period_cumulative[activities.index('PROD GAS')] + period_cumulative[activities.index('REC GAS')])
	vent_percentage =  (period_cumulative[activities.index('VENT GAS')])/(period_cumulative[activities.index('PROD GAS')] + period_cumulative[activities.index('REC GAS')])

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

	try:
		print('\nPecentage of total project wells with facility data; ' + str(float(connected_project_wells)*100/len(well_data)))
	except:
		pass

	#Enter into OPGEE Data 
	field_GOR = OPGEE_data['assessed field'][OPGEE_data['headings'].index('Gas-to-oil ratio (GOR)')]

	OPGEE_data['assessed field'][OPGEE_data['headings'].index('Flaring-to-oil ratio')] = round(field_GOR*flare_percentage,4)
	OPGEE_data['assessed field'][OPGEE_data['headings'].index('Venting-to-oil ratio')] = round(field_GOR*vent_percentage,4)

	OPGEE_data['assessed field'][OPGEE_data['headings'].index('Facility flared gas')] = round(flare_percentage*100,4)
	OPGEE_data['assessed field'][OPGEE_data['headings'].index('Facility vented gas')] = round(vent_percentage*100,4)
	OPGEE_data['assessed field'][OPGEE_data['headings'].index('Facility fuel gas')] = round(fuel_percentage*100,4)
	OPGEE_data['assessed field'][OPGEE_data['headings'].index('Facility gas-to-oil ratio')] = round(gas_oil_ratio,4)

	print('\n--------------------------------------------------------------\n')

	return OPGEE_data

if __name__ == '__main__':
	

	from well_search import well_search
	from OPGEE_defaults import OPGEE_defaults
	from dates_array import dates_array
	from general_well_data_analysis import OPGEE_well_data
	from AB_facility_analysis_new import AB_facility_analysis
	from BC_facility_analysis_new import BC_facility_analysis
	from SK_facility_analysis_new import SK_facility_analysis
	from OPGEE_input_sensitivity import OPGEE_input_sensitivity
	
	date_array = dates_array('2017-01','2017-12')

	#well_data_function = get_formation_well_data() # MONTNEY
	well_data_function = well_search()
	#well_data_function = get_all_post_2005_well_data()


	well_data_headings = well_data_function[0] 
	well_data = well_data_function[1] 
	#well_data = []
	
	OPGEE_data = OPGEE_defaults()

	OPGEE_data = OPGEE_well_data(well_data, well_data_headings, OPGEE_data)

	province_facility_total = collections.OrderedDict()

	OPGEE_data, province_facility_total['AB'], count_AB_wells, count_AB_facilities = AB_facility_analysis(well_data, well_data_headings, OPGEE_data, date_array)
	OPGEE_data, province_facility_total['BC'], count_BC_wells, count_BC_facilities =  BC_facility_analysis(well_data, well_data_headings, OPGEE_data, date_array)
	OPGEE_data, province_facility_total['SK'], count_SK_wells, count_SK_facilities = SK_facility_analysis(well_data, well_data_headings, OPGEE_data, date_array)	
	
	connected_project_wells = count_SK_wells + count_BC_wells + count_AB_wells
	connected_facilities = count_SK_facilities + count_BC_facilities + count_AB_facilities

	OPGEE_data = all_province_facility_summary(well_data, well_data_headings, province_facility_total, connected_project_wells, connected_facilities, OPGEE_data, date_array)

	OPGEE_input_sensitivity(OPGEE_data, well_data)