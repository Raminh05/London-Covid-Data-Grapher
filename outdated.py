import requests
from csv import reader
from csv import writer
from matplotlib import pyplot
from dateutil import parser
import numpy as np


csv_url = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv'


# Fetches data from Ontario gov't servers -> Writes it into a CSV file.
def get_write_data():
    r = requests.get(csv_url)
    with open("ontario_covid.csv", 'wb') as f:
        f.write(r.content)
        f.close()

# Getting London case data from 'Q' Column in the CSV file. Runs through numpy to parse it so that the graph can read it as an integer (seen below).
def plot_cases_london():
    with open("ontario_covid.csv", 'r') as f:
        data = list(reader(f))
        cases = [i[16] for i in data[7::]]
        
    # converting to numpy 
    numpy_cases = np.array(cases)
    return numpy_cases

def plot_cases_ontario():
    with open("ontario_covid.csv", 'r') as f:
        data = list(reader(f))
        cases = [i[35] for i in data[7::]]
        
    # converting to numpy
    numpy_cases = np.array(cases)
    return numpy_cases

   
def plot_dates():
    with open("ontario_covid.csv", 'r') as e:
        data = list(reader(e))
        dates = [parser.parse(i[0]) for i in data[7::]]
        return dates
    
def get_choice():    
    u_choice = input("What do you want to do?\n (a) Just update and write data to the csv\n (b) Update data AND graph London cases\n (c) Update data AND graph Ontario cases\n")

    if u_choice == 'a':
        get_write_data()
        print("Updated csv!")

    elif u_choice == 'b':
        get_write_data()

        dates = plot_dates()
        numpy_cases = plot_cases_london()
    
        print(numpy_cases)

        pyplot.bar(dates, numpy_cases.astype(float), color='blue') # Modified from pyplot.bar(dates, numpy_cases.astype(int)) to this because the Ontario gov't began providing London numbers in floats. 

        pyplot.title('Holy macaroni - London')
        pyplot.xlabel('Date (in months)')
        pyplot.ylabel('Case numbers')
        pyplot.show()

    elif u_choice == 'c':
        get_write_data()

        dates = plot_dates()
        numpy_cases = plot_cases_ontario()

        print(numpy_cases)

        pyplot.bar(dates, numpy_cases.astype(int), color='green')

        pyplot.title('Holy macaroni - Ontario')
        pyplot.xlabel('Date (in months)')
        pyplot.ylabel('Case numbers')
        pyplot.show()

    else:
        print("Invalid choice!")
        get_choice() # Added so that if the user chooses an invalid option, (s)he will get sent back to the questions again to retry.

get_choice()






   

