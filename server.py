import logging
import asyncio
from aiohttp import web
import config
from client import Client


logger = logging.getLogger(__name__)

class Server(object):
    @classmethod
    def start(cls):
        logging.info('Starting Server...')

        cls.app = web.Application()
        cls.app.router.add_route('post', '/github', cls.handle_github)
        cls.app.router.add_route('post', '/gitlab', cls.handle_gitlab)
        cls.app.router.add_route('post', '/jenkins', cls.handle_jenkins)

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

        cls.server = yield from cls.loop.create_server(cls.handler,
                                                       config.SERVER_HOST,
                                                       config.SERVER_PORT)

    @classmethod
    @asyncio.coroutine
    def handle_github(cls, request):
        repositories = config.GITHUB_REPOSITORIES

        if not repository in repositories:
            logger.warning('Repository not found')
            return

        text = 'Hello world'
        return web.Response(body=text.encode('utf-8'))

    @classmethod
    @asyncio.coroutine
    def handle_gitlab(cls, request):
        repositories = config.GITLAB_REPOSITORIES

        if not repository in repositories:
            logger.warning('Repository not found')
            return

        text = 'Hello world'
        return web.Response(body=text.encode('utf-8'))

    @classmethod
    @asyncio.coroutine
    def handle_jenkins(cls, request):
        projects = config.JENKINS_PROJECTS

        if not project in projects:
            logger.warning('Project not found')
            return

        message = 'Jenkins build completed successfully.'

        yield from Client.send_message(message)

        text = 'Hello world'
        return web.Response(body=text.encode('utf-8'))
