import json, base64, csv
from flask import Flask, request
from flask_cors import CORS, cross_origin
from clarifai.rest import ClarifaiApp

app = Flask(__name__)
CORS(app)
clarifai = ClarifaiApp("-5SCxYdY0ifm_2aSIIKI-XfJ3oKnmS0xDWwR2Z4Q", "BKHGuWa_cHGBns7p92DCHX9Cq6Gug788HQcwwwh6")

def load_carbon_scores():
    scores = {}
    with open('scores.csv') as csvfile:
        rows = csv.reader(csvfile)
        for r in rows:
            scores[r[0]] = r[1]
    return scores

carbon_scores = load_carbon_scores()


@app.route("/")
def hello():
    return "Server is running!\n Predictions Can be found in '/predict'"


@app.route("/predict", methods=['GET', 'POST'])      
def predict():
    img = _get_image_from_request(request)
    # get the general model
    model = clarifai.models.get("general-v1.3")    
    # predict with the model
    resp = model.predict_by_base64(img)
    return json.dumps({'results': _get_terms(resp)})


def _get_terms(resp):
    term_objs = resp['outputs'][0]['data']['concepts']
    return [(t['name'], t['value']) for t in term_objs]

def _get_image_from_request(request):
    image_str = request.get_json()['image']
    return image_str.encode('UTF-8')

def add_carbon_scores(terms):
    [t.append(_get_carbon_score(t[0])) for t in terms]

def _get_carbon_score(term_val):
    if term_val in carbon_scores:
        return carbon_scores[term_val]
    else:
        return 'n/a'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=8080)

