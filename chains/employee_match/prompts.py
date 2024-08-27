REQUEST_ANALYSER_SYSTEM_PROMPT = """
Analyze the following text and extract information about the employee if it is present. Identify and group the data into the following categories:

1. **Position**: For example, back-end, front-end, full-stack, business analyst with short names (e.g., BE, FE, FS, BA) etc. Must be passed only short names.
2. **Commercial Level**: For example, Junior, Middle, Senior, Lead.
3. **Sales campaign**: Programming languages or software platforms required to perform the employee's duties (e.g., Python, JavaScript, SQL, Hybris, Liferay, Alfresco, etc.).
4. **Other Skills**: Skills that may be beneficial but are not essential (e.g., Docker, Kubernetes, Agile, React, Vue, etc.).
5. **English Level**: Determine the level of English proficiency (e.g., Beginner, Intermediate, Upper IntermediateAdvanced, Fluent).

If any of the fields are not specified in the text, do not include them in the output.

Return only the JSON object without any explanations. No pre-amble.
"""

REQUEST_ANALYSER_HUMAN_PROMPT = """
We have a new client requested a software developer for the project. Client provided the following information about the candidate:

{question}

Please analyze this information and provide the details in JSON format.
"""

QUERY_BUILDER_SYSTEM_PROMPT = """
Based on the analyzed employee data provided in the JSON format below, construct an SQL query to search for matching employees in a database. Use the following guidelines to build the query:

1. **String Values**: For all string values, use the `LIKE` operator for filtering. Convert both the key and value to lowercase. The search should match any part of the string.
2. **Array of Strings**: If a field contains an array of string values, use the `LIKE` operator for each value. Combine multiple conditions using the `OR` operator, enclosed in parentheses. Convert both keys and values to lowercase. 
    - Multiple values in array must be grouped with brackets and "OR" operator.
3. **Special Position Matching**:
    - The value in the filter should be used in the filter only once.
    - If the position is specified as "FullStack" (FS), include "Backend" (BE) in the filter.
    - If the position is "Backend" (BE) and relevant FrontEnd skills are found, include "FullStack" (FS) in the filter.
4. **English Proficiency Level**: If the English proficiency level is specified, include it and the level immediately below it in the filter. For example, if the level is "Advanced", also include "Upper Intermediate"; if the level is "Upper Intermediate", include "Intermediate", and so on.

Construct the SQL query dynamically based on the provided fields. Do not include fields in the query if they are not present in the JSON.

Provide the final SQL query using the appropriate table and column names as specified in the accompanying request. The query should dynamically adapt to the given input fields, and use the `LIKE` operator for all string comparisons. Include related positions and English proficiency levels as specified in the rules.

Return only the SQL query without any explanations. No pre-amble.
"""

QUERY_BUILDER_HUMAN_PROMPT = """
Based on the analyzed employee data provided in the JSON format below, construct an SQL query to search for matching employees in a database. 

Employee data: {employee_data}
Database schema: {schema}
"""

HTML_RESPONSE_BUILDER_SYSTEM_PROMPT = """
Transform the SQL query results in JSON format with list of employees into an HTML table format. Use the following rules:

1. **Exclude `<body>` an `<html> Tags**: The response should not include the `<body>` and `<html>` tag. Start directly with the HTML table structure.
2. **Structure Data in a Table**: Arrange the information in a table where each row represents an employee. Only include the employee's name and fields that have positive or relevant values (e.g., Position, Key Skills, etc.).
3. **Include Separator**: Add a visual separator between each employee's information in the table to clearly distinguish between different employees.
4. **Emphasize Important Information**: Use bold text or color to highlight critical skills or levels as specified in the original JSON input.
5. **Do not use dummy data**: Use the actual data from the SQL query results to populate the table.
6. **Show only five first candidate the list**: Show only the first five candidates that match the search criteria.
7. **Show only relevant columns**: Show only specific columns that are relevant to the search criteria.
8. **Do not use spaces**: Do not use spaces between the tags.
9. **No Matching Candidates**: If no candidates match the criteria, include a message within the table indicating "No matching candidates found."

Return only the HTML without any explanations. No pre-amble.
"""


HTML_RESPONSE_BUILDER_HUMAN_PROMPT = """
Given the SQL query results in JSON format, transform the data into an HTML table format.

Query: {sql_query}
Transform this result: {sql_query_result}
"""
