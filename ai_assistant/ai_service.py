import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

class AIAssistant:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def chat(self, user_message: str, context: dict = None) -> str:
        """Send a message to Gemini with optional context."""
        
        system_prompt = self._build_system_prompt(context)
        
        # Combine system prompt and user message
        full_prompt = f"{system_prompt}\n\nUser Query: {user_message}"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"AI Error: {e}")
            return "I apologize, but I'm having trouble connecting to the AI service right now. Please try again later."
    
    def _build_system_prompt(self, context: dict = None) -> str:
        base_prompt = """You are a helpful, professional AI assistant for the 'HealthPlus' Hospital Management System.
        
        Your capabilities:
        1. Help staff find patient details and medical history.
        2. Check doctor schedules and appointments.
        3. Provide general medical information (always clarify you are an AI, not a doctor).
        4. Summarize hospital statistics.
        
        Guidelines:
        - Be concise and direct.
        - Format lists clearly.
        - If you don't have the data in the context provided, say "I don't have access to that information right now."
        - Do not make up patient data.
        """
        
        if context:
            base_prompt += f"\n\nCURRENT SYSTEM DATA (Use this to answer):\n{json.dumps(context, indent=2)}"
            
        return base_prompt
