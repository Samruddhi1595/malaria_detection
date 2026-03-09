app.py

This file contains the main backend application for the Malaria Detection System built using Flask.

The script initializes the web server, loads the trained deep learning model, processes uploaded images, and returns prediction results to the user interface.

Main Responsibilities

Model Loading

Imports TensorFlow and loads the trained CNN model (.h5 file).

Automatically detects the model file in the project directory.

Compiles the model using:

Optimizer: Adam

Loss Function: Binary Crossentropy

Metric: Accuracy

Image Preprocessing
The prepare_image() function prepares uploaded images before passing them to the model.

Steps include:

Opening the image using PIL

Converting images to RGB format if needed

Resizing images to match the model's input shape

Normalizing pixel values between 0 and 1

Expanding dimensions to match CNN input requirements

Prediction API
The /predict route receives uploaded images and performs classification.

Workflow:

Accept uploaded image from the client

Preprocess image

Run CNN model prediction

Determine classification threshold

Return results in JSON format

Returned information includes:

Prediction label (Parasitized / Uninfected)

Confidence score

Probability for both classes

Timestamp of prediction

Health Check Endpoint
The /health route provides a system status check indicating whether:

The server is running

The model is successfully loaded

Server Initialization
When the script runs:

It creates required folders (templates, static) if they do not exist

Starts the Flask development server

Displays system information such as:

Model status

Input shape

Server URL
