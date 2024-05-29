

def dates_array(start_date,end_date):
	#takes in start dat and end date in the format YYYY-MM and returns array 

	dates_array = []
	dates_array.append(start_date)

	if start_date == end_date:
		return [start_date]

	while start_date != end_date:

		if int(start_date[-2:]) < 9:
			next_month = int(start_date[-1]) + 1
			next_date = start_date[0:6] + str(next_month)
			dates_array.append(next_date)
		if (9 <= int(start_date[-2:]) < 12):
			next_month = int(start_date[-2:]) + 1
			next_date = start_date[0:5] + str(next_month)
			dates_array.append(next_date)
		if int(start_date[-2:]) == 12:
			next_year = int(start_date[0:4]) + 1
			next_date = str(next_year) + '-01'
			dates_array.append(next_date)

		start_date = next_date


	print(dates_array)

	return dates_array
