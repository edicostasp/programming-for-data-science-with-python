import time
import math
import pandas as pd
#   import numpy as np
import click

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTH_DATA = {'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'may': 5,
              'june': 6,
              'jan': 1,
              'feb': 2,
              'mar': 3,
              'apr': 4,
              'jun': 6}

WEEK_DATA = {'monday': 0,
             'tuesday': 1,
             'wednesday': 2,
             'thursday': 3,
             'friday': 4,
             'saturday': 5,
             'sunday': 6,
             'mon': 0,
             'tues': 1,
             'wed': 2,
             'thur': 3,
             'fri': 4,
             'sat': 5,
             'sun': 6}


def choice(prompt, choices=('y', 'n')):
    """
    Validate the values in a array.

    Return a valid input from the user given an array
    of possible answers.
    """
    while True:
        choice = input(prompt).lower().strip()
        if choice == '0':
            raise SystemExit
        elif ',' not in choice:
            if choice in choices:
                break
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break
        prompt = ("\n!!OOOPS !!!Please be sure to enter a valid option!! /n")
    return choice


def get_filters():
    """
    User specify the city, month, and day to analyze.

    Return -
    city - name of the city to analyze
    month - name of the month to filter by,
            or "all" to apply no month filter
    day - name of the day of week to filter by,
            or "all" to apply no day filter
    """
    print('Hello! I am Python 3.8! Let\'s explore some US bikeshare data!')
    print()
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while 1:
        print('Which city should we look for?')
        city = input('1 = Chicago\n'
                     '2 = New York City\n'
                     '3 = Washington\n'
                     '\n').lower()
        print('*'*40)
        print()
        if city in ('1', 'ch'):
            city = 'chicago'
            print("Chicago City! Here We go !!!")
        if city in ('2', 'ny', 'nyc'):
            city = 'new york city'
            print("New York City! Here We go !!!")
        if city in ('3', 'wa', 'washington dc'):
            city = 'washington'
            print("Washington! Here We go !!!")
        if city not in CITY_DATA:
            print('Please enter a valid city')
            continue
        city = CITY_DATA[city]
        break
    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while 1:
        m_choice = input('Do you want to filter the data ?\n'
                         'Yes\n'
                         'No\n'
                         '\n').lower()
        print()
        if m_choice in ('yes', 'y', 'yus'):
            print('*'*40)
            print('\nThe data is now being filtered ...')
            m_choice = True
        elif m_choice in ('no', 'n', 'nope'):
            m_choice = False
        else:
            print('*'*40)
            print('You did not enter a valid choice. Let\'s try again. ')
            print('*'*40)
            continue
        break

    while 1:
        if m_choice:
            filter = input('You can filter by:\n'
                           '\n'
                           'Month\n'
                           'Day\n'
                           'Both\n'
                           '\n').lower()
            print()
            print('*'*40)
            if filter == 'month':
                print('Which month would you like to see?')
                month = input('jan = January \n'
                              'feb = February\n'
                              'mar = March\n'
                              'apr = April\n'
                              'may = May\n'
                              'jun = June \n'
                              '\n').lower()
                print('*'*40)
                print()
                if month not in MONTH_DATA:
                    print('Sorry I did not understand that input.'
                          'Could you try again?')
                    continue
                month = MONTH_DATA[month]
                day = 'all'
            elif filter == 'day':
                print('Which day would you like to see? ')
                day = input('mon = Monday\n'
                            'tues = Tuesday\n'
                            'wed = Wednesday\n'
                            'thur = Thursday\n'
                            'fri = Friday\n'
                            'sat = Saturday\n'
                            'sun = Sunday\n'
                            '\n').lower()
                print('*'*40)
                print()
                if day not in WEEK_DATA:
                    print('Sorry I did not understand that input.'
                          'Could you try again?')
                    continue
                day = WEEK_DATA[day]
                month = 'all'
            elif filter == 'both':
                print('Which month would you like to see?')
                month = input('jan = January \n'
                              'feb = February\n'
                              'mar = March\n'
                              'apr = April\n'
                              'may = May\n'
                              'jun = June \n'
                              '\n').lower()
                print('*'*40)
                print()
                if month not in MONTH_DATA:
                    print('Sorry I did not understand that input.'
                          'Could you try again?')
                    continue
                month = MONTH_DATA[month]
                print('Which day of the week would you like to see?')
                day = input('mon = Monday\n'
                            'tues = Tuesday\n'
                            'wed = Wednesday\n'
                            'thur = Thursday\n'
                            'fri = Friday\n'
                            'sat = Saturday\n'
                            'sun = Sunday\n'
                            '\n').lower()
                print('*'*40)
                print()
                if day not in WEEK_DATA:
                    print('Sorry I did not understand that input.'
                          'Could you try again?')
                    continue
                day = WEEK_DATA[day]
            else:
                print('Sorry I did not understand that input.'
                      'Could you try again?')
                continue
            break
        else:
            day = 'all'
            month = 'all'
            break

    print('*'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Load the city data and filters by month and day.

    Args -
    (str) city - name of the city
    (str) month - month to filter by,or "all" to apply no month filter
    (str) day - name of the day of week to filter by,
    or "all" to apply no day filter.-

    Return - df - Pandas DataFrame containing city data
    filtered by month and day

    """
    df = pd.read_csv(city)
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    if day != 'all':
        df = df[df['day_of_week'] == day]
    if month != 'all':
        df = df[df['month'] == month]
    df.drop('day_of_week', axis=1, inplace=True)
    df.drop('month', axis=1, inplace=True)
    return df


def time_stats(df):
    """Display statistic on the most common times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
#   temporary_df = pd.read_csv(city)
#   TO DO: display the most common month
    most_freq_month = df['month'].mode()[0]
    for num in MONTH_DATA:
        if MONTH_DATA[num] == most_freq_month:
            most_freq_month = num.title()
    print('The most common month is {}'.format(most_freq_month))

    # TO DO: display the most common day of week
    most_freq_day = df['day_of_week'].mode()[0]
    for num in WEEK_DATA:
        if WEEK_DATA[num] == most_freq_day:
            most_freq_day = num.title()
    print('The most common day of week is {}'.format(most_freq_day))

    # TO DO: display the most common start hour
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    most_freq_hour = df['hour'].mode()[0]
    print('The most common hour of day is {}'.format(most_freq_hour))
    df.drop('hour', axis=1, inplace=True)
    df.drop('day_of_week', axis=1, inplace=True)
    df.drop('month', axis=1, inplace=True)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip.

    Returns Stations Statistics
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print()
    print('Most commonly used start station was {}'
          .format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print()
    print('Most commonly used end station was {}'
          .format(df['End Station'].mode()[0]))

#   TO DO: display most frequent combination of start station and
#   end station trip
    print()
    most_freq_station_comb = df['Start Station'] + ' to '+df['End Station']
    print('The most frequent combination of start station and end station was{}'
          .format(most_freq_station_comb.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration.

    Returns Statistics about Trip Duration
    """
    print('\nCalculating Total Travel Time...\n')
    start_time = time.time()
    travel_durations = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])

    # TO DO: display total travel time
    print()
    td_sum = df['Total Travel Time'].sum()
    sum_seconds = td_sum % 60
    sum_minutes = td_sum//60 % 60
    sum_hours = td_sum//3600 % 60
    sum_days = td_sum//24//3600
    print('Passengers travelled a total of {} days, {} hours,'
          '{} minutes and {} seconds'
          .format(sum_days, sum_hours, sum_minutes, sum_seconds))

    # TO DO: display mean travel time
    print()
    td_mean = math.ceil(df['Trip Duration'].mean())
    mean_seconds = td_mean % 60
    mean_minutes = td_mean//60 % 60
    mean_hours = td_mean//3600 % 60
    mean_days = td_mean // 24 // 3600
    print('Passengers travelled an average of {} hours,'
          '{} minutes and {} seconds'
          .format(mean_hours, mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def user_stats(df):
    """
    Display statistics on bikeshare users.

    Returns statistics
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print()
    types_of_users = df.groupby('User Type', as_index=False).count()
    print('Number of types of users are {}'.format(len(types_of_users)))
    for i in range(len(types_of_users)):
        print('{}s - {}'
              .format(types_of_users['User Type'][i],
                      types_of_users['Start Time'][i]))

    # TO DO: Display counts of gender
    print()
    if 'Gender' not in df:
        print('Shoot, no gender data for this city :(')
    else:
        gender_of_users = df.groupby('Gender', as_index=False).count()
        print('Number of genders of users mentioned in the data are {}'
              .format(len(gender_of_users)))
        for i in range(len(gender_of_users)):
            print('{}s - {}'
                  .format(gender_of_users['Gender'][i],
                          gender_of_users['Start Time'][i]))
        print('Gender data for {} users is not available.'
              .format(len(df)-gender_of_users['Start Time'][0]
                      - gender_of_users['Start Time'][1]))

    # TO DO: Display earliest, most recent, and most common year of birth
    print()
    if 'Birth Year' not in df:
        print('Data related to birth year of users is'
              'not available for this city.')
    else:
        birth = df.groupby('Birth Year', as_index=False).count()
        print('Earliest year of birth was {}.'
              .format(int(birth['Birth Year'].min())))
        print('Most recent year of birth was {}.'
              .format(int(birth['Birth Year'].max())))
        print('Most common year of birth year was {}.'
              .format(int(birth.iloc[birth['Start Time']
                                     .idxmax()]['Birth Year'])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def display_data(df):
    """
    Display the Data.

    Return input results
    """
    choice = input('Would you like to read some of the raw data?'
                   '\nYes'
                   '\nNo'
                   '\n'
                   .lower())
    print()
    if choice in ('yes', 'y', 'yus'):
        choice = True
    elif choice in ('no', 'n', 'nope'):
        choice = False
    else:
        print('You did not enter a valid choice. Let\'s try that again. ')
        display_data(df)
        return

    if choice:
        while 1:
            for i in range(5):
                print(df.iloc[i])
                print()
            choice = input('Another Five?'
                           '\nYes'
                           '\nNo'
                           '\n'
                           .lower())
            if choice in ('yes', 'y', 'yus'):
                print(df.iloc[i])
                continue
            elif choice in ('no', 'n', 'nope'):
                break
            else:
                print('You did not enter a valid choice.')
                return


def main():
    """
    Display Function to choose which statistic user want to see.

    Returns - call for other functions
    """
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        while True:
            select_data = choice('\nPlease select the information you would'
                                 'like to obtain:\n'
                                 '\n'
                                 '[ts] Time Stats\n'
                                 '[ss] Station Stats\n'
                                 '[tds] Trip Duration Stats \n'
                                 '[us] User Stats\n'
                                 '[rd] Raw Data\n'
                                 '\n'
                                 '[0] Exit\n>',
                                 ('ts', 'ss', 'tds', 'us', 'rd', 'r'))
            click.clear()
            if select_data == 'ts':
                time_stats(df)
            elif select_data == 'ss':
                station_stats(df)
            elif select_data == 'tds':
                trip_duration_stats(df)
            elif select_data == 'us':
                user_stats(df)
            elif select_data == 'rd':
                display_data(df)
            elif select_data == '0':
                break

        restart = choice('\nWould you like to restart?'
                         'Enter yes or no.\n').lower()
        print()
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
