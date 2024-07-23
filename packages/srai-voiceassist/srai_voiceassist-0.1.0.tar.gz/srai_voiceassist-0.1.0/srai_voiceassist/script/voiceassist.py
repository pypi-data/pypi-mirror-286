from srai_voiceassist.client_openai_audio import ClientOpenaiAudio
from srai_voiceassist.service_prompt import ServicePrompt
from srai_voiceassist.service_record import ServiceRecord
from srai_voiceassist.service_transcribe import ServiceTranscribe


def main():
    service_record = ServiceRecord()
    service_transcribe = ServiceTranscribe()
    service_prompt = ServicePrompt()
    client_openai_audio = ClientOpenaiAudio()

    while True:
        audio = service_record.record_audio()
        text = service_transcribe.transcribe_audio(audio)
        response = service_prompt.prompt_with_perplexity(text)
        client_openai_audio.play(response)


if __name__ == "__main__":
    main()
