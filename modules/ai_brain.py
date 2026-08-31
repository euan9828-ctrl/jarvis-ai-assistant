"""
AI Brain Module - Powers JARVIS with AI responses using Google Generative AI
"""

import os
import requests
import wikipedia
from dotenv import load_dotenv

load_dotenv()


class AIBrain:
    """AI Brain for JARVIS - Handles intelligent responses"""
    
    def __init__(self):
        """Initialize AI brain"""
        self.api_key = os.getenv("GOOGLE_API_KEY", "")
        self.model_name = "gemini-pro"
        
        print("✓ AI Brain initialized")
    
    def get_response(self, query):
        """
        Get AI response to a query
        
        Args:
            query (str): User query
            
        Returns:
            str: AI response
        """
        # Try Wikipedia first for factual queries
        if self.is_factual_query(query):
            wiki_response = self.get_wikipedia_response(query)
            if wiki_response:
                return wiki_response
        
        # Fall back to Google Generative AI
        return self.get_generative_response(query)
    
    def is_factual_query(self, query):
        """Check if query is likely factual (Wikipedia-suitable)"""
        factual_keywords = [
            "who is", "what is", "when was", "where is", "how many",
            "define", "explain", "tell me about", "what are", "which",
            "biography", "history", "country", "city", "inventor", "scientist"
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in factual_keywords)
    
    def get_wikipedia_response(self, query):
        """Get response from Wikipedia"""
        try:
            # Extract search term from query
            search_term = query.replace("what is", "").replace("who is", "").strip()
            
            # Search Wikipedia
            results = wikipedia.search(search_term, results=1)
            
            if results:
                summary = wikipedia.summary(results[0], sentences=2)
                return f"According to Wikipedia: {summary}"
            
            return None
        
        except wikipedia.exceptions.DisambiguationError:
            return "I found multiple results. Could you be more specific?"
        except wikipedia.exceptions.PageError:
            return None
        except Exception as e:
            print(f"❌ Wikipedia error: {str(e)}")
            return None
    
    def get_generative_response(self, query):
        """Get response from Google Generative AI"""
        try:
            # If API key not set, provide helpful response
            if not self.api_key:
                return self.get_fallback_response(query)
            
            # Try using Google Generative AI
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)
            
            # Generate response with system prompt
            system_prompt = """You are JARVIS, an AI assistant inspired by Tony Stark's AI.
            You are helpful, witty, and professional.
            Keep responses concise and to the point.
            """
            
            response = model.generate_content(f"{system_prompt}\n\nUser: {query}")
            
            return response.text if response else self.get_fallback_response(query)
        
        except Exception as e:
            print(f"❌ AI generation error: {str(e)}")
            return self.get_fallback_response(query)
    
    def get_fallback_response(self, query):
        """Provide a fallback response when AI is unavailable"""
        query_lower = query.lower()
        
        responses = {
            "hello": "Good day. How may I assist you?",
            "how are you": "I am functioning at optimal levels, thank you for asking.",
            "what's your name": "I am JARVIS, your personal AI assistant.",
            "thanks": "You're welcome. Happy to help.",
            "bye": "Goodbye. Call me if you need anything.",
        }
        
        for key, response in responses.items():
            if key in query_lower:
                return response
        
        return f"I'm thinking about: {query}. Unfortunately, I need internet connectivity for full AI responses. Please set up the GOOGLE_API_KEY in your .env file."
    
    def ask_question(self, question):
        """Ask a question and get response"""
        return self.get_response(question)
