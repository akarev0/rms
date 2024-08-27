from langchain_openai import OpenAI

from common.constants.llm import LLMConstants

llm = OpenAI(
    model_name=LLMConstants.MODEL_NAME_GPT,
    max_tokens=LLMConstants.MAX_TOKENS,
    temperature=LLMConstants.TEMPERATURE,
)
