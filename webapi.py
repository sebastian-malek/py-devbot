import logging
import asyncio
from aiohttp import web
import config


logger = logging.getLogger(__name__)

class WebAPI(object):
    @classmethod
    def start(cls):
        logging.info('Starting WebAPI...')

        cls.app = web.Application()
        cls.app.router.add_route('get', '/github', cls.handle_github)

        cls.loop = asyncio.get_event_loop()
        cls.loop.run_until_complete(cls.run())

    @classmethod
    def stop(cls):
        cls.server.close()
        cls.loop.run_until_complete(cls.server.wait_closed())

        cls.loop.run_until_complete(cls.app.shutdown())
        cls.loop.run_until_complete(cls.handler.finish_connections(60.0))
        cls.loop.run_until_complete(cls.app.cleanup())

    @classmethod
    @asyncio.coroutine
    def run(cls):
        cls.handler = cls.app.make_handler()

        cls.server = yield from cls.loop.create_server(cls.handler, config.HOST, config.PORT)

    @classmethod
    @asyncio.coroutine
    def handle_github(cls, request):
        text = 'Hello world'
        return web.Response(body=text.encode('utf-8'))
