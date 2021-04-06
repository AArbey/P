#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#					Imports						#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

import os
import sys
from gtts import gTTS

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option,create_choice

import youtube_dl
import ffmpeg
from youtubesearchpython.__future__ import VideosSearch


import connect4
from connect4 import ConnectBoard, draw_board, initial_board

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#				Initializing					#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

ListsOfBoards = []

TOKEN = 'ODE4MTgwOTg5MzE4MjAxMzkz.YEUUbA.czY8LGfSlh3BCnFBRtpuWrrovcA'

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [757997610442424390]

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#				 ON READY EVENT 				#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
@client.event
async def on_ready():
	print(client.user, 'has connected to Discord!')


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#				ON SLASH EVENTS				    #
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#



@slash.slash(name="connect",
             description="Connect the bot to an audio channel.",
             options=[
               create_option(
                 name="channel",
                 description="Which channel?",
                 option_type=7,
                 required=True,
               )
             ],
             guild_ids=guild_ids)
async def _connect(ctx, channel: str):
	message = ctx.author
	await channel.connect()
	for vc in client.voice_clients:
		if vc.is_connected():
			await ctx.send(content="Connected")
			for vc in client.voice_clients:
				if vc.guild == message.guild:
					if vc.is_connected():
						if vc.is_playing():
							vc.stop()
						source = await discord.FFmpegOpusAudio.from_probe("hellothere.mp3")
						vc.play(source)


@slash.slash(name="disconnect",
             description="Disconnect the bot from an audio channel.",
             guild_ids=guild_ids)
async def _disconnect(ctx):
	user = ctx.author
	for vc in client.voice_clients:
		if vc.guild == user.guild:
			await vc.disconnect()
	await ctx.send(content="Disconnected")


@slash.slash(name="die",
             description="Kill the bot.",
             guild_ids=guild_ids)
async def _die(ctx):
	for vc in client.voice_clients:
		if vc.is_connected():
			await vc.disconnect()
	await ctx.send(content="See you soon")
	sys.exit()

@slash.slash(name="Stop",
             description="Stop whatever the bot is doing.",
             guild_ids=guild_ids)
async def _disconnect(ctx):
	message = ctx.author
	for vc in client.voice_clients:
		if vc.guild == message.guild:
			if vc.is_connected():
				if vc.is_playing():
					vc.stop()
	
	await ctx.send(content="Stopped")

@slash.slash(name="play",
             description="Play a youtube video from a WEB adress.",
             options=[
               create_option(
                 name="url",
                 description="What is the video's url?",
                 option_type=3,
                 required=True,
               )
             ],
             guild_ids=guild_ids)

async def _play(ctx, url: str):
	message = ctx.author
	await ctx.send(content="Playing...")
	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
	result = ydl.extract_info(url,download=False)
	if int(result['formats'][1]['filesize']) > 50000000:
		await ctx.send("youtube video too big(<50MB):"+str(result['formats'][1]['filesize']))
		return
	print(result['formats'][1]['filesize'])

	ydl_opts = {
	'format': 'bestaudio/best',
	'outtmpl': 'song.%(ext)s',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])

	for vc in client.voice_clients:
		if vc.guild == message.guild:
			if vc.is_connected():

				if vc.is_playing():
					vc.stop()

				source = await discord.FFmpegOpusAudio.from_probe("song.mp3")
				vc.play(source)
	
@slash.slash(name="search",
             description="Plays the first video on youtube related to what you type.",
             options=[
               create_option(
                 name="name",
                 description="What is the video's name?",
                 option_type=3,
                 required=True,
               )
             ],
             guild_ids=guild_ids)

async def _search(ctx, name: str):
	message = ctx.author
	videosSearch = VideosSearch(str(name), limit = 1)
	videosResult = await videosSearch.next()
	await ctx.send(content="Playing "+name+ " on Youtube")

	url = videosResult['result'][0]['link']
	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
	result = ydl.extract_info(url,download=False)
	if int(result['formats'][1]['filesize']) > 50000000:
		await ctx.send("youtube video too big(<50MB):"+str(result['formats'][1]['filesize']))
		return
	print(result['formats'][1]['filesize'])

	ydl_opts = {
	'format': 'bestaudio/best',
	'outtmpl': 'song.%(ext)s',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])

	for vc in client.voice_clients:
		if vc.guild == message.guild:
			if vc.is_connected():

				if vc.is_playing():
					vc.stop()

				source = await discord.FFmpegOpusAudio.from_probe("song.mp3")
				vc.play(source)

@slash.slash(name="say",
             description="Make the bot say whatever you want.",
             options=[
               create_option(
                 name="text",
                 description="What do you want the bot to say?",
                 option_type=3,
                 required=True,
               )
             ],
             guild_ids=guild_ids)

async def _say(ctx, text: str):
	message = ctx.author
	await ctx.send(content="Talking...")
	lang = "en"
	audio = gTTS(text=text,lang=lang,slow=False)
	audio.save("tts.mp3")
	for vc in client.voice_clients:
		if vc.guild == message.guild:
			if vc.is_connected():
				if vc.is_playing():
					vc.stop()
				source = await discord.FFmpegOpusAudio.from_probe("tts.mp3")
				vc.play(source)


@slash.slash(name="replay",
             description="Replay the last audio.",
             guild_ids=guild_ids)
async def _replay(ctx):
	message = ctx.author
	for vc in client.voice_clients:
		if vc.guild == message.guild:
			if vc.is_connected():
				await ctx.send(content="Replaying...")
				if vc.is_playing():
					vc.stop()
				source = await discord.FFmpegOpusAudio.from_probe("song.mp3")
				vc.play(source)


@slash.slash(name="Message",
             description="Make the bot say by text whatever you want?",
             options=[
               create_option(
                 name="text",
                 description="What do you want the bot to say?",
                 option_type=3,
                 required=True,
               )
             ],
             guild_ids=guild_ids)
async def _disconnect(ctx, text: str):
	await ctx.send(content="You said "+text)
	

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#				ON MESSAGE EVENTS				#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

@client.event
async def on_message(message):

	#=-=- Global Variables and other variables =-=-=#
	global IdsOfBoards
	messagetxt = message.content.lower()
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

	#=-=- Make sure it does not react to itself -=-=#
	if message.author == client.user:
		return
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

	# DUBUGGING
	#elif message.author == 'Ezyo#2334':
	#	print(message.content)


	#=-=-=-=-= Initializing connect 4 game =-=-=-=-=#
	elif 'play connect 4' in messagetxt:
		
		InitialBoard = initial_board()

		board_message = await message.channel.send(draw_board(InitialBoard))

		if 'vs' in message.content:
			pass
		else:
			ListsOfBoards.append(ConnectBoard(board_message.id, 3, InitialBoard))
		
		print(ListsOfBoards)

		await board_message.add_reaction("⬅")
		await board_message.add_reaction("➡")
		await board_message.add_reaction("⬇")
		return
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#


	#=-=-=-=-=-=-=- random reaction -=-=-=-=-=-=-=-=#
	elif messagetxt == 'get out of here':
		await message.channel.send("Well f**k y...")
		await client.change_presence(status=discord.Status.offline)
		return

	elif messagetxt == 'come here':
		await client.change_presence(status=discord.Status.online)
		await message.channel.send("Back for more!")
		return
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#


	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#


	elif message.content == 'MOM':
		await message.delete()
		for vc in client.voice_clients:
			if vc.guild == message.guild:
				if vc.is_connected():
					if vc.is_playing():
						vc.stop()
					source = await discord.FFmpegOpusAudio.from_probe("MOM.mp3")
					vc.play(source)

	elif message.content == 'RUSH':
		await message.delete()
		for vc in client.voice_clients:
			if vc.guild == message.guild:
				if vc.is_connected():
					if vc.is_playing():
						vc.stop()
					source = await discord.FFmpegOpusAudio.from_probe("rush.mp3")
					vc.play(source)

	elif message.content.lower() == 'monkey':
		for vc in client.voice_clients:
			if vc.guild == message.guild:
				if vc.is_connected():
					if vc.is_playing():
						vc.stop()
					source = await discord.FFmpegOpusAudio.from_probe("monkey.mp3")
					vc.play(source)

	elif message.content.lower() == 'hellothere':
		await message.delete()
		for vc in client.voice_clients:
			if vc.guild == message.guild:
				if vc.is_connected():
					if vc.is_playing():
						vc.stop()
					source = await discord.FFmpegOpusAudio.from_probe("helloecho.mp3")
					vc.play(source)

	

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#				ON REACTION EVENTS				#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
@client.event
async def on_reaction_add(reaction, user):
	global ListsOfBoards

	if user == client.user:
		return

	for ConnectBoard in ListsOfBoards:
		if reaction.message.id == ConnectBoard.messageID:
			if reaction.emoji == "⬅":
				await reaction.message.edit(content=ConnectBoard.left())
				await reaction.remove(user)

			elif reaction.emoji == "➡":
				await reaction.message.edit(content=ConnectBoard.right())
				await reaction.remove(user)

			elif reaction.emoji == "⬇":
				hasWon, board = ConnectBoard.place()
				if hasWon:
					ListsOfBoards.remove(ConnectBoard)
					await reaction.message.clear_reactions()
				await reaction.message.edit(content=board)
				await reaction.remove(user)

			return

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#				ON TYPING EVENTS				#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#


client.run(TOKEN)
