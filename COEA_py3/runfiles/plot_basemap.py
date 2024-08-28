import mpl_toolkits
#mpl_toolkits.__path__.append('C:/Python27/Lib/site-packages/mpl_toolkits')
from mpl_toolkits.basemap import Basemap
import shapefile
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import shapely
import matplotlib.pyplot as plt

def plot_basemap():

	print('\nPlotting Basemap...\n')

	m = Basemap(resolution = 'h', llcrnrlon=-125,llcrnrlat=48.7,urcrnrlon=-101,urcrnrlat=60.2, epsg=4269, area_thresh = 10000)
	#induced seismic
	#m = Basemap(resolution = 'h', llcrnrlon=-123.5,llcrnrlat=53.8,urcrnrlon=-115.5,urcrnrlat=57.6, epsg=4269, area_thresh = 10000)
	#including SK - llcrnrlon=-123, not including SK llcrnrlon=-128
	# North America
	#m = Basemap(resolution = 'h', llcrnrlon=-130,llcrnrlat=30,urcrnrlon=-80,urcrnrlat=65, epsg=4269, area_thresh = 10000)
	#http://server.arcgisonline.com/arcgis/rest/services
	#EPSG Number of America is 4269
	
	m.drawcountries(linewidth = 1, color = 'black')
	m.drawstates(linewidth = 1, color = 'black')
	m.drawcoastlines(linewidth=1)
	#m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 2000, verbose= True)
	#m.shadedrelief()
	
	return m

def montney_shape_plot(basemap):
	
	#ensure the shapefile folder is in the same directory

	sf = shapefile.Reader("Montney Shapefile/Montney.shp")
	
	montney_shape = sf.shape(0)

	points_array = []
	lattitude_array = []
	longitude_array = []
	count = 0

	for point in montney_shape.points:
		#print(point)
		lattitude_array.append(point[0])
		longitude_array.append(point[1])

	plt.plot(lattitude_array,longitude_array)

	return basemap, montney_shape

if __name__ == '__main__':

	plot_basemap()

	plt.show()