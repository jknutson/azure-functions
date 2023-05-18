import matplotlib
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

# agg is a backend that is non-interactive; it can only write to files
matplotlib.use('agg')

# incident_data should be an InputStream (e.g. from Azure BlobStorageTrigger), or path to a CSV file
def generate_report(incident_data):
    """Generate report(s) from incident data

    Parameters:
    incident_data (io.StringIO, str): StringIO or path to CSV file

    Returns:
    list of str: List of paths to generated report(s)
    """
    use_columns = ['IncidentNumber', 'IncidentDate', 'IncidentTime', 'IncidentType']
    df = pd.read_csv(incident_data, usecols=use_columns,
                     parse_dates={'IncidentDateTime':['IncidentDate', 'IncidentTime']},
                     date_format='%d/%m/%Y %H:%M:%S')
    df['IncidentCode'] = df['IncidentType'].str.split().str[0]
    df.dropna(subset=['IncidentType'], inplace=True)
    df['IncidentSeries'] = (df['IncidentCode'].astype(int) / 100).astype(int) * 100
    df['IncidentCategory'] = df['IncidentSeries'].map(INCIDENT_CODES)

    report_path = 'incidents.pdf'
    fig=df['IncidentCategory'].value_counts().plot(kind='pie').get_figure()
    fig.savefig(report_path)

    return [report_path]

if __name__ == "__main__":
    import sys
    incident_csv = '/Users/john.knutson/Downloads/incidents.csv'
    if len(sys.argv) > 1:
        incident_csv = sys.argv[1]
    generate_report(incident_data=incident_csv)
