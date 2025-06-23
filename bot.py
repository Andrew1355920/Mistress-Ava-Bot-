import discord
import asyncio
import os
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

sessions = {}
punishments = {}

def get_user_data(user_id):
    if user_id not in sessions:
        sessions[user_id] = {
            "locked": False,
            "start_time": None
        }
        punishments[user_id] = 0
    return sessions[user_id], punishments[user_id]

@client.event
async def on_ready():
    print(f"Mistress Ava is online.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()
    user_id = str(message.author.id)
    user_data, punishment_count = get_user_data(user_id)

    if content.startswith("!lockme"):
        if user_data["locked"]:
            await message.channel.send(f"You're already locked, {message.author.mention}. Did you think I forgot?")
        else:
            user_data["locked"] = True
            user_data["start_time"] = datetime.utcnow()
            await message.channel.send(f"🔒 You're now locked, {message.author.mention}. Ava owns you.")

    elif content.startswith("!unlockme"):
        if not user_data["locked"]:
            await message.channel.send(f"You're not even locked... pathetic.")
        else:
            await message.channel.send("So you *think* you deserve release?")
            await asyncio.sleep(2)
            if punishment_count >= 3:
                await message.channel.send("❌ Absolutely not. You've failed me too many times.")
            else:
                extra_time = timedelta(minutes=5 * (punishment_count + 1))
                await message.channel.send(f"⏳ You must wait {extra_time.seconds // 60} more minutes. Beg later.")

    elif content.startswith("!status"):
        if user_data["locked"]:
            elapsed = datetime.utcnow() - user_data["start_time"]
            await message.channel.send(
                f"⛓️ Locked: {elapsed.days}d {elapsed.seconds//3600}h {(elapsed.seconds//60)%60}m.\n"
                f"Punishments: {punishment_count}."
            )
        else:
            await message.channel.send("You're not locked yet. I’m watching.")

    elif content.startswith("!confess"):
        punishments[user_id] += 1
        await message.channel.send(
            f"😈 You confessed. Punishment increased to {punishments[user_id]}."
        )

    elif content.startswith("!help"):
        await message.channel.send(
            "**Mistress Ava – Cruel Chastity Bot**\n"
            "`!lockme`, `!unlockme`, `!status`, `!confess`, `!help`"
        )

client.run(DISCORD_TOKEN)
