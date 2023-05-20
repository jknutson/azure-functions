import calendar
import matplotlib
import pandas as pd

# agg is a backend that is non-interactive; it can only write to files
# matplotlib.use('agg')

class Reporter:
    FIGSIZE=(11,8.5)
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

    def __init__(self, incident_data):
        self.incident_data = incident_data
        use_columns = ['IncidentNumber', 'IncidentDate', 'IncidentTime', 'IncidentType']
        df = pd.read_csv(self.incident_data, usecols=use_columns,
                        parse_dates={'IncidentDateTime':['IncidentDate', 'IncidentTime']},
                        date_format='%m/%d/%Y %H:%M:%S')
        df['IncidentCode'] = df['IncidentType'].str.split().str[0]
        df.dropna(subset=['IncidentType'], inplace=True)
        df['IncidentSeries'] = (df['IncidentCode'].astype(int) / 100).astype(int) * 100
        df['IncidentCategory'] = df['IncidentSeries'].map(self.INCIDENT_CODES)
        self.df = df


    def generate_reports(self):
        """Generate report(s) from incident data

        Parameters:
        incident_data (io.StringIO, str): StringIO or path to CSV file

        Returns:
        list of str: List of paths to generated report(s)
        """

        reports = []
        reports.extend(self.generate_summary_report())
        reports.extend(self.generate_monthly_report())

        return reports

    def generate_sanitized_csv(self, outfile):
        self.df.to_csv(outfile)
        return outfile

    def generate_summary_report(self):
        """Generate summary report(s) from dataframe

        Parameters:
        pandas.DataFrame: dataframe with incident data

        Returns:
        list of str: List of paths to generated report(s)
        """

        summary_report_path = 'incidents_summary.png'
        plot=self.df['IncidentCategory'].value_counts().plot(kind='pie', figsize=self.FIGSIZE)
        plot.set(title='Dayton Fire Department - Calls Summary')
        fig=plot.get_figure()
        fig.savefig(summary_report_path)
        return [summary_report_path]

    def generate_monthly_report(self):
        """Generate monthly report(s) from dataframe

        Parameters:
        pandas.DataFrame: dataframe with incident data

        Returns:
        list of str: List of paths to generated report(s)
        """

        month_report_path = 'incidents_month.png'
        dg = self.df.groupby(self.df.IncidentDateTime.dt.month)['IncidentCategory'].value_counts().unstack().fillna(0)
        dg.rename(index=lambda x: calendar.month_abbr[x], inplace=True)
        plot = dg.plot.bar(stacked=True, figsize=self.FIGSIZE)
        plot.set(title='Dayton Fire Department - Calls by Month',
                xlabel='Month', ylabel='Number of Calls')
        fig=plot.get_figure()
        fig.savefig(month_report_path)
        return [month_report_path]

if __name__ == "__main__":
    import sys
    incident_csv = '/Users/john.knutson/Downloads/incidents_2021.csv'
    if len(sys.argv) > 1:
        incident_csv = sys.argv[1]
    # if len(sys.argv) > 2:
    #     output_csv = sys.argv[2]
    #     reporter.generate_sanitized_csv(output_csv)
    reporter = Reporter(incident_data=incident_csv)
    reports = reporter.generate_reports()
    print(f"reports generated: {reports}")
