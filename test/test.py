import requests
import base64

url = "http://127.0.0.1:5000/predict"
f = open('./burger.jpeg', 'rb')
json = {
    "image": base64.b64encode(f.read()).decode('UTF-8')
}

r = requests.post(url, json=json)

print(r.text)

print('Done')
