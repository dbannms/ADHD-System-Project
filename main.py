from tools import task_chunker

print("ADHD Task Management Agent")
print("--------------------------")

task = input("Enter your task: ")
minutes = int(input("How many minutes will you work? "))

result = task_chunker(task, minutes)

print(result)