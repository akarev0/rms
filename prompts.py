# prompts.py

from langchain.prompts import PromptTemplate

# Define a prompt for greeting
greeting_prompt = PromptTemplate(
    input_variables=["name"], template="Hello, {name}! How can I assist you today?"
)

# Define a prompt for getting employee details
employee_details_prompt = PromptTemplate(
    input_variables=["employee_name"],
    template="Please provide details for the employee named {employee_name}.",
)

# Define a prompt for listing resources
list_resources_prompt = PromptTemplate(
    input_variables=["skip", "limit"],
    template="List resources starting from {skip} with a limit of {limit}.",
)
