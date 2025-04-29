from app import app, db, Task
from datetime import datetime

def add_test_task():
    with app.app_context():
        # Create a test task
        test_task = Task(
            title="Test Task",
            date=datetime.now().date(),
            time=datetime.now().time(),
            location="Test Location",
            description="Test Description"
        )
        
        # Add to database
        db.session.add(test_task)
        db.session.commit()
        
        print("Test task added successfully!")
        
        # Verify the task was added
        tasks = Task.query.all()
        print(f"Total tasks in database: {len(tasks)}")
        for task in tasks:
            print(f"Task: {task.title}, Date: {task.date}, Time: {task.time}")

if __name__ == "__main__":
    add_test_task() 