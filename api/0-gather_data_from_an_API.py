#!/usr/bin/python3
""" Library to gather data from an API """

import requests
import sys
""" Function to gather data from an API """

if __name__ == "__main__":
    employee_id = sys.argv[1]

    user_url = "https://jsonplaceholder.typicode.com/users/{}".format(
        employee_id)
    todo_url = "https://jsonplaceholder.typicode.com/todos?userId={}".format(
        employee_id)

    user_info = requests.request("GET", user_url).json()
    todo_info = requests.request("GET", todo_url).json()

    employee_name = user_info.get("name")
    task_completed = list(
        filter(lambda x: (x["completed"] is True), todo_info))
    task_completed_count = len(task_completed)
    total_tasks = len(todo_info)

    print("Employee {} is done with tasks({}/{}):".format(employee_name,
          task_completed_count, total_tasks))

    [print("\t {}".format(task.get("title"))) for task in task_completed]
