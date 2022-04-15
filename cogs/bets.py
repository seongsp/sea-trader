# bets.py

import discord, os, random
from discord.ext import commands
from dotenv import load_dotenv
import datetime

class Bets(commands.Cog):

    def __init__(self, bot, checkUserExists, ref, getDailyCooldown):
        self.bot = bot
        self.checkUserExists = checkUserExists
        self.ref = ref
        self.getDailyCooldown = getDailyCooldown
    
    # user flips a coin and either wins double their bet or loses all
    @commands.command()
    async def bet(self, ctx, ante):
        self.checkUserExists(ctx)

        if not ante.isnumeric():
            await ctx.message.channel.send("Invalid input.")

        # get user's betting data
        userId = ctx.message.author.id    
        userRef = self.ref.get(str(userId))
        userData = userRef[0][str(userId)]
        balance = int(userData["balance"])
        wins = int(userData["wins"])
        losses = int(userData["losses"])
        ante = int(ante)

        if ante <= balance:
            # bet
            coinFlip = random.randint(0, 1)
            if coinFlip == 0: #win
                newBalance = balance + ante
                self.ref.update({
                    "{0}/balance".format(str(userId)): newBalance,
                    "{0}/wins".format(str(userId)): wins + 1,
                })
                await ctx.message.channel.send("Won {0} coins.".format(ante))
            else: #lose
                newBalance = balance - ante
                self.ref.update({
                    "{0}/balance".format(str(userId)): newBalance,
                    "{0}/losses".format(str(userId)): losses + 1,
                })
                await ctx.message.channel.send("Lost {0} coins.".format(ante))
        else:
            # ante exceeds your balance
            await ctx.message.channel.send("Your bet exceeds your balance.")

    # user claims 200 tokens daily rewards every 8 hours
    @commands.command()
    async def claim(self, ctx):
        self.checkUserExists(ctx)

        dailyCooldown = self.getDailyCooldown(ctx)
        if dailyCooldown == "Claim Now!":
            # get user's betting data
            userId = ctx.message.author.id    
            userRef = self.ref.get(str(userId))
            userData = userRef[0][str(userId)]
            balance = int(userData["balance"])

            self.ref.update({
                "{0}/balance".format(str(userId)): balance + 200,
                "{0}/prevClaimDate".format(str(userId)): str(datetime.datetime.now()),
            })

            await ctx.message.channel.send("Claimed: 200 coins")
        else:
            await ctx.message.channel.send(f"Please wait: {dailyCooldown}")
