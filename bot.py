import logging
import discord
import config


logger = logging.getLogger(__name__)

class Bot(object):
    @classmethod
    def start(cls, loop):
        logging.info('Starting Bot...')

        cls.loop = loop

    @classmethod
    def stop(cls):
        pass
