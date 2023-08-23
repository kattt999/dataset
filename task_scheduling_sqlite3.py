import sqlite3
import heapq

# Connect to the SQLite database
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create tasks table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        due_date TEXT,
        priority INTEGER,
        resources TEXT,
        progress INTEGER
    )
''')
conn.commit()

# Sample in-memory data structures to simulate storage
tasks = {}
task_queue = []

# Function to add a task to the priority queue
def add_task_to_queue(task_id):
    task = tasks[task_id]
    heapq.heappush(task_queue, (task['due_date'], task['priority'], task_id))

def get_tasks():
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    task_list = [{'id': row[0], 'title': row[1], 'due_date': row[2], 'priority': row[3], 'resources': row[4], 'progress': row[5]} for row in rows]
    return task_list

def create_task(title, due_date, priority, resources):
    cursor.execute('INSERT INTO tasks (title, due_date, priority, resources, progress) VALUES (?, ?, ?, ?, ?)',
                   (title, due_date, priority, resources, 0))
    conn.commit()
    task_id = cursor.lastrowid
    add_task_to_queue(task_id)
    return task_id

def update_task(task_id, title, due_date, priority, resources):
    cursor.execute('UPDATE tasks SET title=?, due_date=?, priority=?, resources=? WHERE id=?',
                   (title, due_date, priority, resources, task_id))
    conn.commit()
    # Re-add the task to the queue as its properties might have changed
    add_task_to_queue(task_id)

def delete_task(task_id):
    cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    conn.commit()

# Rest of your functions...

def main():
    # Initialization code...

    while True:
        print("\nSelect an action:")
        print("1. Get tasks")
        print("2. Create task")
        print("3. Update task")
        print("4. Delete task")
        print("5. Get next task")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            task_list = get_tasks()
            print("\nTasks:")
            for task in task_list:
                print(task)
        elif choice == '2':
            title = input("Enter task title: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            priority = int(input("Enter priority: "))
            resources = input("Enter resources (comma-separated): ")
            task_id = create_task(title, due_date, priority, resources)
            print(f"Task created with ID: {task_id}")
        elif choice == '3':
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter task title: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            priority = int(input("Enter priority: "))
            resources = input("Enter resources (comma-separated): ")
            update_task(task_id, title, due_date, priority, resources)
            print("Task updated successfully.")
        elif choice == '4':
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)
            print("Task deleted successfully.")
        elif choice == '5':
            # Implement get next task functionality
            pass
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

    # Close the database connection when done
    conn.close()

if __name__ == '__main__':
    main()
