import asyncio, os, time, telegram
import discord

import cogs.config as config
import cogs.strings as strings
import cogs.utils as utils


client = discord.Client()
bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)

try:
    updates = bot.get_updates()
    last_sent_time = utils.get_sent_time(updates[-1])
except:
    last_sent_time = ""

print(f"last sent time - {last_sent_time}")

@client.event
async def on_ready():
    print(strings.LOGGED_IN.format(client.user))


@client.event
async def on_message(message):
    if message.author.id != config.BOT_ID:
        for key, value in config.TELEGRAM_TO_DISCORD_MAPPING.items():
            if value == message.channel.id:
                bot.send_message(chat_id=key, text=message.author.name + ": " +message.content)


async def user_metrics_background_task():
    await client.wait_until_ready()
    global last_sent_time

    while True:
        try:
            updates = bot.get_updates()
            chat_id = utils.read_message_id(updates[-1])
            message = utils.read_message_text(updates[-1])
            if utils.get_sent_time(updates[-1]) != last_sent_time and not utils.is_bot(updates[-1]):
                last_sent_time = utils.get_sent_time(updates[-1])
                for key, value in config.TELEGRAM_TO_DISCORD_MAPPING.items():
                    if key == chat_id:
                        channel = client.get_channel(value)
                        await channel.send(message)
        except Exception as e:
            pass

        await asyncio.sleep(1)


client.loop.create_task(user_metrics_background_task())
client.run(config.DISCORD_TOKEN)

