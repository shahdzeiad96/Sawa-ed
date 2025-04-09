
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# the base URL 
OPENAI_API_URL = "https://api.aimlapi.com/v1/chat/completions"
API_KEY = '17c7002d4b0b4654ac1642929c14c89e' 


# Function to communicate with OpenAI's API
def get_chatbot_response(user_message):
    payload = {
        "model": "gpt-4-0125-preview",  
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 150,  
        "temperature": 0.7,  
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload))

    print("Raw API response:", response.text)

    if response.status_code == 200:
        response_data = response.json()
        
        print("Parsed response data:", response_data)

        chatbot_reply = ""
        if "choices" in response_data:
            chatbot_reply = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

        if not chatbot_reply:
            return "Sorry, I couldn't get a valid response from the chatbot."

        return chatbot_reply
    else:
        raise Exception(f"Error from chatbot API: {response.status_code}, {response.text}")

