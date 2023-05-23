import pandas as pd
import re

#TODO: Create parsing function for each syntax

data = pd.read_csv('Test.csv') #!Read the test data
df = pd.DataFrame(data) #? Make it a pandas DataFrame
pattern = r"(?:.*-){3}.*"

def parseSyntaxOne(string): #TODO: Make this parse the first syntax
    pass

def parseSyntaxTwo(string): #TODO: Make this parse the second syntax
    pass

def detectSyntaxThree(string):
    pass

def parseSyntaxFour(string):
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
        pass
    elif "..." in text:
        pass
    elif match:
         pass
    else:
        result = parseSyntaxFour(text)
        print(result)