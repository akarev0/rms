from langchain_core.prompts import ChatPromptTemplate
from chains.employee_match.v2.prompts import SYSTEM_QUESTION, SYSTEM_RESPONSE
from chains.employee_match.v2.templates import question_template, response_template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_QUESTION),
        ("human", question_template),
    ]
)


prompt_response = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_RESPONSE),
        ("human", response_template),
    ]
)
