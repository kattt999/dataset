from flask import Flask, request, jsonify
import heapq
import datetime

app = Flask(__name__)

# Sample route for the root URL
@app.route('/')
def home():
    return "Welcome to the Task Management App"

# Sample in-memory data structures to simulate storage
tasks = {}
resources = {}

# Priority queue for task scheduling based on due date and priority
task_queue = []

# Function to add a task to the priority queue
def add_task_to_queue(task_id):
    task = tasks[task_id]
    print(task, "\n")
    heapq.heappush(task_queue, (task['due_date'], task['priority'], task_id))

initial_tasks = [
    {
        'id' : 1,
        'title' : 'Finish Project',
        'due_date' : '2023-08-31',
        'priority' : 3,
        'resources' : ['John', 'Sarah'],
        'progress' : 0
    },
        {
        'id' : 2,
        'title' : 'Prepare presentation',
        'due_date' : '2023-08-25',
        'priority': 2,
        'resources' : ['Alice', 'Bob'],
        'progress' : 0
    },
        {
        'id' : 3,
        'title' : 'Review code',
        'due_date' : '2023-08-29',
        'priority': 1,
        'resources' : ['Michael'],
        'progress' : 0
    }
]

for task in initial_tasks:
    
    tasks[task['id']] = task
    # print("task : ", task, "\n")
    
    # print("task[id]: ", task['id'],"\n")
    # print("tasks[task['id']]: ", tasks[task['id']],"\n")

    add_task_to_queue(task['id'])

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = list(tasks.values())
    return jsonify({'task': task_list})


# Endpoint to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_id = len(tasks) + 1
    task = {
        'id': task_id,
        'title': data['title'],
        'due_date': data['due_date'],
        'priority': data['priority'],
        'resources': [],
        'progress': 0
    }
    tasks[task_id] = task
    add_task_to_queue(task_id)
    return jsonify({'message': 'Task created successfully', 'task_id': task_id}), 201


# Endpoint to update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    task = tasks[task_id]
    task['title'] = data['title']
    task['due_date'] = data['due_date']
    task['priority'] = data['priority']
    add_task_to_queue(task_id)
    return jsonify({'message': 'Task updated successfully'})

# Endpoint to delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404

    del tasks[task_id]
    return jsonify({'message': 'Task deleted successfully'})

# Endpoint to allocate resources to a task
@app.route('/tasks/<int:task_id>/resources', methods=['POST'])
def allocate_resources(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    tasks[task_id]['resources'] = data['resources']
    return jsonify({'message': 'Resources allocated successfully'})

# Endpoint to get the next task to work on based on scheduling algorithm
@app.route('/tasks/next', methods=['GET'])
def get_next_task():
    if task_queue:
        _, _, next_task_id = heapq.heappop(task_queue)
        return jsonify(tasks[next_task_id])
    else:
        return jsonify({'message': 'No tasks available'})

# Endpoint to update task progress
@app.route('/tasks/<int:task_id>/progress', methods=['PUT'])
def update_task_progress(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    tasks[task_id]['progress'] = data['progress']
    return jsonify({'message': 'Task progress updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
