import logging
import asyncio
from webapi import WebAPI
from bot import Bot


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Starting DevBot...')

    Bot.start()
    WebAPI.start()

    loop = asyncio.get_event_loop()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        WebAPI.stop()
        Bot.stop()
    finally:
        loop.close()

if __name__ == '__main__':
    main()
