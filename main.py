import discord
from discord.ext import commands
import random
import asyncio
import os
from keep_alive import keep_alive
import base64
import urllib,requests
from bs4 import BeautifulSoup
os.system("pip3 install discord-py-slash-command")
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
    embed.add_field(name="팁", value="슬래시커맨드로 할 시 서버의 핑이 안좋으면 불러오지 못하니 슬래시커맨드 말고 !status명령어를 입력해주세요", inline=False)
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
        data = requests.get(f"https://api.minetools.eu/ping/{address}").json()
        player = f"{data['players']['sample']}"
        p = []
        u = []
        for i in eval(player):
            p.append(i["name"])
            u.append(i["id"])
        pl = "``"
        n = 0
        for i in eval(player):
            pl = f"{pl}{str(p[n])} ({str(u[n])}), "
            n =+ 1
        pl = f"{pl}``"
        embed.add_field(name='Player List', value=pl, inline=False)
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{address}")
        embed.set_footer(text=f'{ctx.author} 님이 명령어를 사용함', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    except:
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{address}")
        embed.set_footer(text=f'{ctx.author} 님이 명령어를 사용함', icon_url=ctx.author.avatar_url)
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
    await ctx.send(content="추출중입니다. 잠시만 기다려주세요",delete_after=3)
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
        data = requests.get(f"https://api.minetools.eu/ping/{address}").json()
        player = f"{data['players']['sample']}"
        p = []
        u = []
        for i in eval(player):
            p.append(i["name"])
            u.append(i["id"])
        pl = "``"
        n = 0
        for i in eval(player):
            pl = f"{pl}{str(p[n])} ({str(u[n])}), "
            n =+ 1
        pl = f"{pl}``"
        embed.add_field(name='Player List', value=pl, inline=False)
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{address}")
        embed.set_footer(text=f'{ctx.author} 님이 명령어를 사용함', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    except:
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{address}")
        embed.set_footer(text=f'{ctx.author} 님이 명령어를 사용함', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
keep_alive()
bot.run(os.getenv("token"))
