import asyncio
import websockets
import json
import logging
from typing import Callable, Dict, Any

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstantLLMClient:
    def __init__(self, api_key: str, server_url = "ws://instantllm.ddns.net", show_logs=True):
        self.server_url = server_url
        self.api_key = api_key
        self.websocket_connection = None
        self.send_flags: Dict[str, Any] = {}
        self.message_handler: Callable[[Dict[str, Any]], None] = None
        self.reconnect_flag = True
        self.show_logs = show_logs
        self.show_received_message = True
        self.show_sent_message = True

    def log(self, level, message):
        if self.show_logs:
            if level == 'info':
                logger.info(message)
            elif level == 'error':
                logger.error(message)

    async def connect(self):
        backoff = 1  
        while self.reconnect_flag:
            try:
                self.log('info', 'Connecting to server')
                self.websocket_connection = await websockets.connect(f"{self.server_url}/ws/third_party/{self.api_key}")
                self.log('info', 'Connected to server')
                await self.receive_messages()
            except Exception as e:
                self.log('error', f"Connection failed: {e}")
                if self.reconnect_flag:
                    await asyncio.sleep(backoff)
                    backoff = min(backoff * 2, 60)  # Exponential backoff, max 60 seconds
                else:
                    break

    async def close_connection(self):
        self.reconnect_flag = False
        if self.websocket_connection:
            await self.websocket_connection.close()
            self.log('info', 'Connection closed')

    def set_message_handler(self, handler: Callable[[Dict[str, Any]], None]):
        self.message_handler = handler

    async def send_message(self, token: str, message: Dict[str, Any]) -> bool:
        if token not in self.send_flags:
            self.send_flags[token] = True

        if self.websocket_connection:
            if not self.send_flags[token]:
                self.send_flags[token] = True  # Reset the flag
                return False
            
            await self.websocket_connection.send(json.dumps({
                "token": token,
                "message": message
            }))

            if self.show_sent_message:
                self.log('info', f"Sent message: {message}")
            return True
        return False

    async def receive_messages(self):
        websocket = self.websocket_connection
        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                action = data['message'].get('action')
                token = data['token']

                if self.show_received_message:   
                    self.log('info', f"Received message: {data}")

                if action == 'n/a':
                    self.send_flags[token] = True

                if action == 'STOP':
                    self.send_flags[token] = False
                
                elif self.message_handler:
                    asyncio.create_task(self.message_handler(data))

        except Exception as e:
            self.log('error', f"Connection to server closed: {e}")

    async def run(self):
        self.log('info', 'Connecting to InstantLLM')
        await self.connect()
