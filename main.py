import os
import discord
import requests
import json
import random
from replit import db

client = discord.Client()
bot_token = os.environ['TOKEN']

sad_words = ['sad', 'depressed', 'unhappy', 'miserable']

starter_encouragements = ["Cheer up!", "Don't be sad", "Hang in there"]

def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return quote

def update_encouragements(e):
	if "encouragements" in db.keys():
		encouragements = db["encouragements"]
		encouragements.append(e)
		db["encouragements"] = encouragements
	else:
		db["encouragements"] = [e]

def delete_encourage(i):
	encouragements = db['encouragements']
	if len(encouragements) > i:
		del encouragements[i]
		db['encouragements'] = encouragements


@client.event
async def on_ready():
	print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	msg = message.content
	if msg.startswith("!inspire"):
		random_quote = get_quote()
		await message.channel.send(random_quote)
	
	if any(word in msg for word in sad_words):
		options = starter_encouragements
		if "encouragements" in db.keys():
			options = options + db["encouragements"]
		await message.channel.send(random.choice(options))

	if msg.startswith("!add"):
		m = msg.split("!add ", 1)[1]
		update_encouragements(m)
		await message.channel.send("added to db")
	
	if msg.startswith("!del"):
		encouragements = []
		if "encouragements" in db.keys():
			index = int(msg.split("!del", 1)[1])
			delete_encourage(index)
			encouragements = db["encouragements"]
		await message.channel.send(encouragements)

client.run(bot_token)
