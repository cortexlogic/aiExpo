print('Loading libs...')

import numpy as np
import torch
import cv2
from fastai.transforms import *

# the base model of the model we are using
# only necessay for defining the transforms
# can also be skipped but then transforms should be defined explicitly
from fastai.model import resnet34


sz=256 # size of image
print('Loading model...')
model = torch.load('models4deploy/hotdog.h5', map_location='cpu') # load model to cpu
model.eval() # turns model into prediction mode
tfms = tfms_from_model(resnet34, sz) # define transforms

print('running')
cap = cv2.VideoCapture(0) # initiate camera

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # change the channel order and make pixels in range 0-1
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)/255 

    proc = tfms[1](rgb) # send image through transforms
    # create a flipped copy of the image, because bug is causing the model to fail when sending a single image
    proc = np.stack([proc, proc[:,:,::-1]]) 
    proc_V = V(T(proc)) # Turn the array into a torch tensor

    preds = model(proc_V) # get prediction

    prob = np.exp(np.mean(to_np(preds)[:,1])) # turn into mean probability

    # make decision
    if prob > 0.5: label = 'Not Hot Dog'
    else: label = 'Hot Dog'

    # flip image horizontally to give mirror effect when displaying image
    rgb = (rgb[:,::-1,::-1] * 255).astype('uint8')

    # Display the resulting frame with label
    cv2.putText(rgb, label, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)
    cv2.imshow('frame', rgb)
    if cv2.waitKey(1) & 0xFF == ord('q'): # stop program when "Q" is pressed
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
