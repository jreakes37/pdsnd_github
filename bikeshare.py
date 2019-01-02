import time
import pandas as pd
import numpy as np

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
    cities = ['chicago', 'new york city', 'washington']

    while True:
        city = input('Please enter the name of the city for which you would like to see data: ')
        if city.lower() in cities:
            break
        else:
            print('That is not a valid input, please try again')
            continue

    # get user input for month (all, january, february, ... , june - only the first six months of the year)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        month = input('Please enter the month for which you would like to see data: ')
        if month.lower() in months:
            break
        else:
            print('That is not a valid input, please try again')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        day = input('Please enter the day for which you would like to see data: ')
        if day.lower() in days:
            break
        else:
            print('That is not a valid input, please try again')
            continue


    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    popular_month = df['month'].mode()[0]

    print('Most Common Month:', popular_month)

    # display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['day_of_week'] = df['Start Time'].dt.weekday_name

    popular_day = df['day_of_week'].mode()[0]

    print('Most Common Day:', popular_day)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('Most popular end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' to ' + df['End Station']

    popular_route = df['route'].mode()[0]

    print('Most popular route:', popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    overall_trip_duration = int(df['Trip Duration'].sum())

    if overall_trip_duration <= 60:
        print('The overall trip duration was: {} seconds.'.format(overall_trip_duration))
    elif overall_trip_duration <= 3600:
        minutes = overall_trip_duration // 60
        print('The overall trip duration was approximately {} minutes.'.format(minutes))
    elif overall_trip_duration <= 86400:
        hours = overall_trip_duration // 3600
        print('The overall trip duration was approximately {} hours.'.format(hours))
    else:
        days = overall_trip_duration // 86400
        print('The overall trip duration was approximately {} days.'.format(days))

    # display mean travel time
    average_trip_duration = int(df['Trip Duration'].mean())

    if average_trip_duration <= 60:
        print('The average trip duration was: {} seconds.'.format(average_trip_duration))
    elif average_trip_duration <= 3600:
        minutes = average_trip_duration // 60
        seconds = average_trip_duration % 60
        print('The average trip duration was {} minutes and {} seconds.'.format(minutes, seconds))
    else:
        hours = average_trip_duration // 3600
        print('The average trip duration was approximately {} hours.'.format(hours))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        subscriber = df['User Type'].value_counts()['Subscriber']
        print('{} subscribers.'.format(subscriber))
    except:
        print('No subscribers')

    try:
        customer = df['User Type'].value_counts()['Customer']
        print('{} customers.'.format(customer))
    except:
        print('No customers')

    try:
        dependent = df['User Type'].value_counts()['Dependent']
        print('{} dependents.'.format(dependent))
    except:
        print('No dependents')

    # Display counts of gender
    try:
        females = df['Gender'].value_counts()['Female']
        males = df['Gender'].value_counts()['Male']
        undisclosed = sum(pd.isnull(df['Gender']))
        print('Number of females:', females)
        print('Number of males:', males)
        print('Number of undisclosed:', undisclosed)
    except:
        print('Gender information is not available for Washington')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print('The earliest year of birth: {}.'.format(earliest))
        print('The most recent year of birth: {}.'.format(most_recent))
        print('The most common year of birth: {}.'.format(most_common))
    except:
        print('Birth Year information not available for Washington')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats_question = input('\nWould you like to see time stats info? Enter yes or no\n')
        if time_stats_question != 'yes':
            pass
        else:
            time_stats(df)

        station_stats_question = input('\nWould you like to see station stats info? Enter yes or no\n')
        if station_stats_question != 'yes':
            pass
        else:
            station_stats(df)

        trip_duration_stats_question = input('\nWould you like to see trip duration stats info? Enter yes or no\n')
        if trip_duration_stats_question != 'yes':
            pass
        else:
            trip_duration_stats(df)

        user_stats_question = input('\nWould you like to see user stats stats info? Enter yes or no\n')
        if user_stats_question != 'yes':
            pass
        else:
            user_stats(df)

        raw_data = input('\nWould you like to see the first five lines of raw data from your chosen data-set? Enter yes or no.\n')
        if raw_data.lower() != 'yes':
            pass
        else:
            print(df.head(5))
            while True:
                df = df[5: ]
                next_question = input('\nWould you like to see another five lines?\n')
                if next_question.lower() != 'yes':
                    break
                else:
                    print(df.head(5))
                    continue


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
