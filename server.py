import logging
import asyncio
from aiohttp import web
import config
from client import Client


logger = logging.getLogger(__name__)

class Server(object):
    @classmethod
    def start(cls):
        logger.info('Starting Server...')

        cls.app = web.Application()

        cls.app.router.add_route('post', '/github', cls.handle_github)
        cls.app.router.add_route('post', '/gitlab', cls.handle_gitlab)

        cls.app.router.add_route('post', '/jenkins', cls.handle_jenkins)

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
                                                       config.SERVER_HOST,
                                                       config.SERVER_PORT)

    @classmethod
    @asyncio.coroutine
    def handle_github(cls, request):
        data = yield from request.json()
        repository_name = data['repository']['full_name']

        if not repository_name in config.GITHUB_REPOSITORIES:
            logger.warning('Repository not found')
            return web.Response()

        branch = data['ref'].split('/')[2]
        commits = data['commits']

        yield from Client.send_message(
            '[**github**] {} commit(s) pushed to {} ({})'
            .format(len(commits), repository_name, branch)
        )

        for commit in commits:
            message = commit['message']
            author_name = commit['author']['name']
            commit_id = commit['id'][:7]

            yield from Client.send_message('{} {} {}'.format(commit_id, author_name, message))

        return web.Response()

    @classmethod
    @asyncio.coroutine
    def handle_gitlab(cls, request):
        if not repository_name in config.GITLAB_REPOSITORIES:
            logger.warning('Repository not found')
            return

        return web.Response()

    @classmethod
    @asyncio.coroutine
    def handle_jenkins(cls, request):
        data = yield from request.json()
        project_name = data['name']

        if not project_name in config.JENKINS_PROJECTS:
            logger.warning('Project not found')
            return web.Response()

        build_status = data['build']['status']
        build_number = data['build']['number']

        status = 'failed :heavy_multiplication_x:'

        if build_status == 'SUCCESS':
            status = 'completed successfully :heavy_check_mark:'

        yield from Client.send_message(
            '[**jenkins**] {}: build {} {}'
            .format(project_name, build_number, status)
        )

        return web.Response()
