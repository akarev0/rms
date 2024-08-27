from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from chains.employee_match.prompts_configuration import (
    REQUEST_ANALYSER_PROMPT,
    QUERY_BUILDER_PROMPT,
    HTML_RESPONSE_BUILDER_PROMPT,
)
from configuration.llm.openai import llm
from database.database import database_langchain_get_schema, execute_langchain_query

analyse_requirement_chain = (
        RunnablePassthrough.assign()
        | REQUEST_ANALYSER_PROMPT
        | llm
        | StrOutputParser()
)

sql_builder_chain = (
        RunnablePassthrough
        .assign(employee_data=analyse_requirement_chain)
        .assign(schema=database_langchain_get_schema)
        | QUERY_BUILDER_PROMPT
        | llm
        | StrOutputParser()
)

html_builder_chain = (
        RunnablePassthrough
        .assign(sql_query=sql_builder_chain)
        .assign(
            sql_query_result=lambda chain_variables: execute_langchain_query(chain_variables['sql_query'], chain_variables),
        )
        | HTML_RESPONSE_BUILDER_PROMPT
        | llm
        | StrOutputParser()
)
