import pandas as pd

#TODO: Filter each syntax for the schedule in the for loop below

data = pd.read_csv('Test.csv') #!Read the test data
df = pd.DataFrame(data) #? Make it a pandas DataFrame

def parseSyntaxOne(string):
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

def parseSyntaxTwo(string): #! I will do the parsing
    pass

def parseSyntaxThree(string): #! I will do the parsing
    pass

for text in df['lesson_info']:
    #TODO: Filter each syntax for the schedule
    if True: #TODO: Make this detect the first syntax: 18.05.2023, שיעור 4, חרצ'נקו ולרי, ביטול שעור
        pass 
    elif True: #TODO: Make this detect the second syntax(Choose the syntax which is easier to detect. The harder to detect syntax place in the else statement)
        pass
    else: #TODO: In here goes the syntax which is harder to detect
        pass