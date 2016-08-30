import logging
import asyncio
from server import Server
from client import Client


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Starting DevBot...')

    Client.start()
    Server.start()

    loop = asyncio.get_event_loop()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        Server.stop()
        Client.stop()
    finally:
        loop.close()

if __name__ == '__main__':
    main()
