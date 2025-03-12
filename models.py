import google.generativeai as genai

genai.configure(api_key="AIzaSyANKkeejIAj6tr-ekfXw6uPUIr1mVGW2QE")  # Replace with your API Key

# List all available models
models = genai.list_models()
for model in models:
    print(model.name)
