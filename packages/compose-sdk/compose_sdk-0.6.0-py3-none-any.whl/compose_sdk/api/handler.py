import ssl
import websockets
import queue
import urllib.parse
import sys
import math

from ..scheduler import Scheduler
from ..core import EventType
from .ws_message import (
    encode_json,
    encode_ws_message,
    decode_file_transfer_message,
    decode_json_message,
)

from .constants import WS_CLIENT


class DisconnectionError(Exception):
    pass


class APIHandler:
    def __init__(
        self,
        scheduler: Scheduler,
        isDevelopment: bool,
        apiKey: str,
        package_name: str,
        package_version: str,
    ) -> None:
        self.scheduler = scheduler

        self.isDevelopment = isDevelopment
        self.apiKey = apiKey
        self.package_name = package_name
        self.package_version = package_version

        self.reconnection_interval = WS_CLIENT["RECONNECTION_INTERVAL"][
            "BASE_IN_SECONDS"
        ]

        self.listeners: dict[str, callable] = {}

        self.ws = None
        self.is_connected = False
        self.push = None

        self.send_queue = queue.Queue()

    def add_listener(self, id: str, listener: callable) -> None:
        if id in self.listeners:
            raise ValueError(f"Listener with id {id} already exists")

        self.listeners[id] = listener

    def remove_listener(self, id: str) -> None:
        if id not in self.listeners:
            return

        del self.listeners[id]

    def connect(self, on_connect_data: dict) -> None:
        self.scheduler.run_until_complete(self.__makeConnectionRequest(on_connect_data))

    async def send(self, data: object, sessionId: str | None = None) -> None:
        headerStr = (
            data["type"]
            if data["type"] == EventType.SdkToServer.INITIALIZE
            else data["type"] + sessionId
        )

        binary = encode_ws_message(headerStr, encode_json(data))

        if self.is_connected == True:
            await self.push(binary)
        else:
            self.send_queue.put(binary)

    async def __makeConnectionRequest(self, on_connect_data: dict) -> None:
        WS_URL = (
            WS_CLIENT["URL"]["DEV"] if self.isDevelopment else WS_CLIENT["URL"]["PROD"]
        )

        headers = {
            WS_CLIENT["CONNECTION_HEADERS"]["API_KEY"]: self.apiKey,
            WS_CLIENT["CONNECTION_HEADERS"]["PACKAGE_NAME"]: self.package_name,
            WS_CLIENT["CONNECTION_HEADERS"]["PACKAGE_VERSION"]: self.package_version,
        }

        ssl_context = None
        if not self.isDevelopment:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED

        try:
            async with websockets.connect(
                uri=WS_URL, extra_headers=headers, ssl=ssl_context
            ) as ws:
                try:
                    print("🌐 Connected to Compose server.")

                    self.current_backoff_multiplier = 1
                    self.is_connected = True

                    async def push(data):
                        if ws is not None:
                            await ws.send(data)

                    self.push = push

                    await self.send(on_connect_data)

                    async for message in ws:
                        self.__flush_send_queue()
                        await self.__on_message(message)

                except websockets.ConnectionClosed as e:
                    self.is_connected = False
                except Exception as e:
                    self.is_connected = False
                finally:
                    raise DisconnectionError(
                        "Disconnected from Compose server during connection"
                    )

        except Exception as e:
            reconnect_after = self.reconnection_interval
            self.reconnection_interval *= math.ceil(
                WS_CLIENT["RECONNECTION_INTERVAL"]["BACKOFF_MULTIPLIER"]
            )

            if isinstance(e, DisconnectionError):
                print(
                    f"🔄 Disconnected from Compose server. Attempting to reconnect after {reconnect_after} seconds...",
                )

            elif hasattr(e, "headers"):
                try:
                    error_reason = urllib.parse.unquote(
                        e.headers.get(WS_CLIENT["ERROR_RESPONSE_HEADERS"]["REASON"])
                    )
                    error_code = urllib.parse.unquote(
                        e.headers.get(WS_CLIENT["ERROR_RESPONSE_HEADERS"]["CODE"])
                    )
                    print(
                        f"\n🔴 {error_reason}\nError Code: {error_code}\n",
                        file=sys.stderr,
                    )
                    return
                except Exception as e:
                    print(e)

            else:
                print(
                    f"🔄 Failed to connect to Compose server. Attempting to reconnect after {reconnect_after} seconds...",
                )

            await self.scheduler.sleep(reconnect_after)
            await self.__makeConnectionRequest(on_connect_data)

            return

    async def __on_message(self, message) -> None:
        # First 2 bytes are always event type
        event_type = message[:2].decode("utf-8")

        if event_type == EventType.ServerToSdk.FILE_TRANSFER:
            data = decode_file_transfer_message(message)
        else:
            data = decode_json_message(message)

        for listener in self.listeners.values():
            listener(data)

    def __flush_send_queue(self) -> None:
        if self.is_connected:
            while not self.send_queue.empty():
                binary = self.send_queue.get()
                self.scheduler.create_task(self.ws.send(binary))
