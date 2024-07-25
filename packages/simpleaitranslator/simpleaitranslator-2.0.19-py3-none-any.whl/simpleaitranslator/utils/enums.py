from enum import Enum


class ChatGPTModel(Enum):
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4o = "gpt-4o"

    def __str__(self):
        return self.value