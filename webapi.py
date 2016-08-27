import logging


logger = logging.getLogger(__name__)

class WebAPI(object):
    @classmethod
    def start(cls, loop):
        logging.info('Starting WebAPI...')

        cls.loop = loop

    @classmethod
    def stop(cls):
        pass
