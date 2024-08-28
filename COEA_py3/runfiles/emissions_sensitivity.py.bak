#--- A script to show two types of stacked plotting

import numpy as np
import matplotlib.pyplot as plt
import csv
import collections
from return_statistics import remove_outliers
from datetime import datetime
from map_to_drive import map_to_drive #path to Project Data folder

def get_additional_well_data():
	#get additionall data for each well - etc age, depth....

	print('\nGetting Additional Data\n')

	Well_data_location = map_to_drive() +"/Project Data/geoSCOUT_data/post 2005 well data (June 19) v2.csv"

	emissions_sensitivity_location = "C:/Users/alexander.bradley/Google Drive/University of Calgary_/Masters Research/Western Canadian Tight Oil/COEA Results/well_level_results.csv"

	count1 = 0
	new_sens_data = collections.OrderedDict()

	with open(emissions_sensitivity_location) as f:
		#get a list of well ID's from the sens file
		reader = csv.reader(f)
		for row in reader:
			if count1 == 0:
				sens_headings = row
			else:
				wellid = row[sens_headings.index('Well UWI')]
				new_sens_data[wellid] = []
			count1 = count1 + 1

	#parameter = 'Age'
	parameter = 'Org Operator Name'
	
	count2 = 0
	data_count = 0 #count of wells we have data for

	with open(Well_data_location) as f:
		#get new data
		reader = csv.reader(f)
		for row in reader:
			if count2 == 0:
				well_data_headings = row
			else:
				wellid = row[well_data_headings.index('CPA Well ID')]
				start_date = row[well_data_headings.index('On Prod YYYY/MM/DD')]

				if parameter == 'Age':
					if len(start_date) > 0:
						start_date = datetime.strptime(start_date, '%m/%d/%Y')
						end_date = row[well_data_headings.index('Last Prod. YYYY/MM')]
						#end_date = datetime.strptime(end_date, '%m/%d/%Y')
						end_date = datetime.strptime('12/31/2017', '%m/%d/%Y') #set to december 2017
						days_between = (end_date - start_date).days
						years_between = round(float(days_between)/365,2)
						param_value = years_between
				else:
					param_value = row[well_data_headings.index(parameter)]

				if wellid in new_sens_data:
					if len(new_sens_data[wellid]) == 0:
						#ensure the array is empty so we dont double up (there are double wells in the original csv)
						data_count += 1
						new_sens_data[wellid].append(param_value)

			
			count2 = count2 + 1

	print(len(new_sens_data))
	print(data_count)

	#write to new csv then copy pasta
	with open('new_sens_data.csv', 'wb') as f:
		wr = csv.writer(f,delimiter=',')
		for wellid in new_sens_data:
			try:
				row = [wellid,new_sens_data[wellid][0]]
			except:
				row = [wellid,'']
			#print(row)
			wr.writerow(row)



def get_all_emission_data():
	#function opens emissions sensiivity file and saves it in a 
	#dictionary (indexed to UWI)
	
	csv_location = "C:/Users/alexander.bradley/Google Drive/University of Calgary_/Masters Research/Western Canadian Tight Oil/COEA Results/well_level_results.csv"

	well_emissions_data = collections.OrderedDict()

	with open(csv_location) as csv_file:
		csv_reader = csv.reader(csv_file)
		count = 0
		for row in csv_reader:
			if count == 0:
				headings = row
				#print(f' {" ".join(row)}')
				count += 1
			else:
				UWI = row[headings.index('Well UWI')]
				well_emissions_data[UWI] = row

	return headings, well_emissions_data

def formation_average_dict():
	#this is the results using facility level flare rates
	# a function that returns a dictionary of the field averages

	formation_averages = {"Montney (BC)":2.79,
		"Montney (AB)":	3.93,
		"Duvernay (AB)":3.39,
		"Dunvegan (AB)":3.77,
		"Cardium (AB)":	4.12,
		"Charlie Lake (AB)":5.63,
		"Pekisko (AB)":	7.59,
		"Slave Point (AB)":7.62,
		"Beaverhill (AB)":7.80,
		"Lower Shaunavon (SK)":10.14,
		"Bakken (SK)":13.23,
		"Viking (AB)":6.19,
		"Viking (SK)":28.62}

	return formation_averages

def formation_average_dict_well_FFV():
	#this is the results using aggregate well level flare rates
	# a function that returns a dictionary of the field averages

	formation_averages_well_FFV = {"Montney (BC)":2.78,
		"Montney (AB)":	4.115,
		"Duvernay (AB)":3.70,
		"Dunvegan (AB)":5.14,
		"Cardium (AB)":	4.85,
		"Charlie Lake (AB)":5.74,
		"Pekisko (AB)":	8.52,
		"Slave Point (AB)":9.15,
		"Beaverhill (AB)":8.74,
		"Lower Shaunavon (SK)":10.24,
		"Bakken (SK)":11.65,
		"Viking (AB)":8.09,
		"Viking (SK)":27.49}

	return formation_averages_well_FFV


def emission_distribution():


	formation_well_counter = collections.Counter()
	emission_dict = dict()
	formation_weighted_emissions_dict = dict()
	Emission=[]
	field_array = []
	Lon=[]
	Lat=[]

	csv_location = "C:/Users/alexander.bradley/Google Drive/University of Calgary_/Masters Research/Western Canadian Tight Oil/COEA Results/well_level_results.csv"

	with open(csv_location) as csv_file:
		csv_reader = csv.reader(csv_file)
		count = 0
		for row in csv_reader:
			if count == 0:
				headings = row
				#print(f' {" ".join(row)}')
				count += 1
			else:
				formation_name = row[0]
				#if 'Montney' in formation_name:
				#	formation_name = 'Montney'
				formation_well_counter[formation_name] += 1
				if formation_name not in emission_dict:
					emission_dict[formation_name] = []
					formation_weighted_emissions_dict[formation_name] = []
					field_array.append(formation_name)
				#if 'Montney' in formation_name:
				#lon_lat = row[headings.index('[lon,lat]')].split(',')
				#longitude = lon_lat[0][1:] 
				#latitude = lon_lat[1][:-1]
				#print(longitude,latitude)
				#Lon.append(float(longitude)) 
				#Lat.append(float(latitude))         
				#Emission.append(float(row[headings.index('Adjusted Emission Factor (gCO2e/MJ)')])) 
				#print(row[headings.index('WTR Emissions (gCO2e/MJ-crude)')])
				Emission.append(float(row[headings.index('WTR Emissions (gCO2e/MJ-crude)')]))
				emission_dict[formation_name].append(float(row[headings.index('WTR Emissions (gCO2e/MJ-crude)')]))
				#formation_weighted_emissions_dict[formation_name].append(float(row[headings.index('Formation Weighted Emissions')]))
				
				count += 1


	#get dict of formation averages
	#Using facility average FFV rate
	formation_averages = formation_average_dict()
	#Using well aggregate FFV
	formation_averages_well_FFV = formation_average_dict_well_FFV()
	
	print('\nIndividual wells modelled; ' + str(count -1))
	print('\n')
	#select_all fields
	#field_array = emission_dict.keys()
	field_array = ["Montney (BC)","Duvernay (AB)","Montney (AB)","Cardium (AB)","Dunvegan (AB)", "Charlie Lake (AB)","Viking (AB)","Pekisko (AB)","Beaverhill (AB)","Slave Point (AB)","Lower Shaunavon (SK)","Bakken (SK)","Viking (SK)"]
	print(field_array)
	#field_array = field_array[10:]
	#field_array = field_array[6:-1]
	#field_array = field_array[0:6]

	#--- Initialize plots
	#figsize = (6,6)
	#figsize = (13,3)
	figsize = (15,len(field_array)*1)

	figs, axes = plt.subplots(len(field_array),1, figsize = figsize)
	plt.subplots_adjust(hspace=0.3)

	formation_arrays = []
	formation_names = []

	#--- Plotting
	#nbins = 30
	nbins = 'auto'
	#normalised = False
	normalised = True
	axis_count = 0
	x_max = 80
	P10xadjust = 0.05*x_max #How much we want to asjust the P10 test left
	plot_num = 4 #this is the number teh figure will be saved as 

	for formation_name in field_array:
		#-- In the first case we want two distributions seperately, made slightly see through
		
		c=np.random.rand(3,) #random color
		print(c)
		if formation_name[-4:] == '(BC)': c = 'gold'
		if formation_name[-4:] == '(AB)': c = 'darkblue'
		if formation_name[-4:] == '(SK)': c = 'darkred'

		well_count = len(emission_dict[formation_name])

		percentiles = [10,50,90]
		print('\n' + formation_name)
		print('Well Count; ' + str(well_count))
		print('Well-Level Average; ' + str(round(np.mean(emission_dict[formation_name]),3)))
		print('Formation Average; '+ str(formation_averages_well_FFV[formation_name]))
		print('Formation Production Weighted Average; ' + str(round(sum(formation_weighted_emissions_dict[formation_name]),3)))
		for percentile in percentiles:
			print('P' + str(percentile) + '; ' + str(round(np.percentile(emission_dict[formation_name],percentile),3)))
		print('\n')

		#remove outliers 
		new_emissions_array = remove_outliers(emission_dict[formation_name],20) 
		#new_emissions_array = emission_dict[formation_name]

		legend_name = formation_name + ' (' + str(well_count) + ' wells)'
		#legend_name = 'Field ' + str(axis_count)
		
		counts1, bins1, patches1 = axes[axis_count].hist(new_emissions_array,nbins,label=legend_name,alpha=0.5, density = normalised, color = c) #--- the "alpha" parameter scales the "see-throughness" between 0 (invisible) and 1 (solid)
		max_vertical = np.max(counts1)
		axes[axis_count].legend(loc='upper right')
		ytextadjust = 0.05
		ytextadjust = max_vertical*0.1
		#P50 line
	
		pfontsize = 10
		Pfifty = np.percentile(emission_dict[formation_name],50)
		Pten = np.percentile(emission_dict[formation_name],10)
		Pninty = np.percentile(emission_dict[formation_name],90)
		Avg = formation_averages[formation_name] #facility FFV
		Avg_well_FFV = formation_averages_well_FFV[formation_name]
		weighted_avg = sum(formation_weighted_emissions_dict[formation_name])


		axes[axis_count].axvline(Pfifty, color='k', linestyle='dashed', linewidth=1.2)
		axes[axis_count].annotate('P50', xytext=(Pfifty+0.05, ytextadjust), xy =(Pfifty+0.2, ytextadjust), fontsize = pfontsize)
		axes[axis_count].axvline(Pten, color='k', linestyle=':', linewidth=1.5)
		axes[axis_count].annotate('P10', xytext=(Pten-P10xadjust, ytextadjust), xy =(Pten+0.2, ytextadjust), fontsize = pfontsize)
		axes[axis_count].axvline(Pninty, color='k', linestyle=':', linewidth=1.5)
		axes[axis_count].annotate('P90', xytext=(Pninty+0.05, ytextadjust), xy =(Pninty+0.2, ytextadjust), fontsize = pfontsize)
		
		#Facility FFVs
		#axes[axis_count].set_xticks(np.arange(0,x_max+5,step=5))
		#axes[axis_count].axvline(Avg, color='r', linestyle='dashed', linewidth=1.5, label='Formation Mean (2017)')
		
		#Weights average 
		axes[axis_count].set_xticks(np.arange(0,x_max+5,step=5))
		axes[axis_count].axvline(weighted_avg, color='r', linestyle='dashed', linewidth=2, label='Production Weighted Mean (2017)')

		#axes[axis_count].annotate('Avg', xytext=(Avg+0.05, 0.05), xy =(Avg+0.2, 0.05), fontsize = pfontsize)
		axes[axis_count].set_xticks(np.arange(0,x_max+5,step=5))
		axes[axis_count].set_xticklabels([])

		#-- In the second we want to stack these on top of each other, so we place the two vectors of data inside a third vector:
		formation_arrays.append(new_emissions_array) 
		formation_names.append(formation_name)

		axes[axis_count].set_xlim(right=x_max,left=0)
		axes[axis_count].set_ylim(top=0.5,bottom=0)
		#adjust yaxis uniquely for fiel maximums
		axes[axis_count].set_ylim(top=max_vertical*1.3,bottom=0)

		#Reverse Legend order
		handles, labels = axes[axis_count].get_legend_handles_labels()
		axes[axis_count].legend(handles[::-1], labels[::-1], prop={'size': 8}, loc='upper right')



		axis_count += 1

	x4 = np.concatenate([formation_arrays])

	#count3, bins3, patches3 = axes[axis_count+1].hist(formation_arrays,nbins,stacked=True,alpha=0.5,label=formation_names)
	#count4, bins4, patches4 = axes[axis_count+1].hist(x4,nbins,histtype='step',linewidth=2,label="Total")

	#--- Format Plot
	#axes[0].set_title("Distributions of Field Emissions Intensity (Well Level); nbins = " + str(nbins))
	#axes[0].set_title("Well to Refinery Emissions Variability (gCO2e/MJ Crude)")

	axes[axis_count-1].set_xlabel('gCO2e/MJ-crude')
	axes[axis_count-1].xaxis.labelpad = 10
	axes[axis_count-1].set_xticklabels(np.arange(0,x_max+5,step=5))
	#axes[1].set_title("Stack Histograms")

	axes[0].set_ylabel('Relative Distribution Density')
	axes[0].yaxis.set_label_coords(-0.09,len(field_array)*-0.45)

	#axes[0].set_xlim(right=35,left=0)
	#axes[1].set_xlim(right=35,left=0)

	#axes[1].legend(loc='best')


	figs.savefig('well_level_emissions_distributions_' + str(plot_num), dpi=500)

	plt.show()

def correlation_matrix(field):

	import matplotlib.pyplot as plt
	import pandas
	import numpy
	from pandas.plotting import scatter_matrix

	#csv_location = "C:/Users/alexander.bradley/Google Drive/University of Calgary_/Masters Research/Western Canadian Tight Oil/COEA Results/cardium_sensitivity.csv"
	csv_location = "C:/Users/alexander.bradley/Google Drive/University of Calgary_/Masters Research/Western Canadian Tight Oil/COEA Results/well_level_results.csv"

	#field = 'Cardium'

	data = pandas.read_csv(csv_location)

	data = data[data.Formation == field]

	#print(list(data))

	data =  data.drop(['Formation','Geoscout Formation','Province','Facility GOR (scf/bbl)','Well UWI','Area','[lon,lat]','Operator','2017 Prod Time (yrs)','Formation BOE (2017)','Cum BOE (2017)','Drill & Dev Emissions (gCO2e/MJ)','WTR - No Allocation (gCO2e/MJ-crude)'], axis = 1)
	#data = data.loc[data['Vent (%)'] == 100]


	print(list(data))
	print('Well Count; ' + str(len(data)))

	correlations = data.corr()
	print correlations.round(2)

	#put to csv
	#correlations.to_csv(field + '_Correlation_Matrix_Values.csv')

	# plot correlation matrix
	fig = plt.figure()
	ax = fig.add_subplot(111)
	cax = ax.matshow(correlations, vmin=-1, vmax=1, cmap='bwr')
	fig.colorbar(cax)
	ticks = numpy.arange(0,len(list(correlations)),1)
	ax.set_xticks(ticks)
	ax.set_yticks(ticks)
	ax.set_xticklabels(list(data), rotation=90, size = 8)
	ax.set_yticklabels(list(data), rotation=0, size = 8)
	plt.subplots_adjust(top=0.75) #hspace=None
	plt.title(field + ' Correlation Matrix', y=-0.15)

	plt.tight_layout()

	plt.show()

	#remove a couple columns for the scatter matrix

	#data = data.drop(['D&D EF (gCO2eq/MJ crude)','Field Depth (ft)','Field Age (yrs)'], axis =1)

	print(data.shape)

	#remove outliers
	from scipy import stats
	Z_score =  3
	data = data[(np.abs(stats.zscore(data.astype(float))) < Z_score).all(axis=1)]


	scatter_matrix = scatter_matrix(data) #range_padding=0.5
	
	[s.xaxis.label.set_rotation(30) for s in scatter_matrix.reshape(-1)]
	[s.yaxis.label.set_rotation(0) for s in scatter_matrix.reshape(-1)]
	[s.xaxis.label.set_fontsize(10) for s in scatter_matrix.reshape(-1)]
	[s.yaxis.label.set_fontsize(10) for s in scatter_matrix.reshape(-1)]
	[s.get_yaxis().set_label_coords(-0.85,0.5) for s in scatter_matrix.reshape(-1)]

	plt.subplots_adjust(bottom = 0.2, top = 0.9, left = 0.2)
	plt.title(field + ' Field Scatter Matrix (Outliers Z > ' + str(Z_score) + ' removed)', y = len(list(data)), x = -2.1,  size =12)
	plt.show()

def data_analysis():

	headings, well_emissions_data = get_all_emission_data()

	flare_count = collections.Counter()
	vent_count = collections.Counter()
	well_count = collections.Counter()
	operator_count = collections.Counter()
	param_venting = collections.OrderedDict()
	param_flaring = collections.OrderedDict()
	param_all = collections.OrderedDict()
	#param = 'Well GOR (scf/bbl)'
	#param = 'Gas production (scf/day)'
	#param = 'Oil Production (bbl/day)'
	param = 'Age (yrs)'

	bins = np.linspace(0,10,21) #three month bins
	#bins = np.linspace(0,10,121) #1 month bins 
	#print(bins)

	min_flare_perc = 90
	min_vent_perc = 90

	for well in well_emissions_data:
		formation = well_emissions_data[well][headings.index('Formation')]
		if formation not in param_all:
			param_all[formation] = []

		if formation == 'Cardium (AB)':
			operator = well_emissions_data[well][headings.index('Operator')]
			param_val = float(well_emissions_data[well][headings.index(param)])
			well_count[formation] += 1
			vent_percent =  float(well_emissions_data[well][headings.index('Vent (%)')])
			flare_percent =  float(well_emissions_data[well][headings.index('Flare (%)')])
			param_all[formation].append(param_val)

			if vent_percent >= min_vent_perc:
				vent_count[formation] += 1
				if formation not in param_venting:
					param_venting[formation] = [param_val]
				else:
					param_venting[formation].append(param_val)
			
			if flare_percent >= min_flare_perc:
				flare_count[formation] += 1
				if formation not in param_flaring:
					param_flaring[formation] = [param_val]
				else:
					param_flaring[formation].append(param_val)

	print('\nFlaring')
	print('Formation',str(min_flare_perc) + '"%"Flare Wells', 'Well Count', 'Percent', 'Mean ' + param)
	for formation in sorted(flare_count.keys()):
		print(formation, flare_count[formation],well_count[formation], round(float(flare_count[formation])*100/well_count[formation],2), round(np.mean(param_flaring[formation]),2))

	print('\nVenting')
	print('Formation',str(min_vent_perc) + '"%"Vent Wells', 'Well Count', 'Percent', 'Mean ' + param)
	for formation in sorted(vent_count.keys()):
		print(formation, vent_count[formation], well_count[formation],round(float(vent_count[formation])*100/well_count[formation],2), round(np.mean(param_venting[formation]),2))

	
	counts, hbins, bars = plt.hist(param_venting[formation], bins = bins, density = False, label= param)
	plt.legend()
	print('\n')
	print(list(counts))
	print(list(hbins))
	plt.show()
	
	counts, hbins, bars = plt.hist(param_all[formation], bins = bins, density = False, label= param)
	print('\n')
	print(list(counts))
	print(list(hbins))

	
if __name__ == '__main__':
	
	field = 'Bakken (SK)'
	#field = 'Montney (AB)'

	correlation_matrix(field)

	#emission_distribution()

	#data_analysis()

	#get_additional_well_data()