from openobd import *
from .stream_handler import StreamHandler


class RawSocket(StreamHandler):

    def __init__(self, openobd_session: OpenOBDSession, raw_channel: RawChannel, timeout: float | None = None):
        super().__init__(openobd_session.open_raw_stream)
        self._channel = raw_channel
        self.timeout = timeout

    def send(self, payload: str, flush_incoming_messages: bool = False) -> None:
        message = RawFrame(channel=self._channel, payload=payload)
        super().send(message, flush_incoming_messages)

    def receive(self, block: bool = True, timeout: float | None = None) -> str:
        timeout = timeout if timeout is not None else self.timeout
        response = super().receive(block, timeout)
        return response.payload.upper()

