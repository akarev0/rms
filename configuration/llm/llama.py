import os
from langchain_ollama import ChatOllama

from common.constants.llm import LLMConstants

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "")

llm = ChatOllama(
    model=LLMConstants.MODEL_NAME_LLAMA,
    temperature=LLMConstants.TEMPERATURE,
    base_url=OLLAMA_HOST,
)
