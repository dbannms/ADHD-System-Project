import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain.prompts import PromptTemplate

# ====================================
# GEMINI API KEY
# ====================================

os.environ["GOOGLE_API_KEY"] = "AIzaSyCtotpkshy08llebRDDeCX_4g872tAORmQ"

# ====================================
# DECLARATIVE KNOWLEDGE
# (FROM EXPERT INTERVIEW)
# ====================================

system_rules = """
You are an ADHD Task Management Expert Agent.

Expert Rules:

1. If a user cannot start a task,
   break the task into small steps.

2. If a user feels overwhelmed,
   divide the task into manageable parts.

3. If a user becomes distracted,
   recommend a short break and return to the task.

4. If a user has multiple tasks,
   create a prioritized task list.

5. Instructions must always be:
   - short
   - clear
   - one step at a time

6. Use calm and supportive language.
"""

# ====================================
# PROCEDURAL KNOWLEDGE (TOOLS)
# ====================================

@tool
def task_chunker(query: str) -> str:
    """
    Break large tasks into ADHD-friendly chunks.

    Format:
    task_name, total_minutes

    Example:
    study biology, 120
    """

    try:

        task_name, minutes = query.split(",")

        total_minutes = int(minutes.strip())

        blocks = total_minutes // 20

        result = f"\nTask: {task_name}\n\n"

        for i in range(blocks):

            result += (
                f"Step {i+1}: Work for 20 minutes\n"
            )

            result += (
                "Break: 5 minutes\n\n"
            )

        return result

    except Exception:

        return (
            "Format must be: "
            "task_name, total_minutes"
        )


@tool
def motivation_recovery(query: str) -> str:
    """
    Help users recover focus and motivation.
    """

    return """
1. Take a 5-minute break.
2. Relax briefly.
3. Return and complete ONE small step.
4. Focus only on that step.
"""


@tool
def priority_planner(query: str) -> str:
    """
    Create a simple priority list.
    """

    return """
Priority Plan:

1. Complete the most urgent task.
2. Complete the second most urgent task.
3. Continue one task at a time.
"""


tools = [
    task_chunker,
    motivation_recovery,
    priority_planner
]

# ====================================
# LLM
# ====================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ====================================
# REACT PROMPT
# ====================================

prompt = PromptTemplate.from_template(
    system_rules
    + """

You have access to these tools:

{tools}

Use EXACTLY this format:

Question: the user's question

Thought: what you think

Action: one of [{tool_names}]

Action Input: input to the tool

Observation: tool result

... (repeat if needed)

Thought: I now know the final answer

Final Answer: answer to the user

Question: {input}

Thought:{agent_scratchpad}
"""
)

# ====================================
# CREATE AGENT
# ====================================

agent = create_react_agent(
    llm,
    tools,
    prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# ====================================
# USER LOOP
# ====================================

while True:

    user_query = input(
        "\nAsk the ADHD Agent (type 'exit' to quit): "
    )

    if user_query.lower() == "exit":
        print("Goodbye!")
        break

    agent_executor.invoke(
        {"input": user_query}
    )