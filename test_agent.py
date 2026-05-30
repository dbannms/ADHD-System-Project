import os
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "AIzaSyCtotpkshy08llebRDDeCX_4g872tAORmQ"

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("Available Gemini Models:\n")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)