#Import necessary libraries
from flask import Flask, render_template, request

import numpy as np
import os

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model

#load model
model =load_model("model/model1.h5")

print('@@ Model loaded')


def pred_rice_dieas(rice_plant):
  test_image = load_img(rice_plant, target_size = (56, 56)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  
  result = model.predict(test_image).round(6) # predict diseased palnt or not
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result) # get the index of max value

  if pred == 0:
    return "Diseased Rice  Plant: Blast", 'blast.html' # if index 0 burned leaf
  elif pred == 1:
      return 'Diseased Rice  Plant: Leaf Blight', 'leaf_blight.html' # # if index 1
  elif pred == 2:
      return 'Diseased Rice  Plant: Brown spots', 'brown_spot.html'  # if index 2  fresh leaf
  elif pred == 3:
      return 'Diseased Rice  Plant: Leaf Smut', 'leaf_smut.html' # # if index 1
  elif pred == 4:
      return 'Diseased Rice  Plant: Shealth Blight', 'shealth_blight.html' # # if index 1
  elif pred == 5:
      return 'Diseased Rice  Plant: Tungro', 'tungro.html' # # if index 1
  else:
      return "Healthy Rice  Plant", 'healthy_plant.html' # if index 3

#------------>>pred_rice_dieas<<--end
    

# Create flask instance
app = Flask(__name__)

# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')
    
 
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = pred_rice_dieas(rice_plant=file_path)
              
        return render_template(output_page, pred_output = pred, user_image = file_path)
    
# For local system & cloud
if __name__ == "__main__":
    app.run(threaded=False,) 
    
    