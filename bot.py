import calendar
import discord
from discord.ext import commands, tasks
import pandas as pd
from datetime import datetime
from scrapy import cmdline
import os
import calendar

# TODO: Maybe change to OS instead of scrapy cmdline? (line 74-75)

description = '''A Discord Bot to scrape school schedules form sites
'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
TOKEN = 'MTA4NzM3MTgyOTUzNjExMjY5MA.Gcnjcl.u5B4HjoSkW6d-5h3WJ91hl_ENcaiuE6T1FawDQ'

teacherDict = {
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

@tasks.loop(minutes=30)
async def check():
    channel = bot.get_channel(1090195068352217090) #! Channel ID
    #! NOT WORKING
    cmdline.execute("scrapy runspider systemChanges.py".split()) #? run system changes web scraper
    cmdline.execute("scrapy runspider systemEvents.py".split()) #? run system events web scraper
    # os.system('cmd /k "scrapy runspider systemChanges.py"')
    # os.system('cmd /k "scrapy runspider systemEvents.py"') 
    try:
        change_df = pd.read_csv('changesDiff.csv')
        rowNumber = len(change_df.index)
        for i in range(rowNumber):
            date = change_df.iloc[i]['date']
            action = change_df.iloc[i]['cancellation']
            teacher = change_df.iloc[i]['instructor'].strip()
            lessonName = teacherDict[teacher]
            lessonDay = get_day(date)
            lessonTime = change_df.iloc[i]['lesson_number']

            embed=discord.Embed(type='rich' ,title=f"{action} POG CHAMP WOO POG SKIBIDI BOP BOP BOP BOP YES YES YES", description=f'ביום {lessonDay} {lessonTime} התבטל שיעור {lessonName}  ({teacher}) ', color=0xff0000)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/785034172862955530/1088864300313096222/twitch-poggers.png')
            embed.set_footer(text=f"בתאריך: {date}")
            await channel.send(embed=embed)
        df = pd.DataFrame()
        df.to_csv('changesDiff.csv', index=False)
    except:
        try:
            event_df = pd.read_csv('eventsDiff.csv')
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

#! Runs bot
bot.run(TOKEN)