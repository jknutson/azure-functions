import io
import pandas as pd

INCIDENT_CODES = {
    100: 'Fire Group.',
    200: 'Rupture / Explosion.',
    300: 'Rescue & Emergency Medical Service (EMS)',
    400: 'Hazardous Condition (no Fire)',
    500: 'Service Call.',
    600: 'Good Intent.',
    700: 'False Alarm & False Call.',
    800: 'Severe Weather & Natural Disaster Group.'
}

# incident_data should be an InputStream (e.g. from Azure BlobStorageTrigger), or path to a CSV file
def generate_report(incident_data):
    """Generate report(s) from incident data

    Parameters:
    incident_data (azure.functions.InputStream, str): Azure Functions InputStream or path to CSV file

    Returns:
    list of str: List of paths to generated report(s)
    """
    if type(incident_data) != str:
        blob_data = io.StringIO(incident_data)
    else:
        blob_data = incident_data
    use_columns = ['IncidentNumber', 'IncidentDate', 'IncidentTime', 'IncidentType']
    df = pd.read_csv(blob_data, usecols=use_columns,
                     parse_dates={'IncidentDateTime':['IncidentDate', 'IncidentTime']},
                     date_format='%d/%m/%Y %H:%M:%S')
    df['IncidentCode'] = df['IncidentType'].str.split().str[0]
    df.dropna(subset=['IncidentType'], inplace=True)
    df['IncidentSeries'] = (df['IncidentCode'].astype(int) / 100).astype(int) * 100
    df['IncidentCategory'] = df['IncidentSeries'].map(INCIDENT_CODES)

    fig=df['IncidentCategory'].value_counts().plot(kind='pie').get_figure()
    fig.savefig('fig.png')

if __name__ == "__main__":
    import sys
    incident_csv = '/Users/john.knutson/Downloads/incidents.csv'
    if len(sys.argv) > 1:
        incident_csv = sys.argv[1]
    generate_report(incident_data=incident_csv)
