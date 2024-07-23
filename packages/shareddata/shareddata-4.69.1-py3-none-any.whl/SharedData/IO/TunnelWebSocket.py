import asyncio
import websockets
import argparse
import httpx

def get_args():
    parser = argparse.ArgumentParser(description="Websocket tunnel configuration")
    parser.add_argument('--local_host', type=str, default='127.0.0.1', help="Local host address")
    parser.add_argument('--local_port', type=int, default=2222, help="Local port number")
    parser.add_argument('--remote_uri', type=str, required=True, help="Remote WebSocket URI wss://")
    parser.add_argument('--proxy_uri', type=str, required=False, help="Proxy URI http:// or https://")
    return parser.parse_args()

# Configuration
args = get_args()
LOCAL_HOST = args.local_host
LOCAL_PORT = args.local_port
REMOTE_URI = args.remote_uri
PROXY_URI = args.proxy_uri

async def forward_data(websocket, reader, writer):
    try:
        async for message in websocket:
            writer.write(message)
            await writer.drain()
    except Exception as e:
        print(f"Error in forward_data: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def handle_client(reader, writer):
    try:
        websocket = await connect_via_proxy(REMOTE_URI, PROXY_URI)
        # Create tasks for bidirectional data forwarding
        if websocket:
            to_server = asyncio.create_task(forward_socket_to_websocket(reader, websocket))
            to_client = asyncio.create_task(forward_data(websocket, reader, writer))
            
            await asyncio.gather(to_server, to_client)
    except Exception as e:
        print(f"Error in handle_client: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def forward_socket_to_websocket(reader, websocket):
    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break
            await websocket.send(data)
    except Exception as e:
        print(f"Error in forward_socket_to_websocket: {e}")

async def connect_via_proxy(remote_uri, proxy_uri):
    if proxy_uri:
        transport = httpx.AsyncHTTPTransport(
            proxy=proxy_uri,
            verify=True,
        )
        async with httpx.AsyncClient(transport=transport) as client:
            ws = await websockets.connect(remote_uri, http_client=client)
            return ws
    else:
        return await websockets.connect(remote_uri)

async def main():
    server = await asyncio.start_server(handle_client, LOCAL_HOST, LOCAL_PORT)
    async with server:
        print(f"Listening on {LOCAL_HOST}:{LOCAL_PORT}...")
        await server.serve_forever()

if __name__ == "__main__":
    args = get_args()
    asyncio.run(main())
