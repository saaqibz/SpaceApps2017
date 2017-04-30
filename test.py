import requests
import base64
import csv
from server import add_carbon_scores, load_carbon_scores

def test1():
    url = "http://127.0.0.1:5000/predict"
    f = open('./burger.jpeg', 'rb')
    json = {
        "image": base64.b64encode(f.read()).decode('UTF-8')
    }

    r = requests.post(url, json=json)

    print(r.text)

    print('Done')

def test2():
    terms = [['black-bean-taco', .99]]
    csv = load_carbon_scores()
    add_carbon_scores(terms)
    print(terms)

if __name__ == '__main__':
    #test1()
    test2()