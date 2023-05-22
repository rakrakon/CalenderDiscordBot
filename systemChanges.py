import scrapy
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from scrapy import FormRequest
import pandas as pd

class PricesSpider(scrapy.Spider):
    name = 'prices'
    start_urls = ['https://beitbiram.iscool.co.il/default.aspx']

    def parse(self, response):
        data = {
            '__EVENTTARGET': 'dnn$ctr7126$TimeTableView$btnChanges',
            'dnn$ctr7126$TimeTableView$ClassesListMobile': '174',
            'dnn$ctr7126$TimeTableView$ControlId': '2',
        }
        yield FormRequest.from_response(response,formdata=data, callback=self.parse_table)

    def parse_table(self, response):
        dfs = pd.read_html(response.text)
        df2 = pd.read_csv('changes.csv')

        def split_string(string):
            #? Split the string by comma
            split_list = string.split(',')

            #! Extracting the values
            lesson_number = split_list[1].strip() #!Works
            action = split_list[3].strip() #! Works
            teacher = split_list[2].strip() #!Works
            date = split_list[0].strip()
            #? Return the extracted values as a dictionary
            return {
                'Lesson Number': lesson_number,
                'Action': action,
                'Teacher': teacher,
                'Date': date
            }

        def compare_dataframes(df1, df2): #! Function to compare the dataframes one sided
            """Compares two dataframes and returns a dataframe showing the rows that are in df1 but not in df2"""
            #! Find rows that are in df1 but not in df2
            df_diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
            df_diff = df_diff[df_diff.isin(df1)].dropna(how='all')

            return df_diff

        for i,df in enumerate(dfs):
            if i == 11:
                lesson_info_df = pd.DataFrame(df[0].values, columns=['lesson_info'])

                df = pd.concat([df, lesson_info_df], axis=1)
                df_split = df['lesson_info'].apply(split_string).apply(pd.Series)

                # Concatenate the split values with the original DataFrame
                df_final = pd.concat([df, df_split], axis=1)
                df_final.drop(['lesson_info',0], axis=1, inplace=True)

                #! Check for differances with the exsisting one
                try:
                    df_diff = compare_dataframes(df_final, df2)
                    df_diff.to_csv('changesDiff.csv', index=False)
                    print(df_diff)
                except Exception:
                    print(f'df_diff: {df_diff}')
                df_final.to_csv('changes.csv', index=False) 
