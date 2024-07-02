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
    city = ''
    #While loop to validate inputs
    while city not in CITY_DATA.keys():
        print("\nPlease choose your city:")
        print("\n1. Chicago 2. New York City 3. Washington")
        print("\nAccepted input:\nFull name of city; not case sensitive (e.g. chicago or CHICAGO).\nFull name in title case (e.g. Chicago).")
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\n Invalid city entry please retry.")
            print("\nRestarting...")

    print(f"\nYou have selected {city.title()} as your city.")

    #Creating a dictionary to store all the months including the 'all' option
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\n Enter the month, between January to June, for which you want the data:")
       
        print("\n(You may also opt to view data for all months, please type 'all' or 'All' or 'ALL' for that.)")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nInvalid input. Please try again in the accepted input format.")
            print("\nRestarting...")

    print(f"\nYou have chosen {month.title()} as your month.")

    #Creating a list to store all the days including the 'all' option
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nEnter a day in the week of your choice for which you're seeking the data:")
        print("\nAccepted input:\nDay name; not case sensitive (e.g. monday or MONDAY).\nDay name in title case (e.g. Monday).")
        print("\n(You can also put 'all' or 'All' to view data for all days in a week.)")
        day = input().lower()

        if day not in DAY_LIST:
            print("\nInvalid input. Please try again in one of the accepted input formats.")
            print("\nRestarting...")
    print("Here are the inputs provided")
    print(f"\nYou have chosen {day.title()} as your day.")
    print(f"\nYou have chosen to view data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")
    print('-'*40)
  #  print('-'*40)
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
    print("\ data loading...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #Returns the selected file as a dataframe (df) with relevant columns
    return df



#Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """

    start_time = time.time()

    #mode to the popular month for travel
    popular_month = df['month'].mode()[0]

    print(f"Popular Travel Month (1 = January,...,6 = June): {popular_month}")
#mode to the popular day of the week for travel
    popular_day = df['day_of_week'].mode()[0]

    print(f"\n Popular Day: {popular_day}")

    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]

    print(f"\n Popular Start Hour: {popular_hour}")

    print(f"\n Exceution took {(time.time() - start_time)} seconds.")
    print('-'*40)

#Function to calculate station related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """

    start_time = time.time()

    #Uses mode method to find the most common start station
    common_start_station = df['Start Station'].mode()[0]

    print(f"Popular start station: {common_start_station}")

    common_end_station = df['End Station'].mode()[0]

    print(f"\n Popular destination station: {common_end_station}")

    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print(f"\nBest combination {combo}.")

    print(f"\nExecution time {(time.time() - start_time)} seconds.")
    print('-'*40)

#Function for trip duration related statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print(f"\n Trip Duration is {hour} hours, {minute} minutes and {second} seconds.")

    average_duration = round(df['Trip Duration'].mean())
    mins, sec = divmod(average_duration, 60)
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\n Average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nAverage trip duration is {mins} minutes and {sec} seconds.")

    print(f"\n Execution took {(time.time() - start_time)} seconds.")
    print('-'*40)

#Function to calculate user statistics
def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #The total users are counted using value_counts method
    #They are then displayed by their types (e.g. Subscriber or Customer)
    user_type = df['User Type'].value_counts()

    print(f"User Types:\n\n{user_type}")

    #This try clause is implemented to display the numebr of users by Gender
    #However, not every df may have the Gender column, hence this...
    try:
        gender = df['Gender'].value_counts()
        print(f"\nUser Types by Gender:\n\n{gender}")
    except:
        print("\n No Gender Found")

    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("No birth details available.")

    print(f"\n Execution {(time.time() - start_time)} seconds.")
    print('-'*40)

#Function to display the data frame itself as per user request
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you want to see raw data?")
        print("\nYes or yes\nNo or no")
        rdata = input().lower()
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")

    while rdata == 'yes':
        print("Do you want to see raw data?")
        counter += 5
        rdata = input().lower()
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*40)

#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
