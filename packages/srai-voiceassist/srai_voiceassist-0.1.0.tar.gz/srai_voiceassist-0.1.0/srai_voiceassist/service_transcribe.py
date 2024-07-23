import os
import time
import wave
from datetime import datetime
from queue import Queue
from threading import Thread
from typing import Any

from speech_recognition import AudioData

from srai_voiceassist.client_openai_audio import ClientOpenaiAudio


class ServiceTranscribe:

    def __init__(
        self,
    ) -> None:
        self.thread = None
        self.is_running = False
        self.queue_recording: Queue[Any] = None
        self.queue_transcription = Queue[Any]()
        self.client = ClientOpenaiAudio()

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
        if self.queue_recording is None:
            raise ValueError("Queue recording must be set before starting the service")
        self.is_running = True
        while self.is_running:
            audio = self.queue_recording.get()
            print("Writing audio to file", flush=True)
            name_promt = str(time.mktime(datetime.now().timetuple()))[:-2]
            name_file_wave = name_promt + ".wav"
            with wave.open(name_file_wave, "wb") as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 2 bytes per sample
                wav_file.setframerate(44100)  # 16 kHz sampling rate
                wav_file.writeframes(audio.get_wav_data())

            print("Transcribing!", flush=True)
            transcription = self.client.transcribe_for_bytes(audio)
            self.queue_transcription.put(transcription)
            os.remove(name_file_wave)
            print(f"Transcription done! {self.queue_transcription.qsize()}", flush=True)

    def transcribe_audio(self, audio: AudioData) -> str:
        print("Writing audio to file", flush=True)
        name_promt = str(time.mktime(datetime.now().timetuple()))[:-2]
        name_file_wave = name_promt + ".wav"
        with wave.open(name_file_wave, "wb") as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(44100)  # 16 kHz sampling rate
            wav_file.writeframes(audio.get_wav_data())

        print("Transcribing!", flush=True)
        transcription = self.client.transcribe_for_file(name_file_wave)
        os.remove(name_file_wave)
        return transcription["text"]

    def transcribe_for_file(self, path_file: str) -> str:
        print("Transcribing!", flush=True)
        print(path_file)
        transcription = self.client.transcribe_for_file(path_file)
        # os.remove(name_file_wave)
        return transcription["text"]

    def transcribe_for_bytes(self, audio_bytes: bytes) -> str:
        print(len(audio_bytes))
        print("Transcribing!", flush=True)
        transcription = self.client.transcribe_for_bytes(audio_bytes)
        # os.remove(name_file_wave)
        return transcription["text"]
