import logging
import asyncio
from aiohttp import web
import config
import jenkins
import github


logger = logging.getLogger(__name__)

class Server(object):
    @classmethod
    def start(cls):
        logger.info('Starting Server...')

        cls.app = web.Application()

        cls.app.router.add_route('post', '/github', github.handle_request)
        cls.app.router.add_route('post', '/gitlab', cls.handle_gitlab)
        cls.app.router.add_route('post', '/jenkins', jenkins.handle_request)

        cls.loop = asyncio.get_event_loop()
        cls.loop.run_until_complete(cls.run())

    @classmethod
    def stop(cls):
        logger.info('Stopping Server...')

        cls.server.close()
        cls.loop.run_until_complete(cls.server.wait_closed())

        cls.loop.run_until_complete(cls.app.shutdown())
        cls.loop.run_until_complete(cls.handler.finish_connections(60.0))
        cls.loop.run_until_complete(cls.app.cleanup())

    @classmethod
    @asyncio.coroutine
    def run(cls):
        cls.handler = cls.app.make_handler()

        cls.server = yield from cls.loop.create_server(cls.handler,
                                                       config.HOST,
                                                       config.PORT)

    @classmethod
    @asyncio.coroutine
    def handle_gitlab(cls, request):
        if not repository_name in config.GITLAB_REPOSITORIES:
            logger.warning('Repository not found')
            return

        return web.Response()
