import openai
import logging
from config import OPENAI_API_KEY, WEATHER_API_KEY

logger = logging.getLogger('jarvis')

class AIBrain:
    """Handles AI-powered responses and external API calls"""
    
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.model = "gpt-3.5-turbo"
        logger.info("AI Brain initialized")
    
    def generate_response(self, prompt, context=""):
        """Generate a response using GPT"""
        try:
            full_prompt = f"""{context}
            
User: {prompt}
JARVIS:"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are JARVIS, an AI assistant inspired by the character from Iron Man. You are formal, intelligent, and helpful. Keep responses concise and under 100 words."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            reply = response.choices[0].message.content.strip()
            logger.info(f"Generated response: {reply}")
            return reply
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I'm having difficulty processing that request."
    
    def get_weather(self, location=""):
        """Get weather information"""
        try:
            # Placeholder for weather API integration
            # In production, use OpenWeatherMap or similar service
            logger.info(f"Fetching weather for {location}")
            return "The weather is pleasant today."
        except Exception as e:
            logger.error(f"Error fetching weather: {str(e)}")
            return "I'm unable to fetch weather information at the moment."
    
    def get_news(self):
        """Get latest news headlines"""
        try:
            # Placeholder for news API integration
            # In production, use NewsAPI or similar service
            logger.info("Fetching latest news")
            return [
                {"title": "Technology advancing rapidly"},
                {"title": "New innovations in AI"},
                {"title": "Global economy updates"}
            ]
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")
            return []
