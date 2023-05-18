import azure.functions as func
import io
import logging
from azure.storage.blob import BlobClient, BlobServiceClient
from azure.identity import DefaultAzureCredential

# relative import(s)
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
    incident_data = io.StringIO(inputblob)
    generated_reports = reports.generate_report(incident_data=incident_data)
    logging.info(f"generated reports: {generated_reports}")
    outputblob.set(open(generated_reports[0], 'rb').read())