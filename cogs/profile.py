# profile.py

import discord, os
from discord.ext import commands
from dotenv import load_dotenv

class Profile(commands.Cog):

    def __init__(self, bot, checkUserExists, ref, getDailyCooldown):
        self.bot = bot
        self.checkUserExists = checkUserExists
        self.ref = ref
        self.getDailyCooldown = getDailyCooldown

    # returns balance of user
    @commands.command()
    async def bal(self, ctx):
        self.checkUserExists(ctx)

         # get user's betting data
        userId = ctx.message.author.id    
        userRef = self.ref.get(str(userId))
        userData = userRef[0][str(userId)]
        balance = int(userData["balance"])

        await ctx.channel.send("Balance: {0} coins.".format(balance))
    
    @commands.command()
    async def leaderboard(self, ctx):
        self.checkUserExists(ctx)

    # returns the data profile of the user
    @commands.command()
    async def profile(self, ctx):
        self.checkUserExists(ctx)

        # get user's data
        userId = ctx.message.author.id    
        userRef = self.ref.get(str(userId))
        userData = userRef[0][str(userId)]
        balance = int(userData["balance"])
        wins = int(userData["wins"])
        losses = int(userData["losses"])
        dailyClaimDate = userData["prevClaimDate"]

        embedVar = discord.Embed(title="{0}'s profile:".format(ctx.message.author.name),
                    color=0x3273a8)

        embedVar.add_field(name = 'Balance', value = balance, inline = True)
        embedVar.add_field(name = 'Wins', value = wins, inline = True)
        embedVar.add_field(name = 'Losses', value = losses, inline = True)

        winPercentage = round(1.0*wins/(wins+losses), 2) if wins + losses > 0 else "N/A"
        embedVar.add_field(name = 'Win%',value = winPercentage, inline = True)

        dailyCooldown = self.getDailyCooldown(ctx)
        embedVar.add_field(name = 'Daily Cooldown', value = dailyCooldown, inline = True)

        await ctx.message.channel.send(embed=embedVar)
