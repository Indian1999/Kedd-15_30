import requests

def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error when accessing jokes:")
        print("HTTP status code:", response.status_code)
        return None
        
while True:
    joke = get_joke()
    print(joke["setup"])
    input()
    print(joke["punchline"])
    input()