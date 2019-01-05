
import io
import json
import sys,cv2
import scipy.misc
import matplotlib
import matplotlib.pyplot as plt
from keras.models import model_from_json
from keras.models import load_model
from keras import backend as K
K.set_image_dim_ordering('th')
import os
import re
import base64
import numpy as np
from PIL import Image

# Default output
res = {"result": 0,
       "data": [], 
       "error": ''}
img_data_list=[]
try:
    # Get post data
    if os.environ["REQUEST_METHOD"] == "POST":
        num_channel=1

        def sorted_nicely( l ): 
            convert = lambda text: int(text) if text.isdigit() else text 
            alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
            return sorted(l, key = alphanum_key)



        filepath = []
        im_list = []
        for path, subdirs, files in os.walk('C:\\Users\\user\\Desktop\\HRACRS text generate\\char'):
                   for filename in files:
                        f = os.path.join(path, filename)
                        filepath.append(f)
        s = set(filepath)
        for filename in sorted_nicely(s):
                image = cv2.imread(filename)
                input_img=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                input_img_resize=cv2.resize(input_img,(28,28))
                #img_data_list.append(input_img_resize)
                im_list.append(input_img_resize)

        img_data = np.array(im_list)
        img_data = img_data.astype('float32')


        img_data = (img_data) / 255.
        print (img_data.shape)

        if num_channel==1:
            if K.image_dim_ordering()=='th':
                img_data= np.expand_dims(img_data, axis=1) 
                print (img_data.shape)
            else:
                img_data= np.expand_dims(img_data, axis=4) 
                print (img_data.shape)

        else:
                if K.image_dim_ordering()=='th':
                    img_data=np.rollaxis(img_data,3,1)
        print (img_data.shape)

        # Load trained model
        model = load_model('cgi-bin/models/model.hdf5')
        list_labels = []
        for data in img_data:
            im_data=data
            im_data= np.expand_dims(im_data, axis=1)
            print (im_data.shape)
             # Predict class
            predictions = model.predict(im_data)[0]
            label = np.argmax(predictions)
            list_labels.append(float(label))

        res["result"] = 1
        res['data'] = list_labels


except Exception as e:
    # Return error data
    res['error'] = str(e)

# Print JSON response
print("Content-type: application/json")
print("") 
print(json.dumps(res))


