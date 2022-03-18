import discord, json
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick (self, ctx, user: discord.User = None, *, reason = None):
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

        if user == None:
            embed = discord.Embed(title=Lang["LanguageData"]["Ban"]["InitError"])
            embed.add_field(name=Lang["LanguageData"]["Ban"]["Unentered User"], value=f'{Lang["LanguageData"]["CommonPhrases"]["Usage"]} `//ban 511212466487689216 {Lang["LanguageData"]["Ban"]["ExampleReason"]}`', inline=True)
            embed.set_footer(text=f'{ctx.message.author.name} - Error: Ax01', icon_url=ctx.message.author.avatar.url)
            embed.timestamp = datetime.utcnow()


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban (self, ctx, user: discord.User = None, *, reason = None):
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

        if user is None:
            embed = discord.Embed(title=Lang["LanguageData"]["Ban"]["InitError"])
            embed.add_field(name=Lang["LanguageData"]["Ban"]["Unentered User"], value=f'{Lang["LanguageData"]["CommonPhrases"]["Usage"]} `//kick 511212466487689216 {Lang["LanguageData"]["Ban"]["ExampleReason"]}`', inline=True)
            embed.set_footer(text=f'{ctx.message.author.name} - Error: Ax01', icon_url=ctx.message.author.avatar.url)
            embed.timestamp = datetime.utcnow()

            await ctx.reply(embed=embed, mention_author=False)
        if user.id not in [member.id for member in ctx.guild.members]:
            BanConfirm = Button(label=Lang["LanguageData"]["Ban"]["ButtonConfirm"], style=discord.ButtonStyle.danger)
            BanCancel = Button(label=Lang["LanguageData"]["Ban"]["ButtonCancel"])

            async def BanConfirmed(interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(Lang["LanguageData"]["Ban"]["AccessDenied"], ephemeral=True)
                else:
                    await ctx.guild.ban(user)
                    Confirmed = discord.Embed(title=Lang["LanguageData"]["Ban"]["Inside_Title"], description=Lang["LanguageData"]["Ban"]["ConfirmedTitlePre"] + " " + user.name + " " + Lang["LanguageData"]["Ban"]["ConfirmedTitlePost"])
                    Confirmed.add_field(name=Lang["LanguageData"]["Ban"]["Reason"], value=f'`{Reason}`', inline=True)
                    Confirmed.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar.url)
                    Confirmed.timestamp = datetime.utcnow()
                    await interaction.response.edit_message(embed=Confirmed, view=None)

            async def BanCanceled(interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(Lang["LanguageData"]["Ban"]["AccessDenied"], ephemeral=True)
                else:
                    Canceled = discord.Embed(title=Lang["LanguageData"]["Ban"]["CanceledTitle"], description=Lang["LanguageData"]["Ban"]["ExtraCancelPre"] + " " + user.name + " " + Lang["LanguageData"]["Ban"]["ExtraCancelPost"])
                    Canceled.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar.url)
                    Canceled.timestamp = datetime.utcnow()
                    await interaction.response.edit_message(embed=Canceled, view=None)

            BanConfirm.callback = BanConfirmed
            BanCancel.callback = BanCanceled

            view = View(timeout=50)
            view.add_item(BanConfirm)
            view.add_item(BanCancel)

            async def on_timeout(self) -> None:
                await ctx.send(Lang["LanguageData"]["Ban"]["Timeout"])
            
            Reason = ''

            if reason == None:
                    Reason = Lang["LanguageData"]["Ban"]["NoReason"]
            else:
                    Reason = reason

            embed = discord.Embed(title=Lang["LanguageData"]["Ban"]["Inside_Title"], description=Lang["LanguageData"]["Ban"]["BanAskPre"] + f"**__{user.name}__**" + Lang["LanguageData"]["Ban"]["BanAskPost"])
            embed.add_field(name=Lang["LanguageData"]["Ban"]["Reason"], value=f'`{Reason}`', inline=True)
            embed.add_field(name=Lang["LanguageData"]["Ban"]["HowLong"], value=f'`{Lang["LanguageData"]["Ban"]["indefinitely"]}`', inline=True)
            embed.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar.url)
            embed.timestamp = datetime.utcnow()
            await ctx.reply(embed=embed, mention_author=False, view=view)

def setup(bot):
    bot.add_cog(Moderation(bot))