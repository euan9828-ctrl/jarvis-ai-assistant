import re
import logging
from datetime import datetime, timedelta

logger = logging.getLogger('jarvis')

class CommandParser:
    """Parses voice commands into structured commands"""
    
    def __init__(self):
        self.task_keywords = ['task', 'todo', 'add', 'create', 'list', 'complete', 'done', 'delete', 'remove']
        self.query_keywords = ['weather', 'time', 'date', 'news', 'tell me', 'what is', 'how']
        self.reminder_keywords = ['remind', 'reminder', 'remember', 'alert']
        self.control_keywords = ['stop', 'quit', 'exit', 'help', 'status']
        logger.info("Command Parser initialized")
    
    def parse(self, text):
        """Parse a natural language command"""
        if not text:
            return {'type': 'unknown', 'intent': None, 'data': {}}
        
        text_lower = text.lower()
        
        # Determine command type
        if any(keyword in text_lower for keyword in self.control_keywords):
            return self.parse_control_command(text)
        elif any(keyword in text_lower for keyword in self.task_keywords):
            return self.parse_task_command(text)
        elif any(keyword in text_lower for keyword in self.reminder_keywords):
            return self.parse_reminder_command(text)
        elif any(keyword in text_lower for keyword in self.query_keywords):
            return self.parse_query_command(text)
        else:
            return {'type': 'conversation', 'intent': 'chat', 'data': {'text': text}}
    
    def parse_task_command(self, text):
        """Parse task-related commands"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['list', 'show', 'what', 'get']):
            return {'type': 'task', 'intent': 'list', 'data': {}}
        elif any(word in text_lower for word in ['complete', 'done', 'finish', 'mark']):
            return {'type': 'task', 'intent': 'complete', 'data': {}}
        elif any(word in text_lower for word in ['delete', 'remove', 'remove']):
            return {'type': 'task', 'intent': 'delete', 'data': {}}
        else:
            # Extract task title
            title = self.extract_title(text)
            return {'type': 'task', 'intent': 'create', 'data': {'title': title}}
    
    def parse_reminder_command(self, text):
        """Parse reminder-related commands"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['list', 'show', 'get']):
            return {'type': 'reminder', 'intent': 'list', 'data': {}}
        else:
            # Extract reminder text and time
            reminder_text = self.extract_title(text)
            time_info = self.extract_time(text)
            return {'type': 'reminder', 'intent': 'set', 'data': {'text': reminder_text, 'time': time_info}}
    
    def parse_query_command(self, text):
        """Parse query commands"""
        text_lower = text.lower()
        
        if 'weather' in text_lower:
            location = self.extract_location(text)
            return {'type': 'query', 'intent': 'weather', 'data': {'location': location}}
        elif 'time' in text_lower:
            return {'type': 'query', 'intent': 'time', 'data': {}}
        elif 'date' in text_lower:
            return {'type': 'query', 'intent': 'date', 'data': {}}
        elif 'news' in text_lower:
            return {'type': 'query', 'intent': 'news', 'data': {}}
        else:
            return {'type': 'query', 'intent': 'general', 'data': {'query': text}}
    
    def parse_control_command(self, text):
        """Parse control commands"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['stop', 'quit', 'exit']):
            return {'type': 'control', 'intent': 'stop', 'data': {}}
        elif 'help' in text_lower:
            return {'type': 'control', 'intent': 'help', 'data': {}}
        elif 'status' in text_lower:
            return {'type': 'control', 'intent': 'status', 'data': {}}
        else:
            return {'type': 'control', 'intent': 'unknown', 'data': {}}
    
    def extract_title(self, text):
        """Extract task/reminder title from text"""
        # Remove common prefixes
        cleaned = re.sub(r'(create|add|make|set|remind me to|task|todo)\s+', '', text, flags=re.IGNORECASE)
        return cleaned.strip()
    
    def extract_time(self, text):
        """Extract time information from text"""
        # Simple time extraction - can be improved with NLP
        time_patterns = {
            'in 5 minutes': (datetime.now() + timedelta(minutes=5)).isoformat(),
            'in 10 minutes': (datetime.now() + timedelta(minutes=10)).isoformat(),
            'in 1 hour': (datetime.now() + timedelta(hours=1)).isoformat(),
            'tomorrow': (datetime.now() + timedelta(days=1)).isoformat(),
        }
        
        for pattern, time_value in time_patterns.items():
            if pattern in text.lower():
                return time_value
        
        return datetime.now().isoformat()
    
    def extract_location(self, text):
        """Extract location from text"""
        # Simple location extraction
        location_keywords = ['in', 'at', 'for']
        for keyword in location_keywords:
            if keyword in text.lower():
                parts = text.lower().split(keyword)
                if len(parts) > 1:
                    return parts[-1].strip().split()[0]
        return 'current location'
