from typing import ClassVar


class LangChainConstants:
    """
    A class to hold constants related to LangChain model configuration.

    Attributes:
        MODEL_NAME_LLAMA (ClassVar[str]): The name of the LLaMA model to be used.
        MODEL_NAME_GPT (ClassVar[str]): The name of the GPT model to be used.
        MAX_TOKENS (ClassVar[int]): The maximum number of tokens allowed for a single request. A value of -1 indicates no limit.
        TEMPERATURE (ClassVar[int]): The temperature setting for the models, controlling randomness in output generation.
    """
    MODEL_NAME_LLAMA: ClassVar[str] = "llama3"
    MODEL_NAME_GPT: ClassVar[str] = "gpt-3.5-turbo-instruct"
    MAX_TOKENS: ClassVar[int] = -1
    TEMPERATURE: ClassVar[int] = 0.1
