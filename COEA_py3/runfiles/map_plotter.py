#map plotter

#from plot_basemap import plot_basemap
import matplotlib.pyplot as plt

def map_plotter(map_,coordinates_array,color,markersize):

	#coordinates_array = [[lon,lat],[lon,lat],[lon,lat]]
	
	for i in range(0,len(coordinates_array)):
		longitude, latitude = coordinates_array[i]
		map_.plot(latitude, longitude, 'ok',  markersize=markersize, color=color)

	#plt.show()

	return map_


if __name__ == "__main__":

	m = plot_basemap()

	coordinates_array = [[53.267266, -116.829470]]

	map_plotter(m,coordinates_array,'red', 5)

