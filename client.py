import logging
import asyncio
import discord
import config


logger = logging.getLogger(__name__)

class Client(object):
    @classmethod
    def start(cls):
        logging.info('Starting Client...')

        cls.client = discord.Client()

        cls.loop = asyncio.get_event_loop()
        cls.loop.run_until_complete(cls.run())

    @classmethod
    def stop(cls):
        cls.loop.run_until_complete(cls.client.logout())

    @classmethod
    @asyncio.coroutine
    def run(cls):
        token = config.DISCORD_TOKEN

        cls.client.start(token)

    @classmethod
    @asyncio.coroutine
    def send_message(cls, message):
        channel = config.DISCORD_CHANNEL

        yield from cls.client.send_message(channel, message)
