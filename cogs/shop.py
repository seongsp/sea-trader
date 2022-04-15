# shop.py

import discord, os, random
from discord.ext import commands
from dotenv import load_dotenv
import datetime

class Shop(commands.Cog):

    def __init__(self, bot, checkUserExists, ref):
        self.bot = bot
        self.checkUserExists = checkUserExists
        self.ref = ref
    
    # shows what items the users can buy
    @commands.command()
    async def shop(self, ctx):
        self.checkUserExists(ctx)

        embedVar = discord.Embed(title="Shop", color=0x3273a8)
        embedVar.add_field(name = 'Auto Claimer', value = "1200: Claim accrues every 8 hours", inline = True)

        await ctx.message.channel.send(embed=embedVar)
