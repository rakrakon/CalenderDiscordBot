import calendar
import discord
from discord.ext import commands, tasks
import pandas as pd
from datetime import datetime
import os

# TODO: Maybe change to OS instead of scrapy cmdline? (line 74-75)

description = '''A Discord Bot to scrape school schedules form sites
'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
TOKEN = 'MTA4NzM3MTgyOTUzNjExMjY5MA.Gcnjcl.u5B4HjoSkW6d-5h3WJ91hl_ENcaiuE6T1FawDQ'

teacherDictBeitBiram = {
    'גרופמן לירז' : 'ביולוגיה',
    'רז בוחבוט איילת' : 'ספרות',
    'קליינמן טלי' : 'מתמטיקה',
    'ברמן דנה' : 'מתמטיקה',
    'דבי עובדי' : 'מתמטיקה',
    'אורי אוריון' : 'מתמטיקה',
    'טל דנה' : 'מתמטיקה',
    'אלמגור איריס' : 'מתמטיקה',
    'אלעד אמיר' : 'מתמטיקה',
    'אוחיון מירב' : 'מתמטיקה',
    'קינן הילה' : 'אומנות',
    'הנדלמן גיא' : 'קולנוע',
    'מישוריס ילנה' : 'תיאטרון',
    'בן שמחון אביבית' : 'אנגלית',
    'לוי גלי' : 'אנגלית',
    'בלילה אטיאס ליאת' : 'לשון',
    'חרצנקו ולרי' : 'ספורט',
    'הראל עוז' : 'ספורט',
    'ריכלין אלכסי' : 'ספורט',
    'צוקרן אפרת' : 'תנ"ך',
    'בורכוב מירי' : 'ערבית',
    'מיכלוביץ רונה' : 'ערבית',
    'רחלין אולגה' : 'אנגלית',
    'גולדשטיין יניטה' : 'היסטוריה'
}

teacherDictIroni = {
    'בוהדנה שמעון' : 'היסטוריה אזרחית',
    'איינס טל' : 'אנגלית',
    'פריזגר יואל' : 'אנגלית מצטיינים',
    'אזרייב אלכס' : 'אנגלית',
    'גידלביץ אירינה' : 'אנגלית\חינוך',
    'סנש שירה' : 'אנגלית רמה ב',
    "חג'יר ג'ומאנה" : 'אנגלית רמה ב',
    'אמסלם עפרה' : 'עברית',
    'מרקוביצקי לידור לילך' : 'מתמטיקה מיצוי',
    'שקד אהרון רוני' : 'מתמטיקה ע.מדעית',
    'שחם נעומי' : 'מתמטיקה מצוינות',
    'כהן אלינור' : 'מתמטיקה מיצוי',
    'דובנקו ולרי' : 'מתמטיקה א1',
    'רוזן זאקס מיכל' : 'מתמטיקה א2',
    'עירקי רחמים רותם' : 'מתמטיקה א2',
    'גרוסברד מריאנה' : 'מתמטיקה טכניונית',
    'ארז עירית' : 'מתמטיקה א1',
    'פארס קריסטין' : 'מתמטיקה א2',
    'רדינסקי נטאשה' : 'מתמטיקה טכניונית',
    "אבו ח'דרה דאנא" : 'ערבית',
    'יצחקי גילית': 'פלא ספרות',
    'צור עדי': 'פלא ספרות',
    'שינולד נגה*': 'פלא ספרות',
    'מילשטיין תמרי לירז': 'חינוך-גופני בנות',
    'מלכה אלירן': 'חינוך-גופני בנים',
    "תורג'מן שגית": 'תנ"ך',
    "ענבר לילך": 'ביולוגיה',
    "צבר שמיר": 'פיזיקה עתודה\טכניונית',
    "שביב גבי": 'פיזיקה טכניונית',
    "ורשבסקי פנינה": 'מתמטיקה רמה ב',
    "תירם בת-אל": 'פלאתרפיה',
    "הופמן נלי": 'אומנות',
    "שטרנברג אדם": 'גיאוגרפיה',
    "לביא יונית": 'מרכז למידה',
    "ברוק נאנית חנה": 'תאטרון',
    "שקולניטסקי מיכאל": 'רובוטיקה',
    "זאדה מנשה": 'של"ח',

    
}


dayDict = {
    'Sunday' : 'ראשון',
    'Monday' : 'שני',
    'Tuesday' : 'שלישי',
    'Wednesday' : 'רביעי',
    'Thursday' : 'חמישי',
    'Friday' : 'שישי',
    'Saturday' : 'שבת',    
}

def get_day(date_str):
    dt = datetime.strptime(date_str, '%d.%m.%Y').date()
    day = calendar.day_name[dt.weekday()] 
    return dayDict[day]

@bot.event
async def on_ready():
    check.start()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Task Scheduler started')
    print('------')

#! Reali check function
@tasks.loop(minutes=30)
async def checkReali():
    channel = bot.get_channel(1090195068352217090) #! Channel ID
    os.system("scrapy runspider systemChangesReali.py")
    os.system("scrapy runspider systemEventsReali.py") 
    try:
        change_df = pd.read_csv('changesDiffReali.csv')
        rowNumber = len(change_df.index)
        for i in range(rowNumber):
            date = change_df.iloc[i]['date']
            action = change_df.iloc[i]['cancellation']
            teacher = change_df.iloc[i]['instructor'].strip()
            lessonName = teacherDictBeitBiram[teacher]
            lessonDay = get_day(date)
            lessonTime = change_df.iloc[i]['lesson_number']

            embed=discord.Embed(type='rich' ,title=f"{action} POG CHAMP WOO POG SKIBIDI BOP BOP BOP BOP YES YES YES", description=f'ביום {lessonDay} {lessonTime} התבטל שיעור {lessonName}  ({teacher}) ', color=0xff0000)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/785034172862955530/1088864300313096222/twitch-poggers.png')
            embed.set_footer(text=f"בתאריך: {date}")
            await channel.send(embed=embed)
        df = pd.DataFrame()
        df.to_csv('changesDiff.csv', index=False)
    except:
        pass
    try:
        event_df = pd.read_csv('eventsDiffReali.csv')
        rowNumber = len(event_df.index)
        for i in range(rowNumber):
            date = event_df.iloc[i]['date']
            event = event_df.iloc[i]['event']
            classes = event_df.iloc[i]['classes']
            eventDay = get_day(date)
            eventTime = event_df.iloc[i]['time']

            embed=discord.Embed(type='rich' ,title=f"{event} POG CHAMP WOO POG SKIBIDI BOP BOP BOP BOP YES YES YES", description=f'ביום {eventDay} משיעור {eventTime} יש {event}', color=0x51ff00)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/785034172862955530/1088864300313096222/twitch-poggers.png')
            embed.set_footer(text=f"בתאריך: {date} לכיתות {classes}")
            await channel.send(embed=embed)
        df = pd.DataFrame()
        df.to_csv('eventsDiff.csv', index=False)
    except:
        pass


@tasks.loop(minutes=30)
async def checkIroni():
    channel = bot.get_channel(1090195068352217090) #TODO: set Channel ID
    os.system("scrapy runspider systemChangesIroni.py")
    os.system("scrapy runspider systemEventsIroni.py")
    try:
        change_df = pd.read_csv('changesDiffIroni.csv')
        rowNumber = len(change_df.index)
        for i in range(rowNumber):
            date = change_df.iloc[i]['date']
            action = change_df.iloc[i]['cancellation']
            teacher = change_df.iloc[i]['instructor'].strip()
            lessonName = teacherDictIroni[teacher]
            lessonDay = get_day(date)
            lessonTime = change_df.iloc[i]['lesson_number']

            embed=discord.Embed(type='rich' ,title=f"{action} POG CHAMP WOO POG SKIBIDI BOP BOP BOP BOP YES YES YES", description=f'ביום {lessonDay} {lessonTime} התבטל שיעור {lessonName}  ({teacher}) ', color=0xff0000)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/785034172862955530/1088864300313096222/twitch-poggers.png')
            embed.set_footer(text=f"בתאריך: {date}")
            await channel.send(embed=embed)
        df = pd.DataFrame()
        df.to_csv('changesDiffIroni.csv', index=False)
    except:
        pass
    try:
        event_df = pd.read_csv('eventsDiffIroni.csv')
        rowNumber = len(event_df.index)
        for i in range(rowNumber):
            date = event_df.iloc[i]['date']
            event = event_df.iloc[i]['event']
            classes = event_df.iloc[i]['classes']
            eventDay = get_day(date)
            eventTime = event_df.iloc[i]['time']

            embed=discord.Embed(type='rich' ,title=f"{event} POG CHAMP WOO POG SKIBIDI BOP BOP BOP BOP YES YES YES", description=f'ביום {eventDay} משיעור {eventTime} יש {event}', color=0x51ff00)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/785034172862955530/1088864300313096222/twitch-poggers.png')
            embed.set_footer(text=f"בתאריך: {date} לכיתות {classes}")
            await channel.send(embed=embed)
        df = pd.DataFrame()
        df.to_csv('eventsDiffIroni.csv', index=False)
    except:
        pass

#! Runs bot
bot.run(TOKEN)