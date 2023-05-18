import azure.functions as func
# import csv
import io
import logging
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
    blob_data = io.StringIO(inputblob)
    df = pd.read_csv(blob_data)
    drop_columns = [
        'totalRows','Address','Latitude','Longitude',
        'Unnamed 18','Unnamed 19','Unnamed 20',
        'Unnamed 21','Unnamed 22','Unnamed 23', 'Unnamed: 24'
    ]
    sanitized_df = df.drop(labels=drop_columns, axis='columns')
    logging.info(df)