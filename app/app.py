from flask import Flask, request, jsonify, render_template
from flask.logging import create_logger
import logging

import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler

from predict import model_fn, predict_fn

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def scale(payload):
    """Scales Payload"""

    LOG.info("Scaling Payload: \n %s" , payload)
    scaler = StandardScaler().fit(payload.astype(float))
    scaled_adhoc_predict = scaler.transform(payload.astype(float))
    return scaled_adhoc_predict

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    LOG.info("==========")
    if request.method == "POST":
        LOG.info("I am a post")
        if request.form:
            LOG.info("I have form data")
            #print(request.form['kommentar'])
        if request.data:
            LOG.info("I have data")
            LOG.info(request.data)
        if request.json:
            LOG.info("I have json")
            # Do stuff with the data...
            return jsonify({"message": "OK"})
        else:
            LOG.info("fail")

    data = request.data
    LOG.info("Form data is: \n %s", data.decode('utf-8'))

    # get an output prediction from the pretrained model, model
    result = predict_fn(data.decode('utf-8'),model)
    LOG.info("Prediction value is: %s", result)
    return str(result)


if __name__ == "__main__":
    # load pretrained model as model
    model = model_fn("./model")
    app.run(host='0.0.0.0', port=80, debug=True) # specify port=80
