s is our magic toy factory!
import os

# Our toy blueprints (your new code!)
scripts = {
    "0-gather_data_from_an_API.py": """#!/usr/bin/python3
"""API data gathering script"""
import requests
import sys


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
""",

    "1-export_to_CSV.py": """#!/usr/bin/python3
"""Script to export employee TODO list to CSV format"""
import csv
import requests
import sys


if __name__ == "__main__":
    employee_id = sys.argv[1]

    # Fetch user data
    user_url = "https://jsonplaceholder.typicode.com/users/{}".format(
        employee_id)
    todo_url = "https://jsonplaceholder.typicode.com/todos?userId={}".format(
        employee_id)

    user_info = requests.request("GET", user_url).json()
    todo_info = requests.request("GET", todo_url).json()

    username = user_info.get("username")

    # Prepare CSV filename
    csv_filename = "{}.csv".format(employee_id)

    # Export data to CSV
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        
        for task in todo_info:
            csv_writer.writerow([
                employee_id,
                username,
                task.get("completed"),
                task.get("title")
            ])
""",

    "2-export_to_JSON.py": """#!/usr/bin/python3
"""Python script that exports data in the JSON format"""
import json
import requests
from sys import argv


if __name__ == "__main__":
    # Request user info by employee ID
    request_employee = requests.get(
        'https://jsonplaceholder.typicode.com/users/{}/'.format(argv[1]))
    
    # Convert json to dictionary
    user = json.loads(request_employee.text)
    
    # Extract username
    username = user.get("username")

    # Request user's TODO list
    request_todos = requests.get(
        'https://jsonplaceholder.typicode.com/users/{}/todos'.format(argv[1]))
    
    # Dictionary to store task status(completed) in boolean format
    tasks = {}
    
    # Convert json to list of dictionaries
    user_todos = json.loads(request_todos.text)
    
    # Loop through dictionary & get completed tasks
    for dictionary in user_todos:
        tasks.update({dictionary.get("title"): dictionary.get("completed")})

    task_list = []
    for k, v in tasks.items():
        task_list.append({
            "task": k,
            "completed": v,
            "username": username
        })

    json_to_dump = {argv[1]: task_list}
    
    # Export to JSON
    with open('{}.json'.format(argv[1]), mode='w') as file:
        json.dump(json_to_dump, file)
""",

    "3-dictionary_of_list_of_dictionaries.py": """#!/usr/bin/python3
"""Python script that exports data in the JSON format for all employees"""
import json
import requests


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/"
    users = requests.get(url + "users").json()
    
    # Export to JSON
    with open("todo_all_employees.json", "w") as jsonfile:
        json.dump({
            u.get("id"): [{
                "task": t.get("title"),
                "completed": t.get("completed"),
                "username": u.get("username")
            } for t in requests.get(url + "todos",
                                    params={"userId": u.get("id")}).json()]
            for u in users}, jsonfile)
"""
}

# The magic happens here!
if __name__ == "__main__":
    print("Let's build some toy scripts together!")
    for filename, content in scripts.items():
        with open(filename, 'w') as file:
            file.write(content)
        # Make the files ready to run (like giving them magic boots!)
        os.chmod(filename, 0o755)
        print(f"Created and filled {filename}—it's ready to play!")
    print("All done! Your toy village is built!")
