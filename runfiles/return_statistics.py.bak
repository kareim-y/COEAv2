
import numpy as np
import matplotlib.pyplot as plt

def boxplot(array, name):

	plt.boxplot(array)
	plt.ylim(ymin=0)
	plt.title("Boxplot of " + name)
	print(array)
	print('\n')
	plt.show()


def is_outlier(points, thresh):
    """
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh


def histogram(array, name):

	#takes in an array and a name of the data and returns a histogram with automated bins 
    array = np.array(array)
    #x = array
    x = array[~is_outlier(array,40)]
    plt.hist(x, bins='auto', color = np.random.rand(3,))  # arguments are passed to np.histogram
    plt.title("Histogram of " + name)# + " w 'auto' bins & removed outliers (Z > 50)")
    plt.show()

    return x

def remove_outliers(array,thresh):

    array = np.array(array)
    x = array[~is_outlier(array,thresh)]

    return x

def return_statistics(array, name):

    if len(array) == 0:
        print('\nEmpty array - statistics not calculated\n')


    if len(array) > 0:
        print('\n~~~~~~~~~~~ Statistical Summary of ' + name + ' ~~~~~~~~~~~')
        print('Count; ' + str(len(array)))
        print('Average; ' + str("%.2f" %np.mean(array)))
        print('Median; ' + str("%.2f" %np.median(array)))
        print('Minimum; ' + str("%.2f" %np.min(array)))
        print('Maximum; ' + str("%.2f" %np.max(array)))
        print('10th Percentile; ' + str("%.2f" %np.percentile(array,10)))
        print('90th Percentile; ' + str("%.2f" %np.percentile(array,90)))
        print('\n')


