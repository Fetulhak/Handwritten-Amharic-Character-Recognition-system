
import io
import json
import sys,cv2
import scipy.misc
import matplotlib
import matplotlib.pyplot as plt
from keras.models import model_from_json
from keras.models import load_model
from keras import backend as K
K.set_image_dim_ordering('tf')
import os
import re
import base64
import numpy as np
from PIL import Image
from model import model

# Default output
res = {"result": 0,
       "data": [], 
       "error": ''}
img_data_list=[]
cnt = 0
try:

    
    if os.environ["REQUEST_METHOD"] == "POST":

            filepath = ''
            for path, subdirs, files in os.walk('C:\\Users\\user\\Desktop\\HRACRS text generate\\saver\\nn'):
                   for filename in files:
                        f = os.path.join(path, filename)
                        filepath = f
            image = cv2.imread(filepath)
            img = cv2.blur(image, (5, 5))
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret,thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)

            kernel = np.ones((5,200), np.uint8)
            img_dilation = cv2.dilate(thresh, kernel, iterations=1)
            im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[1])

            for i, ctr in enumerate(sorted_ctrs):
                if cv2.contourArea(ctr) > 800:

                    # Get bounding box
                    x, y, w, h = cv2.boundingRect(ctr)

                    # Getting ROI
                    roi = image[y:y+h, x:x+w]
                    im = cv2.resize(roi,None,fx=4, fy=4, interpolation = cv2.INTER_CUBIC)
                    ret_1,thresh_1 = cv2.threshold(im,200,255,cv2.THRESH_BINARY_INV)

                    cv2.bitwise_not(thresh_1, thresh_1)
                    gray = cv2.cvtColor(thresh_1,cv2.COLOR_BGR2GRAY)

                    ret,thresh_2 = cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)
                    kernel = np.ones((5, 5), np.uint8)
                    words = cv2.dilate(thresh_2, kernel, iterations=6)

                    im,ctrs_1, hier = cv2.findContours(words, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    #sort contours
                    sorted_ctrs_1 = sorted(ctrs_1, key=lambda ctr: cv2.boundingRect(ctr)[0])

                    for j, ctr_1 in enumerate(sorted_ctrs_1):
                        if cv2.contourArea(ctr_1) > 800:

                            x_1, y_1, w_1, h_1 = cv2.boundingRect(ctr_1)

                            # Getting ROI
                            roi_1 = thresh_2[y_1:y_1+h_1, x_1:x_1+w_1]

                            resize_img = cv2.resize(roi_1 , (28 , 28))
                            cv2.imwrite("C:\\Users\\user\\Desktop\\HRACRS text generate\\char\\" + str(i) + str(cnt)+".jpg", resize_img)
                            cnt = cnt + 1




except Exception as e:
    # Return error data
    print(str(e))