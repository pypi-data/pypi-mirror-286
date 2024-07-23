from queue import Queue
from threading import Thread

import speech_recognition as sr
from speech_recognition import AudioData


class ServiceRecord:

    def __init__(
        self,
    ) -> None:
        self.thread = None
        self.is_running = False
        self.queue_recording = Queue()
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 7000
        self.recognizer.pause_threshold = 1.0

    def start(self):
        self.thread = Thread(target=self._start)
        self.thread.start()

    def stop(self):
        self.is_running = False

    def join(self):
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    def _start(self):
        self.is_running = True
        with sr.Microphone() as source:
            print("adjusting for ambient noise", flush=True)
            self.recognizer.adjust_for_ambient_noise(source)
            print("ambient noise adjusted", flush=True)

            while self.is_running:
                print("Listening!", flush=True)
                audio = self.recognizer.listen(source)
                self.queue_recording.put(audio)
                print(f"Recording done! Queue size: {self.queue_recording.qsize()}", flush=True)

    def record_audio(self) -> AudioData:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise", flush=True)
            self.recognizer.adjust_for_ambient_noise(source)
            print("Ambient noise adjusted", flush=True)

            print("Listening!", flush=True)
            audio = self.recognizer.listen(source)
            print("Recording done!", flush=True)
            return audio
