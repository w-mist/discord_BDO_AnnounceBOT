#####	announcementToolForBDO_pub.py			#####
#####	- programmed by tmp (In-Game family name)	#####
#####	- distributed under GNU/GPLv3			#####
#####	- contact: tmp OR la1n#6395 (Discord)		#####

import discord
from discord.ext import tasks
import sys
import asyncio
import ntplib
from datetime import datetime
from datetime import timedelta
from time import ctime
import math

# チラシの裏
s_VERSION = "1.0.1"
s_RELDATE = "191030"

# 曜日毎ボス定義
dict_Mon = {
	"01:30" : "クザカ・ヌーベル",
	"11:00" : "クザカ",
	"16:00" : "クザカ・クツム",
	"19:00" : "カランダ・ヌーベル",
	"23:00" : "カランダ・クツム"
}
dict_Tue = {
	"01:30" : "クザカ・ヌーベル",
	"11:00" : "クザカ",
	"16:00" : "クザカ・クツム",
	"19:00" : "ヌーベル・クツム",
	"23:00" : "カランダ・ヌーベル"
}
dict_Wed = {
	"01:30" : "クザカ・ヌーベル",
	"16:00" : "ヌーベル・クツム",
	"19:00" : "クザカ・カランダ",
	"23:00" : "ガーモス"
}
dict_Thu = {
	"01:30" : "クザカ・カランダ",
	"11:00" : "クザカ",
	"16:00" : "ヌーベル・クツム",
	"19:00" : "ヌーベル・クツム",
	"23:00" : "オピン"
}
dict_Fri = {
	"01:30" : "クザカ・カランダ",
	"11:00" : "ヌーベル",
	"16:00" : "ヌーベル・クツム",
	"19:00" : "ギュント・ムラカ",
	"23:00" : "カランダ・クツム"
}
dict_Sat = {
	"01:30" : "オピン",
	"11:00" : "クザカ・ヌーベル",
	"16:00" : "カランダ・クツム",
	"19:00" : "クザカ・カランダ"
}
dict_Sun = {
	"01:30" : "ガーモス",
	"11:00" : "カランダ・クツム",
	"14:00" : "ベル",
	"16:00" : "カランダ・クツム",
	"19:00" : "ガーモス",
	"22:30" : "ギュント・ムラカ",
	"23:00" : "オピン"
}

# アナウンス時刻:出現時刻定義 (月<->土)
dict_AnnounceTime = {
	"10:30" : "11:00",
	"15:30" : "16:00",
	"18:30" : "19:00",
	"22:30" : "23:00",
	"01:00" : "01:30"
}

# アナウンス時刻:出現時刻定義 (日)
dict_AnnounceTime_Sun = {
	"10:30" : "11:00",
	"12:50" : "14:00",	# 日曜のみ
	"13:10" : "14:00",	# 日曜のみ
	"13:20" : "14:00",	# 日曜のみ
	"15:30" : "16:00",
	"18:30" : "19:00",
	"22:00" : "22:30",	# 日曜のみ
	"22:30" : "23:00",
	"01:00" : "01:30"
}

# アナウンス時刻のズレ修正のために HH:MM:00 まで待機するHH:00
list_FixAnnounceTimeHH = [9, 12, 14, 17, 21, 0, 3, 6]

# 定数パラメータ
s_TOKEN = "hogePiyoFooBar"	##### BOTのアクセストークンを"で挟んで書くこと #####
n_CHANNEL_ID = 1234567890	##### 送信先チャンネル名のIDを数字のみで指定すること #####
f_INTERVAL = 600		# [sec], loop interval. default=300 (600 or 300)
s_NTPSRV1 = "ntp.nict.jp"
s_NTPSRV2 = "ntp.jst.mfeed.ad.jp"
s_NTPSRV3 = "time.cloudflare.com"
s_BOTNAME = "もっちゅあ！"	##### BOTの名前を書くこと #####

client = discord.Client()

# 起動時処理
@client.event
async def on_ready():
	print('--')
	print('[' + datetime.now().strftime('%H:%M:%S.%f')[:-3] + ']' + ' starting up... settings are')
	print('username=' + str(client.user.name))
	print('id=' + str(client.user.id))
	print('targetChannel=' + str(f_CHANNEL_ID))
	print('interval=' + str(f_INTERVAL) + ' sec')
	print('--')
	sLocalNowWithBrace = '[' + datetime.now().strftime('%H:%M:%S.%f')[:-3] + ']'
	print(sLocalNowWithBrace + " BOT: " + s_BOTNAME + " is up. ver=" + s_VERSION + "_" + s_RELDATE)
	await SendMessage(sLocalNowWithBrace + " BOT: " + s_BOTNAME + " is up. ver=" + s_VERSION + "_" + s_RELDATE)

## 常時監視処理
@tasks.loop(seconds=f_INTERVAL)
async def MakeMessage():
	sLocalNowWithBrace = '[' + datetime.now().strftime('%H:%M:%S.%f')[:-3] + ']'

	## ntp経由の時刻取得処理
	ntp = ntplib.NTPClient()
	ctCurrentTime = ""
	try:
		ctCurrentTime = ctime(ntp.request(s_NTPSRV1).tx_time)
	except Exception as e1:
		print(sLocalNowWithBrace + "! an exception occured;")
		print(type(e1))
		print(e1)
	else:
		print(sLocalNowWithBrace + " ntp.request(" + s_NTPSRV1 + ") success.")
	finally:
		if ctCurrentTime == "":
			try:
				ctCurrentTime = ctime(ntp.request(s_NTPSRV2).tx_time)
			except Exception as e2:
				print(sLocalNowWithBrace + "! an exception occured;")
				print(type(e2))
				print(e2)
			else:
				print(sLocalNowWithBrace + " ntp.request(" + s_NTPSRV2 + ") success.")
			finally:
				if ctCurrentTime == "":
					try:
						ctCurrentTime = ctime(ntp.request(s_NTPSRV3).tx_time)
					except Exception as e3:
						print(sLocalNowWithBrace + " ! an exception occured;")
						print(type(e3))
						print(e3)
						await SendMessage("えくせぷしょん！（もうだめぽ）")
						sys.exit(-1)
					else:
						print(sLocalNowWithBrace + " ntp.request(" + s_NTPSRV3 + ") success.")

	## 最寄りインターバル時刻への待機処理
	dtNtpTime = datetime.strptime(ctCurrentTime, '%a %b %d %H:%M:%S %Y')
	fNtpTimeHH = dtNtpTime.hour
	fNtpTimeMM = dtNtpTime.minute
	fNtpTimeSS = dtNtpTime.second
	if fNtpTimeMM % (f_INTERVAL//60) != 0 or \
		(fNtpTimeHH in list_FixAnnounceTimeHH and fNtpTimeMM == 0):
		# 起動時 OR 定時に必ずsync
		fSleepSS = (math.ceil(fNtpTimeMM/10)*10-fNtpTimeMM)*60 - fNtpTimeSS - (datetime.now().microsecond/1000000)
#		if fSleepSS < 0:
#			fSleepSS = f_INTERVAL + fSleepSS
		if fSleepSS >= 1:
			print(sLocalNowWithBrace + " wait for next interval (" + str(fSleepSS) + " seconds) at tasks.loop().")
			print(sLocalNowWithBrace + " fNtpTimeHH=" + str(fNtpTimeHH) + " fNtpTimeMM=" + str(fNtpTimeMM) \
				+ " fNtpTimeSS=" + str(fNtpTimeSS) + " datetime.now().microsecond=" + str(datetime.now().microsecond))
			await asyncio.sleep(fSleepSS)
			sLocalNowWithBrace = '[' + datetime.now().strftime('%H:%M:%S.%f')[:-3] + ']'
			print("")
			print(sLocalNowWithBrace + " woke up!")
		else:
			print(sLocalNowWithBrace + " seems no need to wait next interval. (fSleepSS=" + str(fSleepSS) + ")")
	else:
		print(sLocalNowWithBrace + " seems no need to wait next interval (at initial or regular time).")

	## アナウンス時間チェック
	bAnnounceTime = False
	sLocalDay = datetime.now().strftime('%a')
	if sLocalDay != "Sun":
		for dtKey, dtValue in dict_AnnounceTime.items():
			dtBeginTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, \
						datetime.strptime(dtKey, "%H:%M").hour, datetime.strptime(dtKey, "%H:%M").minute, 0)
			dtEndTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, \
						datetime.strptime(dtValue, "%H:%M").hour, datetime.strptime(dtValue, "%H:%M").minute, 0)
			if dtNtpTime >= dtBeginTime and dtNtpTime < dtEndTime:
				# 出現メッセージ(残り00分)は出さない
				bAnnounceTime = True
				print(sLocalNowWithBrace + " announce time is incoming. (sLocalDay=" + sLocalDay + ")" \
					+ " dtBeginTime(" + str(dtBeginTime) + ") datetime.now()(" + str(datetime.now()) + ") dtEndTime(" + str(dtEndTime) + ")")
				break
	elif sLocalDay == "Sun":
		for dtKey, dtValue in dict_AnnounceTime_Sun.items():
			dtBeginTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, \
						datetime.strptime(dtKey, "%H:%M").hour, datetime.strptime(dtKey, "%H:%M").minute, 0)
			dtEndTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, \
						datetime.strptime(dtValue, "%H:%M").hour, datetime.strptime(dtValue, "%H:%M").minute, 0)
			if dtNtpTime >= dtBeginTime and dtNtpTime < dtEndTime:
				# 出現メッセージ(残り00分)は出さない
				bAnnounceTime = True
				print(sLocalNowWithBrace + " announce time is incoming. (sLocalDay=" + sLocalDay + ")" \
					+ " dtBeginTime(" + str(dtBeginTime) + ") datetime.now()(" + str(datetime.now()) + ") dtEndTime(" + str(dtEndTime) + ")")
				break
	else:
		print("! unknown day.")
		sys.exit(-1)
	if bAnnounceTime == False:
		print(sLocalNowWithBrace + " not announce time. (bAnnounceTime=" + str(bAnnounceTime) + ")")

	## アナウンス曜日チェック, ボス名決定
	sBossName = ""
	fRemainingSS = -1	# seconds
	bDeterminedBossName = False
	bVellbell = False
	if bAnnounceTime == True:
		sEndHHMM = datetime.strftime(dtEndTime, "%H:%M")
		if sLocalDay == "Mon" and sEndHHMM in dict_Mon:
			sBossName = dict_Mon[sEndHHMM]
		elif sLocalDay == "Tue" and sEndHHMM in dict_Tue:
			sBossName = dict_Tue[sEndHHMM]
		elif sLocalDay == "Wed" and sEndHHMM in dict_Wed:
			sBossName = dict_Wed[sEndHHMM]
		elif sLocalDay == "Thu" and sEndHHMM in dict_Thu:
			sBossName = dict_Thu[sEndHHMM]
		elif sLocalDay == "Fri" and sEndHHMM in dict_Fri:
			sBossName = dict_Fri[sEndHHMM]
		elif sLocalDay == "Sat" and sEndHHMM in dict_Sat:
			sBossName = dict_Sat[sEndHHMM]
		elif sLocalDay == "Sun" and sEndHHMM in dict_Sun:
			## ベル特例
			if datetime.now().hour == 12 or datetime.now().hour == 13:
				bVellbell = True
				sBossName = dict_Sun["14:00"]	# 決め打ち
				if datetime.now().minute == 50:
					fRemainingSS = (dtEndTime - datetime.now()).seconds
				elif datetime.now().minute == 10:
					fRemainingSS = (dtEndTime - datetime.now()).seconds
				elif datetime.now().minute == 20:
					fRemainingSS = (dtEndTime - datetime.now()).seconds
			else:
				sBossName = dict_Sun[sEndHHMM]
		else:
			print(sLocalNowWithBrace + " unknown day or no data in dict_" + sLocalDay + ".")
		if sBossName != "":
			bDeterminedBossName = True
	if bDeterminedBossName == True:
		print(sLocalNowWithBrace + " sBossName=" + sBossName)
	else:
		print(sLocalNowWithBrace + " sBossName couldnt be determined. (bDeterminedBossName=" + str(bDeterminedBossName) + ")")

	## 出現までの時間チェック
	if bDeterminedBossName == True:
		if bVellbell != True:
			fRemainingSS = (dtEndTime - datetime.now()).seconds
	if fRemainingSS != -1:
		print(sLocalNowWithBrace + " fRemainingSS=" + str(fRemainingSS) + " [sec]")
	else:
		print(sLocalNowWithBrace + " fRemainingSS = -1 (bDeterminedBossName=" + str(bDeterminedBossName) + ")")

	## アナウンス文字列作成
	sPopMsg = ""
	if fRemainingSS != -1:
		fStrictRemainingSS = math.ceil(fRemainingSS/10)*10//60
		fLooseRemainingSS = math.ceil(fRemainingSS/100)*100//60
		sPopMsg = sBossName + "出現" + str(fLooseRemainingSS) + "分前"
		if fStrictRemainingSS != fLooseRemainingSS:
			sPopMsg += "(?)"

	## 送信
	if sPopMsg != "":
		print(sLocalNowWithBrace + " sending mesg=\"" + sPopMsg + "\"")
		print("")
		await SendMessage(sPopMsg)
	else:
		print(sLocalNowWithBrace + " not sending mesg. (sPopMsg=\"" + str(sPopMsg) + "\")")
		print("")

## メッセージ送信
async def SendMessage(msg):
	await client.wait_until_ready()
	channel = client.get_channel(f_CHANNEL_ID)
	await channel.send(msg)

## BOTメッセージに応答しない処理
@client.event
async def on_message(message):
	if message.author.bot:
		return

MakeMessage.start()
client.run(s_TOKEN)
