import base64
from flask import Flask, request
from clarifai.rest import ClarifaiApp

app = Flask(__name__)
clarifai = ClarifaiApp("-5SCxYdY0ifm_2aSIIKI-XfJ3oKnmS0xDWwR2Z4Q", "BKHGuWa_cHGBns7p92DCHX9Cq6Gug788HQcwwwh6")

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
    return "{}".format(_get_terms(resp))


def _get_terms(resp):
    term_objs = resp['outputs'][0]['data']['concepts']
    return [(t['name'], t['value']) for t in term_objs]

def _get_image_from_request(request):
    image_str = request.get_json()['image']
    return image_str.encode('UTF-8')


if __name__ == "__main__":
    app.run(debug=True, port=5000)