import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
from app_log import log
from mongodb import MongoDB
import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

#Running via Api
@app.route('/predict_api', methods=['POST'])
def predict_api():
    if request.method == 'POST':
        try:
            data = request.json["data"]
            new_data = [list(data.values())]
            output = model.predict(new_data)[0]
            if output == 1:
                text = 'The Forest is in Danger'
            else:
                text = 'Forest is Safe'
            return jsonify(text)

        except Exception as e:
            log.error('error in input from Postman', e)
            return jsonify('Check the input again!')
    else:
        return 'Method not POST'


#Running via html
@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def home():
    try:
        log.info("Home page loaded successfully")
        return render_template('home.html')
    except Exception as e:
        log.exception("Something went wrong on initiation process")


@app.route('/predict',methods=['POST', 'GET'])
@cross_origin()
def predict():
    if request.method == 'POST':
        try:
            data=[float(x) for x in request.form.values()]
            final_features = [np.array(data)]
            output=model.predict(final_features)[0]
            if output == 0:
                text = 'Forest is Safe!'
            else:
                text = 'Forest is in Danger!'
            return render_template('home.html', prediction_text = f"{text} --- Chance of Fire is {output}")     
        except Exception as e:
            log.error('Input error, check input', e)
            return render_template('home.html', prediction_text = "Check the Input again!!!")
    else:
        return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)