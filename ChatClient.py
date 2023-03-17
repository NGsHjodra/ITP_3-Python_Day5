import asyncio
import aioconsole

class ChatClient:
    def __init__(self, name):
        self.name = name

    # read messages from the server and print them to the console
    async def receive_messages(self, reader):
        while True:
            print("Waiting for message")
            message = await reader.readline()
            print("Message received")
            if not message:
                break
            print(message.decode().rstrip())


    # read messages from the user and send them to the server
    async def send_messages(self, writer):
        print(f'Enter messages to send to the server. Enter "exit" to exit.')
        while True:
            message = await aioconsole.ainput()
            if message == 'exit':
                break

            print(f'Sending: {message}')
            writer.write((message + "\n").encode())
            # writer.write_eof()
            await writer.drain()


    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection('10.237.4.38', 8888)
        self.writer.write(self.name.encode())
        await self.writer.drain()

        # get event loop
        loop = asyncio.get_event_loop()

        # start a task to send messages to the server
        # loop.run_until_complete(self.receive_messages(self.reader))
        # loop.run_until_complete(self.send_messages(self.writer))

        t2 = asyncio.create_task(self.receive_messages(self.reader))
        t1 = asyncio.create_task(self.send_messages(self.writer))

        # await asyncio.create_task(self.receive_messages(self.reader))
        # await asyncio.create_task(self.send_messages(self.writer))
        # #
        await asyncio.gather(t1, t2)

if __name__ == '__main__':
    name = input('Enter your name: ')
    client = ChatClient(name)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(client.connect())
    except KeyboardInterrupt:
        pass

    loop.close()
