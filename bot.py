import discord
from discord.ext import commands
import pandas as pd
from datetime import datetime
import calendar
import random

#TODO: Clock this script and the 2 webscrapers

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

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
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.command()
async def check(ctx):
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
            await ctx.send(embed=embed)
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
                await ctx.send(embed=embed)
            df = pd.DataFrame()
            df.to_csv('eventsDiff.csv', index=False)
        except:
            await ctx.send('No changes were made')

#! Runs bot
bot.run(TOKEN)