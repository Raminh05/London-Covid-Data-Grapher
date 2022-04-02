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
def ontario_cases(ontario_csv_url):
    try:
        #print("Downloading Ontario COVID CSV")
        wget.download(ontario_csv_url, "ontario_covid.csv")
        #print("\nSucessfully downloaded Ontario CSV")

        # Extracts data from csv
        with open("ontario_covid.csv", 'r') as f:
            data = list(reader(f))
            count = [i[35] for i in data[7::]][-1]
            date = [i[0] for i in data[7::]][-1]
            f.close()
            print("Sucessfully parsed Ontario data!")
            return count, date

    except:
        print("Could not download Ontario CSV file")
        count = 'x'
        date = 'x'
        return count, date

# -- Fetches status data from another Ontario CSV -- #
def ontario_status(status_csv_url):
    try:
        #print("Downloading Ontario status CSV")
        wget.download(status_csv_url, "ontario_status.csv")
        #print("\nSucessfully downloaded status CSV")

        with open("ontario_status.csv", 'r') as e:
            data = list(reader(e))
            hospitalizations = [i[13] for i in data[60::]][-1]
            icu_admissions = [i[14] for i in data[60::]][-1]
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
        #print("Downloading MLHU XLSX")
        wget.download(excel_url, "mlhu.xlsx")
        print("\nSucessfully downloaded MLHU XLSX")
        
        # Attempts to parse report from MLHU
        try:
            #print("Parsing MLHU data from XLSX")
            wb = load_workbook("mlhu.xlsx")
            worksheet = wb["Daily status"]
            new_cases = worksheet["B14"].value
            os.remove("mlhu.xlsx")
            #print("Sucessfully parsed MLHU data!")
        except:
            print("Could not parse MLHU data from XLSX")
            new_cases = "x"

    except:
        print("MLHU did not update XLSX for today yet!")
        new_cases = "x"

    return new_cases

# -- Creates csv, writes case data to it -- #
def create_write_csv(filename, data, ontario_count, hospitalizations):

    with open(filename, 'a') as f:
        f.write(str(ontario_count[1]) + "," + str(data) + "," + str(ontario_count[0]) + "," + str(hospitalizations) + "," + "\n")
        f.close()
    print("Finished writing data onto main csv.")

# -- Main -- #
def main():

    # Variable declaration
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    excel_url = "https://www.healthunit.com/uploads/summary_of_covid-19_cases_in_middlesex-london_" + date + ".xlsx"
    csv_urls = ['https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv', 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv']

    # -- Debugging Section -- #

    # print(excel_url)
    # headers = "date, mlhu, ontario\n"
    # write_header(filename, headers)

    # -- Debugging section ends -- #

    with concurrent.futures.ProcessPoolExecutor() as executor:
        f1 = executor.submit(ontario_cases, csv_urls[0])
        f2 = executor.submit(ontario_status, csv_urls[1])
        f3 = executor.submit(london, excel_url)

        ontario_and_date = f1.result()
        status_data = f2.result()
        mlhu = f3.result()

        # If london() cannot parse data from mlhu
        if mlhu == 'x':
            print("Falling back to Ontario data for MLHU")
            with open("ontario_covid.csv", 'r') as f:
                data = list(reader(f))
                mlhu = [i[16] for i in data[7::]][-1]
                f.close()
    
    # ontario_and_date = ontario()
    # mlhu = london(excel_url)
    # Test

    # Console output
    print("\nThere are " + str(mlhu) + " new cases in the Middlesex-London region today.")
    print("There are " + str(ontario_and_date[0]) + " new cases in Ontario today.")

    print("\nThere are " + str(status_data[0]) + " people hospitalized with COVID-19")
    print("There are " + str(status_data[1]) + " people in the ICU with COVID-19")

    print("\nData retrieved on: " + str(ontario_and_date[1]))

    create_write_csv("london_covid.csv", mlhu, ontario_and_date, status_data[0])
    os.remove("ontario_covid.csv")
    os.remove("ontario_status.csv")

if __name__ == '__main__':
    main()
    

























