import discord
from discord.ext import commands
import random
import asyncio
import os
from keep_alive import keep_alive
import base64
import urllib,requests
from bs4 import BeautifulSoup
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)
slash = SlashCommand(bot, sync_commands=True)
def randomcolor():
    return random.randint(0x000000,0xffffff)
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="/help",url="https://www.twitch.tv/mcstatuschecker"))
    print(f'{bot.user.name} 준비 끝!')
@slash.slash(name='help')
async def help_(ctx:SlashContext):
    embed = discord.Embed(title="도움말",color=randomcolor(),description="이 봇의 명령어 도움말")
    embed.add_field(name="상태 확인", value="/status <JE(1.4+),BE서버 주소>", inline=False)
    await ctx.reply(embed=embed)
@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title="도움말",color=randomcolor(),description="이 봇의 명령어 도움말")
    embed.add_field(name="상태 확인", value="/status <JE(1.4+),BE서버 주소>", inline=False)
    await ctx.reply(embed=embed)
@bot.command()
async def hellothisisverification(ctx):
    await ctx.reply("레칼#5252(712290125505363980)")
@bot.command()
async def status(ctx,address):
    maker=requests.get(f"https://api.mcsrvstat.us/2/{address}")
    output=maker.json()
    if output["online"] is not True:
        await ctx.send("서버가 오프라인입니다")
    res = requests.get(f'https://mcsrvstat.us/server/{address}')
    soup = BeautifulSoup(res.content, 'html.parser')
    serverinf = soup.findAll('span', 'badge bg-info')
    imgUrl = soup.find("img","d-none d-sm-block")["src"]
    svinf = []
    for i in serverinf:
        svinf.append(i.get_text())
    embed = discord.Embed(title=f"{address}'s status", color=random.randint(0x000000,0xFFFFFF))
    embed.add_field(name='Server Domain', value=f"{svinf[0]}", inline=False)
    embed.add_field(name='Server Ip', value=f"{svinf[1]}", inline=False)
    embed.add_field(name='Server Port', value=f"{svinf[2]}", inline=False)
    embed.add_field(name='Protocol Version', value=f"{svinf[3]}", inline=False)
    embed.add_field(name='Server Version', value=output["version"], inline=False)
    motd = output["motd"]["clean"]
    m = "\n"
    for i in motd:
        m = m + f'{i}\n'
    embed.add_field(name='Server motd', value=m, inline=False)
    player = str(output["players"]["online"]) + " / " + str(output["players"]["max"])
    embed.add_field(name='Player', value=player, inline=False)
    try:
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{address}")
    except:
        pass
    await ctx.send(embed=embed)
@slash.slash(
  name = 'status',
  options=[manage_commands.create_option(
    name = "address",
    description='확인할 JE 1.4+ 서버/BE 서버 주소(IP).',
    option_type = 3,
    required = True
  )]
)
async def check(ctx:SlashContext, address:str):
    maker=requests.get(f"https://api.mcsrvstat.us/2/{address}")
    output=maker.json()
    if output["online"] is not True:
        await ctx.send("서버가 오프라인입니다",hidden=True)
    res = requests.get(f'https://mcsrvstat.us/server/{address}')
    soup = BeautifulSoup(res.content, 'html.parser')
    serverinf = soup.findAll('span', 'badge bg-info')
    imgUrl = soup.find("img","d-none d-sm-block")["src"]
    svinf = []
    for i in serverinf:
        svinf.append(i.get_text())
    embed = discord.Embed(title=f"{address}'s status", color=random.randint(0x000000,0xFFFFFF))
    embed.add_field(name='Server Domain', value=f"{svinf[0]}", inline=False)
    embed.add_field(name='Server Ip', value=f"{svinf[1]}", inline=False)
    embed.add_field(name='Server Port', value=f"{svinf[2]}", inline=False)
    embed.add_field(name='Protocol Version', value=f"{svinf[3]}", inline=False)
    embed.add_field(name='Server Version', value=output["version"], inline=False)
    motd = output["motd"]["clean"]
    m = "\n"
    for i in motd:
        m = m + f'{i}\n'
    embed.add_field(name='Server motd', value=m, inline=False)
    player = str(output["players"]["online"]) + " / " + str(output["players"]["max"])
    embed.add_field(name='Player', value=player, inline=False)
    try:
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{address}")
    except:
        pass
    await ctx.send(embed=embed)
keep_alive()
bot.run(os.getenv("token"))
