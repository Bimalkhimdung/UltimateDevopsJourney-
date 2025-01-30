import requests

url = "http://localhost:11415/api/generate"

data = {
    "model": "deepseek/deepseek-r1",
    "prompt": "Explain black holes in simple terms.",
    "stream": False
}

response = requests.post(url, json=data)
result = response.json()

print(result["response"]) 
