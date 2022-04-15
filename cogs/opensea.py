# opensea.py

import discord, requests, json
from discord.ext import commands

class OpenSea(commands.Cog):

    def __init__(self, bot, checkUserExists):
        self.bot = bot
        self.checkUserExists = checkUserExists
    
    # provides statistics of a single collection provided its slug
    @commands.command()
    async def stats(self, ctx, slug):
        self.checkUserExists(ctx)

        url = "https://api.opensea.io/api/v1/collection/{0}".format(slug)
        response = requests.request("GET", url)

        if response.status_code == 404:
            await ctx.message.channel.send(slug + " is not a valid collection slug.")
        else:
            res = (json.loads(response.text)["collection"])
            statRes = res["stats"]
            
            embedVar = discord.Embed(title="{0} statistics".format(res["name"]), 
                    url="https://opensea.io/collection/{0}/".format(slug),
                    color=0x3273a8)
            embedVar.set_thumbnail(url = res["image_url"])

            embedVar.add_field(name = 'Floor', value = statRes["floor_price"], inline = True)
            embedVar.add_field(name = 'Total Volume', value = round(statRes["total_volume"], 2), inline = True)
            embedVar.add_field(name = 'Owners', value = statRes["num_owners"], inline = True)

            embedVar.add_field(name = 'Volume(24H)', value = round(statRes["one_day_volume"], 2), inline = True)
            embedVar.add_field(name = 'Volume(7D)', value = round(statRes["seven_day_volume"], 2), inline = True)
            embedVar.add_field(name = 'Volume(30D)', value = round(statRes["thirty_day_volume"], 2), inline = True)

            embedVar.add_field(name = 'AVG Price(24H)', value = round(statRes["one_day_average_price"], 2), inline = True)
            embedVar.add_field(name = 'AVG Price(7D)', value = round(statRes["seven_day_average_price"], 2), inline = True)
            embedVar.add_field(name = 'AVG Price(30D)', value = round(statRes["thirty_day_average_price"], 2), inline = True)

            embedVar.add_field(name = 'Total Supply', value = statRes["total_supply"], inline = True)
            embedVar.add_field(name = 'Total Sales', value = statRes["total_sales"], inline = True)
            embedVar.add_field(name = 'Market Cap', value = round(statRes["market_cap"], 2), inline = True)

            await ctx.message.channel.send(embed=embedVar)

