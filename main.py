import discord, os
from discord.ext import commands
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta
import time

from cogs.bets import Bets
from cogs.profile import Profile
from cogs.opensea import OpenSea
from cogs.shop import Shop

load_dotenv()

firebase_config = {
  "type": os.getenv('TYPE'),
  "project_id": os.getenv('PROJECT_ID'),
  "private_key_id": os.getenv('PRIVATE_KEY_ID'),
  "private_key": os.getenv('PRIVATE_KEY').replace('\\n', '\n'),
  "client_email": os.getenv('CLIENT_EMAIL'),
  "client_id": os.getenv('CLIENT_ID'),
  "auth_uri": os.getenv('AUTH_URI'),
  "token_uri": os.getenv('TOKEN_URI'),
  "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER'),
  "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL'),
}

cred = credentials.Certificate(firebase_config)
databaseApp = firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('DATABASE_URL')
})

PREFIX = '!'

bot = commands.Bot(command_prefix=PREFIX, description='Sea Trader')
ref = db.reference("/")

# get daily cooldown in "HH:MM:SS HRS Left" string format, or "Claim Now!" when cooldown is finished
def getDailyCooldown(ctx):
    # get user's data
    userId = ctx.message.author.id    
    userRef = ref.get(str(userId))
    userData = userRef[0][str(userId)]
    format = "%Y-%m-%d %H:%M:%S.%f"
    prevClaimDate = userData["prevClaimDate"]
    
    if prevClaimDate != "":
        prevClaimDatetime = datetime.strptime(prevClaimDate, format)
        currentDatetime = datetime.now()
        dateDifferenceDelta = currentDatetime - prevClaimDatetime
        if dateDifferenceDelta.total_seconds() >= 28800: # has been greater than 8 hrs
            return "Claim Now!"
        else: # return HH:MM:SS HRS Left
            remainingSeconds = 28800 - dateDifferenceDelta.total_seconds()
            timeLeft = time.strftime('%H:%M:%S', time.gmtime(remainingSeconds))
            return f"{timeLeft} HRS Left"
    else:
        return "Claim Now!"

# checks if the user exists in the database, if not create their profile
def checkUserExists(ctx):
    userId = ctx.message.author.id    
    userRef = ref.get(str(userId))
    if userRef[0] == None:
        ref.set({
                userId: {
                    "balance": 400,
                    "wins": 0,
                    "losses": 0,
                    "prevClaimDate": ""
            }
        })

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="!help"))

bot.add_cog(Bets(bot, checkUserExists, ref, getDailyCooldown))
bot.add_cog(Profile(bot, checkUserExists, ref, getDailyCooldown))
bot.add_cog(OpenSea(bot, checkUserExists))
bot.add_cog(Shop(bot, checkUserExists, ref))

bot.run(os.getenv('TOKEN'), bot=True, reconnect=True)