from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
import torch
import cv2
from fastai.transforms import *
from fastai.model import resnet34
from fastai.dataset import open_image

print('Libraries Loaded.')

app = Flask(__name__)
api = Api(app)

print('Loading model ...')
model = torch.load('../data/export/hotdog.h5')
model.eval()
sz=224
tfms = tfms_from_model(resnet34, sz, aug_tfms=transforms_side_on, max_zoom=1.1)

print('Ready to predict!')

# argument parsing
#parser = reqparse.RequestParser()
#parser.add_argument('data')

class isHotDog(Resource):
    def post(self):
        # use parser and find the user's query
        #args = parser.parse_args()
        #print(args)
        #user_query = args['data']#/255
        #print(type(user_query))

        r = request
        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)/255
        
        proc = tfms[1](img)
        proc = np.stack([proc, proc[:,:,::-1]])
        proc_V = V(T(proc))

        preds = model(proc_V)

        prob = np.exp(np.mean(to_np(preds)[:,1]))

        if prob > 0.5: label = 'Not Hot Dog'
        else: label = 'Hot Dog'

        # create JSON object
        output = {'prediction': label} #, 'confidence': round(prob,4)
        
        return output


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(isHotDog, '/')


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',
            port=5000, 
            debug=True)
