# Imports
import concurrent.futures
from openpyxl import load_workbook
from datetime import datetime
import wget
from csv import reader 
import os

# -- Writes csv headers. Add to main() if need be. #
def write_header(filename, headers):

    print("Writing headers...")
    with open(filename, 'w') as f:
        f.write(headers)
        f.close()

# -- Fetches data from Ontario csv. -- #
def case_figures(ontario_csv_url):
    
    try:
        wget.download(ontario_csv_url, "ontario_covid.csv")

        # Extracts data from csv
        with open("ontario_covid.csv", 'r') as f:
            data = list(reader(f))
            count = data[-1][-1]
            date = data[-1][0]
            mlhu = data[-1][16]
            f.close()
            print("Sucessfully parsed Ontario data!")
            return count, date, mlhu

    except:
        print("Could not download Ontario CSV file")
        count = 'x'
        date = 'x'
        mlhu = 'x'
        return count, date, mlhu

# -- Fetches status data from another Ontario CSV -- #
def ontario_status(status_csv_url):
    try:
        wget.download(status_csv_url, "ontario_status.csv")

        with open("ontario_status.csv", 'r') as e:
            data = list(reader(e))
            hospitalizations = data[-1][13]
            icu_admissions = data[-1][14]
            e.close()
            print("Parsed status data!")

    except:
        print("Something went wrong with parsing the status CSV")
        hospitalizations = 'x'
        icu_admissions = 'x'
    
    return hospitalizations, icu_admissions
    
# -- Fetches and parses excel file from MLHU -- #
def london(excel_url):

    # Attempts to download report from MLHU
    try:
        wget.download(excel_url, "mlhu.xlsx")
        print("\nSucessfully downloaded MLHU XLSX")
        
        # Attempts to parse report from MLHU
        try:
            wb = load_workbook("mlhu.xlsx")
            worksheet = wb["Daily status"]
            new_cases = worksheet["B14"].value
            os.remove("mlhu.xlsx")
        except:
            print("Could not parse MLHU data from XLSX")
            new_cases = "x"

    except:
        print("MLHU did not update XLSX for today yet!")
        new_cases = "x"

    return new_cases

# -- Creates csv, writes case data to it -- #
def create_write_csv(filename, main_case_data, hospitalizations):

    with open(filename, 'a') as f:
        f.write(str(main_case_data[1]) + "," + str(main_case_data[2]) + "," + str(main_case_data[0]) + "," + str(hospitalizations) + "," + "\n")
        f.close()
    print("Finished writing data onto main csv.")

# -- Main -- #
def main():

    # Variable declaration
    csv_urls = ['https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv', 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv']

    with concurrent.futures.ProcessPoolExecutor() as executor:
        f1 = executor.submit(case_figures, csv_urls[0])
        f2 = executor.submit(ontario_status, csv_urls[1])

        case_data = f1.result()
        status_data = f2.result()
    
    # Console output
    print("\nThere are " + str(case_data[2]) + " new cases in the Middlesex-London region today.")
    print("There are " + str(case_data[0]) + " new cases in Ontario today.")

    print("\nThere are " + str(status_data[0]) + " people hospitalized with COVID-19")
    print("There are " + str(status_data[1]) + " people in the ICU with COVID-19")

    print("\nData retrieved on: " + str(case_data[1]))

    create_write_csv("london_covid.csv", case_data, status_data[0])
    os.remove("ontario_covid.csv")
    os.remove("ontario_status.csv")

if __name__ == '__main__':
    main()
