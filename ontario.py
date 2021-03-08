import numpy as np
from csv import reader
import requests
from matplotlib import pyplot
from dateutil import parser

ontario_csv_url = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv'

# Pyplot labels
label_x = 'Date (months)'
label_y = 'Cases'

def get_write_data(ontario_csv_url):
    r = requests.get(ontario_csv_url)
    with open("ontario_covid.csv", 'wb') as f:
        f.write(r.content)
        f.close()

def dates():
    with open("ontario_covid.csv", 'r') as e:
        data = list(reader(e))
        dates = [parser.parse(i[0]) for i in data[7::]]
        return dates
    
def plot_cases_ontario(label_x, label_y):
    with open("ontario_covid.csv", 'r') as f:
        data = list(reader(f))
        cases = [i[35] for i in data[7::]]
        
    # converting to numpy
    numpy_cases = np.array(cases)
    # Print whole case array to console
    print(numpy_cases)
    
    date = dates()

    pyplot.bar(date, numpy_cases.astype(int), color='green')

    pyplot.title('Holy Macaroni - Ontario')
    pyplot.xlabel(label_x)
    pyplot.ylabel(label_y)
    pyplot.show()

def run_program_ontario():
    get_write_data(ontario_csv_url)
    dates()
    plot_cases_ontario(label_x, label_y)



