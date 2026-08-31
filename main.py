#!/usr/bin/env python3
"""
JARVIS AI Assistant - A voice-controlled AI that handles daily tasks
"""

import os
import sys
import json
import schedule
import threading
import datetime
from dotenv import load_dotenv

# Import JARVIS modules
from modules.voice_handler import VoiceHandler
from modules.task_manager import TaskManager
from modules.ai_brain import AIBrain
from modules.scheduler import TaskScheduler

# Load environment variables
load_dotenv()

class JARVIS:
    """Main JARVIS AI Assistant Class"""
    
    def __init__(self):
        """Initialize JARVIS with all components"""
        print("=" * 60)
        print("Initializing JARVIS AI Assistant...")
        print("=" * 60)
        
        self.voice_handler = VoiceHandler()
        self.task_manager = TaskManager()
        self.ai_brain = AIBrain()
        self.scheduler = TaskScheduler(self.task_manager)
        
        self.running = True
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        
        print("✓ JARVIS initialized successfully!")
        print("=" * 60)
    
    def listen_and_respond(self):
        """Main listening loop - listens for voice commands"""
        while self.running:
            try:
                print("\n🎤 Listening for your command...")
                
                # Listen for voice input
                command = self.voice_handler.listen()
                
                if command:
                    print(f"📝 Command received: {command}")
                    
                    # Process the command
                    response = self.process_command(command)
                    
                    # Speak the response
                    self.voice_handler.speak(response)
                    
            except KeyboardInterrupt:
                print("\n\n🛑 JARVIS shutting down...")
                self.running = False
                break
            except Exception as e:
                if self.debug:
                    print(f"❌ Error: {str(e)}")
                self.voice_handler.speak("I encountered an error. Please try again.")
    
    def process_command(self, command):
        """Process user commands"""
        command_lower = command.lower()
        
        # Task Management Commands
        if "add task" in command_lower or "create task" in command_lower:
            return self.handle_add_task(command)
        
        elif "list tasks" in command_lower or "show tasks" in command_lower:
            return self.handle_list_tasks()
        
        elif "complete task" in command_lower or "mark task" in command_lower:
            return self.handle_complete_task(command)
        
        elif "delete task" in command_lower or "remove task" in command_lower:
            return self.handle_delete_task(command)
        
        # Schedule Commands
        elif "schedule" in command_lower or "set reminder" in command_lower:
            return self.handle_schedule(command)
        
        # Time/Date Commands
        elif "what time" in command_lower or "current time" in command_lower:
            return self.get_current_time()
        
        elif "what date" in command_lower or "today's date" in command_lower:
            return self.get_current_date()
        
        # Help Command
        elif "help" in command_lower or "what can you do" in command_lower:
            return self.get_help()
        
        # Status Command
        elif "status" in command_lower:
            return self.get_status()
        
        # Default: Send to AI Brain
        else:
            return self.ai_brain.get_response(command)
    
    def handle_add_task(self, command):
        """Handle adding a new task"""
        # Extract task name from command
        task_name = command.replace("add task", "").replace("create task", "").strip()
        
        if not task_name:
            return "Please specify what task you'd like me to add."
        
        task_id = self.task_manager.add_task(task_name)
        return f"✓ Task added: {task_name}"
    
    def handle_list_tasks(self):
        """Handle listing all tasks"""
        tasks = self.task_manager.get_all_tasks()
        
        if not tasks:
            return "You have no tasks at the moment."
        
        response = "Here are your tasks: "
        for task in tasks:
            status = "completed" if task.get("completed") else "pending"
            response += f"\n• {task.get('name')} ({status})"
        
        return response
    
    def handle_complete_task(self, command):
        """Handle marking a task as complete"""
        task_name = command.replace("complete task", "").replace("mark task", "").strip()
        
        if not task_name:
            return "Please specify which task to complete."
        
        success = self.task_manager.complete_task(task_name)
        
        if success:
            return f"✓ Task completed: {task_name}"
        else:
            return f"Could not find task: {task_name}"
    
    def handle_delete_task(self, command):
        """Handle deleting a task"""
        task_name = command.replace("delete task", "").replace("remove task", "").strip()
        
        if not task_name:
            return "Please specify which task to delete."
        
        success = self.task_manager.delete_task(task_name)
        
        if success:
            return f"✓ Task deleted: {task_name}"
        else:
            return f"Could not find task: {task_name}"
    
    def handle_schedule(self, command):
        """Handle scheduling tasks"""
        return self.scheduler.parse_schedule_command(command)
    
    def get_current_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    def get_current_date(self):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today's date is {current_date}"
    
    def get_help(self):
        """Get help information"""
        help_text = """
        I can help you with:
        • Adding, listing, completing, and deleting tasks
        • Scheduling reminders and events
        • Telling you the time and date
        • Answering general questions
        • Managing your daily schedule
        
        Try saying things like:
        - "Add task buy groceries"
        - "List tasks"
        - "Complete task buy groceries"
        - "Set a reminder for 3 PM"
        - "What time is it?"
        - "What's today's date?"
        """
        return help_text
    
    def get_status(self):
        """Get JARVIS status"""
        tasks = self.task_manager.get_all_tasks()
        pending = len([t for t in tasks if not t.get("completed")])
        completed = len([t for t in tasks if t.get("completed")])
        
        status = f"""
        JARVIS Status:
        • Pending tasks: {pending}
        • Completed tasks: {completed}
        • System: Online and ready
        """
        return status
    
    def start(self):
        """Start JARVIS in a separate thread"""
        print("\n🚀 Starting JARVIS voice listening thread...")
        listening_thread = threading.Thread(target=self.listen_and_respond, daemon=False)
        listening_thread.start()
        
        # Start scheduler in background
        print("⏰ Starting task scheduler...")
        scheduler_thread = threading.Thread(target=self.scheduler.run, daemon=True)
        scheduler_thread.start()
        
        # Keep main thread alive
        listening_thread.join()


def main():
    """Main entry point"""
    jarvis = JARVIS()
    
    try:
        jarvis.start()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
