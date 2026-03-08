# Malaria Detection Using Deep Learning
## Project Description
Malaria is a serious and life-threatening disease caused by parasites transmitted through mosquito bites. Early detection of malaria is important for effective treatment. Traditional diagnosis using microscopic examination of blood smear images requires skilled professionals and can be time-consuming.
This project uses **Deep Learning (Convolutional Neural Networks)** to automatically detect malaria parasites from blood smear images. The model classifies images into two categories:
* **Parasitized (infected)**
* **Uninfected (healthy)**
A **Flask web application** is built to allow users to upload an image and get a prediction from the trained model.


# Features
* Deep Learning model for malaria detection
* Image classification using CNN
* Web interface for uploading images
* Real-time prediction using a trained model
* Organized project structure for easy understanding

# Dataset
The dataset used in this project contains microscopic images of red blood cells.

Classes:
* Parasitized
* Uninfected

Dataset Source:
https://www.kaggle.com/datasets/iarunava/cell-images-for-detecting-malaria

Total Images: **27,000+ blood smear images**


# Technologies Used
* Python
* TensorFlow / Keras
* OpenCV
* NumPy
* Flask
* HTML
* CSS
* Matplotlib
* Scikit-learn


# Project Structure
Malaria-Detection/
dataset/
Contains training and testing image data
model/
Contains the trained deep learning model
notebooks/
Jupyter notebooks used for training and experimentation
static/
Static files such as CSS, images, and uploaded files
templates/
HTML files used for the Flask web interface
app.py
Main Flask application file
requirements.txt
List of required Python libraries
README.md
Project documentation


# Model Architecture
The deep learning model used is a **Convolutional Neural Network (CNN)** designed for image classification.

Main layers used:
* Convolutional Layers
* Max Pooling Layers
* Flatten Layer
* Dense Layers
* Sigmoid Output Layer

The model learns features from blood smear images to detect malaria parasites.


# Installation
Clone the repository
git clone https://github.com/Samruddhi1595/malaria_detection

Navigate to the project folder
cd malaria-detection

Install required dependencies

pip install -r requirements.txt


# How to Run the Project
Run the Flask application
python app.py
Open your browser and go to
http://127.0.0.1:5000/
Upload a blood smear image and the model will predict whether it is **Parasite**
