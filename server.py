import asyncio

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


async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr, port = writer.get_extra_info('peername')
    data = None

    while data != b'quit':
        # получаем данные
        try:
            data = await reader.read(1024)  # New
        except ConnectionError:
            print(f'{bcolors.FAIL}Client suddenly closed while receiving from {addr}:{port}{bcolors.ENDC}')
            break
        message = data.decode()
        print(f'{bcolors.OKCYAN}Received message from {addr}:{port}: {message!r}{bcolors.ENDC}')

        # отправляем данные обратно
        try:
            writer.write(data)
            await writer.drain()
            print(f'{bcolors.OKBLUE}Sent {message!r} to: {addr}:{port}{bcolors.ENDC}')
        except ConnectionError:
            print(f'{bcolors.FAIL}Client suddenly closed, cannot send{bcolors.ENDC}')
            break

    writer.close()
    await writer.wait_closed()
    print(f'{bcolors.WARNING}Disconnected by: {addr}:{port}{bcolors.ENDC}')


async def run_server() -> None:
    server = await asyncio.start_server(handle_connection, HOST, PORT)
    print(f'{bcolors.OKGREEN}Server started.{bcolors.ENDC}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server())
