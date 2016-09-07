import logging
import asyncio
from aiohttp import web


logger = logging.getLogger(__name__)

class Jenkins(object):
    @classmethod
    @asyncio.coroutine
    def handle_request(cls, request):
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