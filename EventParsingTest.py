import pandas as pd

df = pd.read_csv('Test.csv')

df[['date', 'description']] = df['event_info'].str.split(',', expand=True)
df[['event', 'time']] = df['description'].str.split('משיעור', expand=True)
df[['time', 'classes']] = df['time'].str.split('לכיתות', expand=True)
df.drop(['event_info', 'description', 'Unnamed: 0', '0'], axis=1, inplace=True)
df.to_csv('Parsed.csv', index=False)