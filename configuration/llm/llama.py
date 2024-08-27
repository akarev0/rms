from langchain_ollama import ChatOllama

from common.constants.llm import LLMConstants

llm = ChatOllama(
    model=LLMConstants.MODEL_NAME_LLAMA,
    temperature=LLMConstants.TEMPERATURE,
    max_tokens=LLMConstants.MAX_TOKENS,
)