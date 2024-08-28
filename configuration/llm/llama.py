from langchain_ollama import ChatOllama

from common.constants.llm import LLMConstants

llm = ChatOllama(
    model=LLMConstants.MODEL_NAME_LLAMA,
    temperature=LLMConstants.TEMPERATURE,
    base_url="http://localhost:11434/api/chat",
)
