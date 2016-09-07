import logging
import asyncio
from aiohttp import web


logger = logging.getLogger(__name__)

class GitHub(object):
    @classmethod
    @asyncio.coroutine
    def handle_request(cls, request):
        event = request.headers.get('X-GitHub-Event', None)

        result = web.Response()

        if event == 'ping':
            result = yield from cls.on_ping(request)
        elif event == 'push':
            result = yield from cls.on_push(request)

        return result

    @classmethod
    @asyncio.coroutine
    def on_ping(cls, request):
        return web.Response()

    @classmethod
    @asyncio.coroutine
    def on_push(cls, request):
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
