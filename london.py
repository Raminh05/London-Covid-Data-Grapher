from selenium import webdriver
from selenium.webdriver.chrome.options import Options as options
import time
from dateutil.parser import parse
from csv import reader
import numpy as np
from matplotlib import pyplot

# Parameters for Chrome Driver running in headless mode
chrome_option = options()
chrome_option.add_argument("--headless")

# Pyplot labels
label_x = 'Date (months)'
label_y = 'Cases'

# Variables for CSV file
filename = 'london_covid.csv'
headers = "day, new_cases\n"

def write_header(filename, headers):
    with open(filename, 'w') as f:
        f.write(headers)
        f.close()

def get_data(chrome_option):
    # Start Chrome Webdriver
    PATH = "C:\Program Files (x86)\Webdriver\chromedriver.exe"
    driver = webdriver.Chrome(PATH, options=chrome_option)

    url = 'https://app.powerbi.com/view?r=eyJrIjoiMzE5MzJlOTItOWE2ZS00MDNlLTlkNDEtMTcyYTg5OGFhMTFiIiwidCI6ImRjNTYxMjk1LTdjYTktNDFhOS04M2JmLTUwODM0ZDZhOWQwZiJ9'
    driver.get(url)
    return driver

def parse_case(containers):
    new_cases = containers[24].text # Index 24 in the item-container list is where the new cases data is shown
    print("There are " + new_cases + " new cases of COVID-19 in the Middlesex region since the previous day.")
    return new_cases

def parse_date(containers):
    date = containers[29].text # Index 29 in the item-container list is where the date is shown on the site
    return date

def write_data_to_csv(filename, date, new_cases):
    with open(filename, 'a') as g: # SET THE DANG PERMISSIONS FOR THE WRITE THING AS APPEND NOT WRITE! OR ELSE, THIS WILL OVERWRITE THE HEADERS! Also , this is needed to actually append new case data everyday onto the file rather than overwriting data.
        g.write(date[0] + "," + new_cases + "," + "\n")
        g.close()

def parse_date_from_csv(filename):
    with open(filename, 'r') as f:
        data = list(reader(f))
        dates = [parse(i[0]) for i in data[0::]]
    return dates
   
def parse_case_from_csv(filename):
    with open(filename, 'r') as f:
        data = list(reader(f))
        cases = [i[1] for i in data[0::]]

    numpy_cases = np.array(cases)
    return numpy_cases

def plot_data(label_x, label_y, dates, cases):
    pyplot.bar(dates, cases.astype(int), color='blue')
    pyplot.title('Holy Macaroni - London')
    pyplot.xlabel(label_x)
    pyplot.ylabel(label_y)
    pyplot.show()

def run_program_london():
    driver = get_data(chrome_option)
    
    # Driver finds ALL of the item-containers on the data report and puts it in a list
    containers = driver.find_elements_by_class_name("visual-container-component")

    # Wait 3 seconds for the site to load...
    time.sleep(3)

    # Parsing new case figures and date from the item-container list
    new_cases = parse_case(containers)
    date = parse_date(containers).split()

    # Calling the csv stuff
    write_data_to_csv(filename, date, new_cases)

    # no likey having 99999 chrome tabs open after scrape is done
    driver.quit()

    # parsing the dates and cases for pyplot to understand
    dates = parse_date_from_csv(filename)
    cases = parse_case_from_csv(filename)

    # Actually plotting everything
    plot_data(label_x, label_y, dates, cases)
    


## Print figures to console (uncomment if need be)
# print("There are " + new_cases + " new cases of COVID-19 in the Middlesex region since the previous day.")
# print("Data updated on " + date[0])

