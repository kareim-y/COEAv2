#shapefile_reader

import shapefile
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry.polygon import Polygon
import shapely
from plot_basemap import plot_basemap
import matplotlib.pyplot as plt
import numpy as np
import collections
from descartes.patch import PolygonPatch
from distance_between_coordinates import distance_between_coordinates
import matplotlib as mpl 
from shapely import wkt
from shapely.ops import linemerge, unary_union, polygonize	
from matplotlib.legend import Legend
from map_to_drive import map_to_drive #path to Project Data folder

def plot_infrastructure():

	infrastructure = dict()
	#infrastructure['Fort St John, BC'] = [-120.848, 56.2499]
	#infrastructure['Site C Dam'] = [-120.916355, 56.198]
	#infrastructure['Grand Prarie, AB'] = [-118.8906, 55.1597]
	#infrastructure['Fox Creek, AB'] = [-116.8137, 54.402]
	infrastructure['Calgary'] = [-114.07112, 51.04989]
	infrastructure['Edmonton'] = [-113.491583, 53.543866]
	infrastructure['Vancover'] = [-123.11919, 49.265819]
	infrastructure['Regina'] = [-104.622718, 50.451331]
	#infrastructure['Dawson Creek, BC'] = [-120.2533, 55.7596]


	for location in infrastructure:
		x_adjust = 0.01
		y_adjust = 0.25
		if 'Fox' in location:
			y_adjust =  0.09
		if 'Fox Creek, AB' in location:
			y_adjust =  0.09
		if 'Calgary' in location:
			y_adjust = -0.38
		if 'Edmonton' in location:
			x_adjust, y_adjust = -0.8, 0.1
		if 'Vancover' in location:
			x_adjust, y_adjust = 0.8,0 


		plt.plot(infrastructure[location][0], infrastructure[location][1], 's', markersize=6, color='maroon')
		plt.text(infrastructure[location][0]+x_adjust, infrastructure[location][1] + y_adjust, location, fontsize=12, horizontalalignment='center')

def get_formation_color(formation, parameter):

	#parameter is the property we want to base out colors on - e.g Water use, Emissions etc


	emissions_dict = {"Dunvegan": 3.77,
  "Duvernay": 3.39,
  "Beaverhill": 7.8,
  "Belly River":4.85,
  "Montney": 4,
  "Montney (AB)": 3.93,
  "Montney (BC)": 2.79,
  "Bakken":13.23,
  "Lower Shaunavon":10.14,
  "Charlie Lake":5.63,
  "Viking":15,
  "Viking (AB)": 6.19,
  "Viking (SK)": 28.62,
  "Cardium":4.12,
  "Slave Point":7.62,
  "Pekisko":7.59}

	water_dict = {"Dunvegan": 4335,
  "Duvernay": 36534,
  "Beaverhill": 907,
  "Belly River":860,
  "Montney": 13000,
  "Montney (AB)": 11961,
  "Montney (BC)": 14453,
  "Bakken":660,
  "Lower Shaunavon":0,
  "Charlie Lake":3617,
  "Viking":624,
  "Viking (AB)": 624,
  "Viking (SK)": 624,
  "Cardium": 3116,
  "Slave Point": 1803,
  "Pekisko":2476}

  	default_dict = {"Dunvegan": "blue",
  "Duvernay": "blue",
  "Beaverhill": "purple",
  "Belly River": "orange",
  "Montney": "green",
  "Montney (AB)": "darkgreen",
  "Montney (BC)": "lightgreen",
  "Bakken": "gray",
  "Lower Shaunavon": "brown",
  "Charlie Lake": "fuchsia",
  "Viking": "red",
  "Viking (AB)": "firebrick",
  "Viking (SK)": "black",
  "Cardium": "cyan",
  "Slave Point": "orange",
  "Pekisko":'blue',
  "WASKAHIGAN":'blue',
  "KAYBOB SOUTH":'aqua',
  "GRIZZLY": 'purple',
  'SIMONETTE': 'violet',
  'HERITAGE MONTNEY': 'lime',
  'NORTHERN MONTNEY': 'darkgreen',
  None: None,
  "": "purple"
  }

  	#heatmapping
  	if parameter == 'emissions':
	  	#cmap = mpl.cm.get_cmap('YlOrRd')
	  	cmap = mpl.cm.get_cmap('hot_r')
	  	norm = mpl.colors.Normalize(vmin=0, vmax=15.0)
		rgba = cmap(norm(emissions_dict[formation]))

	if parameter == 'water':
	  	cmap = mpl.cm.get_cmap('cool')
	  	norm = mpl.colors.Normalize(vmin=0, vmax=35000)
		rgba = cmap(norm(water_dict[formation]))
	#based on range

	if parameter == 'default':
		rgba = default_dict[formation]

	if parameter == 'none':
		rgba = "none"

	if parameter == 'black':
		rgba = 'black'

	if parameter == 'random':
		rgba = np.random.rand(3,)


	return rgba

def plot_shapefile(shape_data,shape_name,count):

	alpha = 0.2

	fill_map_type = "default"
	outline_map_type = 'default'
	line_width = 1.5

	#if we want color from a property and cmap
	fill_color = get_formation_color(shape_name, fill_map_type)
	#fill_color = color
	outline_color = get_formation_color(shape_name, outline_map_type)

	points_array = []
	lattitude_array = []
	longitude_array = []
	text_count = []

	for point in shape_data.points:
		#print(point)
		if shape_name == 'Pekisko':
			#we want to remove everything east (less than) of -111
			#PROBABLY SHOULDNT FORCE FIT LIKE THIS< IT CAN BE A PLACEHOLDER FOR NOW!
			if point[0] <= -110.4: 
				lattitude_array.append(point[0])
				longitude_array.append(point[1]+0.55)
				points_array.append(point)
		else:
			lattitude_array.append(point[0])
			longitude_array.append(point[1])
			points_array.append(point)


	#Split AB and BC Montney
	AB_BC_border_lat = -119.93
	BC_montney_lat = []
	BC_montney_lon = []
	AB_montney_lat = []
	AB_montney_lon = []
	'''
	if shape_name == 'Montney':
		for point in points_array:
			if point[0] < AB_BC_border_lat:
				BC_montney_lat.append(point[0])
				BC_montney_lon.append(point[1])
			else:
				AB_montney_lat.append(point[0])
				AB_montney_lon.append(point[1])

		plt.plot(BC_montney_lat,BC_montney_lon, label= shape_name + ' (BC)', color = get_formation_color(shape_name+ ' (BC)', outline_map_type), linewidth = line_width)
		plt.fill(BC_montney_lat,BC_montney_lon, alpha = alpha, color = get_formation_color(shape_name + ' (BC)', fill_map_type))
		plt.plot(AB_montney_lat,AB_montney_lon, label=shape_name + ' (AB)', color = get_formation_color(shape_name+ ' (AB)', outline_map_type), linewidth = line_width)
		plt.fill(AB_montney_lat,AB_montney_lon, alpha = alpha, color = get_formation_color(shape_name+ ' (AB)', fill_map_type))
	'''
	
	#split AB and AK viking
	

	SK_AB_border_lat = -110
	AB_viking_lat = []
	AB_viking_lon = []
	SK_viking_lat = []
	SK_viking_lon = []
	if shape_name == 'Viking':
		for point in points_array:
			if point[0] < SK_AB_border_lat:
				AB_viking_lat.append(point[0])
				AB_viking_lon.append(point[1])
			else:
				SK_viking_lat.append(point[0])
				SK_viking_lon.append(point[1])

		plt.plot(AB_viking_lat,AB_viking_lon, label= shape_name + ' (AB)' , color = get_formation_color(shape_name+ ' (AB)', outline_map_type), linewidth = line_width)
		plt.fill(AB_viking_lat,AB_viking_lon, alpha = alpha, color = get_formation_color(shape_name+ ' (AB)', fill_map_type))
		try:
			plt.plot(SK_viking_lat,SK_viking_lon, label=shape_name + ' (SK)', color = get_formation_color(shape_name+ ' (SK)', outline_map_type), linewidth = line_width)
			plt.fill(SK_viking_lat,SK_viking_lon, alpha = alpha, color = get_formation_color(shape_name+ ' (SK)', fill_map_type))
		except:
			pass

	#the Duvernay has multiple parts to the single shape... which complicates things
	#we only want to plot shapes 1 and 11 (indexed by zero)
	if shape_name == 'Duvernay':
		points = np.array(shape_data.points)
		intervals = list(shape_data.parts) + [len(shape_data.points)]
		print(intervals)
		counter = 0
		for (i, j) in zip(intervals[:-1], intervals[1:]):
			#plt.plot(*zip(*points[i:j]))
			if counter in [1,11]:
				plt.fill(*zip(*points[i:j]),color=get_formation_color(shape_name, fill_map_type), alpha = alpha)
				plt.plot(*zip(*points[i:j]), label=shape_name, color = get_formation_color(shape_name, outline_map_type), linewidth = line_width)
			counter +=1


	#find centre of shape for text
	centroid = [np.mean(lattitude_array), np.mean(longitude_array)]

	#adjust text loction slightly
	#centroid[1] is the y-axis
	if shape_name == 'Beaverhill':
		centroid[1] = centroid[1] + 0.7
		centroid[0] + centroid[0] + 0.2
	if shape_name == 'Montney':
		centroid[0] = centroid[0] - 1.2
	if shape_name == 'Belly River':
		centroid[0] = centroid[0] - 0.1
	if shape_name == 'Duvernay':
		centroid[0] = centroid[0] + 0.3
		centroid[1] = centroid[1] + 0.5
	if shape_name == 'Slave Point':
		centroid[1] = centroid[1] + 0.3


	x, y = [-110.90, 56.70]

	point_trial = Point(-110.90, 56.70)


	#testing if a point is in a polygon
	#polygon = Polygon(montney_shape.points)
	#print(len(points_array))
	#print(str(sf.shapeType))
	#print(polygon.contains(point_trial))

	#print('\n\n')

	#for name in dir(montney_shape):
	#    if not name.startswith('_'):
	#        print(name)



	print(len(lattitude_array))

	if shape_name not in ['Duvernay','Viking']: 
		plt.plot(lattitude_array,longitude_array, color = get_formation_color(shape_name, outline_map_type), linewidth = line_width, label=shape_name)
		plt.fill(lattitude_array,longitude_array, alpha = alpha, color = get_formation_color(shape_name, fill_map_type))

	#Only Show Unique Labels Not Doubles 
	
	handles, labels = plt.gca().get_legend_handles_labels()
	by_label = collections.OrderedDict(zip(labels, handles))
	leg = plt.legend(by_label.values(), by_label.keys(), markerscale=3, bbox_to_anchor=(0.93, 0.95), fontsize=12)
	leg.set_title('Fields with Induced\n   Seismic Events',prop = {'size': 12})
	
	#set thickness of legend lines
	
	for legobj in leg.legendHandles:
		legobj.set_linewidth(4.0)
	
	plt.title('Western Canadian Tight Oil Formations')
	
	#plot text for fields but dont repeat
	if (shape_name == 'Beaverhill') and (count != 719):
		pass
	elif (shape_name == 'Belly River') and (count != 13):
		pass
	elif (shape_name == 'Slave Point') and (count != 266):
		pass
	#else: 
	#	plt.text(centroid[0], centroid[1], shape_name, fontsize=9, horizontalalignment='center')
	#plt.plot(x, y, 'ok', markersize = 5, color = 'red')


	#if count == 4:
	#	break
			


def formation_shapefile_plotter():

	print('\nPlotting Tight Fields on a Basemap...\n')

	shapefile_locations = collections.OrderedDict()

	#shapefile_locations['Slave Point'] = map_to_drive() + "Project Data/AER/Field_shapefiles/AER_Order_System_SHP/Field_region.shp"
	#shapefile_locations['Beaverhill'] = map_to_drive() + "Project Data/AER/Field_shapefiles/AER_Order_System_SHP/Field_region.shp"
	shapefile_locations['AB_pools'] = map_to_drive() + "Project Data/AER/Field_shapefiles/AER_Order_System_SHP/Field_region.shp"
	#shapefile_locations['Saskatchewan_pools'] = map_to_drive() + "Project Data/SK_gov/Sask_pool_shapefiles/PoolLand.shp"
	#shapefile_locations['BC_pools'] = map_to_drive() + "Project Data/BCOGC/OG_OIL_AND_GAS_FIELDS_SP/OG_FIELDS_polygon.shp"
	#shapefile_locations['Montney'] = map_to_drive() + "Project Data/AER/Field_shapefiles/Montney Shapefile/Montney.shp" 
	#shapefile_locations['Duvernay']= map_to_drive() + "Project Data/AER/Field_shapefiles/Duvernay_Petroleum_System/shalegas_fms_py_ll.shp"
	shapefile_locations['BC_regional_fields'] = 'C:/Users/alexander.bradley/Desktop/"Project Data/BCOGC/OG_REGIONAL_FIELDS_SP/OG_REG_FLD_polygon.shp'
	#shapefile_locations['US_CAN_fields'] = map_to_drive() + "Project Data/AER/Field_shapefiles/tight_fields/tight_fields_JSON.txt-polygon.shp"
	#shapefile_locations['Montney'] = map_to_drive() + "Project Data/AER/Field_shapefiles/Montney_Isopach_litho/fg1624_py_ll.shp"
	#shapefile_locations['Beaverhill'] = map_to_drive() + "Project Data/AER/Field_shapefiles/Beaverhill_Lake_Isopach/fg1103_py_ll.shp" 
	#shapefile_locations['Charlie Lake'] = map_to_drive() + "Project Data/AER/Field_shapefiles/Charlie_Lake_Isopach_and_Lithofacies/fg1631_py_ll.shp"
	#shapefile_locations['Belly River'] = map_to_drive() + "Project Data/AER/Field_shapefiles/Belly_River_Isopach/fg2416_py_ll.shp"
	#shapefile_locations['Pekisko']= map_to_drive() + "Project Data/AER/Field_shapefiles/Rundle_(Pekisko)_Isopach_and_Lithofacies/fg1434_py_ll.shp"


	#BEAVERHILL - shapes of interest (count) = [57 through 63]
	#BELLY RIVER - Isopach [1007.0 only, maybe break down more]

	plot_basemap()


	for shape_file in shapefile_locations:

		sf = shapefile.Reader(shapefile_locations[shape_file])

		print('\n\n')

		shapes = sf.shapeRecords()

		print('Shapefile; ', shape_file)
		print('Number of shapefile shapes; ', len(shapes))

		count = 0


		for shape in shapes:

			shape_data = shape.shape

			try:
				#if we are dealing with data from the AER
				int(shape.record[0])
				shape_name = shape.record[1].split(' ')
				shape_name = shape_name[0] + ' ' + shape_name[1]
			except:
				#we have the tight field data from stackoverflow
				shape_name = shape.record[0]


			if shape_file == 'US_CAN_fields':
				if shape_name in ['Dunvegan', 'Viking','Cardium', 'Bakken / Lower Shaunavon']:
					if shape_name == 'Duverney':
						shape_name = 'Duvernay'
					if shape_name == 'Bakken / Lower Shaunavon':
						#rename the lower shauv formation different from bakken
						Shaunavon_point = Point(-109.8056493, 49.2249863)
						bakken_shaun_polygon = Polygon(shape_data.points)
						if bakken_shaun_polygon.contains(Shaunavon_point) == True:
							shape_name = 'Lower Shaunavon'
						if bakken_shaun_polygon.contains(Shaunavon_point) == False:
							shape_name = 'Bakken'

					print('\nPlotting Shape; ', count)
					#print(shape.record)
					plot_shapefile(shape_data,shape_name,count)
			
			if shape_file == 'Montney':
				print('\nPlotting Shape; ', count)
				print(shape.record)
				plot_shapefile(shape_data,'Montney',count)

			if shape_file == 'Belly River':
				if int(shape.record[0]) == 1007:
					print('\nPlotting Shape; ', count)
					#print(shape.record)
					plot_shapefile(shape_data,'Belly River',count)

			#if shape_file == 'Beaverhill':
			#	if count in [57,58,59,60,63]:
			#		print('\nPlotting Shape; ', count)
			#		#print(shape.record)
			#		plot_shapefile(shape_data,'Beaverhill',count)

			if shape_file == 'Charlie Lake':
				if count == 5:
					print('\nPlotting Shape; ', count)
					#print(shape.record)
					plot_shapefile(shape_data, 'Charlie Lake' ,count)

			if shape_file == 'Duvernay':
				if count in [0]:
					print('\nPlotting Shape; ', count)
					#print(shape.record)
					plot_shapefile(shape_data, 'Duvernay' ,count)

			if shape_file == 'Pekisko':
				if count == 3:
					print('\nPlotting Shape; ', count)
					#print(shape.record)
					plot_shapefile(shape_data, 'Pekisko',count)

			if shape_file == 'Slave Point':
				if shape_name in ['0353','0579','RED EARTH','0766']:
					#only want to plot the most popular fields for slave point [EVI,LOON,RED EARTH, sawn lake]
					#print(shape_name)
					print('\nPlotting Shape; ', count)
					#print(shape.record)
					plot_shapefile(shape_data, 'Slave Point' ,count)
				#print(shape_name)

			if shape_file == 'Beaverhill':
				#print(shape_name)
				if shape_name in ['SWAN HILLS','0889','JUDY CREEK','CARSON CREEK','VIRGINIA HILLS']:
					#only want to plot the most popular fields for slave point [swan hills,swan hills sth, Judy creek, crason creek, viginia hills]
					print(shape_name)
					print('\nPlotting Shape; ', count)
					#print(shape.record)
					plot_shapefile(shape_data, 'Beaverhill' ,count)
			
			if shape_file == 'AB_pools':
				#print(shape_name)
				#if we only want induced seismic areas
				if shape_name in ['KAYBOB SOUTH','NORTHERN MONTNEY','HERITAGE','WASKAHIGAN','0930','0433','0844']:
					if shape_name == '0930':
						shape_name = 'WASKAHIGAN'
					elif shape_name == '0433':
						shape_name = 'GRIZZLY'
					elif shape_name == '0844':
						shape_name = 'SIMONETTE'

					#'GILBY','0412','GRIZZLY','0433','INGA','SIMONETTE','0844','GARRINGTON','0405'
					print('\nPlotting Shape; ', count)
					#print(shape.record)
					plot_shapefile(shape_data, shape_name ,count)

			if shape_file == 'Saskatchewan_pools':
				print(shape_name)
				print('\nPlotting Shape; ', count)
				#print(shape.record)
				plot_shapefile(shape_data, 'Beaverhill' ,count)

			if shape_file == 'BC_pools':
				print(shape_name)
				print('\nPlotting Shape; ', count)
				#print(shape.record)
				plot_shapefile(shape_data, 'Beaverhill' ,count)

			if shape_file == 'BC_regional_fields':
				print(shape_name)
				print('\nPlotting Shape; ', count)
				if count == 3:
					shape_name = 'HERITAGE MONTNEY'
					plot_shapefile(shape_data, shape_name ,count)
				if count == 4:
					shape_name = 'NORTHERN MONTNEY'
					plot_shapefile(shape_data, shape_name ,count)


			count += 1

			#plt.show()

			


if __name__ == '__main__':
	
	formation_shapefile_plotter()

	plt.show()