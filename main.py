import json

todo_list_tasks = []

def save_tasks():
    with open('tasks.json', 'w') as f:
        json.dump(todo_list_tasks,f,indent=4)

def load_tasks():
    try:
        with open ('tasks.json', 'r') as f:
            todo_list_tasks.clear()
            todo_list_tasks.extend(json.load(f))
    except FileNotFoundError:
        print('No saved files found')       
def add_task():
    new_task = input("Enter a task: ")
    new_task = {"title": new_task, "done": False}
    todo_list_tasks.append(new_task)
    print(f"Task '{new_task['title']}' added to the list.")

def display_tasks():
    if len(todo_list_tasks) == 0:
        print('No tasks')
        return
    for index, task in enumerate(todo_list_tasks, start=1):
        if task['done']:
            status = '[X]'
        else:
            status = '[ ]'
        title = task['title']
        print(f"{index} - {status} {title}")    


def remove_task():
    display_tasks()
    remove = 0
    while remove < 1 or remove > len(todo_list_tasks):
        remove = int(input('Enter a number of task to remove:'))
        if remove < 1 or remove > len(todo_list_tasks):
            print ("Invalid task number")
    todo_list_tasks.pop(remove-1)
    display_tasks()

def mark_done():
    display_tasks()
    mark = 0
    while mark < 1 or mark > len(todo_list_tasks):
        mark = int(input('Enter a number of task to mark as done:'))
        if mark < 1 or mark > len(todo_list_tasks):
            print ("Invalid task number")
    todo_list_tasks[mark-1]['done'] = True
    display_tasks()

load_tasks()
print('\nWelcome to the menu, please choose an option:\n')
print('1 - Add a task\n2 - Display tasks\n3 - Remove a task\n4 - Mark task as done\n5 - Exit')      
while True:
    try:
        choice = int(input('Select an option: '))
    except ValueError:
        print('Invalid number, please try again.')
        continue
    if choice == 1:
        add_task()
        save_tasks()
    elif choice == 2:
        display_tasks()
    elif choice == 3:
        remove_task()
        save_tasks()
    elif choice == 4:
        mark_done()
        save_tasks()
    elif choice == 5:
        save_tasks()
        print('Exiting the programm...')
        break
    else:
        if choice < 1 or choice > 5:
            print('Invalid number, please try again.')
            continue