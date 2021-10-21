# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

pd.set_option('display.expand_frame_repr', False)


# %%
def print_dash(count):
    """Prints out a string to demarcate a title"""
    
    output = "-" * count
    print(output)

def print_time(start_time, end_time):
    """Prints out the duration a function took to run"""
    print(f"\nThis took {(end_time - start_time):.2f} seconds.")
    print_dash(40)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ""
    while city not in ['washington', 'new york city', 'chicago']:
        city = str.lower(input('\nWhich city would you like to view (Chicago, New York City, Washington)?\n'))
        
    month = ""
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']:
        month = str.lower(input(f'\nWhich month would you like to view for {str.title(city)}?\n'))

    day = ""    
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = str.lower(input(f'\nWhich day of the week like to view for {str.title(city)} during {str.title(month)}?\n'))
    
    df = load_data(city, month, day)

    if df.shape[0] != 0:

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        lines = 'yes'
        count = 0

        while lines == 'yes':
            lines = str.lower(input(f'\nWould you like to see 5 lines of raw data?\n'))

            if str.lower(lines) == 'yes':
                count += 5
                print(df[count:count+5])

        print('-'*40)
    else:
        print("\nNo data available")


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Processing:
        - Makes all dates datetime64 objects to allow for correct processing later on
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    file = CITY_DATA[city]
    
    df = pd.read_csv(file)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    if month != "all":
        df = df.loc[(df['Start Time'].dt.month_name() == str.title(month))]
        if day != "all":
            df = df.loc[(df['Start Time'].dt.day_name() == str.title(day))]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()
    print(f'\nNumber of trips - {df.shape[0]}')
    print('\nCalculating The Most Frequent Times of Travel...\n')
    
    df['month'] = df['Start Time'].dt.month_name()
    print(f"The most common month is {df['month'].value_counts().nlargest(1).index[0]}")
    
    df['week'] = df['Start Time'].dt.day_name()
    print(f"The most common day of the week is {df['week'].value_counts().nlargest(1).index[0]}")

    df['hour_of_day'] = df['Start Time'].dt.hour
    print(f"The most common hour of the day is {df['hour_of_day'].value_counts().nlargest(1).index[0]}:00")

    print_time(start_time, time.time())


# %%
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print(f"Most Common Start Station - {df['Start Station'].value_counts().nlargest(1).index[0]}")

    # TO DO: display most commonly used end station
    print(f"Most Common End Station - {df['End Station'].value_counts().nlargest(1).index[0]}")

    # TO DO: display most frequent combination of start station and end station trip
    station_combo = df.groupby(['Start Station','End Station']).size().reset_index().rename(columns={0:'count'}).sort_values(by=['count'], ascending=False).head(1)
    print(f"Most Common Start and End Stations - Start {station_combo['Start Station'].to_string(index=False)} and End {station_combo['End Station'].to_string(index=False)}")

    print_time(start_time, time.time())


# %%
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print(f"The total travel time is {(df['Trip Duration'].sum())/60/60.:2f} hours")

    # TO DO: display mean travel time
    print(f"The mean travel time is {(df['Trip Duration'].mean())/60.:2f} minutes")

    print_time(start_time, time.time())


# %%
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("User Type Count\n===============\n")
    print(df['User Type'].value_counts().to_string())

    # TO DO: Display counts of gender
    if 'Gender' in df.keys():
        print("\nGender Count\n============\n") 
        print(df['Gender'].value_counts().to_string())

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.keys():
        print("\nInteresting Stats\n=================")
        print(f"\nThe earliest traveller was born in {int(df['Birth Year'].min())}")
        print(f"The most recent traveller was born in {int(df.loc[df['Start Time'] == df['Start Time'].max(), 'Birth Year'].values[0])}")
        print(f"The most common birth year is {int(df['Birth Year'].mode())}")

    print_time(start_time, time.time())


# %%


def main():
    while True:
        get_filters()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


