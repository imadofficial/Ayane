import discord, json
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime

class CPU(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def cpu(self, ctx):
        Userlang = "" #Assigning a variable
        try: #Trying to get userdata
            with open(f"Configurations/Users/{ctx.author.id}.json", "r") as f:
                Data = json.load(f)

            UserLang = Data["Lang"]
        except Exception: #If failed, it creates a new file
            try:
                with open(f"Configurations/Servers/{ctx.guild.id}.json", "r") as f:
                    Data = json.load(f)

                Userang = Data["Lang"]
            except KeyError:
                data = {
                    "Lang": "en_US",
                    "Banned": 0
                }

                json_string = json.dumps(data)

                with open(f"Configurations/Servers/{ctx.guild.id}.json", "w") as outfile:
                    outfile.write(json_string)
                
                Userlang = "en_US"
        
        with open(f'Locale/{Data["Lang"]}.json',  "r", encoding="utf-8") as f:
            Lang = json.load(f)

        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=Lang["LanguageData"]["CPULookup"]["IntelTitle"])
            embed.add_field(name="Intel", value=f"`//cpu intel 9900K`", inline=True)
            embed.add_field(name="AMD", value=f"`//cpu amd 9900K`", inline=True)
            embed.add_field(name="Exynos", value=f"`//cpu exynos 2100`", inline=True)
            embed.add_field(name="Apple", value=f"`//cpu apple A14`", inline=True)
            embed.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar.url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def intel (self, ctx, *, CPU=None):
        Userlang = "" #Assigning a variable

        try: #Trying to get userdata
            with open(f"Configurations/Users/{ctx.author.id}.json", "r") as f:
                Data = json.load(f)

            UserLang = Data["Lang"]
        except Exception: #If failed, it creates a new file
            try:
                with open(f"Configurations/Servers/{ctx.guild.id}.json", "r") as f:
                    Data = json.load(f)

                Userang = Data["Lang"]
            except KeyError:
                data = {
                    "Lang": "en_US",
                    "Banned": 0
                }

                json_string = json.dumps(data)

                with open(f"Configurations/Servers/{ctx.guild.id}.json", "w") as outfile:
                    outfile.write(json_string)
                
                Userlang = "en_US"

        if CPU == None:
            pass


def setup(bot):
    bot.add_cog(CPU(bot))