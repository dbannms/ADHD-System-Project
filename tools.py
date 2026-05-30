def task_chunker(task, minutes):

    blocks = minutes // 20

    result = f"\nTask: {task}\n\n"

    for i in range(blocks):
        result += f"Step {i+1}: Work for 20 minutes\n"
        result += "Break: 5 minutes\n\n"

    return result


def motivation_recovery():

    return """
1. Take a short break.
2. Relax for a few minutes.
3. Return and complete one small step.
"""


def priority_planner(tasks):

    result = "Priority Task List:\n\n"

    for i, task in enumerate(tasks, start=1):
        result += f"{i}. {task}\n"

    return result