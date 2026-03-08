# Model Files
This folder contains the trained deep learning model used for malaria detection.

## Files
### malaria_model.h5
This file contains the trained Convolutional Neural Network (CNN) model used to classify blood smear images.
The model predicts whether a red blood cell image is:
* Parasitized
* Uninfected

The model was trained using a malaria cell image dataset.
### labels.txt
This file contains the class labels used by the model during prediction.
Example labels:
Parasitized
Uninfected
## Usage
The model is loaded in the Flask application using TensorFlow/Keras.
Example:
```
from tensorflow.keras.models import load_model

model = load_model("model/malaria_model.h5")
```

The model then predicts the class of uploaded blood smear images.

