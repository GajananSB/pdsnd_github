import time
import pandas as pd
import numpy as np
import datetime
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    #get the name of the city
    while city is None :
        input_city = input("Enter city name (chicago, new york city, washington): ").lower()
        if input_city.lower() in ['chicago', 'new york city', 'washington'] :
            city = input_city
        else:
            print("\n\tERROR : {} is not a valid city\n".format(input_city))

    # get user input for month (all, january, february, ... , june)
    month = None

    while month is None:
       input_month = input("Enter month till june (all, january, february, ... , june): ").lower()
       if input_month.lower() in ['all','january', 'february','march','april','may','june']:
             month = input_month
       else:
            print("\n\tERROR : {} is not a valid month\n".format(input_month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while day is None:
        input_day = input("Enter day of week (all, monday, tuesday, ... sunday): ").lower()
        if input_day in ['all', 'monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']:
            day = input_day
        else:
            print("\n\tERROR : {} is not a valid day\n".format(input_day))

    print('-'*60)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city.replace(' ','_')+'.csv')
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] =  [month == 'all' or mt.strftime('%b').lower() == month[:3] for mt in df['Start Time']]
    df['day'] = [day == 'all' or  calendar.day_name[ dt.weekday()].lower() == day.lower() for dt in df['Start Time']]
    
    dfmn = df[df['month'] == True ]
    dfdt = dfmn[dfmn['day'] == True]

    return dfdt


def get_max_value(dt):
    """
    Returns key with max value

    Args:
        (dict) dt - key-value pair for getting max value
    Returns:
        maxValue - key with Max value
    """
    maxValue = None

    cnts = list(dt.values())
    cnts.sort(reverse = True)
    max = cnts[0]

    for k,v in dt.items():
        if v == max:
            maxValue = k

    return maxValue
    
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = dict()
    weekdays = dict()
    start_hour = dict()

    for lbl, i in df.iterrows():
        tt = i[1]
        mtname = tt.strftime('%b')
        months[mtname] = months.get(mtname,0) + 1
        wod = calendar.day_name[ tt.weekday()]
        weekdays[wod] = weekdays.get(wod,0) + 1
        hr = str(tt.hour)
        start_hour[hr] = start_hour.get(hr,0) + 1

    # display the most common month
    print("\nMost common month is : {}\n".format(get_max_value(months)))

    # display the most common day of week
    print("\nMost common day of week is : {}\n".format(get_max_value(weekdays)))

    # display the most common start hour
    print("\nMost common start hour is : {}\n".format(get_max_value(start_hour)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    input("\n...press any key to continue...\n")
    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    str_stn = dict()
    end_stn = dict()
    str_to_end_stn = dict()

    for lbl, i in df.iterrows():
        start_station = i[4]
        str_stn[start_station] = str_stn.get(start_station,0) + 1
        end_station = i[5]
        end_stn[end_station] = end_stn.get(end_station,0) + 1
        start_end_station = i[4] + i[5]
        str_to_end_stn[start_end_station] = str_to_end_stn.get(start_end_station,0) + 1

    # display most commonly used start station
    print("\nMost commonly used start station is : {}\n".format(get_max_value(str_stn)))

    # display most commonly used end station
    print("\nMost commonly used end station is : {}\n".format(get_max_value(end_stn)))

    # display most frequent combination of start station and end station trip
    print("\nMost frequent combination of start station and end station trip is : {}\n".format(get_max_value(str_to_end_stn)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    input("\n...press any key to continue...\n")
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    tt = datetime.timedelta(0)

    for lbl, i in df.iterrows():
        st = i[1]
        et = i[2]
        tt += et-st

    # display total travel time
    print("\nTotal travel time is: {}".format(tt))

    # display mean travel time
    print("\nMean travel time is : {}\n".format(datetime.timedelta(df.mean()[1])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    input("\n...press any key to continue...\n")
    print('-'*60)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    usr_type = dict()
    gdr = dict()
    brt_date = dict()
    for lbl, i in df.iterrows():
        typ = i[6]
        usr_type[typ] = usr_type.get(typ,0) + 1
        gdr[i[7]] = gdr.get(i[7],0) + 1
        bd = str(i[8])
        if bd != str(float('nan')) :
            brt_date[bd] = brt_date.get(bd,0) + 1
                 
    # Display counts of user types
    print("Counts for user types are as follows:")
    for k,v in usr_type.items():
        print("{} : {}".format(k,v))

    # Display counts of gender
    print("\nCounts for gender types are as follows:")
    for k,v in gdr.items():
        print("{} : {}".format(k,v))

    # Display earliest, most recent, and most common year of birth
    #if df.has_key('Birth Year'):
    if 'Birth Year' in df:
        print("\nEarliest year of birth is: {}".format(df['Birth Year'].min()))
        print("\nMost recent year of birth is: {}".format(df['Birth Year'].max()))
        print("\nMost common year of birth is: {}".format(get_max_value(brt_date)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    input("\n...press any key to continue...\n")    
    print('-'*60)


def main():
    """
    main function, which calls the individual functions to get the data from the different cities and 
    displays the statistics of the data
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
