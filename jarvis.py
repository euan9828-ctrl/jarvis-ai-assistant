#!/usr/bin/env python3
"""
JARVIS AI Assistant
A voice-enabled AI assistant that handles daily tasks and responds to voice commands
"""

import sys
import os
import json
from datetime import datetime
import threading

from voice_engine import VoiceEngine
from task_manager import TaskManager
from ai_brain import AIBrain
from command_parser import CommandParser
from utils.logger import setup_logger

logger = setup_logger('jarvis')

class JARVIS:
    def __init__(self):
        """Initialize JARVIS AI Assistant"""
        logger.info("Initializing JARVIS AI Assistant...")
        
        self.voice_engine = VoiceEngine()
        self.task_manager = TaskManager()
        self.ai_brain = AIBrain()
        self.command_parser = CommandParser()
        
        self.running = False
        self.listening = False
        self.is_woken = False
        
        logger.info("JARVIS initialized successfully")
    
    def speak(self, text):
        """Make JARVIS speak"""
        logger.info(f"JARVIS: {text}")
        self.voice_engine.speak(text)
    
    def listen(self):
        """Listen for voice commands"""
        logger.info("Listening for commands...")
        self.listening = True
        
        try:
            audio = self.voice_engine.listen()
            if audio:
                text = self.voice_engine.recognize_speech(audio)
                logger.info(f"Recognized: {text}")
                return text
        except Exception as e:
            logger.error(f"Error during listening: {str(e)}")
            self.speak("Sorry, I didn't catch that. Please repeat.")
        
        self.listening = False
        return None
    
    def check_wake_word(self, text):
        """Check if wake word is detected"""
        if text and 'jarvis' in text.lower():
            self.is_woken = True
            return True
        return False
    
    def process_command(self, command):
        """Process user command and execute appropriate action"""
        logger.info(f"Processing command: {command}")
        
        # Parse the command
        parsed = self.command_parser.parse(command)
        command_type = parsed.get('type')
        intent = parsed.get('intent')
        data = parsed.get('data')
        
        logger.info(f"Command type: {command_type}, Intent: {intent}")
        
        # Handle different command types
        if command_type == 'task':
            return self.handle_task_command(intent, data)
        elif command_type == 'query':
            return self.handle_query_command(intent, data)
        elif command_type == 'reminder':
            return self.handle_reminder_command(intent, data)
        elif command_type == 'control':
            return self.handle_control_command(intent, data)
        else:
            # Use AI brain for general conversation
            return self.ai_brain.generate_response(command)
    
    def handle_task_command(self, intent, data):
        """Handle task-related commands"""
        if intent == 'create':
            task = self.task_manager.create_task(data)
            response = f"I've created a task: {data.get('title', 'New Task')}"
        elif intent == 'list':
            tasks = self.task_manager.get_pending_tasks()
            response = self.format_task_list(tasks)
        elif intent == 'complete':
            self.task_manager.mark_complete(data.get('task_id'))
            response = "Task marked as complete."
        elif intent == 'delete':
            self.task_manager.delete_task(data.get('task_id'))
            response = "Task deleted."
        else:
            response = "I'm not sure what you'd like me to do with that task."
        
        return response
    
    def handle_query_command(self, intent, data):
        """Handle query commands like weather, news, etc."""
        if intent == 'weather':
            weather = self.ai_brain.get_weather(data.get('location', 'current'))
            response = f"The current weather is {weather}"
        elif intent == 'time':
            response = f"The current time is {datetime.now().strftime('%I:%M %p')}"
        elif intent == 'date':
            response = f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"
        elif intent == 'news':
            news = self.ai_brain.get_news()
            response = self.format_news(news)
        else:
            response = self.ai_brain.generate_response(f"Tell me about {intent}")
        
        return response
    
    def handle_reminder_command(self, intent, data):
        """Handle reminder commands"""
        if intent == 'set':
            reminder = self.task_manager.create_reminder(data)
            response = f"I'll remind you to {data.get('text')} at {data.get('time')}"
        elif intent == 'list':
            reminders = self.task_manager.get_reminders()
            response = self.format_reminders(reminders)
        else:
            response = "I can help you with reminders."
        
        return response
    
    def handle_control_command(self, intent, data):
        """Handle control commands (start, stop, etc.)"""
        if intent == 'stop':
            self.running = False
            response = "Goodbye, sir."
        elif intent == 'help':
            response = self.get_help_text()
        else:
            response = "I didn't understand that control command."
        
        return response
    
    def format_task_list(self, tasks):
        """Format tasks for voice output"""
        if not tasks:
            return "You have no pending tasks."
        
        response = f"You have {len(tasks)} pending tasks: "
        for i, task in enumerate(tasks[:5], 1):
            response += f"{i}. {task.get('title', 'Untitled')}. "
        
        if len(tasks) > 5:
            response += f"And {len(tasks) - 5} more."
        
        return response
    
    def format_news(self, news_items):
        """Format news for voice output"""
        if not news_items:
            return "I couldn't fetch the latest news."
        
        response = "Here are the latest news headlines: "
        for i, item in enumerate(news_items[:3], 1):
            response += f"{i}. {item.get('title', 'No title')}. "
        
        return response
    
    def format_reminders(self, reminders):
        """Format reminders for voice output"""
        if not reminders:
            return "You have no active reminders."
        
        response = f"You have {len(reminders)} reminders: "
        for i, reminder in enumerate(reminders[:3], 1):
            response += f"{i}. {reminder.get('text', 'Unnamed')} at {reminder.get('time')}. "
        
        return response
    
    def get_help_text(self):
        """Get help text"""
        return """I can help you with:
        Tasks: Create, list, complete, or delete tasks
        Queries: Check weather, time, date, and news
        Reminders: Set and manage reminders
        Control: Start listening, stop, and more
        Just say 'Jarvis' to wake me up, then give your command.
        """
    
    def run(self):
        """Main run loop for JARVIS"""
        self.running = True
        logger.info("JARVIS is running...")
        self.speak("Good day, sir. I am online and ready to assist.")
        
        try:
            while self.running:
                # Listen for wake word
                if not self.is_woken:
                    logger.info("Waiting for wake word...")
                    command = self.listen()
                    
                    if command and self.check_wake_word(command):
                        self.speak("Yes, sir? How may I assist you?")
                else:
                    # Listen for actual command
                    command = self.listen()
                    
                    if command:
                        response = self.process_command(command)
                        self.speak(response)
                        self.is_woken = False
                    else:
                        self.is_woken = False
        
        except KeyboardInterrupt:
            logger.info("JARVIS interrupted by user")
            self.speak("Shutting down, sir. Farewell.")
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            self.speak("I encountered an error. Please restart me.")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Shutdown JARVIS"""
        logger.info("Shutting down JARVIS...")
        self.running = False
        self.voice_engine.cleanup()
        logger.info("JARVIS shutdown complete")


if __name__ == '__main__':
    jarvis = JARVIS()
    jarvis.run()
