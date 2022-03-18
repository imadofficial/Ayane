import discord, json
from discord.ext import commands
import os

with open("Configurations/Config.json", "r") as f:
    config = json.load(f) #Loads the JSON containing all the configs

def get_prefix(bot, message):
    try:
        with open(f'Configurations/Servers/{str(message.guild.id)}.json', 'r') as f:
            prefixes = json.load(f)
        return [prefixes["Prefix"], f"<@{bot.user.id}> "]
    except Exception:
        data = {
                "Lang": "en_US",
                "Banned": 0,
                "Prefix": "//"
        }

        json_string = json.dumps(data)

        with open(f"Configurations/Servers/{str(message.guild.id)}.json", "w") as outfile:
            outfile.write(json_string)

        return ["//", f"<@{bot.user.id}> "]

bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help') #removes help

@bot.slash_command()
async def about (ctx):
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
                "Banned": 0,
                "Prefix": "//"
            }

            json_string = json.dumps(data)

            with open(f"Configurations/Servers/{ctx.guild.id}.json", "w") as outfile:
                outfile.write(json_string)
            
            Userlang = "en_US"

    with open(f'Locale/{Data["Lang"]}.json',  "r", encoding="utf-8") as f:
        Lang = json.load(f)

    with open("Configurations/Config.json", "r") as f:
        config = json.load(f)

    embed = discord.Embed(title=Lang["LanguageData"]["about"]["Properties"])
    embed.add_field(name=Lang["LanguageData"]["about"]["Version"], value=f'`{config["Currentversion"]["Version"]} ({config["Currentversion"]["Build"]}.{config["Currentversion"]["SubBuild"]})`',inline=True)
    embed.add_field(name=Lang["LanguageData"]["about"]["Branch"], value=f'`Stable`',inline=True)
    embed.add_field(name=Lang["LanguageData"]["about"]["Milestone Version"], value=f'`{config["Currentversion"]["Milestone"]}`',inline=True)
    embed.add_field(name=Lang["LanguageData"]["about"]["Release Date"], value=f'`{Lang["Metadata"]["BuildRelease"]}`',inline=True)
    embed.add_field(name=Lang["LanguageData"]["about"]["Python library used"], value=f"[Pycord (v{discord.__version__})](https://github.com/Pycord-Development/pycord)", inline=True)
    embed.add_field(name=Lang["LanguageData"]["about"]["LanguageFrameworkVersion"], value=f'`v{config["Currentversion"]["TranslationFrameworkVer"]}`', inline=True)
    await ctx.respond(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f'v{config["Currentversion"]["Version"]} ({config["Currentversion"]["Build"]}) [{len(bot.guilds)}] (//)'),
                                                        status=discord.Status.do_not_disturb)
    
    print('Bot is ready!')

for filename in os.listdir('Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')

bot.run("Njk4NDk5MTg5NTkxNzY5MTU4.XpGuEA.6CtulgTzHW1IlrobPufoEBRNVXM")