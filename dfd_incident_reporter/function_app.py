import azure.functions as func
# import csv
import io
import logging
import matplotlib.pyplot as plt
import pandas as pd
from azure.storage.blob import BlobClient, BlobServiceClient
from azure.identity import DefaultAzureCredential

import reports

app = func.FunctionApp()

@app.function_name(name="BlobTrigger1")
@app.blob_trigger(arg_name="myblob",
                  path="dfd-uploads/incidents.csv",
                  connection="")
@app.blob_input(arg_name="inputblob",
                path="dfd-uploads/incidents.csv",
                connection="")
@app.blob_output(arg_name="outputblob",
                path="dfd-reports/incidents.pdf",
                connection="")
def test_function(myblob: func.InputStream, inputblob: str, outputblob: func.Out[str]):
    generated_reports = reports.generate_report(incident_data=myblob)
    logging.info(f"generated reports: {generated_reports}")
    outputblob.set(generated_reports[0])