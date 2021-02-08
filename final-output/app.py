# -*- coding: utf-8 -*-
"""
Created on 
Template modified from BAIS6040
@author: Eric Schelin, Navin Mukraj, Sean O'Bryan
"""
import os
import pandas as pd

import json

from flask import Flask
from flask_restful import Api, Resource, request
import joblib


port = int(os.getenv('PORT', '5000'))

app = Flask(__name__)
api = Api(app)

# argument parsing
#parser = reqparse.RequestParser()
#parser.add_argument('query')
  
class PredictRegression(Resource):
    def get(self):
        model_path = 'data/regressionModel.pkl'
        with open(model_path, 'rb') as f:
            regression_model = joblib.load(f)
                
        # get the query parameters
        #param = request.args.get('param')
        # params = request.args
        params = request.args.to_dict()
        print(params)

        # independents=pd.DataFrame(params,index=[0])
        # independents=pd.DataFrame([params.values()], columns=params.keys())
        independents = pd.DataFrame.from_records([params])

        # make a prediction
        predictions = regression_model.predict(independents)


        # create JSON object
        #pd.DataFrame(predictions, columns=['Prediction'])
        output = pd.DataFrame(predictions, columns=['Prediction']).to_json(orient='table')
        output=json.loads(output)
        
        return output
    
    def post(self):
        model_path = 'data/regressionModel.pkl'
        with open(model_path, 'rb') as f:
            regression_model = joblib.load(f)
                
        # get the form data
        # params = request.form
        params = request.form.to_dict()
        print(params)
        # [('bathrooms', '1'), ('year_buitl', '2000'), ('total_living_area', '2000')]
        # independents=pd.DataFrame(params,index=[0])
        # independents = pd.DataFrame([params.values()], columns=params.keys())
        independents = pd.DataFrame.from_records([params])

        # make a prediction
        predictions = regression_model.predict(independents)

        # create JSON object
        #pd.DataFrame(predictions, columns=['Prediction'])
        output = pd.DataFrame(predictions, columns=['Prediction']).to_json(orient='table')
        output=json.loads(output)
        
        return output

# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictRegression, '/regression')

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=port)