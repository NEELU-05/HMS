import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

print(f"Testing Gemini API with key: {api_key[:5]}...{api_key[-5:]}")

try:
    genai.configure(api_key=api_key)
    # Try the standard model first
    model = genai.GenerativeModel('gemini-pro')
    print("Attempting to generate content with 'gemini-pro'...")
    response = model.generate_content("Hello, are you working?")
    print("Success! Response:", response.text)
except Exception as e:
    print("\nERROR DETAILS:")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")
    
    # If that fails, list available models
    print("\nListing available models for this key:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as list_err:
        print(f"Could not list models: {list_err}")
