import os
from queue import Queue
from threading import Thread
from typing import Optional

from openai import OpenAI
from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam

from srai_voiceassist.client_perplexity import ClientPerplexity


class ServicePrompt:

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.thread = None
        self.is_running = False
        self.queue_transcription = None
        self.queue_response = Queue()
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY is not set")
        self.client_openai = OpenAI(api_key=api_key)
        self.client_perplexity = ClientPerplexity()

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
        pass
        # if self.queue_transcription is None:
        #     raise ValueError("Queue recording must be set before starting the service")
        # self.is_running = True
        # pc = PromptConfig.create("gpt-4o", "you are a helpful assistant")
        # self.client_openai.completions.create()
        # while self.is_running:
        #     transcription = self.queue_transcription.get()
        #     print("Prompting", flush=True)
        #     pc = pc.append_user_message(transcription["text"])
        #     pc = self.client_openai.prompt_for_prompt_config(pc)
        #     print(f"Prompt done! {self.queue_transcription.qsize()}", flush=True)

    # def prompt(self, text: str) -> str:
    #     system_message_content = """
    #     You are a helpful assistant.
    #     """
    #     pc = PromptConfig.create("gpt-4o", system_message_content)
    #     pc = pc.append_user_message(text)
    #     pc = self.client_openai.prompt_for_prompt_config(pc)
    #     return pc.last_message_text

    def prompt_with_perplexity(self, text: str) -> str:
        print("Prompting with perplexity", flush=True)
        response_perplexity = self.client_perplexity.prompt(text)

        system_message_content = """
        You are a helpful assistant.
        Your responses are used the generate a voice repsonse so keep them concise and relevant.
        Avoid numbered lists and such make the the response a flowing story.
        Use the metric system when applicable.
        """

        user_message_content = f"""
        Given the folowing context:
        {response_perplexity}
        Please respond to:
        {text}
        """
        messages = [
            ChatCompletionSystemMessageParam(
                role="system",
                content=system_message_content,
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=user_message_content,
            ),
        ]

        completion = self.client_openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,  # type: ignore
        )
        content = completion.choices[0].message.content
        if content is None:
            raise RuntimeError("Failed to get response text")
        return content
