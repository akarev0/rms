from database.database import (
    database_langchain_get_schema,
    execute_langchain_query,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from configuration.llm.llama import llm
from chains.employee_match.v2.prompts_configuration import prompt, prompt_response

sql_chain = (
    RunnablePassthrough.assign(schema=database_langchain_get_schema)
    | prompt
    | llm.bind(stop=["SQL Result:"])
    | StrOutputParser()
)

full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        schema=database_langchain_get_schema,
        response=lambda variables: execute_langchain_query(
            variables["query"], variables
        ),
    )
    | prompt_response
    | llm
    | StrOutputParser()
)
