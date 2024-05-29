#OPGEE_data
import collections
#def OPGEE_defaults():
	
def OPGEE_defaults():

	print('\n~~~~~~~~~~~~ OPGEE DATA ~~~~~~~~~~~~')
	print('\nFunction creates an ordered dictionary for the required OPGEE inputs')
	print('To change the defaults see file labelled OPGEE defaults\n')
	print('OPGEE_data[headings] - Shows the headings of out input data')
	print('OPGEE_data[defaults] - Shows the default inputs for the data')
	print('OPGEE_data[units] - Shows the units for the inputs')
	print('OPGEE_data[excel position] - Shows the postion of the input in excel')
	print('\n')

	OPGEE_data = collections.OrderedDict()

	OPGEE_data['headings'] = []
	OPGEE_data['units'] = [] 
	OPGEE_data['defaults'] = []
	OPGEE_data['assessed field'] = []
	OPGEE_data['excel position'] = []


		#list of headings
	opgee_input_data = [[	'Downhole pump',	'NA',	0,	9],
	[	'Water reinjection',	'NA',	0,	10],
	[	'Natural gas reinjection',	'NA',	0,	11],
	[	'Water flooding',	'NA',	0,	12],
	[	'Gas lifting',	'NA',	0,	13],
	[	'Gas flooding',	'NA',	0,	14],
	[	'Steam flooding',	'NA',	0,	15],
	[	'Oil sands mine (integrated with upgrader)',	'NA',	0,	16],
	[	'Oil sands mine (non-integrated with upgrader)',	'NA',	0,	17],
	[	'Field location (Country)',	'NA',	'Canada',	20],
	[	'Field name',	'NA',	'Generic',	21],
	[	'Field age',	'yr.',	35,	22],
	[	'Field depth',	'ft',	7240,	23],
	[	'Oil production volume',	'bbl/d',	0,	24],
	[	'Number of producing wells',	'[-]',	1,	25],
	[	'Number of water injecting wells',	'[-]',	0,	26],
	[	'Production tubing diameter',	'in',	2.775,	27],
	[	'Productivity index',	'bbl/psi-d',	3,	28],
	[	'Reservoir pressure',	'psi',	1556.6,	29],
	[	'Reservoir temperature',	'deg F',	150,	30],
	[	'Offshore?',	'[0-1]',	0,	31],
	[	'API gravity',	'deg. API',	30,	34],
	[	'Gas composition N2',	'mol%',	2,	36],
	[	'Gas composition CO2',	'mol%',	6,	37],
	[	'Gas composition C1',	'mol%',	84,	38],
	[	'Gas composition C2',	'mol%',	4,	39],
	[	'Gas composition C3',	'mol%',	2,	40],
	[	'Gas composition C4+',	'mol%',	1,	41],
	[	'Gas composition H2S',	'mol%',	1,	42],
	[	'Gas-to-oil ratio (GOR)',	'scf/bbl oil',	908,	46],
	[	'Water-to-oil ratio (WOR)',	'bbl water/bbl oil',	4.31,	47],
	[	'Water injection ratio',	'bbl water/bbl oil',	0,	48],
	[	'Gas lifting injection ratio',	'scf/bbl liquid',	0,	49],
	[	'Gas flooding injection ratio',	'scf/bbl oil',	0,	50],
	[	'Flood gas',	'NA',	0,	51,	],
	[	'Percentage of newly acquired CO2',	'percent',	0, 58],
	[	'Source of CO2',	'NA',	0,	59],
	[	'Percentage of sequestration credit assigned to the oilfield',	'%',	0,	62],
	[	'Steam-to-oil ratio (SOR)',	'bbl steam/bbl oil',	0,	63],
	[	'Fraction of required electricity generated onsite',	'[-]',	0,	64],
	[	'Fraction of remaining natural gas reinjected',	'[-]',	0,	65],
	[	'Fraction of produced water reinjected',	'[-]',	1,	66],
	[	'Fraction of steam generation via cogeneration ',	'[-]',	0,	67],
	[	'Fraction of steam generation via solar thermal',	'[-]',	0,	68],
	[	'Heater/treater',	'NA',	1,	70],
	[	'Stabilizer column',	'NA',	1,	71],
	[	'Upgrader type',	'[1-8]',	0,	72],
	[	'Associated Gas Processing Path',	'NA',	5,	77],
	[	'Flaring-to-oil ratio',	'scf/bbl oil',	0,	86],
	[	'Venting-to-oil ratio',	'scf/bbl oil',	0,	87],
	[	'Volume fraction of diluent',	'[-]',	0,	88],
	[	'Low carbon richness (semi-arid grasslands)',	'NA',	0,	92],
	[	'Moderate carbon richness (mixed)',	'NA',	1,	93],
	[	'High carbon richness (forested)',	'NA',	0,	94],
	[	'Low intensity field development',	'NA',	0,	96],
	[	'Moderate intensity field development',	'NA',	1,	97],
	[	'High intensity field development',	'NA',	0,	98],
	[	'Ocean tanker (Fraction Transport)',	'[-]',	0,	102],
	[	'Transport Barge (Fraction Transport)',	'[-]',	0,	103],
	[	'Pipeline (Fraction Transport)',	'[-]',	0.97,	104],
	[	'Rail (Fraction Transport)',	'[-]',	0.03,	105],
	[	'Truck (Fraction Transport)',	'[-]',	1,	106],
	[	'Ocean tanker (Distance Transport)',	'Mile',	5082,	108],
	[	'Barge (Distance Transport)',	'Mile',	500,	109],
	[	'Pipeline (Distance Transport)',	'Mile',	2143,	110],
	[	'Rail (Distance Transport)',	'Mile',	2143,	111],
	[	'Truck (Distance Transport)',	'Mile',	50,	112],
	[	'Ocean tanker size, if applicable',	'Ton',	250000,	113],
	[	'Small sources emissions',	'gCO2eq/MJ',	0.5,	115],
	[	'Distance of travel for survey', 'mi', 1000, 120],
	[	'Weight of land survey vehicle', 'tons', 25, 121],
	[	'Weight of ocean survey vehicle', 'tons', 100, 122],
	[	'Number of dry wells drilled per field found', 'wells', 0, 123],
	[	'Number of exploratory/scientific wells drilled after field discovery', 'wells', 0, 124],
	[	'Horizontal well fraction', 'fraction', 1, 127],
	[	'Length of lateral', 'ft', 0, 128],
	[	'Fraction of wells fractured', 'fraction', 0, 129],
	[	'Fracturing fluid injection volume', 'million gal', 1, 130],
	[	'Fracture pressure gradient', 'psi/ft', 0.7, 131],
	[	'Facility name', 'N/A', 0, 134],
	[	'Facility type', 'N/A', 0, 135],
	[	'Facility gas-to-oil ratio', 'scf/bbl oil', 0, 136],
	[	'Facility flared gas', '%', 0, 137],
	[	'Facility vented gas', '%', 0, 138],
	[	'Facility fuel gas', '%', 0, 139],
	[	'Fugitive percentage alteration of base case','fraction',0,142],
	[	'Electricity Consumption', 'kwh/scf', 0, 145],
	[	'EUR boe/well', 'bbl', 100000, 148],
	[	'Coordinates', '[lon,lat]', 0, 155],
	[	'Formation', '[-]', 0, 156],
	[	'Province', '[-]', 0, 157],
	[	'Area', '[lon,lat]', 0, 158]]


	for i in range(0,len(opgee_input_data)):
		OPGEE_data['headings'].append(opgee_input_data[i][0])
		OPGEE_data['units'].append(opgee_input_data[i][1])
		OPGEE_data['defaults'].append(opgee_input_data[i][2])
		OPGEE_data['assessed field'].append(opgee_input_data[i][2])
		OPGEE_data['excel position'].append(opgee_input_data[i][3])


	return OPGEE_data