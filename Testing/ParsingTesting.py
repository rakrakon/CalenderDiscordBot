import pandas as pd
import re

#TODO: Implement this method in the systemChanges.py file

data = pd.read_csv('Test.csv') #!Read the test data
df = pd.DataFrame(data) #? Make it a pandas DataFrame
outputDF = pd.DataFrame(columns=['Lesson number', 'Action', 'Teacher', 'Date'])
pattern = r"(?:.*-){3}.*" #* Pattern for the third syntax

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
outputDF.to_csv('Parsed.csv', index=False)