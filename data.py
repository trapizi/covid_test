import urllib
import requests
from datetime import date
from codecs import iterdecode
from contextlib import closing
import os
import csv
import pandas as pd
import json

CSV_URL = 'https://data.nsw.gov.au/data/dataset/60616720-3c60-4c52-b499-751f31e3b132/resource/945c6204-272a-4cad-8e33-dde791f5059a/download/pcr_testing_table1_location.csv'
cwd = os.path.dirname(os.path.realpath(__file__))
file_template = "processed-data-{}".format(date.today())
current_date_csv_file = file_template + ".csv"
current_date_json_file = file_template + ".json"


def get_data():
    #process_csv()
    csv_to_json()
    return get_json_data_by_lga()

def request_data():
    csv_file = open(current_date_csv_file, 'wb')
    req = requests.get(CSV_URL)
    url_content = req.content

    csv_file.write(url_content)
    csv_file.close()
    # with closing(requests.get(CSV_URL, stream=True)) as r:
    #     r = iterdecode(csv.reader(r.iter_lines(), 'utf-8'), 
    #                         delimiter=',', 
    #                         quotechar='"')


    
def process_csv():

    #Filter out data that have empty LGA code or name
    f = current_date_csv_file
    df = pd.read_csv(f)

    vector_not_null = df['lga_code19'].notnull()
    df_not_null = df[vector_not_null]

    df_not_null.to_csv(current_date_csv_file, index=None, header=True, encoding='utf-8-sig')

def csv_to_json():
    data = []
    csv_file = current_date_csv_file

     #read csv file
    with open(csv_file, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 

        for row in csvReader: 
            data.append(row)
  
    with open(current_date_json_file, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(data, indent=4)
        jsonf.write(jsonString)
          
# Return JSON file grouped by LGA code and name         
def get_json_data_by_lga():
    """
    {
        "lga_code": 14170,
        "lga_name": "Inner West (A) example"
        "total_count": 3,
        "greatest": {
            "count": 2,
            "date": "02-May-2021"
        },
        "least": {
            "count": 1,
            "date": "01-May-2021"
        }
    },
    """
    data = []
    json_file = open(current_date_json_file,"r")
    json_object = json.load(json_file)
    json_file.close()
    
    not_found = True
    for item in json_object:
        for lga in data:
            formatted_lga_code19 = str(int(float(item["lga_code19"])))
            formatted_lga_code_json = str(int(float(lga['lga_code'])))
            if formatted_lga_code19 == formatted_lga_code_json:
                not_found = False
                lga['total_count'] +=1
        if not_found:
                data.append({
                    # Convert string to float then to int to round up the lga code then back
                    "lga_code": str(int(float(item["lga_code19"]))),
                    "lga_name": item["lga_name19"],
                    "total_count" : 1,
                    "greatest": {
                        "count": 0,
                        "date": ""
                    },
                    "least" : {
                        "count": 0,
                        "date": ""
                    }
                })

    json_output = json.dumps(data, indent=4)
    with open("output.json", 'w') as output:
        json.dump(data, output)
    return json_output

if __name__ == "__main__":
    get_data()