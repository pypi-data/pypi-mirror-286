import os
from io import BytesIO
from typing import Literal, Optional

import sounddevice as sd
import soundfile as sf
from openai import OpenAI


class ClientOpenaiAudio:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY is not set")
        self.client_openai = OpenAI(api_key=api_key)

    def get_default_transcribe_model_id(self) -> str:
        return "whisper-1"

    def get_default_tts_model_id(self) -> str:
        return "tts-1"

    def transcribe_for_bytes(
        self,
        audio_bytes: bytes,
    ) -> dict:
        model_id = self.get_default_transcribe_model_id()
        bytes_io = BytesIO(audio_bytes)
        with bytes_io as file:
            transcription = self.client_openai.audio.transcriptions.create(
                model=model_id, file=file, response_format="verbose_json", timestamp_granularities=["word"]
            )
        return transcription.model_dump()

    def transcribe_for_file(
        self,
        path_file_audio: str,
    ) -> dict:
        model_id = self.get_default_transcribe_model_id()
        with open(path_file_audio, "rb") as file:
            transcription = self.client_openai.audio.transcriptions.create(
                model=model_id, file=file, response_format="verbose_json", timestamp_granularities=["word"]
            )
        return transcription.model_dump()

    def text_to_speech_for_file(
        self,
        text: str,
        path_file_audio: str,
        *,
        voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "alloy",
        response_format: Literal["mp3", "opus", "aac", "flac"] = "mp3",
        model_id: Optional[str] = None,
    ) -> None:
        if model_id is None:
            model_id = self.get_default_tts_model_id()
        speech = self.client_openai.audio.speech.create(
            model=model_id,
            voice=voice,
            response_format=response_format,
            input=text,
        )
        speech.write_to_file(path_file_audio)

    def text_to_speech_for_text(
        self,
        text: str,
        *,
        voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "alloy",
        response_format: Literal["mp3", "opus", "aac", "flac"] = "mp3",
        model_id: Optional[str] = None,
    ) -> bytes:
        if model_id is None:
            model_id = self.get_default_tts_model_id()
        speech = self.client_openai.audio.speech.create(
            model=model_id,
            voice=voice,
            response_format=response_format,
            input=text,
        )

        bytes_io = BytesIO()
        for chunk in speech.iter_bytes():
            bytes_io.write(chunk)
            print(f"Buffer size: {bytes_io.tell()}")
        bytes_io.seek(0)
        return bytes_io.read()

    def play(
        self,
        text: str,
    ) -> None:

        spoken_response = self.client_openai.audio.speech.create(
            model="tts-1-hd",
            voice="fable",
            response_format="opus",
            input=text,
        )

        buffer = BytesIO()
        for chunk in spoken_response.iter_bytes(chunk_size=4096):
            buffer.write(chunk)
        buffer.seek(0)

        with sf.SoundFile(buffer, "r") as sound_file:
            data = sound_file.read(dtype="int16")
            sd.play(data, sound_file.samplerate)
            sd.wait()
