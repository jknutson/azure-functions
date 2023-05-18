import azure.functions as func
# import csv
import io
import logging
import matplotlib.pyplot as plt
import pandas as pd
from azure.storage.blob import BlobClient, BlobServiceClient
from azure.identity import DefaultAzureCredential

app = func.FunctionApp()

@app.function_name(name="BlobTrigger1")
@app.blob_trigger(arg_name="myblob",
                  path="dfd-uploads/incidents.csv",
                  connection="")
@app.blob_input(arg_name="inputblob",
                path="dfd-uploads/incidents.csv",
                connection="")
def test_function(myblob: func.InputStream, inputblob: str):
    # TODO: use a more efficient approach here, i.e. iterate/streaming
    # reader = csv.reader(inputblob, delimiter=',', quotechar='"')
    # reader = csv.reader(inputblob, skipinitialspace=True, quoting=csv.QUOTE_ALL)
    # for row in reader:
    #     logging.info(', '.join(row))
    column_converters = {
        ''
    }
    incident_codes = {
        100: 'Fire Group.',
        200: 'Rupture / Explosion.',
        300: 'Rescue & Emergency Medical Service (EMS)',
        400: 'Hazardous Condition (no Fire)',
        500: 'Service Call.',
        600: 'Good Intent.',
        700: 'False Alarm & False Call.',
        800: 'Severe Weather & Natural Disaster Group.'
    }
    blob_data = io.StringIO(inputblob)
    use_columns = ['IncidentNumber', 'IncidentDate', 'IncidentTime', 'IncidentType']
    df = pd.read_csv(blob_data, usecols=use_columns,
                     parse_dates={'IncidentDateTime':['IncidentDate', 'IncidentTime']},
                     date_format='%d/%m/%Y %H:%M:%S')
    df['IncidentCode'] = df['IncidentType'].str.split().str[0]
    df.dropna(subset=['IncidentType'],inplace=True)
    df['IncidentSeries'] = (df['IncidentCode'].astype(int) / 100).astype(int) * 100
    df['IncidentCategory'] = df['IncidentSeries'].map(incident_codes)
    # This is returns sum of unique grouped values, not sure how to pass to matplotlib though
    df['IncidentCategory'].value_counts()
    
    # sanitized_df['IncidentCode'] = sanitized_df['IncidentCode'].astype(int)
    # sanitized_df['IncidentCodeSeries'] = int(math.floor(sanitized_df['IncidentCode'] / 100.0) * 100)
    logging.info(df)