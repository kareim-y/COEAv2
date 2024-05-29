
#from plot_basemap import plot_basemap
import matplotlib.pyplot as plt
import collections 
from matplotlib.legend import Legend

def get_well_coordinates(well_data, well_data_headers, well_UWI):

	LATITUDE_index = well_data_headers.index("Surf-Hole Latitude (NAD83)")
	LONGITUDE_index = well_data_headers.index("Surf-Hole Longitude (NAD83)")

	latitude = float(well_data[well_UWI][LATITUDE_index][:-1])
	longitude = -float(well_data[well_UWI][LONGITUDE_index][:-1])

	return [longitude, latitude]

def plot_color_label_for_tight_oil(well, well_data, well_data_headings):

	formation = well_data[well][well_data_headings.index('Prod./Inject. Frmtn')]

	if formation in ['Mbakken_M', 'Dtorquay', 'D3_forks','Mbakken_M;Dtorquay']:
		color = 'black'
		label = 'Bakken'

	elif formation in ['Dbvrhl_lk', 'Dswan_hl']:
		color = 'orange'
		label = 'Beaverhill'

	elif formation in ['Kbelly_rv']:
		color = 'grey'
		label = 'Belly River' 

	elif formation in ['Kcard_ss']:
		color = 'orchid'
		label = 'Cardium'

	elif formation in ['TRchly_lk', 'TRbndrylk']:
		color = 'red'
		label = 'Charlie Lake'

	elif formation in ['Kdunvegan']:
		color = 'purple'
		label = 'Dunvegan'

	elif formation in ['Dduvernay']:
		color = 'chocolate'
		label = 'Duvernay'

	elif formation in ['Jshaunv_L']:
		color = 'chocolate'
		label = 'Lower Shaunavon'

	elif formation in ['TRmontney','TRdoig','TRdoig;TRmontney']:
		color = "darkgreen"
		label = 'Montney'

	elif formation in ['Mpekisko']:
		color = 'cyan'
		label = 'Pekisko'

	elif formation in ['Dslave_pt']:
		color = 'brown'
		label = 'Slave Point'

	elif formation in ['Kvik_ss']:
		color = 'navy'
		label = 'Viking'

	else:
		color = None
		label = ''
		#print(formation)


	return color, label



def well_plotter(well_data, well_data_headings):

	plot_ask = str(raw_input('\nWould you like to plot the wells (Y/N)?   '))
	print('\n')

	if plot_ask.upper() == 'N':

		return

	else:

		plot_basemap()

		count = 0

		color = 'black'

		for well in well_data:

			count = count + 1

			well_count = len(well_data)

			x,y = get_well_coordinates(well_data, well_data_headings, well)

			color, label = plot_color_label_for_tight_oil(well, well_data, well_data_headings)
			plt.plot(x, y, 'ok', markersize=4, color=color, label = label) #

			if count % 1000 == 0:
				print(str(count) + ' of ' + str(well_count)+ ' wells plotted')

			
	
	#plt.clf()
	#only unique labels
	ax = plt.gca()
	handles, labels = plt.gca().get_legend_handles_labels()
	by_label = collections.OrderedDict(zip(labels, handles))
	leg = plt.legend(by_label.values(), by_label.keys(), title = 'Formations', markerscale=2, bbox_to_anchor=(0.93, 0.95), fontsize=14)
	leg.set_title('Formations',prop = {'size': 14})
	plt.show()
	print('\n')

	return
if __name__ == '__main__':

	from well_search import well_search

	well_data_headings, well_data, field_name = well_search()

	plot_basemap()

	well_plotter(well_data, well_data_headings)

	plt.show()