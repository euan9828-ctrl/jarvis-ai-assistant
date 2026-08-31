import json
import os
from datetime import datetime, timedelta
import logging
from config import TASK_DB_PATH, CALENDAR_DB_PATH

logger = logging.getLogger('jarvis')

class TaskManager:
    """Manages tasks, reminders, and calendar events"""
    
    def __init__(self):
        self.task_db_path = TASK_DB_PATH
        self.calendar_db_path = CALENDAR_DB_PATH
        self.ensure_db_files()
        logger.info("Task Manager initialized")
    
    def ensure_db_files(self):
        """Ensure database files exist"""
        os.makedirs(os.path.dirname(self.task_db_path), exist_ok=True)
        
        for db_path in [self.task_db_path, self.calendar_db_path]:
            if not os.path.exists(db_path):
                with open(db_path, 'w') as f:
                    json.dump({'tasks': [], 'reminders': [], 'events': []}, f)
    
    def create_task(self, task_data):
        """Create a new task"""
        try:
            tasks = self.load_tasks()
            task_id = len(tasks.get('tasks', [])) + 1
            
            new_task = {
                'id': task_id,
                'title': task_data.get('title', 'Untitled'),
                'description': task_data.get('description', ''),
                'due_date': task_data.get('due_date'),
                'priority': task_data.get('priority', 'normal'),
                'status': 'pending',
                'created_at': datetime.now().isoformat(),
                'completed_at': None
            }
            
            tasks['tasks'].append(new_task)
            self.save_tasks(tasks)
            logger.info(f"Task created: {new_task['title']}")
            return new_task
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            return None
    
    def get_pending_tasks(self):
        """Get all pending tasks"""
        try:
            tasks = self.load_tasks()
            return [t for t in tasks.get('tasks', []) if t.get('status') == 'pending']
        except Exception as e:
            logger.error(f"Error getting tasks: {str(e)}")
            return []
    
    def mark_complete(self, task_id):
        """Mark a task as complete"""
        try:
            tasks = self.load_tasks()
            for task in tasks.get('tasks', []):
                if task['id'] == task_id:
                    task['status'] = 'completed'
                    task['completed_at'] = datetime.now().isoformat()
                    self.save_tasks(tasks)
                    logger.info(f"Task {task_id} marked as complete")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error marking task complete: {str(e)}")
            return False
    
    def delete_task(self, task_id):
        """Delete a task"""
        try:
            tasks = self.load_tasks()
            tasks['tasks'] = [t for t in tasks.get('tasks', []) if t['id'] != task_id]
            self.save_tasks(tasks)
            logger.info(f"Task {task_id} deleted")
            return True
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}")
            return False
    
    def create_reminder(self, reminder_data):
        """Create a new reminder"""
        try:
            tasks = self.load_tasks()
            reminder_id = len(tasks.get('reminders', [])) + 1
            
            new_reminder = {
                'id': reminder_id,
                'text': reminder_data.get('text', 'Reminder'),
                'time': reminder_data.get('time'),
                'date': reminder_data.get('date', datetime.now().date().isoformat()),
                'is_recurring': reminder_data.get('is_recurring', False),
                'recurring_pattern': reminder_data.get('recurring_pattern'),
                'is_active': True,
                'created_at': datetime.now().isoformat()
            }
            
            tasks['reminders'].append(new_reminder)
            self.save_tasks(tasks)
            logger.info(f"Reminder created: {new_reminder['text']}")
            return new_reminder
        except Exception as e:
            logger.error(f"Error creating reminder: {str(e)}")
            return None
    
    def get_reminders(self):
        """Get all active reminders"""
        try:
            tasks = self.load_tasks()
            return [r for r in tasks.get('reminders', []) if r.get('is_active')]
        except Exception as e:
            logger.error(f"Error getting reminders: {str(e)}")
            return []
    
    def load_tasks(self):
        """Load tasks from database"""
        try:
            with open(self.task_db_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading tasks: {str(e)}")
            return {'tasks': [], 'reminders': [], 'events': []}
    
    def save_tasks(self, tasks):
        """Save tasks to database"""
        try:
            with open(self.task_db_path, 'w') as f:
                json.dump(tasks, f, indent=2)
            logger.info("Tasks saved to database")
        except Exception as e:
            logger.error(f"Error saving tasks: {str(e)}")
