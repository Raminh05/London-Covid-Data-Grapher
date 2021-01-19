import requests
from bs4 import BeautifulSoup as soup
from csv import reader
from csv import writer
from matplotlib import pyplot
from dateutil import parser
import numpy as np


csv_url = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv'



def get_write_data():
    r = requests.get(csv_url)
    with open("ontario_covid.csv", 'wb') as f:
        f.write(r.content)
        f.close()
        
def plot_cases():
    with open("ontario_covid.csv", 'r') as e:
        data = list(reader(e))
        cases = [i[16] for i in data[7::]]
        
    # converting to numpy 
    numpy_cases = np.array(cases)
    return numpy_cases
   

def plot_dates():
    with open("ontario_covid.csv", 'r') as e:
        data = list(reader(e))
        dates = [parser.parse(i[0]) for i in data[7::]]
        return dates
    
    
    

u_choice = input("What do you want to do?\n (a) Just update and write data to the csv\n (b) Update data AND show graph\n")

if u_choice == 'a':
    get_write_data()
    print("Updated csv!")

elif u_choice == 'b':
    get_write_data()

    dates = plot_dates()
    numpy_cases = plot_cases()

    pyplot.bar(dates, numpy_cases.astype(int))

    pyplot.title('Holy macaroni')
    pyplot.xlabel('Date (in months)')
    pyplot.ylabel('Case numbers')
    pyplot.show()

    print("Finished!")

else:
    print("Invalid choice!")






   

