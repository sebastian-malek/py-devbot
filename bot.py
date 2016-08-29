import logging
import asyncio
import discord
import config


logger = logging.getLogger(__name__)

class Bot(object):
    @classmethod
    def start(cls):
        logging.info('Starting Bot...')

        cls.loop = asyncio.get_event_loop()
        cls.loop.run_until_complete(cls.run())

    @classmethod
    def stop(cls):
        pass

    @classmethod
    @asyncio.coroutine
    def run(cls):
        pass
