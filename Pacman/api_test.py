import requests
import time

url = "https://pacman-a10cd-default-rtdb.europe-west1.firebasedatabase.app/highscores.json"

data = {
    "username": "Willie",
    "score": 9999999,
    "timestamp": time.time()
}

try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Data sent successfully")
    else:
        print("Error:", response.status_code)
except Exception as ex:
    print("Error:", ex)
    
""" Hibakezelés 101
while True:
    try:
        a = int(input("a = "))
        b = int(input("b = "))
        print(f"{a} / {b} = {a / b}")
    except ZeroDivisionError:
        print("Nullával nem szabad osztani!")
    except ValueError:
        print("value error")
    except Exception as ex:
        print(ex)
"""