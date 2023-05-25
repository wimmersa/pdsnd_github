import pandas as pd
import time

###Dictionary for cities and their corelating .csv files###
CITY_DATA = { 'chicago': 'chicago.csv',
			'new york': 'new_york_city.csv',
			'washington': 'washington.csv' }
			
###Helper functions used for improving readability in the printed results###
def index_to_week_day(ind):
	if int(ind) in range(0,7):
		days = { 0 : 'Monday', 1 : 'Tuesday', 2 : 'Wednesday', 3 : 'Thursday', 4 : 'Friday', 5 : 'Saturday', 6 : 'Sunday'}
		return days[ind]
	else:
		return('No data')
def index_to_month(ind):
	if int(ind) in range(1,7):
		months = { 1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June'}
		return months[ind]
	else:
		return 'No data'
def seconds_to_time(sec):
	inp_time = time.gmtime(sec)
	str_time = time.strftime('%H:%M:%S', inp_time)
	return str_time

### Functions ###
def load_data(city, month, day):

	"""
	Loads data for the specified city and filters by month and day if applicable.

	Args:
		(str) city - name of the city to analyze
		(str) month - name of the month to filter by, or "all" to apply no month filter
		(str) day - name of the day of week to filter by, or "all" to apply no day filter
	Returns:
		df - pandas DataFrame containing city data filtered by month and day
	"""
	
	# load data file into a dataframe
	#TODO: REPLACE FILE PATH WITH LOCAL ONE
	df = pd.read_csv(r"C:\Users\wimmersa\OneDrive - Mediengruppe RTL\Udactiy\#3 Git Project\CSV_files\{}".format(CITY_DATA[city]))

	# convert the Start Time column to datetime
	df['Start Time'] = pd.to_datetime(df['Start Time'])

	# extract month and day of week from Start Time to create new columns
	df['month'] = df['Start Time'].dt.month
	df['day_of_week'] = df['Start Time'].dt.day_of_week
	df['hour'] = df['Start Time'].dt.hour
	


	# filter by month if applicable
	if month != 'all':
		# use the index of the months list to get the corresponding int
		months = ['january', 'february', 'march', 'april', 'may', 'june']
		month = months.index(month) + 1
	
		# filter by month to create the new dataframe
		df = df[df['month'] == month]

	# filter by day of week if applicable
	if day != 'all':
		# filter by day of week to create the new dataframe
		days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
		day = days.index(day) 
		df = df[df['day_of_week'] == day]
	
	return df

def display_raw_data_chunks(df, chunk_size=5):
	"""function to display 5 rows of raw data at a time
	Args:
		(pd.dataframe) df - pandas dataframe to work with
		(int) chunk_size - amount of rows per chunk
	user can stop loop by pressing q 
	chunk_generator is only needed in this place so I placed the function within this function 
	default chunk size is 5 and not costumizable by the user
	"""
	def chunk_generator(df, chunk_size):
		"""generator for chunking the dataframe, takes arguments from parent function 
			args:
			(pd.dataframe) df - dataframe to work with
			(int) chunk_size - amount of rows to display per chunk 
		"""
		num_chunks = len(df) // chunk_size + 1
		for i in range(num_chunks):
			start = i * chunk_size
			end = min(start + chunk_size, len(df))
			yield df[start:end]
	chunk_gen = chunk_generator(df, chunk_size)
	while True: 
		try: 
			user_answer = input('Press enter to display 5 rows or "q" to quit ')
			if user_answer.lower() == 'q':
				return 
			next_chunk = next(chunk_gen)
			print(next_chunk)
		except StopIteration:
			print('End of data')
			return

#following functions are for displaying the processed information 
def print_01_travel_data(df):
	try: 
		#most common month 
		most_common_month = df['month'].value_counts().idxmax()
		#most common day of week
		most_common_day = df['day_of_week'].value_counts().idxmax() 
		#most common hour of day
		most_common_hour_of_day = df['hour'].value_counts().idxmax()
		print('#### #1 POPULAR TIMES OF TRAVEL #### ')
		print('The most common month is: ', index_to_month(most_common_month))
		print('The most common day is: ', index_to_week_day(most_common_day))
		print('The most common hour is: ', most_common_hour_of_day)
		print('##########################')
	except:
		print('Uncompatible data')

def print_02_stations_and_trips_data(df):
	
	try: 
		df['start_end'] = df['Start Station'] + ' to ' + df['End Station']
		#most common start station
		most_common_start_station = df['Start Station'].value_counts().idxmax()
		#most common end station 
		most_common_end_station = df['End Station'].value_counts().idxmax()
		#most common trip from start to end aka the combination
		most_commen_start_end_com = df['start_end'].value_counts().idxmax()
		print('#### #2 POPULAR STATIONS AND TRIP #### ')
		print('The most common start station is: ', most_common_start_station)
		print('The most common end station is: ', most_common_end_station)
		print('The most common combination is: ', most_commen_start_end_com)
		print('##########################')
	except:
		print('Uncompatible data')

def print_03_trip_duration(df):
	
	try:
		#total travel time
		total_travel_time = df['Trip Duration'].sum()
		#average travel time 
		average_travel_time = df['Trip Duration'].mean()
		print('#### #3 TRIP DURATION #### ')
		print('The total travel time is: ', seconds_to_time(total_travel_time))
		print('The average travel time: ', seconds_to_time(average_travel_time))
		print('##########################')
	except: 
		print('Uncompatible data')

def print_04_user_info(df):
	
	try: 
		#counts of each user type
		user_type_count = df['User Type'].value_counts()
		print('#### #4 USER INFO #### ')
		print('User Types: ', user_type_count)
		if 'Gender' and 'Birth Year' in df.columns:
		
			#counts of each gender
			gender_count = df['User Type'].value_counts()
			#earliest, most recent, most common year of birth
			earliest_user_year = df['Birth Year'].min()
			latest_user_year = df['Birth Year'].max()
			most_common_user_year = df['Birth Year'].value_counts().idxmax()
			print('Earliest user birth year: ', int(earliest_user_year))
			print('Latest user birth year: ', int(latest_user_year))
			print('Most common user birth year: ', int(most_common_user_year))
		else:
			print('No further usa data available in this city')
		print('##########################')
	except: 
		print('Uncompatible data')

def get_user_input():
	"""takes no arguments
	#gets user input for pre defined cities, months and also all weekdays
	#user can also choose all, to display all data 
	#return:
		a tuple with strings that contains the city, month and day the user chose 
	"""
	while True:
		allowed_cities = ['washington', 'new york', 'chicago']
		allowed_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday', 'all']
		allowed_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
		city = ''
		day = ''
		month = ''
		while city not in allowed_cities:
			city = input("Choose a city (Washington, New York or Chicago):  ").lower()
		while month not in allowed_months:
			month = input("Choose a month between January and June (or all):  ").lower()
		while day not in allowed_days:
			day = input("Choose a weekday (Monday to Sunday or all):  ").lower()
		return (city, month, day)
		break
			

def show_raw_data(df):
	"""
	#askes the user if he wants to see raw data and displays it in chunks at a time
	#returns after the last row was displayed
	args:
		(pd.dataframe) - dataframe to work with
	"""
	answers = ['yes', 'y', 'no', 'n']
	raw_data_input = ''
	while raw_data_input not in answers:
		raw_data_input = input("Do you want to see the raw data? (y/n):  ").lower()
	if raw_data_input == 'yes' or raw_data_input == 'y':
		
		display_raw_data_chunks(df)
	else:
		return

def repeat_analysis():
	"""takes no arguments
	#checks if user wants to repeat the program
	#does not return a value
	"""
	while True: 
		answers = ['yes', 'y', 'no', 'n']
		start_over = ''
		while start_over not in answers:
				start_over = input('Do you want to try again? yes or no?:  ').lower()
				return start_over
				break

#### MAIN APPLICATION ####

def main():
	#main programm loop
	while True:
		###getting input and loading data
		user_input = get_user_input()
		city, month, day = user_input
		start_time = time.process_time()
		df = load_data(city, month, day)

		###printing data###
		print_01_travel_data(df)
		print_02_stations_and_trips_data(df)
		print_03_trip_duration(df)
		print_04_user_info(df)
		end_time = time.process_time()
		print('This took: {} seconds to calculate on the cpu'.format(end_time - start_time))

		###check for raw data###
		show_raw_data(df)
		
		###check to re-run program###
		is_repeating = repeat_analysis()
		if is_repeating == 'yes' or is_repeating == 'y':
			continue
		else:
			break 

if __name__ == "__main__":
	main()