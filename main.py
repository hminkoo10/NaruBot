import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
import random
import asyncio
import os
from keep_alive import keep_alive
import base64
import urllib,requests
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver import ActionChains
#import selenium
import time
from bs4 import BeautifulSoup
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
from discord.utils import get
from youtube_search import YoutubeSearch
import youtube_dl
import re
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
ID = "hminkoo10"
PW = os.getenv("pw")

def click_virtual_btn(driver, target):
    func_g = driver.find_element_by_xpath("//img[@alt='{}']".format(target))
    func_g = func_g.find_element_by_xpath("./../..")
    func_g.click()

def charge_pin(pin):
    try:
        #chrome_options = Options()
        #chrome_options.add_argument('headless')
        driver = webdriver.Chrome()#, options=chrome_options)

        # 로그인하기
        driver.get("https://m.cultureland.co.kr/mmb/loginMain.do")

        WebDriverWait(driver, 200).until(
                EC.element_to_be_clickable((By.ID, 'btnLogin'))
            )

        driver.find_element_by_name("userId").send_keys(ID)

        driver.find_element_by_name("passwd").click()

        for i in PW:
            click_virtual_btn(driver, i)

        driver.find_element_by_id("mtk_done").click()
        driver.find_element_by_id("btnLogin").click()

        # 핀번호 충전하기
        driver.get("https://m.cultureland.co.kr/csh/cshGiftCard.do")

        WebDriverWait(driver, 200).until(
                EC.element_to_be_clickable((By.ID, 'btnCshFrom'))
            )
        driver.find_element_by_id("txtScr11").send_keys(pin[0:4])
        driver.find_element_by_id("txtScr12").send_keys(pin[4:8])
        driver.find_element_by_id("txtScr13").send_keys(pin[8:12])
        for i in range(12, len(pin)):
            click_virtual_btn(driver, pin[i])
            time.sleep(0.1)
            
        time.sleep(1)
        driver.find_element_by_id("btnCshFrom").click()

        # 결과 확인하기
        WebDriverWait(driver, 200).until(
                EC.element_to_be_clickable((By.ID, 'inSafeSub'))
            )

        result = driver.find_element_by_xpath("//*[@id='wrap']/div[3]/section/dl/dd").get_attribute("innerHTML")
        result = result[:-1]

        driver.quit()
        return result

    except:
        return "0"
def randomcolor():
    return random.randint(0x000000,0xffffff)
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="/help",url="https://www.twitch.tv/NaruBot"))
    print(f'{bot.user.name} 준비 끝!')
@bot.listen()
async def on_guild_join(guild):
    await guild.owner.send(f'`{bot.user.name}`를 {guild.name}에 초대해주셔서 감사드립니다!\n앞으로 {bot.user.name}는 더 발전하겠습니다 \n https://koreanbots.dev/bots/936468074314493954 여기서 하트추가를 눌러주시면 감사하겠습니다!')
@bot.listen()
async def on_command_error(ctx, error):
	print(error)
	m = re.search(r'You are on cooldown. Try again in (.*)s', str(error))
	if m:
		asdf = m.groups()[0]
		embed = discord.Embed(
		    title="잠시만요!",
		    description=f"쿨타임에 걸렸어요! 이 명령어를 {asdf}초 후에 다시 사용하실 수 있어요!")
		await ctx.message.reply(embed=embed)
		return
	else:
		m = re.search(r'Command "(.*)" is not found', str(error))
		if m:
			asdf = m.groups()[0]
			embed = discord.Embed(
			    title="잠시만요!",
			    description=
			    f"이 명령어를 사용할 수 없어요! `={asdf}`는 없는 명령어에요! 다른 명령어로 변경됬을 수도 있으니 `=help`로 모든 명령어 목록을 보세요!"
			)
			#await ctx.message.reply(embed=embed)
			return
		else:
			m = re.search(r'User "(.*)" not found.', str(error))
			if m:
				asdf = m.groups()[0]
				embed = discord.Embed(
				    title="잠시만요!",
				    description=
				    f"이 명령어를 사용할 수 없어요! `{asdf}`는 없는 사용자에요! 사용자 멘션이나 사용자의 풀 닉네임을 제시해주세요!"
				)
				await ctx.message.reply(embed=embed)
				return
			elif str(error) == "This command can only be used in private messages.":
				embed = discord.Embed(
				    title="잠시만요!",
				    description=
				    f"이 명령어를 사용할 수 없어요! 이 명령어는 제 DM으로만 사용할 수 있어요! 혹시 모르니 DM을 보내드릴게요!"
				)				
				await ctx.message.reply(embed=embed)
				await ctx.author.send("사용할 수 없던 명령어를 이곳, 제 DM에서 쳐보세요. 서버 채팅에서 친다면 누가 사용자님의 개인정보를 훔쳐갈지도 몰라요! :eyes:")
			else:
				embed = discord.Embed(
				    title="잠시만요!",
				    description=
				    f"이 명령어를 사용할 수 없어요! 발생한 오류는 다음과 같아요! \n\n```{str(error)}```"
				)
				await ctx.message.reply(embed=embed)
				return
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
        pl = f"``{pl}``"
        if pl == "````":
            pl = "too many players!"
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
        if pl == "````":
            pl = "too many players!"
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
"""
@bot.command()
async def donate(ctx, pin):
    await ctx.channel.purge(limit=1)
    result = charge_pin(pin)
    if result == "0":
        embed = discord.Embed(title="오류",description="상품권 번호가 올바르지 않습니다.",color=discord.Color.red())
    else:
        embed = discord.Embed(title="성공",description="{}원을 후원해주셔서 감사합니다!".format(result),color=discord.Color.green())
        print("충전 성공 : {}원이 충전 되었습니다.".format(result))
"""
keep_alive()
bot.run(os.getenv("token"))
