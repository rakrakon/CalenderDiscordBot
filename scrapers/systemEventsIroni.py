import scrapy
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from scrapy import FormRequest
import pandas as pd

#TODO: Direct path to correct class
class EventsSpider(scrapy.Spider):
    name = 'events'
    start_urls = ['https://ironih.iscool.co.il/default.aspx']


    def parse(self, response):
        data = {
            '__EVENTTARGET' : 'dnn$ctr3413$TimeTableView$btnEvents',
           'dnn$ctr3413$TimeTableView$ClassesList': '21',
            'dnn$ctr3413$TimeTableView$ControlId': '5',
        }
        yield FormRequest.from_response(response,formdata=data, callback=self.parse_table)

    def parse_table(self, response):
        dfs = pd.read_html(response.text)
        try:
            df2 = pd.read_csv('data\eventsIroni.csv')
        except Exception:
            df2 = pd.DataFrame()

        def compare_dataframes(df1, df2): #! Function to compare the dataframes one sided
            #% Find rows that are in df1 but not in df2
            df_diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
            df_diff = df_diff[df_diff.isin(df1)].dropna(how='all')

            return df_diff

        for i,df in enumerate(dfs):
            if i == 11:
                #TODO: add if statement in line 37 to check if it is משיעור or just שיעור
                event_info_df = pd.DataFrame(df[0].values, columns=['event_info'])
                df = pd.concat([df, event_info_df], axis=1)
                df[['date', 'description']] = df['event_info'].str.split(',', expand=True)
                df[['event', 'time']] = df['description'].str.split('משיעור', expand=True)
                df[['time', 'classes']] = df['time'].str.split('לכיתות', expand=True)
                df.drop(['event_info', 'description', 0], axis=1, inplace=True)
                
                try:
                    df_diff = compare_dataframes(df, df2)
                    df_diff.to_csv('data\eventsDiffIroni.csv')
                    print(df_diff)
                except Exception:
                    print(Exception)
                df.to_csv('data\eventsIroni.csv', index=False)