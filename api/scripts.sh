#!/bin/bash

# Create 0-gather_data_from_an_API.py
cat > 0-gather_data_from_an_API.py << 'EOF'
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
EOF

# Create 1-export_to_CSV.py
cat > 1-export_to_CSV.py << 'EOF'
#!/usr/bin/python3
"""
    python script that exports data in the CSV format
"""
import csv
import json
import requests
from sys import argv


if __name__ == "__main__":
    """
        request user info by employee ID
    """
    request_employee = requests.get(
        'https://jsonplaceholder.typicode.com/users/{}/'.format(argv[1]))
    """
        convert json to dictionary
    """
    user = json.loads(request_employee.text)
    """
        extract username
    """
    username = user.get("username")

    """
        request user's TODO list
    """
    request_todos = requests.get(
        'https://jsonplaceholder.typicode.com/users/{}/todos'.format(argv[1]))
    """
        dictionary to store task status(completed) in boolean format
    """
    tasks = {}
    """
        convert json to list of dictionaries
    """
    user_todos = json.loads(request_todos.text)
    """
        loop through dictionary & get completed tasks
    """
    for dictionary in user_todos:
        tasks.update({dictionary.get("title"): dictionary.get("completed")})

    """
        export to CSV
    """
    with open('{}.csv'.format(argv[1]), mode='w') as file:
        file_editor = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
        for k, v in tasks.items():
            file_editor.writerow([argv[1], username, v, k])
EOF

# Create 2-export_to_JSON.py
cat > 2-export_to_JSON.py << 'EOF'
#!/usr/bin/python3
"""
    python script that exports data in the JSON format
"""
import json
import requests
from sys import argv

if __name__ == "__main__":
    """
        request user info by employee ID
    """
    request_employee = requests.get(
        'https://jsonplaceholder.typicode.com/users/{}/'.format(argv[1]))
    """
        convert json to dictionary
    """
    user = json.loads(request_employee.text)
    """
        extract username
    """
    username = user.get("username")

    """
        request user's TODO list
    """
    request_todos = requests.get(
        'https://jsonplaceholder.typicode.com/users/{}/todos'.format(argv[1]))
    """
        dictionary to store task status(completed) in boolean format
    """
    tasks = {}
    """
        convert json to list of dictionaries
    """
    user_todos = json.loads(request_todos.text)
    """
        loop through dictionary & get completed tasks
    """
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
    """
        export to JSON
    """
    with open('{}.json'.format(argv[1]), mode='w') as file:
        json.dump(json_to_dump, file)
EOF

# Create 3-dictionary_of_list_of_dictionaries.py
cat > 3-dictionary_of_list_of_dictionaries.py << 'EOF'
#!/usr/bin/python3
"""
    python script that exports data in the JSON format
"""
import json
import requests

if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/"
    users = requests.get(url + "users").json()
    """
        export to JSON
    """

    with open("todo_all_employees.json", "w") as jsonfile:
        json.dump({
            u.get("id"): [{
                "task": t.get("title"),
                "completed": t.get("completed"),
                "username": u.get("username")
            } for t in requests.get(url + "todos",
                                    params={"userId": u.get("id")}).json()]
            for u in users}, jsonfile)
EOF

# Make all scripts executable
chmod +x 0-gather_data_from_an_API.py
chmod +x 1-export_to_CSV.py
chmod +x 2-export_to_JSON.py
chmod +x 3-dictionary_of_list_of_dictionaries.py

echo "All Python files have been created and made executable!"
