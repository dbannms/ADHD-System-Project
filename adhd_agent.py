import os
import google.generativeai as genai

from knowledge_base import RULES
from tools import task_chunker, motivation_recovery, priority_planner

# ====================================
# GEMINI API KEY
# ====================================

os.environ["GOOGLE_API_KEY"] = ""

genai.configure(
    api_key=os.environ["GOOGLE_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

# ====================================
# ADHD AGENT
# ====================================

print("\n===================================")
print(" ADHD TASK MANAGEMENT AGENT")
print("===================================")

while True:

    user_input = input(
        "\nAsk the ADHD Agent (type 'exit' to quit): "
    )

    if user_input.lower() == "exit":
        print("\nGoodbye!")
        break

    thought = ""
    rule_match = ""
    action = ""
    tool_output = ""

    # ====================================
    # CASE 1 - MULTIPLE ASSIGNMENTS
    # ====================================

    if (
        "assignment" in user_input.lower()
        and (
            "5" in user_input.lower()
            or "many" in user_input.lower()
            or "overwhelmed" in user_input.lower()
        )
    ):

        thought = "User is overwhelmed by multiple assignments."

        rule_match = "multiple_tasks"

        action = "priority_planner()"

        tool_output = priority_planner(
            [
                "Assignment 1",
                "Assignment 2",
                "Assignment 3",
                "Assignment 4",
                "Assignment 5",
            ]
        )

    # ====================================
    # CASE 2 - DISTRACTED
    # ====================================

    elif "distracted" in user_input.lower():

        thought = "User is experiencing frequent distraction."

        rule_match = "distracted"

        action = "motivation_recovery()"

        tool_output = motivation_recovery()

    # ====================================
    # CASE 3 - LOST MOTIVATION
    # ====================================

    elif "motivation" in user_input.lower():

        thought = "User has lost motivation."

        rule_match = "lost_motivation"

        action = "motivation_recovery()"

        tool_output = motivation_recovery()

    # ====================================
    # CASE 4 - CANNOT START TASK
    # ====================================

    elif "cannot start" in user_input.lower():

        thought = "User cannot start the task."

        rule_match = "cannot_start"

        action = "task_chunker()"

        tool_output = task_chunker(
            "Assignment",
            60
        )

    # ====================================
    # CASE 5 - LARGE PROJECT
    # ====================================

    elif "project" in user_input.lower():

        thought = "User feels overwhelmed by a large project."

        rule_match = "overwhelmed"

        action = "task_chunker()"

        tool_output = task_chunker(
            "Large Project",
            120
        )

    # ====================================
    # DEFAULT
    # ====================================

    else:

        thought = "General ADHD support request."

        rule_match = "general"

        action = "Gemini reasoning"

    # ====================================
    # PROMPT
    # ====================================

    prompt = f"""
You are an ADHD Task Management Agent.

Expert Knowledge:
{RULES}

User Question:
{user_input}

Tool Result:
{tool_output}

Instructions:
1. Use the expert rules.
2. Give short and clear recommendations.
3. Use calm and supportive language.
4. Explain reasoning briefly.

Output format:

REASONING:
...

RECOMMENDATIONS:
1.
2.
3.
"""

    response = model.generate_content(prompt)

    # ====================================
    # EXECUTION TRACE
    # ====================================

    print("\n===================================")
    print(" AI EXECUTION TRACE")
    print("===================================")

    print("\nTHOUGHT:")
    print(thought)

    print("\nRULE MATCH:")
    print(rule_match)

    print("\nACTION:")
    print(action)

    if tool_output != "":
        print("\nTOOL OUTPUT:")
        print(tool_output)

    # ====================================
    # FINAL RESPONSE
    # ====================================

    print("\n===================================")
    print(" FINAL RESPONSE")
    print("===================================\n")

    print(response.text)
