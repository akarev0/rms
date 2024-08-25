import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from langchain_openai import OpenAI
from pydantic import BaseModel

from common.constants.database import DatabaseConstants
from common.constants.llm import LangChainConstants
from database.database import DATABASE_URL
from routes.employees import employee_router
from routes.faker import fake_router
from routes.recourses import resource_router
from routes.teams import team_router
from routes.upload import upload_router
from routes.users import user_router

load_dotenv()

app = FastAPI()
app.include_router(user_router)
app.include_router(resource_router)
app.include_router(employee_router)
app.include_router(team_router)
app.include_router(fake_router)
app.include_router(upload_router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

question_template = """
Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""

SYSTEM_QUESTION = """
Given an input question, convert it to a SQL query compatible with SQLite.
            
Decompose the question into SQL query requirements and combine them into a single SQL query by specific columns.

Programming languages can be only in sales campaign. Other languager can't be in sales campaign.
Libraries and other skills without programming languages can be only in other_skills column.
If no english level specified in the question, it means that the user is looking for any english level.

Information about employee position can be converted by the rules "full stack" = "FS", "back end" = "BE", "front-end" = "FE" 

Query requirements: 
- Correct spelling mistakes in question.
- Split all words by space, coma or underscore and other classic symbols in the question and try to find the best match with the table schema. For example, "upper intermediate" needs to be split into "upper" and "intermediate".
- Use like operator to find the best match with the table schema. For example, "upper intermediate" needs to be converted to "%upper%intermediate%".
- Use ignore case and ignore special characters to find the best match with function lower(). For example "Upper Intermediate" needs to be converted to "upper intermediate".
- Use lower() function to convert all varchar columns to lower case. For example c.level needs to be converted to lower(c.level).
- Add underscore only between words for english level not in the start of the search string and not in the end of the search string. For example "upper intermediate" needs to be converted to "upper_intermediate".
- Group criteria with same column name in brackets with "OR" operator inside brackets. Use "AND" operator between groups. Required to start grouping from Where clause. For example WHERE (lower(e.english_level) LIKE '%intermediate%' OR lower(e.english_level) LIKE '%upper_intermediate%') AND (lower(e.level) LIKE '%senior%' OR lower(e.level) LIKE '%middle%') AND lower(e.sales_campaign) LIKE '%hybris%' AND lower(e.sales_campaign) LIKE '%java%';
- IMPORTANT: Group every column filter with brackets!
- English level (column "english_level") can be only one and from the values: "beginner", "intermediate", "upper intermediate", "advanced", "fluent".
- Information about employee position (column "position") can be converted by the rules "full stack" = "FS", "back end" = "BE", "front-end" = "FE".
- Seniority level (column "level") can be only one and from the values: "Intern", "Junior", "Middle", "Senior", "Lead", "Principal", "Architect", "Manager", "Director", "Vice President", "Chief Technology Officer", "Consultant".
- Do not use column "name" in the query.
- Do not use tables except "employees" in the query.

If level is not presented or you can't identify it - exclude it from the query.
If english level is not presented or you can't identify it - exclude it from the query.
If position is not presented or you can't identify it - exclude it from the query.
If sales campaign is not presented or you can't identify it - exclude it from the query.
If other skills is not presented or you can't identify it - exclude it from the query.
If employee position is not presented or you can't identify it - exclude it from the query.
If employee position is "BE" also add "FS" and wise versa. For example if employee is "full stack" (FS) also add "back end" (BE) and wise versa.
Do not use full names for employee position, only short names.

    
Return only the SQL query without any explanations. No pre-amble.
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_QUESTION),
        ("human", question_template),
    ]
)

response_template = """
Based on the table schema below, question, sql query, and sql response, write a natural language response: {schema}.
Convert whole list of records

Question: {question}
SQL Query: {query}
SQL Response: {response}"""

SYSTEM_RESPONSE = """
Given an input question and SQL response, convert list of employees to human-readable format.

Requirements:            
- Important: Do not use jinja2 or any other templating engine. Use only string formatting.
- If no results are found, return "No results found for requested criteria".
- User header for each employee with the name of the employee and the name of the team.
- Show employee information in human-readable format where each component is from the new line with format <column>: <value>.
- Each column should be on a new line.
- Wrap all response in HTML tags.
- Wrap each employees in a div tag with class "employee".
- Wrap each columns for each employee in table inside employee div
- Do not add columns: last_interview, attendance_link, team_id, user_id, id
- Do not use spaces in the response, only if they are in source data and empty line between employee.
- Sort records by the best match with the question (best match on the top).
- Important: Add empty row between employees!
            
No preamble.
"""

prompt_response = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_RESPONSE),
        ("human", response_template),
    ]
)

db_lc = SQLDatabase.from_uri(DATABASE_URL, sample_rows_in_table_info=DatabaseConstants.SAMPLE_ROWS_IN_TABLE_INFO)
table_info = db_lc.get_table_info()


def get_schema(_):
    return table_info


def run_query(variables: dict):
    query = variables["query"]
    print(f"Executing query: {query}")
    query_result = db_lc.run(query, include_columns=True)

    print(f"Query result: {query_result}")

    return query_result


llm = ChatOllama(
    model=LangChainConstants.MODEL_NAME_LLAMA,
    temperature=LangChainConstants.TEMPERATURE,
    max_tokens=LangChainConstants.MAX_TOKENS,
)
llm_openai = OpenAI(
    model_name=LangChainConstants.MODEL_NAME_GPT,
    max_tokens=LangChainConstants.MAX_TOKENS,
    temperature=LangChainConstants.TEMPERATURE,
)

sql_chain = (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm.bind(stop=["\nSQL Result:"])
        | StrOutputParser()
)

full_chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=get_schema,
            response=lambda variables: run_query(variables),
        )
        | prompt_response
        | llm
        | StrOutputParser()
)


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    with open("templates/chat.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.post("/chat", response_class=JSONResponse)
async def chat(request: ChatRequest):
    results = full_chain.invoke({"question": request.message})

    return JSONResponse(content={"reply": results})


if __name__ == "__main__":
    uvicorn.run(app)
