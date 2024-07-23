import asyncio
import websockets
import argparse
from urllib.parse import urlparse
import aiohttp

def get_args():
    parser = argparse.ArgumentParser(description="WebSocket tunnel configuration")
    parser.add_argument('--local_host', type=str, default='127.0.0.1', help="Local host address")
    parser.add_argument('--local_port', type=int, default=2222, help="Local port number")
    parser.add_argument('--remote_uri', type=str, required=True, help="Remote WebSocket URI wss://")
    parser.add_argument('--proxy', type=str, help="Proxy server address in the format http://user:pass@host:port")
    return parser.parse_args()

# Configuration
args = get_args()
LOCAL_HOST = args.local_host
LOCAL_PORT = args.local_port
REMOTE_URI = args.remote_uri
PROXY = args.proxy

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
        # Create a proxy URL if a proxy is provided
        if PROXY:
            proxy_url = urlparse(PROXY)
            proxy = f"http://{proxy_url.hostname}:{proxy_url.port}"
            auth = aiohttp.BasicAuth(proxy_url.username, proxy_url.password) if proxy_url.username else None
            ws_kwargs = {"proxy": proxy, "proxy_auth": auth}
        else:
            ws_kwargs = {}

        async with websockets.connect(REMOTE_URI, **ws_kwargs) as websocket:
            # Create tasks for bidirectional data forwarding
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

async def main():
    server = await asyncio.start_server(handle_client, LOCAL_HOST, LOCAL_PORT)
    async with server:
        print(f"Listening on {LOCAL_HOST}:{LOCAL_PORT}...")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
