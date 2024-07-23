import time
from queue import Queue
from threading import Thread
from typing import Literal

import pyaudio
from pyaudio import PyAudio


class ServicePlayback:

    def __init__(
        self,
        playback_format: Literal["wav"] = "wav",
    ) -> None:
        self.thread = None
        self.is_running = False
        self.queue_playback_buffer = Queue()
        self.client = ClientOpenaiWhisper()
        self.player = PyAudio()
        self.playback_format = playback_format

    def start(self):
        self.thread = Thread(target=self._start)
        self.thread.start()

    def stop(self):
        self.is_running = False

    def join(self):
        self.is_running = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    # Function to stream audio
    def enqueue_bytes(self, data: bytes):
        self.queue_playback_buffer.put(data)

    def _start(self):
        self.is_running = True
        if self.playback_format == "wav":
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            CHUNK = 1024
            # TODO add opus support
        else:
            raise ValueError(f"Invalid playback format {self.playback_format}")

        stream = self.player.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
        print("Playback started", flush=True)
        while self.is_running or not self.queue_playback_buffer.empty():
            print("Playing", flush=True)
            if not self.queue_playback_buffer.empty():
                data = self.queue_playback_buffer.get()
                if self.playback_format == "opus":
                    data = decoder.decode(data, CHUNK)

                print(f"Playing {len(data)} bytes", flush=True)
                stream.write(data)
            else:
                time.sleep(0.1)  # Add a small delay if there's no data to avoid busy waiting
