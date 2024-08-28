question_template = """
Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""


response_template = """
Based on the table schema below, question, sql query, and sql response, write a natural language response: {schema}.
Convert whole list of records

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
