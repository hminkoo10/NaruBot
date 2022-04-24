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
try:
  import light_koreanbots as lkb
except:
  os.system("pip3 install light-koreanbots")
finally:
  import light_koreanbots as lkb
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)
slash = SlashCommand(bot, sync_commands=True)
#lkb_client = lkb.LKBClient(bot=bot, token=os.getenv("dbkrpytoken"))
def randomcolor():
    return random.randint(0x000000,0xffffff)
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="/help",url="https://www.twitch.tv/NaruBot"))
    print(f'{bot.user.name} 준비 끝!')
@bot.listen()
async def on_guild_join(guild):
    await guild.owner.send(f'`{bot.user.name}`를 {guild.name}에 초대해주셔서 감사드립니다!\n앞으로 {bot.user.name}는 더 발전하겠습니다 \n https://koreanbots.dev/bots/936468074314493954 여기서 하트추가를 눌러주시면 감사하겠습니다!')
@slash.slash(name='help')
async def help_(ctx:SlashContext):
    embed = discord.Embed(title="도움말",color=randomcolor(),description="이 봇의 명령어 도움말")
    embed.add_field(name="마인크래프트 서버 상태 확인", value="/status <JE(1.4+),BE서버 주소>", inline=False)
    embed.add_field(name="마인크래프트 플래이어 정보 확인", value="/player <JE 플래이어 이름>", inline=False)
    embed.add_field(name="팁", value="슬래시커맨드로 할 시 서버의 핑이 안좋으면 불러오지 못하니 슬래시커맨드 말고 !status명령어를 입력해주세요", inline=False)
    await ctx.reply(embed=embed)
@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title="도움말",color=randomcolor(),description="이 봇의 명령어 도움말")
    embed.add_field(name="마인크래프트 서버 상태 확인", value="/status <JE(1.4+),BE서버 주소>", inline=False)
    embed.add_field(name="마인크래프트 플래이어 정보 확인", value="/player <JE 플래이어 이름>", inline=False)
    embed.add_field(name="팁", value="슬래시커맨드로 할 시 서버의 핑이 안좋으면 불러오지 못하니 슬래시커맨드 말고 !status명령어를 입력해주세요", inline=False)
    await ctx.reply(embed=embed)
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
    await ctx.send(content="추출중입니다. 잠시만 기다려주세요",hidden=True)
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
@bot.command()
async def player(ctx, player):
    res = requests.get(f'https://minecraftuuid.com/?search={player}')
    soup = BeautifulSoup(res.content, 'html.parser')
    uuid = soup.findAll("input","Form-Control")
    plinf = []
    for i in uuid:
        plinf.append(i["value"])
    playernames = [f"```\n{plinf[0]}\n"]
    try:
        n = plinf[3].split(',')
        for i in n:
            playernames.append(f"{i}\n")
        playernames.append("```")
        historyname = ""
        for i in playernames:
            historyname = historyname + i
    except:
        historyname = player
    historyname = historyname.replace(" ","")
    embed = discord.Embed(title=f"{player}'s Information", color=random.randint(0x000000,0xFFFFFF))
    embed.add_field(name='Player UUID', value=f"{plinf[1]}", inline=False)
    embed.add_field(name='Player Name History', value=f"{historyname}", inline=False)
    command113 = '/give @p minecraft:player_head{SkullOwner:"playernamereplacespot"}'
    embed.add_field(name='Player Skull Command (equal or bigger than 1.13)', value=f"{command113.replace('playernamereplacespot',player)}", inline=False)
    command112 = '/give @p minecraft:skull 1 3 {SkullOwner:"playernamereplacespot"}'
    embed.add_field(name='Player Skull Command (equal or smaller than 1.12)', value=f"{command112.replace('playernamereplacespot',player)}", inline=False)
    embed.set_footer(text=f'{ctx.author} 님이 명령어를 사용함', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
@slash.slash(
  name = 'player',
  options=[manage_commands.create_option(
    name = "playername",
    description='JE Player Name',
    option_type = 3,
    required = True
  )]
)
async def checkplayer(ctx:SlashContext, playername:str):
    await ctx.send(content="추출중입니다. 잠시만 기다려주세요",hidden=True)
    res = requests.get(f'https://minecraftuuid.com/?search={playername}')
    soup = BeautifulSoup(res.content, 'html.parser')
    uuid = soup.findAll("input","Form-Control")
    plinf = []
    for i in uuid:
        plinf.append(i["value"])
    playernames = [f"```\n{plinf[0]}\n"]
    try:
        n = plinf[3].split(',')
        for i in n:
            playernames.append(f"{i}\n")
        playernames.append("```")
        historyname = ""
        for i in playernames:
            historyname = historyname + i
    except:
        historyname = playername
    historyname = historyname.replace(" ","")
    embed = discord.Embed(title=f"{player}'s Information", color=random.randint(0x000000,0xFFFFFF))
    embed.add_field(name='Player UUID', value=f"{plinf[1]}", inline=False)
    embed.add_field(name='Player Name History', value=f"{historyname}", inline=False)
    command113 = '/give @p minecraft:player_head{SkullOwner:"playernamereplacespot"}'
    embed.add_field(name='Player Skull Command (equal or bigger than 1.13)', value=f"{command113.replace('playernamereplacespot',playername)}", inline=False)
    command112 = '/give @p minecraft:skull 1 3 {SkullOwner:"playernamereplacespot"}'
    embed.add_field(name='Player Skull Command (equal or smaller than 1.12)', value=f"{command112.replace('playernamereplacespot',playername)}", inline=False)
    embed.set_footer(text=f'{ctx.author} 님이 명령어를 사용함', icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)

@bot.command()
async def tetrio(ctx,player):
    maker=requests.get(f"https://ch.tetr.io/api/users/{player}/")
    output=maker.json()
    if output["success"] is False:
        await ctx.send("플래이어 이름을 다시 확인해주세요")
        raise Exception("이름 다시확인")
    userinfo = output["data"]["user"]
    embed = discord.Embed(title=f"{player}'s Information", color=random.randint(0x000000,0xFFFFFF))
    __id = output["data"]["user"]["_id"]
    embed.add_field(name='Player Id', value=f"{__id}", inline=False)
    embed.add_field(name="Player's Country", value=f"{userinfo['country']}", inline=False)
    joineddate = output["data"]["user"]["ts"].split("T")[0]
    embed.add_field(name='Player Joined date', value=f"{joineddate}", inline=False)
    playtime = int(int(userinfo["gametime"]) // 3600)
    embed.add_field(name='Play Time', value=f"{playtime} Hours", inline=False)
    embed.add_field(name='Friends Count', value=f"{userinfo['friend_count']}", inline=False)
    embed.add_field(name='Number of Games Played', value=f"{userinfo['gamesplayed']}", inline=False)
    embed.add_field(name='Number of Games Won', value=f"{userinfo['gameswon']}", inline=False)
    embed.add_field(name='Number of Games Played - Tetra League', value=f"{userinfo['league']['gamesplayed']}", inline=False)
    embed.add_field(name='Number of Games Won - Tetra League', value=f"{userinfo['league']['gameswon']}", inline=False)
    embed.set_thumbnail(url=f"https://tetr.io/user-content/avatars/{__id}.jpg")
    embed.set_footer(text=f'{ctx.author} 님이 명령어를 사용함', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@slash.slash(
  name = 'tetrio',
  options=[manage_commands.create_option(
    name = "player",
    description="tetr.io player name",
    option_type = 3,
    required = True
  )]
)
async def tetris(ctx:SlashContext, player:str):
    maker=requests.get(f"https://ch.tetr.io/api/users/{player}/")
    output=maker.json()
    if output["success"] is False:
        await ctx.send("플래이어 이름을 다시 확인해주세요")
        raise Exception("이름 다시확인")
    userinfo = output["data"]["user"]
    embed = discord.Embed(title=f"{player}'s Information", color=random.randint(0x000000,0xFFFFFF))
    __id = output["data"]["user"]["_id"]
    embed.add_field(name='Player Id', value=f"{__id}", inline=False)
    if userinfo['country'] is not None:
        country = f":flag_{userinfo['country']}:"
    else:
        country = "None"
    embed.add_field(name="Player's Country", value=f"{country}", inline=False)
    joineddate = output["data"]["user"]["ts"].split("T")[0]
    embed.add_field(name='Player Joined date', value=f"{joineddate}", inline=False)
    playtime = int(int(userinfo["gametime"]) // 3600)
    embed.add_field(name='Play Time', value=f"{playtime} Hours", inline=False)
    embed.add_field(name='Friends Count', value=f"{userinfo['friend_count']}", inline=False)
    embed.add_field(name='Number of Games Played', value=f"{userinfo['gamesplayed']}", inline=False)
    embed.add_field(name='Number of Games Won', value=f"{userinfo['gameswon']}", inline=False)
    embed.add_field(name='Number of Games Played - Tetra League', value=f"{userinfo['league']['gamesplayed']}", inline=False)
    embed.add_field(name='Number of Games Won - Tetra League', value=f"{userinfo['league']['gameswon']}", inline=False)
    embed.set_thumbnail(url=f"https://tetr.io/user-content/avatars/{__id}.jpg")
    embed.set_footer(text=f'{ctx.author} 님이 명령어를 사용함', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
keep_alive()
bot.run(os.getenv("token"))
