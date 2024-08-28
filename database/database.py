import os

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.constants.database import DatabaseConstants

BACKEND_PATH = os.getenv("BACKEND_PATH", "")

DATABASE_URL = f"sqlite:///{os.path.join(BACKEND_PATH, 'test.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

database_langchain = SQLDatabase.from_uri(
    DATABASE_URL,
    sample_rows_in_table_info=DatabaseConstants.SAMPLE_ROWS_IN_TABLE_INFO,
)


def database_langchain_get_schema(_):
    return database_langchain.get_table_info()


def execute_langchain_query(query: str, chain_variables: dict):
    print(f"Variables: {chain_variables}")
    print(f"Executing query: {query}")
    query_result = database_langchain.run(query, include_columns=True)

    print(f"Query result: {query_result}")
    if not query_result:
        return []

    return query_result


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
