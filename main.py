from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from langchain_ollama import ChatOllama
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from database.database import DATABASE_URL
from routes.users import user_router
from routes.recourses import resource_router
from routes.employees import employee_router
from routes.teams import team_router
from routes.faker import fake_router
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


load_dotenv()


app = FastAPI()
app.include_router(user_router)
app.include_router(resource_router)
app.include_router(employee_router)
app.include_router(team_router)
app.include_router(fake_router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

question_template = """
Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given an input question, convert it to a SQL query compatible with SQLite."
            "Return only the SQL query without any explanations. No pre-amble.",
        ),
        ("human", question_template),
    ]
)


response_template = """
Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
prompt_response = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given an input question and SQL response, convert it to a natural "
            "language answer. No pre-amble.",
        ),
        ("human", response_template),
    ]
)


db_lc = SQLDatabase.from_uri(DATABASE_URL)


def get_schema(_):
    return db_lc.get_table_info()


def run_query(query: str):
    print(f"Executing query: {query}")
    return db_lc.run(query)


llm = ChatOllama(model="llama3", base_url="http://localhost:11434")

sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm.bind(stop=["\nSQL Result:"])
    | StrOutputParser()
)

full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        schema=get_schema,
        response=lambda vars: run_query(vars["query"]),
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
