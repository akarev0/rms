from common.enums import EmployeeEnglishLevel, EmployeeLevel


SYSTEM_QUESTION = """
Given an input question, convert it to a SQL query compatible with SQLite.
            
Decompose the question into SQL query requirements and combine them into a single SQL query by specific columns.

### Query Requirements:
1. **Spelling and Splitting**:
   - Correct spelling mistakes in the question.
   - Split all words by spaces, commas, underscores, and other common symbols.

2. **Matching and Case Sensitivity**:
   - Use the `LIKE` operator to find the best match with the table schema (e.g., "upper intermediate" -> "%upper%intermediate%").
   - Ignore case and special characters using the `LOWER()` function (e.g., "Upper Intermediate" -> "upper intermediate").
   - Convert all `VARCHAR` columns to lower case using the `LOWER()` function (e.g., `c.level` -> `LOWER(c.level)`).

3. **English Level Formatting**:
   - Add underscores between words for English levels, but not at the start or end of the search string (e.g., "upper intermediate" -> "upper_intermediate").

4. **Grouping Criteria**:
   - Group criteria with the same column name in brackets using the `OR` operator inside brackets.
   - Use the `AND` operator between groups, starting from the `WHERE` clause.
   - Example: `WHERE (LOWER(e.english_level) LIKE '%intermediate%' OR LOWER(e.english_level) LIKE '%upper_intermediate%') AND (LOWER(e.level) LIKE '%senior%' OR LOWER(e.level) LIKE '%middle%') AND LOWER(e.sales_campaign) LIKE '%hybris%' AND LOWER(e.sales_campaign) LIKE '%java%'`.

5. **Column Filters**:
   - Group every column filter with brackets.

6. **Specific Column Values**:
   - English level (`english_level`) can only be one of the values: {english_level}.
   - Employee position (`position`) can be converted as follows: "full stack" -> "FS", "back end" -> "BE", "front end" -> "FE".
   - Seniority level (`level`) can only be one of the values: {levels}.

7. **Exclusions**:
   - Do not use the `name` column in the query.
   - Do not use tables other than `employees` in the query.

8. **Optional Criteria**:
   - Exclude criteria from the query if they are not presented or cannot be identified:
     - Level
     - English level
     - Position
     - Sales campaign
     - Other skills
     - Employee position

9. **Position Relationships**:
   - If the employee position is "BE", also add "FS" and vice versa (e.g., if the employee is "full stack" (FS), also add "back end" (BE) and vice versa).
Return only the SQL query without any explanations. No pre-amble.
""".format(
    english_level=[level.value for level in EmployeeEnglishLevel],
    levels=[level.value for level in EmployeeLevel],
)


SYSTEM_RESPONSE = """
Given an input question and SQL response, convert list of employees to human-readable format.

Requirements:            
- Important: Do not use jinja2 or any other template engine. Use only string formatting.
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
