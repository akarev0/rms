from langchain_core.prompts import ChatPromptTemplate

from chains.employee_match import prompts as skills_extractor_prompt
from common.constants.langchain import LangChainConstants

REQUEST_ANALYSER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            LangChainConstants.SYSTEM_PROMPT,
            skills_extractor_prompt.REQUEST_ANALYSER_SYSTEM_PROMPT,
        ),
        (
            LangChainConstants.HUMAN_PROMPT,
            skills_extractor_prompt.REQUEST_ANALYSER_HUMAN_PROMPT,
        ),
    ]
)

QUERY_BUILDER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            LangChainConstants.SYSTEM_PROMPT,
            skills_extractor_prompt.QUERY_BUILDER_SYSTEM_PROMPT,
        ),
        (
            LangChainConstants.HUMAN_PROMPT,
            skills_extractor_prompt.QUERY_BUILDER_HUMAN_PROMPT,
        ),
    ]
)

HTML_RESPONSE_BUILDER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            LangChainConstants.SYSTEM_PROMPT,
            skills_extractor_prompt.HTML_RESPONSE_BUILDER_SYSTEM_PROMPT,
        ),
        (
            LangChainConstants.HUMAN_PROMPT,
            skills_extractor_prompt.HTML_RESPONSE_BUILDER_HUMAN_PROMPT,
        ),
    ]
)
