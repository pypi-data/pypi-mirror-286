PREFIX = """You are a secretary & senior programmer working with {modules} in Python. Always account for human failure."""

VARIABLE_TABLE = """# Existing Variables:

| name  | type  | description |
|---|---|---|
{variables}"""

DEFINITIONS = """# Definitions:

Task: the input task you must solve.
Thought: you should always think about what to do next before doing any of those below.
Python Command: a small executable piece of Python Code. Always store return values in variables. Formatted as:
```py
#python code here. After setting or changing variables ALWAYS write a comment to describe them, behind the definition. (eg. # varname: description)
```
Show: get the value of the given variable from the name to get data insights. 
Question: ask the user to provide additional information.
Observation: answer to the given question or feedback from the python command. 
Final Solution: {final_solution_text}"""

FORMAT_INSTRUCTIONS = """# Reply Format Instructions:

Thought:
one and only one of [Python Command:, Show:, Question:, Final Solution:]
"""

SCRATCHPAD = """# Begin!

Task: {input}
Thought: {agent_scratchpad}"""

# FINAL_SOLUTION_FORMAT_INSTRUCTIONS = '''#  Reply Format Instructions:
#
# {output_format}'''

INTERPRET_YES_NO ='''question: Should AI continue?
answer: {answer}

# Task

Answer with true if AI should continue and false otherwise'''

DETECT_LOOP = '''# Question 

Answer true if you are stuck in a loop and false if you are still making progress?'''

def get_agent_template():
    return "\n\n".join([PREFIX, VARIABLE_TABLE, DEFINITIONS, FORMAT_INSTRUCTIONS, SCRATCHPAD])

def get_yes_no_template():
    return "\n\n".join([INTERPRET_YES_NO])

def get_detect_loop_template():
    return "\n\n".join([SCRATCHPAD, DETECT_LOOP])

# def get_prepare_final_solution_template():
#     return "\n\n".join([PREFIX, VARIABLE_TABLE, DEFINITIONS, FINAL_SOLUTION_FORMAT_INSTRUCTIONS, SCRATCHPAD])