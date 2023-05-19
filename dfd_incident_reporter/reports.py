import matplotlib
import pandas as pd
from matplotlib.ticker import NullFormatter
from matplotlib.dates import MonthLocator, DateFormatter

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
FIGSIZE=(11,8.5)

# agg is a backend that is non-interactive; it can only write to files
matplotlib.use('agg')

def generate_reports(incident_data):
    """Generate report(s) from incident data

    Parameters:
    incident_data (io.StringIO, str): StringIO or path to CSV file

    Returns:
    list of str: List of paths to generated report(s)
    """

    use_columns = ['IncidentNumber', 'IncidentDate', 'IncidentTime', 'IncidentType']
    df = pd.read_csv(incident_data, usecols=use_columns,
                     parse_dates={'IncidentDateTime':['IncidentDate', 'IncidentTime']},
                     date_format='%m/%d/%Y %H:%M:%S')
    df['IncidentCode'] = df['IncidentType'].str.split().str[0]
    df.dropna(subset=['IncidentType'], inplace=True)
    df['IncidentSeries'] = (df['IncidentCode'].astype(int) / 100).astype(int) * 100
    df['IncidentCategory'] = df['IncidentSeries'].map(INCIDENT_CODES)

    reports = []
    reports.extend(generate_summary_report(df))
    reports.extend(generate_monthly_report(df))

    return reports

# incident_data should be an InputStream (e.g. from Azure BlobStorageTrigger), or path to a CSV file
def generate_summary_report(df):
    """Generate report(s) from dataframe

    Parameters:
    pandas.DataFrame: dataframe with incident data

    Returns:
    list of str: List of paths to generated report(s)
    """

    report_path = 'incidents.pdf'
    fig=df['IncidentCategory'].value_counts().plot(kind='pie').get_figure()
    fig.savefig(report_path)
    return reports

# incident_data should be an InputStream (e.g. from Azure BlobStorageTrigger), or path to a CSV file
def generate_summary_report(df):
    """Generate report(s) from dataframe

    Parameters:
    pandas.DataFrame: dataframe with incident data

    Returns:
    list of str: List of paths to generated report(s)
    """

    summary_report_path = 'incidents.pdf'
    plot=df['IncidentCategory'].value_counts().plot(kind='pie', figsize=FIGSIZE)
    plot.set(title='Dayton Fire Department - Calls Summary')
    fig=plot.get_figure()
    fig.savefig(summary_report_path)
    return [summary_report_path]

def generate_monthly_report(df):
    """Generate monthly report(s) from datafram

    Parameters:
    pandas.DataFrame: dataframe with incident data

    Returns:
    list of str: List of paths to generated report(s)
    """

    month_report_path = 'incidents_month.pdf'
    dg = df.groupby(df.IncidentDateTime.dt.month)['IncidentCategory'].value_counts().unstack().fillna(0)
    # print(dg.head())
    # print(dg.info())
    plot = dg.plot.bar(stacked=True, figsize=FIGSIZE)
    plot.set(title='Dayton Fire Department - Calls by Month',
             xlabel='Month', ylabel='Number of Calls')
    # plot.xaxis.set_major_locator(MonthLocator())
    # plot.xaxis.set_major_formatter(DateFormatter('%b'))
    fig=plot.get_figure()
    fig.savefig(month_report_path)
    return [month_report_path]

def generate_monthly_report(df):
    """Generate monthly report(s) from datafram

    Parameters:
    pandas.DataFrame: dataframe with incident data

    Returns:
    list of str: List of paths to generated report(s)
    """

    month_report_path = 'incidents_month.pdf'
    plot=df.groupby(df.IncidentDateTime.dt.month)['IncidentCategory'].value_counts().unstack().plot.bar(stacked=True)
    # TODO: figure out why this only labels "Jan"
    # plot.xaxis.set_major_locator(MonthLocator())
    # plot.xaxis.set_major_formatter(DateFormatter('%b'))
    fig=plot.get_figure()
    fig.savefig(month_report_path)

    return [month_report_path]

if __name__ == "__main__":
    import sys
    incident_csv = '/Users/john.knutson/Downloads/incidents_2022.csv'
    if len(sys.argv) > 1:
        incident_csv = sys.argv[1]
    reports = generate_reports(incident_data=incident_csv)
    print(f"reports generated: {reports}")
