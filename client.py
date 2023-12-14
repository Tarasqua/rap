import asyncio
import argparse
import json

HOST = '127.0.0.1'
PORT = 9999


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


async def run_client(messages: list, delay: int) -> None:
    reader, writer = await asyncio.open_connection(HOST, PORT)

    while True:
        if messages:
            await asyncio.sleep(delay)
            message = messages.pop(0)
            writer.write(f'{message}'.encode())
            await writer.drain()
            print(f'{bcolors.OKBLUE}Sent {message!r}{bcolors.ENDC}')
        else:
            writer.write(b'quit')
            await writer.drain()
            break

        data = await reader.read(1024)
        if not data:
            raise Exception(f'{bcolors.FAIL}Socket closed{bcolors.ENDC}')
        print(f'{bcolors.OKCYAN}Received: {data.decode()!r}{bcolors.ENDC}')


async def run_client_json(messages: list, delay: int):
    reader, writer = await asyncio.open_connection(HOST, PORT)

    while True:
        if messages:
            await asyncio.sleep(delay)
            message = messages.pop(0)
            writer.write(bytes(json.dumps(message), encoding="utf-8"))
            await writer.drain()
            print(f'{bcolors.OKBLUE}Sent {message!r}{bcolors.ENDC}')
        else:
            writer.write(b'quit')
            await writer.drain()
            break

        data = await reader.read(1024)
        if not data:
            raise Exception(f'{bcolors.FAIL}Socket closed{bcolors.ENDC}')
        print(f'{bcolors.OKCYAN}Received: {data.decode()!r}{bcolors.ENDC}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Async client')
    parser.add_argument('seconds_delay', type=int, help='Delay between requests')
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client_json(
        [{'id': 1, "name": 'Kirill'},
         {'id': 2, 'name': 'Darina'},
         {'id': 3, 'name': 'Egor'},
         {'id': 4, 'name': 'Rusik'}],
        args.seconds_delay))
