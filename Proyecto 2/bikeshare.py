import time
import pandas as pd
import numpy as np
from tabulate import tabulate
import os

ruta=os.getcwd()
pd.set_option('display.max_columns', None)

CITY_DATA = { 'chicago': ruta+'\chicago.csv',
              'new york city': ruta+'\new_york_city.csv',
              'washington': ruta+'\washington.csv' }



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=''
    while city not in CITY_DATA.keys():
        print('please enter the city (chicago / new york city / washington):')
        city=input()
    
    filter_date=''
    while (filter_date=='y' or filter_date=='n')==False:
        print('Do you want filter by dates or not: (Y/N)')
        filter_date= input().lower()
        
    if filter_date=='y':
        # TO DO: get user input for month (all, january, february, ... , june)
        months = ['january', 'february', 'march', 'april', 'may', 'june','all']
        month=''
        while month not in months:
            print("please enter the month (e.g. January) or if  you don't want to filter by months enter 'all'")
            month=input().lower()
            if month not in months:
                print('please try wiht something like:'+','.join([str(m) for m in months])+'\n')
            
        
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        days=['all', 'monday', 'tuesday', 'wednesday', 'thursday','friday','saturday','sunday']
        day=''
        while day not in days:
            print('please enter a week name day or enter "all" (e.g.:tuesday):')
            day=input().lower()
            if day not in days:
                print('please try wiht something like:'+','.join([str(d) for d in days])+'\n')
    else:
        month='all'
        day='all'        

    print('-'*40)
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
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city))
    
    
    df=df.rename(columns={'Unnamed: 0':'User ID'})
        
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    
    common_month=df['Start Time'].dt.month_name().mode()[0]
    n_common_month= max(df['month'].value_counts())
    per_common_month=round(max(df['month'].value_counts(normalize=True))*100,2)

    # TO DO: display the most common day of week
    common_day= df['day_of_week'].mode()[0]
    n_common_day= max(df['day_of_week'].value_counts())
    per_common_day=round(max(df['day_of_week'].value_counts(normalize=True))*100,2)
    
   

    # TO DO: display the most common start hour
    common_hour= int(df['Start Time'].dt.hour.mode())
    n_common_hour= max(df['Start Time'].dt.hour.value_counts())
    per_common_hour= round(max(df['Start Time'].dt.hour.value_counts(normalize=True))*100,2)
    
    result={'Period':['Month', 'Day Week','Hour'],
            'Mode':[common_month,common_day,common_hour],
            'Count':[n_common_month,n_common_day,n_common_hour],
            'Percentage':[per_common_month,per_common_day,per_common_hour]}
    
    res=pd.DataFrame(data=result)
    
    print (tabulate(res,headers='keys', tablefmt='fancy_grid', showindex=False, floatfmt='.1f'))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    
    common_SS = df['Start Station'].mode()[0]
    n_common_SS = max(df['Start Station'].value_counts())
    per_common_SS = round(max(df['Start Station'].value_counts(normalize=True))*100,2)

    # TO DO: display most commonly used end station
    common_ES = df['End Station'].mode()[0]
    n_common_ES = max(df['End Station'].value_counts())
    per_common_ES = round(max(df['End Station'].value_counts(normalize=True))*100,2)

    # TO DO: display most frequent combination of start station and end station trip
    
    common_travel = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
    n_common_travel=max((df['Start Station']+' - '+ df['End Station']).value_counts())
    per_common_travel=round(max((df['Start Station']+' - '+ df['End Station']).value_counts(normalize=True))*100,2)
    
    result={'Metric':['Start Station','End Station','Trip (From-To)'],
        'Most Popular':[common_SS, common_SS,common_travel],
         'Travels':[n_common_SS,n_common_ES, n_common_travel],
         '% of Total Travels':[per_common_SS,per_common_ES,per_common_travel]}
    
    res=pd.DataFrame(data=result)
    
    print (tabulate(res,headers='keys', tablefmt='fancy_grid', showindex=False, floatfmt='.1f'))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, month):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    ttt= str((df['End Time']-df['Start Time']).sum()).split('.')[0]
    print(ttt)
    
    # TO DO: display mean travel time
    mtt= str((df['End Time']-df['Start Time']).mean()).split('.')[0]
    
    print('The total travel time during {} was {}'.format(month,ttt) )
    print('The mean travel time during {} was {}\n'.format(month,mtt) )
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    df2=df['User Type'].value_counts().reset_index(level=0)
    df2.columns=['User Type', 'Nro Users']
    df2['Percentage']= df2['Nro Users']/df2['Nro Users'].sum()*100
    print (tabulate(df2, headers='keys', tablefmt='fancy_grid', showindex=False, floatfmt='.1f'))

    # TO DO: Display counts of gender
    
    if city!='washington':
        df2=df['Gender'].value_counts().reset_index(level=0)
    
        df2.columns=['Gender', 'Gender count']
        df2['Percentage']= df2['Gender count']/df2['Gender count'].sum()*100
        print('-'*15+'Users gender'+'-'*15)
        print (tabulate(df2, headers='keys', tablefmt='fancy_grid', showindex=False, floatfmt='.1f'))
    
        # TO DO: Display earliest, most recent, and most common year of birth
        
        earliest_y= min(df['Birth Year'])
        most_recent_y=max(df['Birth Year'])
        most_common_y=df['Birth Year'].mode()[0]
        
        result={' ':['Year'],
            'Earliest':[earliest_y],
             'Most Recent':[most_recent_y],
             'Most Common':[most_common_y]}
        
        res=pd.DataFrame(data=result)
        print('-'*15+'Birth Year of Users'+'-'*15)
        print (tabulate(res, headers='keys', tablefmt='fancy_grid', showindex=False, floatfmt='.0f'))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        pass

def display_data(df):
    val=True
    count=0
    while val!=False:
        answer=input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        if answer=='yes' or answer=='no':
            if answer== 'yes':
                print(df.iloc[count:count+5,:])
                count+=5
            else:
                break
        else:
            continue

# tst=df.head()        

def main():    
    while True:
        
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df,month)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
