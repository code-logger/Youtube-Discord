import random 
from requests import get
from discord.ext import commands 
from config import TOKEN 
import  os 
import discord 
from youtube_dl import YoutubeDL

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="/",intents=intents,help_command=None)

YDL_OPTIONS = {'format': 'bestaudio/audio',    'postprocessors': [{
        'key': 'FFmpegExtractAudio',  'preferredcodec': 'mp3',
    "preferredquality":"64"}],
    'noplaylist':'True'}

@bot.event 
async def on_ready():
    await bot.change_presence(activity=discord.Game("Downloading Youtube Videos..."))
    print("Bot has successfully logged in as: {}".format(bot.user))

def download(url,file_name):
    NEW_DL = YDL_OPTIONS
    NEW_DL['outtmpl'] = file_name
    with YoutubeDL(NEW_DL) as ydl:
        ydl.download([url])

#download("https://www.youtube.com/watch?v=PVjiKRfKpPI")

def search(arg):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            get(arg) 
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)

    return video

class ViewWithButton(discord.ui.View):

    @discord.ui.button(style=discord.ButtonStyle.blurple, label='Download',emoji="⬇")
    async def click_me_button(self, interaction, button):
        if(button.disabled):
            await interaction.followup.send("Already Downloaded!")
            return
        print("Button was clicked!")
        button.disabled = True
        button.label = "Downloading"
        button.style=discord.ButtonStyle.green
        await interaction.response.edit_message(content="Downloading...")
        await interaction.followup.send(content=f"Downloading")
        button.disabled = True
        button.label = "Downloading...."
        url = interaction.message.embeds[0].url
        title = interaction.message.embeds[0].title
        complete_file_path = title + '-'+url.split("=")[-1]+ ".mp3"
        print(dir(button),"\n",button.disabled,dir(button.style),"\n",dir(button.view),"\n",dir(interaction))
        download(url,complete_file_path)
        await interaction.followup.send(file=discord.File(complete_file_path))
        os.remove(complete_file_path)

@bot.command(name="search")
async def nine_nine(ctx,*args):
    if(len(args) == 0):
        await ctx.send("Please Send the query for the command !")
        return
    dt = search(args[0])
    if(dt['duration'] > 420):
        await ctx.reply("Video is too big...")
        return
    print(dt['title'], dt['webpage_url'],dt['thumbnail'],)
    embed  = discord.Embed(title=dt['title'],url=dt['webpage_url'],description=dt['description'],color=0xFF5733)
    embed.set_image(url=dt['thumbnail'])
    await ctx.send(embed=embed,view=ViewWithButton())




bot.run(TOKEN)
