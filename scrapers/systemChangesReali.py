import re
import scrapy
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from scrapy import FormRequest
import pandas as pd

class ChangesSpider(scrapy.Spider):
    name = 'changes'
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
        try:
            df2 = pd.read_csv('changesReali.csv')
        except Exception:
            df2 = pd.DataFrame()

        outputDF = pd.DataFrame(columns=['Lesson number', 'Action', 'Teacher', 'Date'])
        pattern = r"(?:.*-){3}.*" #* Pattern for the third syntax

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
        
        def parseSyntaxOne(string):
            #? Split the string by comma
            split_list = string.split(',')

            #* Extracting the values
            lesson_number = split_list[1].strip()
            action = ' '.join(split_list[3].strip().split(' ')[:2])
            teacher = ' '.join(split_list[3].strip().split(' ')[2:])
            date = split_list[0].strip()
            
            #? Return the extracted values as a dictionary
            return {
                'Lesson Number': lesson_number,
                'Action': action,
                'Teacher': teacher,
                'Date': date
            }

        def parseSyntaxTwo(string):
                #? Split the string by comma
            split_list = string.split(',')

            #* Extracting the values
            lesson_number = split_list[1].strip()
            action = ' '.join(split_list[2].strip().split(' ')[:2])
            teacher = ' '.join(split_list[2].strip().split(' ')[3:])
            date = split_list[0].strip()
            
            #? Return the extracted values as a dictionary
            return {
                'Lesson Number': lesson_number,
                'Action': action,
                'Teacher': teacher,
                'Date': date
            }

        def parseSyntaxThree(string):
            #? Split the string by comma
            split_list = string.split(',')

            #* Extracting the values
            lesson_number = split_list[1].strip()
            action = split_list[3].strip()
            teacher = split_list[2].strip()
            date = split_list[0].strip()

            #? Return the extracted values as a dictionary
            return {
                'Lesson Number': lesson_number,
                'Action': action,
                'Teacher': teacher,
                'Date': date
            }

        for i,df in enumerate(dfs):
            if i == 11:
                lesson_info_df = pd.DataFrame(df[0].values, columns=['lesson_info'])

                df = pd.concat([df, lesson_info_df], axis=1)
                for text in df['lesson_info']:
                    #!Syntax Filtering
                    match = re.search(pattern, text)
                    
                    if ':' in text:
                        result = parseSyntaxOne(text)
                        df_dictionary = pd.DataFrame([result])
                        outputDF = pd.concat([outputDF, df_dictionary], ignore_index=True)
                    elif "..." in text or match:
                        result = parseSyntaxTwo(text)
                        df_dictionary = pd.DataFrame([result])
                        outputDF = pd.concat([outputDF, df_dictionary], ignore_index=True)
                    else:
                        result = parseSyntaxThree(text)
                        df_dictionary = pd.DataFrame([result])
                        outputDF = pd.concat([outputDF, df_dictionary], ignore_index=True)

                outputDF = outputDF.drop('Lesson number', axis=1)

                #! Check for differances with the exsisting one
                try:
                    df_diff = compare_dataframes(outputDF, df2)
                    df_diff.to_csv('changesDiffReali.csv', index=False)
                    print(df_diff)
                except Exception:
                    print(f'df_diff: {df_diff}')
                outputDF.to_csv('changesReali.csv', index=False) 
