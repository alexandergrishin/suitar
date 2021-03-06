# -*- coding: utf-8 -*-
"""posenet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ajYkmYeAhQTqsb-2_3Nh4lgdXIPCMM_j

# Installing PoseNet
"""

# Clone the repo and install 3rd-party libraries. 
!git clone https://www.github.com/ildoonet/tf-openpose 
# %cd tf-openpose
!pip3 install -r requirements.txt

# Build c++ library for post processing. See : https://github.com/ildoonet/tf-pose-estimation/tree/master/tf_pose/pafprocess
# %cd tf_pose/pafprocess
!sudo apt install swig
!swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace
# %cd ../..

"""# Test the Posenet api

## Upload image from google drive
"""

!pip install PyDrive
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
import io
import zipfile
from google.colab import files
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

#https://drive.google.com/file/d/1bd0POOdO5R5FimgNL579yTxxif7m79_M/view?usp=sharing
#https://drive.google.com/file/d/10tekxZToYnRxbGVhmiqEcH64WKIyXJdL/view?usp=sharing
#https://drive.google.com/file/d/1m2rtdRzcB9FVMwzFiYg2T7_w9jFLU0dx/view?usp=sharing
#https://drive.google.com/file/d/198ZRSerozSm63m6tL7wK1kT8dAbjYKGw/view?usp=sharing
#https://drive.google.com/file/d/1hzOvII2nQh-VZnnnwHCx2MJtSdfa4T9q/view?usp=sharing
download = drive.CreateFile({'id': '116dCMfKIdh5kv5xTNBhvRoS07uoKMV2B'})
download.GetContentFile('ex1.jpg')
download = drive.CreateFile({'id': '1bd0POOdO5R5FimgNL579yTxxif7m79_M'})
download.GetContentFile('ex2.jpg')
download = drive.CreateFile({'id': '10tekxZToYnRxbGVhmiqEcH64WKIyXJdL'})
download.GetContentFile('ex3.jpg')
download = drive.CreateFile({'id': '1m2rtdRzcB9FVMwzFiYg2T7_w9jFLU0dx'})
download.GetContentFile('ex4.jpg')
download = drive.CreateFile({'id': '198ZRSerozSm63m6tL7wK1kT8dAbjYKGw'})
download.GetContentFile('ex5.jpg')
download = drive.CreateFile({'id': '1hzOvII2nQh-VZnnnwHCx2MJtSdfa4T9q'})
download.GetContentFile('ex6.jpg')

"""# Getting pose"""

import argparse
import logging
import sys
import time

from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
logger = logging.getLogger('TfPoseEstimator')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
w, h = model_wh('432x368')
if w == 0 or h == 0:
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432, 368))
else:
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(w, h))
def pose_estimate(image_path):
    
        
    # estimate human poses from a single image !
    image = common.read_imgfile(image_path, None, None)
    if image is None:
        logger.error('Image can not be read, path=%s' % image)
        sys.exit(-1)
    t = time.time()
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
    elapsed = time.time() - t

    logger.info('inference image: %s in %.4f seconds.' % (image_path, elapsed))
    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    return image

#choose ex1.jpg, ex2.jpg, ex3.jpg or ex4.jpg
image_path = './ex5.jpg'
new_img = pose_estimate(image_path)
new_img_path = './'+'new_'+ image_path[2:]
print(new_img_path)
cv2.imwrite(new_img_path, new_img)

from IPython.display import Image, display
# display(Image(image_path))
display(Image(new_img_path))

"""###Posenet give response in this format: 


```
BodyPart:0-(0.27, 0.18) score=0.84 
BodyPart:1-(0.27, 0.28) score=0.70 
BodyPart:2-(0.19, 0.30) score=0.71 
BodyPart:3-(0.16, 0.47) score=0.72 
BodyPart:4-(0.20, 0.53) score=0.83 
BodyPart:5-(0.36, 0.27) score=0.70 
BodyPart:6-(0.44, 0.42) score=0.81 
BodyPart:7-(0.33, 0.54) score=0.50 
BodyPart:8-(0.23, 0.53) score=0.39 
BodyPart:9-(0.10, 0.61) score=0.80 
BodyPart:10-(0.18, 0.88) score=0.67
BodyPart:11-(0.36, 0.55) score=0.44 
BodyPart:12-(0.25, 0.62) score=0.70 
BodyPart:13-(0.26, 0.90) score=0.62
BodyPart:14-(0.25, 0.16) score=0.80
BodyPart:15-(0.29, 0.16) score=0.90
BodyPart:16-(0.22, 0.18) score=0.80 
BodyPart:17-(0.31, 0.18) score=0.61
```
"""

# to download the processed image
files.download(new_img_path)

