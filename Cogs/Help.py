import discord, json
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help (self, ctx):
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

        with open("Configurations/Config.json", "r") as f:
            config = json.load(f)

        embed = discord.Embed(title=Lang["LanguageData"]["Help"]["Title"], description=Lang["LanguageData"]["Help"]["Warning"])
        embed.add_field(name=Lang["LanguageData"]["Help"]["SlashCategory"], value=f"`/about`", inline=True)
        embed.add_field(name=Lang["LanguageData"]["Help"]["ModerationCategory"], value=f"`//ban`\n`//kick`", inline=True)
        embed.add_field(name=Lang["LanguageData"]["Help"]["TechCategory"], value=f"`//intelark (BETA)`", inline=True)
        embed.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar.url)
        await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(Help(bot))