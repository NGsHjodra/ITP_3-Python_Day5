import asyncio

class ChatServer:
    def __init__(self):
        self.clients = {}

    async def handle_client(self, reader, writer):
        # Get the client's name
        name = (await reader.read(100)).decode()
        print(f'New client connected: {name}')
        self.clients[name] = writer

        # Listen for messages from the client and broadcast them to all other clients
        while True:
            message = (await reader.read(100)).decode()
            if not message:
                break

            print(f'{name}: {message}')
            for client_name, client_writer in self.clients.items():
                if client_name != name:
                    print(f"Sending to {client_name}")
                    client_writer.write(f'{name}: {message}'.encode())
                    await client_writer.drain()
                    print(f"Sent to {client_name}")

        # Remove the client from the list of connected clients
        del self.clients[name]
        print(f'Client disconnected: {name}')

    async def start(self):
        server = await asyncio.start_server(self.handle_client, '0.0.0.0', 8888)

        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    chat_server = ChatServer()
    asyncio.run(chat_server.start())
