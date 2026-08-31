"""
Task Manager Module - Manages user tasks and to-do lists
"""

import json
import os
from datetime import datetime


class TaskManager:
    """Manages tasks for JARVIS"""
    
    def __init__(self, data_file="data/tasks.json"):
        """Initialize task manager"""
        self.data_file = data_file
        self.tasks = self.load_tasks()
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(data_file) if os.path.dirname(data_file) else ".", exist_ok=True)
        
        print("✓ Task manager initialized")
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error loading tasks: {str(e)}")
            return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.data_file) if os.path.dirname(self.data_file) else ".", exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving tasks: {str(e)}")
    
    def add_task(self, name, description="", priority="normal", due_date=""):
        """
        Add a new task
        
        Args:
            name (str): Task name
            description (str): Task description
            priority (str): Priority level (low, normal, high)
            due_date (str): Due date
            
        Returns:
            int: Task ID
        """
        task = {
            "id": len(self.tasks) + 1,
            "name": name,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        self.tasks.append(task)
        self.save_tasks()
        
        print(f"✓ Task added: {name}")
        return task["id"]
    
    def get_all_tasks(self):
        """Get all tasks"""
        return self.tasks
    
    def get_pending_tasks(self):
        """Get all pending (not completed) tasks"""
        return [t for t in self.tasks if not t.get("completed")]
    
    def get_completed_tasks(self):
        """Get all completed tasks"""
        return [t for t in self.tasks if t.get("completed")]
    
    def complete_task(self, task_name=None, task_id=None):
        """
        Mark a task as complete
        
        Args:
            task_name (str): Name of task to complete
            task_id (int): ID of task to complete
            
        Returns:
            bool: Success status
        """
        for task in self.tasks:
            if (task_name and task["name"].lower() == task_name.lower()) or \
               (task_id and task["id"] == task_id):
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self.save_tasks()
                print(f"✓ Task completed: {task['name']}")
                return True
        
        return False
    
    def delete_task(self, task_name=None, task_id=None):
        """
        Delete a task
        
        Args:
            task_name (str): Name of task to delete
            task_id (int): ID of task to delete
            
        Returns:
            bool: Success status
        """
        for i, task in enumerate(self.tasks):
            if (task_name and task["name"].lower() == task_name.lower()) or \
               (task_id and task["id"] == task_id):
                self.tasks.pop(i)
                self.save_tasks()
                print(f"✓ Task deleted: {task['name']}")
                return True
        
        return False
    
    def update_task(self, task_id, **kwargs):
        """
        Update a task
        
        Args:
            task_id (int): ID of task to update
            **kwargs: Fields to update
            
        Returns:
            bool: Success status
        """
        for task in self.tasks:
            if task["id"] == task_id:
                task.update(kwargs)
                self.save_tasks()
                print(f"✓ Task updated: {task['name']}")
                return True
        
        return False
    
    def get_task_by_id(self, task_id):
        """Get task by ID"""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def get_task_by_name(self, name):
        """Get task by name"""
        for task in self.tasks:
            if task["name"].lower() == name.lower():
                return task
        return None
    
    def search_tasks(self, keyword):
        """Search tasks by keyword"""
        results = []
        keyword_lower = keyword.lower()
        
        for task in self.tasks:
            if keyword_lower in task["name"].lower() or \
               keyword_lower in task["description"].lower():
                results.append(task)
        
        return results
