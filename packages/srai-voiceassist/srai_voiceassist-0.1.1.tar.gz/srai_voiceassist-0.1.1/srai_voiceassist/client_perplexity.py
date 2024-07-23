import os
from typing import Optional

from openai import OpenAI
from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam


class ClientPerplexity:

    def __init__(self, api_key: Optional[str] = None) -> None:
        if api_key is None:
            api_key = os.getenv("PERPLEXITY_API_KEY")
        if api_key is None:
            raise ValueError("PERPLEXITY_API_KEY is not set")
        self.client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

    def prompt(self, prompt: str) -> str:

        messages = [
            ChatCompletionSystemMessageParam(
                role="system",
                content="You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user.",
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=prompt,
            ),
        ]

        # chat completion without streaming
        response = self.client.chat.completions.create(
            model="llama-3-sonar-large-32k-online",
            messages=messages,
        )
        response_text = response.choices[0].message.content
        if response_text is None:
            raise RuntimeError("Failed to get response text")
        return response_text

    # def prompt_json(self, prompt: str) -> dict:
    #       messages = [
    #         ChatCompletionSystemMessageParam(
    #             role="system",
    #             content="You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user.",
    #         ),
    #         ChatCompletionUserMessageParam(
    #             role="user",
    #             content=prompt,
    #         ),
    #     ]

    #     # chat completion without streaming
    #     response = self.client.chat.completions.create(
    #         model="llama-3-sonar-large-32k-online",
    #         messages=messages,
    #     )
    #     response_text = response.choices[0].message.content
    #     if response_text is None:
    #         raise RuntimeError("Failed to get response text")
    #     return response_text
