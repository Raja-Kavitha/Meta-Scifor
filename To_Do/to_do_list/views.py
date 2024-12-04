from django.shortcuts import render, redirect

# Create your views here.
import os

TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.txt')

# Function to read tasks from file
def read_tasks():
    with open(TASKS_FILE, 'r') as file:
        tasks = file.readlines()
    return [task.strip() for task in tasks]

# Function to write tasks to file
def write_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        file.write("\n".join(tasks))

def home(request):
    tasks = read_tasks()

    if request.method == 'POST':
        new_task = request.POST['title']
        tasks.append(new_task)
        write_tasks(tasks)
        return redirect('/')

    return render(request, 'to_do_list/home.html', {'tasks': tasks})

def delete_task(request, task):
    tasks = read_tasks()
    tasks = [t for t in tasks if t != task]
    write_tasks(tasks)
    return redirect('/')
