import json
import signal
import sys

def signal_handler(signal, frame):
    print('\nExiting gracefully...')
    todo.save_tasks()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

todo_list_tasks = []

class Task:
    def __init__(self, title):
        self.title = title
        self.done = False
    def mark_done(self):
        self.done = True
    def to_dict(self):
        return {'title': self.title, 'done': self.done}

class ToDoList:
    def __init__(self):
        self.tasks = []

    def load_tasks(self):
        try:
            with open ('tasks.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print('No saved files found')
            return
        except json.JSONDecodeError:
            print('Saved file is empty or corrupted, starting with an empty list')
            return 
    
        self.tasks.clear()
        for item in data:
            task = Task(item['title'])
            if item.get('done'):
                task.mark_done()
            self.tasks.append(task)    

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)
     
    def add_task(self):
        new_task_title = input("Enter a task: ")
        if not new_task_title:
            print('Task cannot be empty')
            return
        for task in self.tasks:
            if task.title == new_task_title:
                print('Task already exists')
                return
        new_task = Task(new_task_title)
        self.tasks.append(new_task)
        print(f"Task '{new_task.title}' added to the list.")

    def display_tasks(self):
        if not self.tasks:
            print('No tasks')
            return
        for index, task in enumerate(self.tasks, start=1):
            status = '[X]' if task.done else '[ ]'
            print(f"{index} - {status} {task.title}")    

    def remove_task(self):
        if not self.tasks:
            print('No tasks to remove')
            return
        remove = 0
        self.display_tasks()
        while remove < 1 or remove > len(self.tasks):
            try:
                remove = int(input('Enter a number of task to remove:'))
            except ValueError:
                print('Invalid number, please try again.')
                continue
            if remove < 1 or remove > len(self.tasks):
                print ("Invalid task number")
        removed_task = self.tasks.pop(remove-1)
        print(f"Task '{removed_task.title}' has been removed from the list.")
        self.display_tasks()

    def mark_done(self):
        if self.tasks == []:
            print('No tasks to mark as done')
            return
        self.display_tasks()
        mark = 0
        while mark < 1 or mark > len(self.tasks):
            try:
                mark = int(input('Enter a number of task to mark as done:'))
            except ValueError:
                print('Invalid number, please try again.')
                continue
            if mark < 1 or mark > len(self.tasks):
                print ("Invalid task number")
            else:
                task = self.tasks[mark-1]
                if task.done:
                    print('Task already marked as done')
                else:
                    task.mark_done()
                    break   
        self.display_tasks()

    def edit_task(self):
        if not self.tasks:
            print('No tasks to edit')
            return

        self.display_tasks()
        edit = 0
        while edit < 1 or edit > len(self.tasks):
            try:
                edit = int(input('Enter a number of task to edit:'))
            except ValueError:
                print('Invalid number, please try again.')
                continue

            if edit < 1 or edit > len(self.tasks):
                print ("Invalid task number")
        print(f"Current task: {self.tasks[edit-1].title}")
        new_task = input("Enter a new task: ")
        if not new_task:
            print('Task cannot be empty')
            return
        for task in self.tasks:
            if task.title == new_task:
                print('Task with this name already exists')
                return
        self.tasks[edit-1].title = new_task
        self.display_tasks() 
def show_menu(todo: ToDoList):
    print('1 - Add a task\n2 - Display tasks\n3 - Remove a task\n4 - Mark task as done\n5 - Edit a task\n6 - Exit')         
    while True:
        try:
            choice = int(input('Select an option: '))
        except ValueError:
            print('Invalid number, please try again.')
            continue   
        if choice == 1:
            todo.add_task()
            todo.save_tasks()
            print('\n1 - Add a task\n2 - Display tasks\n3 - Remove a task\n4 - Mark task as done\n5 - Edit a task\n6 - Exit') 
        elif choice == 2:
            todo.display_tasks()
            print('\n1 - Add a task\n2 - Display tasks\n3 - Remove a task\n4 - Mark task as done\n5 - Edit a task\n6 - Exit') 
        elif choice == 3:
            todo.remove_task()
            todo.save_tasks()
            print('\n1 - Add a task\n2 - Display tasks\n3 - Remove a task\n4 - Mark task as done\n5 - Edit a task\n6 - Exit') 
        elif choice == 4:
            todo.mark_done()
            todo.save_tasks()
            print('\n1 - Add a task\n2 - Display tasks\n3 - Remove a task\n4 - Mark task as done\n5 - Edit a task\n6 - Exit') 
        elif choice == 5:
            todo.edit_task()
            todo.save_tasks()
            print('\n1 - Add a task\n2 - Display tasks\n3 - Remove a task\n4 - Mark task as done\n5 - Edit a task\n6 - Exit')     
        elif choice == 6:
            todo.save_tasks()
            print('\nTasks saved. Exiting the programm...')
            break
        else:
            print('Invalid number, please try again.')
            continue

if __name__ == "__main__":
    todo = ToDoList()
    todo.load_tasks()
    print('\nWelcome to the menu, please choose an option:\n')
    show_menu(todo)
