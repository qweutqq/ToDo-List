import json
import signal
import sys
from datetime import datetime

def signal_handler(signal, frame):
    print('\nExiting gracefully...')
    todo.save_tasks()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

todo_list_tasks = []

class Task:
    def __init__(self, title, priority = 2, deadline = None):
        self.title = title
        self.done = False
        self.priority = priority
        self.deadline = deadline
    def mark_done(self):
        self.done = True
    def to_dict(self):
        return {'title': self.title, 'done': self.done, 'priority': self.priority, 'deadline': self.deadline.isoformat() if self.deadline else None}

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
            deadline_str = item.get('deadline')
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date() if deadline_str else None
            task = Task(item['title'], item.get('priority', 2), deadline)
            if item.get('done'):
                task.mark_done()
            self.tasks.append(task)    

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)
     
    def show_menu_text(self):
        print('\n1 - Add a task\n2 - Display tasks\n3 - Remove a task\n4 - Mark task as done\n5 - Edit a task\n6 - Search a task\n7 - Sort tasks\n8 - Filter tasks\n9 - Summary\n0 - Exit\n')

    def add_task(self):
        new_task_title = input("Enter a task: ")
        if not new_task_title:
            print('Task cannot be empty')
            return
        
        for task in self.tasks:
            if task.title == new_task_title:
                print('Task already exists')
                return

        priority = input('Enter a priority (1-High, 2-Medium, 3-Low): ')

        try:
            priority = int(priority)
            if priority not in [1, 2, 3]: priority = 2
        except ValueError:
            priority = 2
            print('Invalid priority, defaulting to Medium')

        deadline = input('Enter a deadline (YYYY-MM-DD): ')
        try:
            deadline = datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            deadline = None
            print('Invalid deadline, defaulting to None')

        if deadline:
            deadline = deadline.date()
            if deadline < datetime.now().date():
                deadline = None
                print('Deadline cannot be in the past, defaulting to None')
        else:
            deadline = None
            print('Deadline set to None')

        if deadline:
            new_task = Task(new_task_title, priority, deadline)
        else:    
            new_task = Task(new_task_title, priority)
        self.tasks.append(new_task)
        print(f"Task '{new_task.title}' added to the list.")

    def display_tasks(self):
        if not self.tasks:
            print('No tasks')
            return
        
        priority_names = {1:'High', 2:'Medium', 3:'Low'}
        today = datetime.now().date()

        for index, task in enumerate(self.tasks, start=1):
            priority_label = priority_names.get(task.priority, 'Medium') 
            status = '[X]' if task.done else '[ ]'

            line = f"{index} - {status} {task.title} {priority_label}"

            if task.deadline:
                deadline_str = task.deadline.strftime('%Y-%m-%d')
                if not task.done and task.deadline < today:
                    line += f" ⚠️ OVERDUE! Deadline was: {deadline_str}"
                else:
                    line += f" Deadline: {deadline_str}"
            print(line)            

    def remove_task(self):
        if not self.tasks:
            print('No tasks to remove')
            return
        remove = 0
        self.display_tasks()
        while True:
            s = input('Enter a number of task to remove (0 to cancel): ').strip()
            try:
                num = int(s)
            except ValueError:
                print('Invalid number, please try again.')
                continue
            
            if num == 0:
                print('Removal cancelled.')
                return

            if 1 <= num <= len(self.tasks):
                break
            else:
                print('Invalid task number, try again.')
                
        removed = self.tasks.pop(num-1)
        print(f"Task '{removed.title}' removed.")
        self.display_tasks()

    def mark_done(self):
        if not self.tasks:
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

    def search_task(self):
        if not self.tasks:
            print('No tasks to search')
            return
        
        search = input('Enter a task to search: ').strip()
        if search == '':
            print('Search cannot be empty')
            return
        
        matches = []
        for i, task in enumerate(self.tasks, start=1):
            if search.lower() in task.title.lower():
                matches.append((i,task))

        if matches == []:
            print(f'No tasks contains {search}')
            return
        
        print('Found tasks:')
        priority_names = {1:'High', 2:'Medium', 3:'Low'}
        for i, task in matches:
            status = '[X]' if task.done else '[ ]'
            print(f"{i} - {status} {task.title}(Priority: {priority_names[task.priority]})")

    def sort_tasks(self):
        if not self.tasks:
            print('No tasks to sort. Returning.\n')
            return
        
        print('Sort by: \n 1 - Priority(High to Low)\n 2 - Status(Incomplete tasks first)\n 3 - Title(A to Z)\n 4 - Deadline (Earliset first) 5 - Cancel)')
        try:
            num = int(input('Select an option: '))
        except ValueError:
            print('Invalid number, please try again.')
            return
            
        if num == 1:
            self.tasks.sort(key = lambda task: task.priority, reverse = False)
            print('Tasks sorted succesfully!\n')
            return
        elif num == 2:
            self.tasks.sort(key = lambda task: task.done)
            print('Tasks sorted succesfully!\n')
            return
        elif num == 3:
            self.tasks.sort(key = lambda task: task.title.lower())
            print('Tasks sorted succesfully!\n')
            return
        elif num == 4:
            self.tasks.sort(key=lambda task: task.deadline if task.deadline else datetime.max.date())
            print('Tasks sorted succesfully!\n')
            return
        else:
            print("Canceling...")
            return            

    def filter_tasks(self):
        if not self.tasks:
            print('No tasks to filter. Returning.\n')
            return
        
        print('Choose an option: \n1 - Show all tasks\n2 - Show incomplete tasks\n3 - Show complete tasks\n4 - Cancel')
        try:
            num = int(input('Select an option: '))
        except ValueError:
            print('Invalid number, please try again.')
            return
        
        if num == 1:
            print('All tasks:\n')
            self.display_tasks()
            return
        elif num == 2:
            print('Incomplete tasks:\n')
            for index, task in enumerate(self.tasks, start=1):
                if not task.done:
                    priority_label = {1: 'High', 2: 'Medium', 3: 'Low'}.get(task.priority, 'Medium')
                    status = '[ ]'  # Incomplete task
                    print(f"{index} - {status} {task.title} (Priority: {priority_label})")
            return
        elif num == 3:
            print('Complete tasks:\n')
            for index, task in enumerate(self.tasks, start=1):
                if task.done:
                    priority_label = {1: 'High', 2: 'Medium', 3: 'Low'}.get(task.priority, 'Medium')
                    status = '[X]'  # Completed task
                    print(f"{index} - {status} {task.title} (Priority: {priority_label})")
            return
        else:
            print("Canceling...")
            return

    def task_summary(self):

        if not self.tasks:
            print('No tasks to summarize. Returning.\n')
            return
        
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task.done)
        incomplete_tasks = total_tasks - completed_tasks
        high = sum(1 for task in self.tasks if task.priority == 1)
        medium = sum(1 for task in self.tasks if task.priority == 2)
        low = sum(1 for task in self.tasks if task.priority == 3)

        print(f"\nTotal tasks: {total_tasks}")
        print(f"Completed tasks: {completed_tasks}")
        print(f"Incomplete tasks: {incomplete_tasks}\n")
        print(f"High priority tasks: {high}")
        print(f"Medium priority tasks: {medium}")
        print(f"Low priority tasks: {low}")

def show_menu(todo: ToDoList):
    todo.show_menu_text()           
    while True:
        try:
            choice = int(input('Select an option: '))
        except ValueError:
            print('Invalid number, please try again.')
            continue   
        if choice == 1:
            todo.add_task()
            todo.save_tasks()
            todo.show_menu_text()
        elif choice == 2:
            todo.display_tasks()
            todo.show_menu_text()   
        elif choice == 3:
            todo.remove_task()
            todo.save_tasks()
            todo.show_menu_text()    
        elif choice == 4:
            todo.mark_done()
            todo.save_tasks()
            todo.show_menu_text()    
        elif choice == 5:
            todo.edit_task()
            todo.save_tasks()
            todo.show_menu_text()   
        elif choice == 6:
            todo.search_task()
            todo.save_tasks()
            todo.show_menu_text() 
        elif choice == 7:
            todo.sort_tasks()
            todo.save_tasks()
            todo.show_menu_text()
        elif choice == 8:
            todo.filter_tasks()
            todo.save_tasks()
            todo.show_menu_text()
        elif choice == 9:
            todo.task_summary()
            todo.show_menu_text()                
        elif choice == 0:
            todo.save_tasks()
            print('\nTasks saved. Exiting the programm...')
            break
        else:
            print('Invalid number, please try again.')
            continue

if __name__ == "__main__":
    todo = ToDoList()
    todo.load_tasks()
    print('\nWelcome to the menu, please choose an option:')
    show_menu(todo)
