"""
Scheduler Module - Handles scheduling and reminders for JARVIS
"""

import schedule
import time
import threading
from datetime import datetime, timedelta
import json
import os


class TaskScheduler:
    """Handles task scheduling and reminders"""
    
    def __init__(self, task_manager):
        """Initialize scheduler"""
        self.task_manager = task_manager
        self.reminders = self.load_reminders()
        self.scheduler = schedule.Scheduler()
        self.running = False
        
        print("✓ Task scheduler initialized")
    
    def load_reminders(self, reminder_file="data/reminders.json"):
        """Load reminders from file"""
        try:
            if os.path.exists(reminder_file):
                with open(reminder_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error loading reminders: {str(e)}")
            return []
    
    def save_reminders(self, reminder_file="data/reminders.json"):
        """Save reminders to file"""
        try:
            os.makedirs(os.path.dirname(reminder_file) if os.path.dirname(reminder_file) else ".", exist_ok=True)
            with open(reminder_file, 'w') as f:
                json.dump(self.reminders, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving reminders: {str(e)}")
    
    def parse_schedule_command(self, command):
        """Parse scheduling commands"""
        command_lower = command.lower()
        
        # Extract time and task
        if "at" in command_lower:
            parts = command_lower.split("at")
            task = parts[0].replace("schedule", "").replace("set reminder", "").replace("remind me", "").strip()
            time_str = parts[1].strip()
            
            # Try to parse time
            try:
                reminder_time = self.parse_time(time_str)
                if reminder_time:
                    self.add_reminder(task, reminder_time)
                    return f"✓ Reminder set for {time_str}: {task}"
            except Exception as e:
                return f"I couldn't understand the time. Please try again."
        
        return "Please specify a time for the reminder."
    
    def parse_time(self, time_str):
        """Parse time string"""
        time_str = time_str.strip()
        
        try:
            # Try common formats
            for fmt in ["%I:%M %p", "%H:%M", "%I %p", "%H"]:
                try:
                    parsed = datetime.strptime(time_str, fmt)
                    # Set to today
                    now = datetime.now()
                    return now.replace(hour=parsed.hour, minute=parsed.minute, second=0)
                except ValueError:
                    continue
            
            # If time is in the past, assume tomorrow
            if parsed < datetime.now():
                parsed += timedelta(days=1)
            
            return parsed
        
        except Exception as e:
            print(f"❌ Time parsing error: {str(e)}")
            return None
    
    def add_reminder(self, task, reminder_time):
        """Add a reminder"""
        reminder = {
            "id": len(self.reminders) + 1,
            "task": task,
            "time": reminder_time.isoformat(),
            "created_at": datetime.now().isoformat(),
            "triggered": False
        }
        
        self.reminders.append(reminder)
        self.save_reminders()
        
        # Schedule the reminder
        self.schedule_reminder(reminder)
        
        print(f"✓ Reminder added: {task} at {reminder_time}")
    
    def schedule_reminder(self, reminder):
        """Schedule a reminder to trigger"""
        reminder_time = datetime.fromisoformat(reminder["time"])
        
        def trigger_reminder():
            print(f"⏰ REMINDER: {reminder['task']}")
            # In a real implementation, would call voice_handler.speak()
        
        # Calculate seconds until reminder
        delay = (reminder_time - datetime.now()).total_seconds()
        
        if delay > 0:
            threading.Timer(delay, trigger_reminder).start()
    
    def get_pending_reminders(self):
        """Get all pending reminders"""
        return [r for r in self.reminders if not r.get("triggered")]
    
    def run(self):
        """Run scheduler loop"""
        self.running = True
        
        # Schedule daily task check
        self.scheduler.every().day.at("09:00").do(self.daily_task_check)
        
        print("⏰ Scheduler running...")
        
        while self.running:
            self.scheduler.run_pending()
            time.sleep(60)  # Check every minute
    
    def daily_task_check(self):
        """Daily check for pending tasks"""
        pending = self.task_manager.get_pending_tasks()
        
        if pending:
            print(f"\n📋 Daily Task Check: {len(pending)} pending tasks")
            for task in pending:
                print(f"  • {task['name']}")
