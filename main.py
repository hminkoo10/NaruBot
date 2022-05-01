import discord
from discord.ext import commands
import random
import asyncio
import os
from keep_alive import keep_alive
import base64
import urllib,requests
from bs4 import BeautifulSoup
os.system('pip3 install --upgrade pip')
os.system('pip3 install youtube_search')
os.system('pip3 install discord.py[voice]')
os.system('install-pkg pynacl')
os.system('install-pkg ffmpeg')
os.system("pip3 install discord-py-slash-command")
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
from discord.utils import get
from youtube_search import YoutubeSearch
import youtube_dl
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
    embed.add_field(name="부가기능", value="플래이리스트는 없지만 음악봇 기능이 탑재되어있습니다!", inline=False)
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
        return
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
        return
    userinfo = output["data"]["user"]
    embed = discord.Embed(title=f"{player}'s Information", color=random.randint(0x000000,0xFFFFFF))
    __id = output["data"]["user"]["_id"]
    embed.add_field(name='Player Id', value=f"{__id}", inline=False)
    if userinfo['country'] is not None:
        country = f":flag_{userinfo['country'].lower()}:"
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
    maker=requests.get(f"https://ch.tetr.io/api/users/{player}/records/")
    output=maker.json()
    try:
        line40 = output["data"]["records"]["40l"]
        line40record = int(line40["record"]["endcontext"]["finalTime"] / 60000 * 60)
        embed.add_field(name='40 Line Record', value=f"{line40record} Seconds", inline=False)
        line40recordeddate = line40["record"]["ts"].split("T")[0]
        embed.add_field(name='40 Line Record', value=f"{line40recordeddate}", inline=False)
        line40replayid = line40["record"]["replayid"]
        embed.add_field(name='40 Line Record Replay', value=f"[Replay](https://tetr.io/#r:{line40replayid})", inline=False)
    except:
        pass
    try:
        blitz = output["data"]["records"]["blitz"]
        blitzrecord = int(blitz["record"]["endcontext"]["score"])
        embed.add_field(name='Blitz Record', value=f"{blitzrecord}", inline=False)
        blitzrecordeddate = blitz["record"]["ts"].split("T")[0]
        embed.add_field(name='Blitz Record', value=f"{blitzrecordeddate}", inline=False)
        blitzreplayid = blitz["record"]["replayid"]
        embed.add_field(name='Blitz Record Replay', value=f"[Replay](https://tetr.io/#r:{blitzreplayid})", inline=False)
    except:
        pass
    embed.set_thumbnail(url=f"https://tetr.io/user-content/avatars/{__id}.jpg")
    embed.set_footer(text=f'{ctx.author} 님이 명령어를 사용함', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
volumes = 25
admin = ['657773087571574784']
pf = []

####################################################################


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}
token = os.getenv('token')
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.id = data.get('id')
        self.uploader = data.get('uploader')
        self.uploaderid = data.get('uploader_id')
        self.filename = ytdl.prepare_filename(data)
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
@slash.slash(
  name = 'join'
)
async def 들어와(msg:SlashContext,*,channel:discord.VoiceChannel = None):
    if channel == None:
        channel = msg.author.voice.channel
    if msg.voice_client is not None:
        await msg.voice_client.move_to(channel)
    else:
        await channel.connect()
    await msg.send(content='음성채널에 연결했습니다')
@bot.command(pass_context=True, aliases=['j', 'join'])
async def 들어와(msg,*,channel:discord.VoiceChannel = None):
    if channel == None:
        channel = msg.author.voice.channel
    if msg.voice_client is not None:
        await msg.voice_client.move_to(channel)
    else:
        await channel.connect()
    await msg.send('음성채널에 연결했습니다')

@slash.slash(
  name = 'volume',
  options=[manage_commands.create_option(
    name = "volume",
    description='설정할 소리 크기',
    option_type = 3,
    required = True
  )]
)
async def 볼륨_(ctx:SlashContext, volume:int):
    global volumes
    if ctx.voice_client is None:
        return await ctx.send("봇이 음성채널에 있지 않습니다.")
    else:
        pass
    if volume < 0 and volume > 200:
        await ctx.channel.send(f"{ctx.author.mention}에 의해 불륨이 변경되었습니다.")
    else:
        return await ctx.send("볼륨을 0~200으로 설정해주세요")
    ctx.voice_client.source.volume = volume // 100
    await ctx.send(f"볼륨: {volume}%")
    volumes = volume

@bot.command(pass_context=True, aliases=['v', 'volume'])
async def 소리크기(ctx, vol: int):
    try:
        global volumes
        if ctx.voice_client is None:
            return await ctx.send("봇이 음성채널에 있지 않습니다.")
        if vol < 0 and vol > 200:
            await ctx.send(f"{ctx.author.mention}에 의해 불륨이 변경되었습니다.")
        else:
            return await ctx.send("볼륨을 0~200으로 설정해주세요")
        print(vol / 100)
        ctx.voice_client.source.volume = vol / 100
        await ctx.send(f"볼륨: {vol}%")
        volumes = vol
    except Exception as e:
        print(f'error\n{e}')

@slash.slash(
  name = '중지'
)
async def 중지_(ctx:SlashContext):
    global volumes
    voice = get(bot.voice_clients, guild=ctx.guild)
    volumes = 15

    if voice and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send(content="완료!")
    else:
        await ctx.send(content="음악이 재생되고있지 않습니다.")
@bot.command(pass_context=True, aliases=['s', 'stop'])
async def 중지(ctx):
    global volumes
    voice = get(bot.voice_clients, guild=ctx.guild)
    volumes = 15

    if voice and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("완료!")
    else:
        await ctx.send("음악이 재생되고있지 않습니다.")

@slash.slash(
  name = '일시정지'
)
async def 일시정지_(ctx:SlashContext):
    try:
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send(content="노래가 일시정지 되었습니다.")
        else:
            await ctx.send(content="일시정지할 노래가 없습니다.")
    except Exception as e:
        print('error')
@bot.command(pass_context=True, aliases=['pa', 'pause'])
async def 일시정지(ctx):
    try:
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("노래가 일시정지 되었습니다.")
        else:
            await ctx.send("일시정지할 노래가 없습니다.")
    except Exception as e:
        print('error')

@slash.slash(
  name = '다시재생'
)
async def 다시재생_(ctx:SlashContext):
    try:
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send(content="재생 시작!")
        else:
            print("ERROR")
            await ctx.send(content=":hot_face: 어디선가 오류가 난것 같네요...")
    except Exception as e:
        print('error')
@bot.command(pass_context=True, aliases=['r', 'resume'])
async def 다시재생(ctx):
    try:
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("재생 시작!")
        else:
            print("ERROR")
            await ctx.send(content=":hot_face: 어디선가 오류가 난것 같네요...")
    except Exception as e:
        print('error')
@slash.slash(
  name = '나가'
)
async def 나가_(msg:SlashContext):
    await msg.voice_client.disconnect()
@bot.command(pass_context=True, aliases=['l', 'leave'])
async def 나가(msg):
    await msg.voice_client.disconnect()
@slash.slash(
  name = '재생',
  options=[manage_commands.create_option(
    name = "url",
    description='노래 링크도 가능합니다',
    option_type = 3,
    required = True
  )]
)
async def 재생_(ctx:SlashContext, url:str):
    try:
        await ctx.voice_client.disconnect()
    except:
        pass
    channel = ctx.author.voice.channel
    try:
        ss = await channel.connect()
    except:
        pass
    player = await YTDLSource.from_url(url)
    print(player.id)
    print(player.title)
    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source)
    ctx.voice_client.source.volume = volumes / 100
    ctx.voice_client.source.title = url
    pf.append(player.filename)
    embedt = discord.Embed(title=f'{player.title} 재생중',color=0x00c8ff)
    embedt.set_thumbnail(url=f'https://i.ytimg.com/vi/{player.id}/hqdefault.jpg')
    await ctx.send(embed=embedt)
@bot.command(pass_context=True, aliases=['p', 'play']) #재생
async def 재생(ctx, *, url):
    try:
        await ctx.voice_client.disconnect()
    except:
        pass
    channel = ctx.author.voice.channel
    try:
        ss = await channel.connect()
    except:
        pass
    async with ctx.typing():
        player = await YTDLSource.from_url(url)
        print(player.id)
        print(player.title)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source)
        ctx.voice_client.source.volume = volumes / 100
        ctx.voice_client.source.title = url
    pf.append(player.filename)
    embedt = discord.Embed(title=f'{player.title}재생중!!',color=0x00c8ff)
    embedt.set_thumbnail(url=f'https://i.ytimg.com/vi/{player.id}/hqdefault.jpg')
    await ctx.send(embed=embedt)
@slash.slash(
  name = '반복'
)
async def 반복_(ctx:SlashContext):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and ctx.voice_client.is_playing():
        await ctx.message.add_reaction('<a:complete:760472208774135868>')
        while True:
            try:
                if voice and ctx.voice_client.is_playing() or voice and ctx.voice_client.is_paused():
                    await asyncio.sleep(4)
                else:
                    if not ctx.voice_client.is_connected:
                        await ctx.send(content='반복이 중지되었습니다')
                        return
                    url = ctx.voice_client.source.title
                    player = await YTDLSource.from_url(url)
                    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source)
                    ctx.voice_client.source.title = url
                    await ctx.channel.send(content='노래가 반복중입니다')
            except:
                await ctx.send(content='노래 재생중이 아니므로 반복을 중지합니다')
                return
@bot.command(pass_context=True, aliases=['lo', 'loop'])
async def 반복(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and ctx.voice_client.is_playing():
        await ctx.message.add_reaction('<a:complete:760472208774135868>')
        while True:
            try:
                if voice and ctx.voice_client.is_playing() or voice and ctx.voice_client.is_paused():
                    await asyncio.sleep(4)
                else:
                    if not ctx.voice_client.is_connected:
                        await ctx.send('반복이 중지되었습니다')
                        return
                    url = ctx.voice_client.source.title
                    player = await YTDLSource.from_url(url)
                    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source)
                    ctx.voice_client.source.title = url
                    await ctx.channel.send('노래가 반복중입니다')
            except:
                await ctx.send('노래 재생중이 아니므로 반복을 중지합니다')
                return

keep_alive()
bot.run(os.getenv("token"))
