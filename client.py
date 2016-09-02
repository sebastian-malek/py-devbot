import logging
import asyncio
import discord
import config


logger = logging.getLogger(__name__)

class Client(object):
    @classmethod
    def start(cls):
        logger.info('Starting Client...')

        cls.client = discord.Client()

        cls.loop = asyncio.get_event_loop()
        cls.loop.run_until_complete(cls.client.start(config.DISCORD_TOKEN))

    @classmethod
    def stop(cls):
        logger.info('Stopping Client...')

        cls.loop.run_until_complete(cls.client.logout())

    @classmethod
    @asyncio.coroutine
    def send_message(cls, message):
        channel = cls.client.get_channel(config.DISCORD_CHANNEL_ID)

        yield from cls.client.send_message(channel, message)
