#import dependant python packages
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
#from mpl_toolkits.basemap import Basemap 
import os
import csv
import collections
import pylab
import datetime
import re

#import runfiles I have written
from runfiles.get_AB_water_data import get_AB_water_source_data, AB_water_source_plotter
from runfiles.get_BC_water_data import get_BC_water_data
from runfiles.general_well_data_analysis import general_well_data_analysis, OPGEE_well_data
from runfiles.formation_fluid_functions import get_fluid_data, oil_analysis_summary, OPGEE_well_gas_data, OPGEE_well_oil_data, gas_analysis_summary
from runfiles.AB_water_analysis import AB_water_source_analysis
from runfiles.BC_water_analysis import BC_water_analysis
from runfiles.OPGEE_defaults import OPGEE_defaults
from runfiles.production_analysis import production_analysis,OPGEE_well_production_data
from runfiles.dates_array import dates_array
from runfiles.introduction import introduction
from runfiles.well_search import well_search
from runfiles.search_production_data import search_production_data
from runfiles.python_to_OPGEE import python_to_OPGEE
#from runfiles.induced_seismicity import induced_seismic_assessment
#from runfiles.get_seismic_data import get_NRC_seismic_data
from runfiles.environmental_reports import environmental_reports
from runfiles.well_plotter import well_plotter, get_well_coordinates
from runfiles.OPGEE_input_sensitivity import OPGEE_input_sensitivity
from runfiles.AB_facility_analysis import AB_facility_analysis
from runfiles.BC_facility_analysis import BC_facility_analysis
from runfiles.SK_facility_analysis import SK_facility_analysis
from runfiles.all_province_facility_summary import all_province_facility_summary
from runfiles.OPGEE_drilling_and_development import OPGEE_drilling_and_development
from runfiles.get_DST_data import get_DST_data
from runfiles.DST_analysis import DST_analysis
#from runfiles.shapefile_reader import formation_shapefile_plotter, plot_infrastructure
from runfiles.get_injection_data import get_injection_data
from runfiles.injection_analysis import injection_analysis, injection_dates
from runfiles.get_all_post_2005_well_data import get_tight_oil_wells, get_all_post_2005_well_data

from model_inputs import ModelInputs
import pickle

# Import Model Inputs from .pkl file
with open('model_input_instance.pkl', 'rb') as f:
	inputs_instance = pickle.load(f)

#text welcoming to module etc
introduction()

#----------------OPGEE-----------------
# initialize the dictionary where all OPGEE data will be stored and later exported into OPGEE
OPGEE_data = OPGEE_defaults()
start_time = time.time()
timer = time.time()
print('\n\nData is Loading Please Wait...\n\n')

#--------------------Search Wells---------------#

#this is the set of wells that data will be collectd for in the remainder of the functions
#well_data is stored in a dictionary {'Well UWI' : [well data]} - to know what is stored in the well_data file, print well_data_headings 
well_data_headings, well_data, field_name = well_search()
#well_data_headings, well_data = get_all_post_2005_well_data()
#well_data_headings, well_data, field_name = get_tight_oil_wells()
print('\n\n====================  Data available For Wells  ====================\n')
print(well_data_headings)
print('\n')

#----------------General Data Analysis----------#

#Do analysis of general well data for the secetd wells - e.g, number of wells, TVD's, etc
OPGEE_data = general_well_data_analysis(well_data_headings, well_data, OPGEE_data, field_name)
OPGEE_data = OPGEE_well_data(well_data, well_data_headings, OPGEE_data)

#----------------Plot Wells---------------------#

#plotter is not available because of basemap issuess
#well_plotter(well_data, well_data_headings) #edit within file if basemap (map of Canada) or shapefiles wanted 
#plt.clf()


#-------Post 2005 Production Data--------#

# Kareem Edits
# ask_production = str(input('Get Production Data (Y/N) ?:   '))
ask_production = inputs_instance.prod_data_checkbox
print('Chosen Response to \'Get Production Data (True/False)\': ', inputs_instance.prod_data_checkbox)
print('\n')

# Kareem Edits:
# if ask_production.upper() == 'Y':
if ask_production == True:	

	#Get production Data For the Wells of Interest 
	production_data_headings, production_data, production_well_data, production_well_data_headings = search_production_data(well_data)
	print('==================== Well Production Data Available   ====================\n')
	print(production_data_headings)
	print('\n')

	#------------------------Production Data Analysis-----------------------
	#Analysis of production data, and processing inputs for OPGEE model
	OPGEE_data = production_analysis(well_data, well_data_headings, production_data, production_data_headings, OPGEE_data)
	#clear from memory as takes up a lot of space
	del production_data_headings, production_data, production_well_data, production_well_data_headings


#------------- Post 2005 Injection Data -------------------

#get injection data - there is no connection to OPGEE yet
# ask_injection = str(input('Get Injection Data (Y/N) ?:   '))
ask_injection = inputs_instance.inject_data_checkbox
print('Chosen Response to \'Get Injection Data (True/False)\': ', inputs_instance.inject_data_checkbox)

# if ask_injection[0] == 'Y':
if ask_injection == True:

	date_array = injection_dates()

	injection_analysis(date_array, well_data, well_data_headings)
	print('\n')


#-----------------Formation Fluid Analysis ------------------

#Get formaion fluid data

# ask_fluid_data = str(input('Get Fluid Data (Y/N) ?:   '))
ask_fluid_data = inputs_instance.fluid_data_checkbox
print('Chosen Response to \'Get Fluid Data (True/False)\': ', inputs_instance.fluid_data_checkbox)

# if ask_fluid_data.upper() == 'Y':
if ask_fluid_data == True:

	print('Importing Gas, Water Oil Analysis Data')

	gas_analysis_headings, gas_data  = get_fluid_data('gas', well_data)
	oil_analysis_headings, oil_data = get_fluid_data('oil', well_data)
	#water_data = get_fluid_data('water', 'Montney')

	print('\n\n====================  Gas Analysis Data available   ====================\n')
	print(gas_analysis_headings)
	print('\n')

	#-------------------------Gas analysis-----------------------

	OPGEE_data = gas_analysis_summary(gas_analysis_headings, gas_data, OPGEE_data)
	OPGEE_data = OPGEE_well_gas_data(well_data, gas_analysis_headings, gas_data, OPGEE_data)

	print('\n\n====================  Oil Analysis Data available   ====================\n')
	print(oil_analysis_headings)
	print('\n')

	#--------------------------Oil Analysis----------------------------

	OPGEE_data = oil_analysis_summary(oil_analysis_headings, oil_data, OPGEE_data)
	OPGEE_data = OPGEE_well_oil_data(well_data, oil_analysis_headings, oil_data, OPGEE_data)
	
	print(('Computational Time (s): ' + "%.4f" %(time.time() - timer)))
	print('\n')
	timer = time.time()

	#water_analysis_headings = water_data[0]
	#water_data = water_data[1]

#---------------------DST Pressure Data =--------------

# ask_DST_data = str(input('Get Pressure/DST data (Y/N)?:  '))
ask_DST_data = inputs_instance.pressure_DST_data_checkbox
print('Chosen Response to \'Get Pressure/DST Data (True/False)\': ', inputs_instance.pressure_DST_data_checkbox)

# if ask_DST_data[0].upper() == 'Y':
if ask_DST_data == True:

	DST_data, DST_headings = get_DST_data()

	OPGEE_data = DST_analysis(well_data, well_data_headings, DST_data, DST_headings, OPGEE_data)


#---------------------AB water data---------------------------

# ask_water_data = str(input('Get HF Water Data (Y/N) ?:   '))
ask_water_data = inputs_instance.HF_water_checkbox
print('Chosen Response to \'Get HF Water Data (True/False)\': ', inputs_instance.HF_water_checkbox)


# if ask_water_data.upper() == 'Y':
if ask_water_data == True:	
	#--------------------------AB water Analysis---------------------------------------

	AB_water_source_analysis(well_data_headings, well_data)

	#AB_water_source_plotter(AB_water_data_headings, AB_water_data, well_data_headings, well_data)

	#----------------------------BC Water Analysis ------------------------------------------

	BC_water_analysis(well_data_headings, well_data)

	#-------------------------Year-Month----------------------

print('\n')
# ask_facility_data = str(input('Get Facility Data (Y/N) ?:   '))
ask_facility_data = inputs_instance.facility_data_checkbox
print('Chosen Response to \'Get Facility Data (True/False)\': ', inputs_instance.facility_data_checkbox)

# if ask_facility_data.upper() == 'Y':
if ask_facility_data == True:

	#get data for facilities connected to facilities

	print('\n===========================\n Facility Data Selection\n==========================\n')
	print('Monthly Facility Data is Available from 2014-01 to 2019-12')
	print('Enter The Date Range For Assessment (5-10 seconds per month)')

	start_date = str(inputs_instance.facility_startdate)
	print('Chosen Response for \'Start Date (YYYY-MM)\' is:', inputs_instance.facility_startdate)
	end_date = str(inputs_instance.facility_enddate)
	print('Chosen Response for \'End Date (YYYY-MM)\' is:', inputs_instance.facility_enddate)
	print('\n')

	dates_array = dates_array(start_date,end_date) #dates_array(start,end)

	print(('Period Assessed for Facilities ' + str(dates_array)))
	print('\n')
	
	province_facility_total = collections.OrderedDict()

	#summarising data for each province, getting flare vent rates for wells
	OPGEE_data, province_facility_total['AB'], count_AB_wells, count_AB_facilities = AB_facility_analysis(well_data, well_data_headings, OPGEE_data, dates_array)
	OPGEE_data, province_facility_total['BC'], count_BC_wells, count_BC_facilities =  BC_facility_analysis(well_data, well_data_headings, OPGEE_data, dates_array)
	OPGEE_data, province_facility_total['SK'], count_SK_wells, count_SK_facilities = SK_facility_analysis(well_data, well_data_headings, OPGEE_data, dates_array)	
	
	connected_project_wells = count_SK_wells + count_BC_wells + count_AB_wells
	connected_facilities = count_SK_facilities + count_BC_facilities + count_AB_facilities

	OPGEE_data = all_province_facility_summary(well_data, well_data_headings, province_facility_total, connected_project_wells, connected_facilities, OPGEE_data, dates_array)

#------------------------Induced Seismicity----------------
'''
ask_seismic = str(raw_input('Do Seismic Analysis (Y/N)?   '))
print('\n')

if ask_seismic.upper() == 'Y':

	induced_seismic_assessment(well_data_headings, well_data)

	print('\n\n')
		

ask_enviro_reprts = str(raw_input('See Associated Environmental Reports (Y/N)?   '))

if ask_enviro_reprts.upper() == 'Y':

	selected_env_reports = environmental_reports(well_data_headings, well_data)
'''
#---------OPGEE DRILLING AND DEVELOPMENT--------

OPGEE_data = OPGEE_drilling_and_development(OPGEE_data, well_data, well_data_headings)

#------------OPGEE---------------------------------

print('\n\n~~~~~~~~ OPGEEE INPUTS ~~~~~~~~~\n')
for i in range(0,len(OPGEE_data['headings'])):
	print((OPGEE_data['headings'][i] + '  (' + OPGEE_data['units'][i] + ')   ; ' + str(OPGEE_data['assessed field'][i])))

print('\n\n')
print(('Project total Computational time (seconds): ' + str(time.time() - start_time)))

# ask_OPGEE_sensitivity = str(input('\nWould you like to see distributions of the OPGEE input Parameters? (Y/N):   '))
ask_OPGEE_sensitivity = inputs_instance.OPGEE_distribution_checkbox
print('Chosen Response to \'Would you like to see distributions of the OPGEE input Parameters? (True/False)\': ', inputs_instance.OPGEE_distribution_checkbox)

# if ask_OPGEE_sensitivity[0].upper() == 'Y':
if ask_OPGEE_sensitivity == True:

		OPGEE_input_sensitivity(OPGEE_data, well_data)

# ask_OPGEE_export = str(input('\nExport to OPGEE (Y/N)?   '))
ask_OPGEE_export = inputs_instance.OPGEE_export_checkbox
print('Chosen Response to \'Export to OPGEE (True/False)\': ', inputs_instance.OPGEE_export_checkbox)

# if ask_OPGEE_export.upper() == 'Y':
if ask_OPGEE_export == True:	

	python_to_OPGEE(OPGEE_data)


