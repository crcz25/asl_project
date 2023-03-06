# American Sign Language Recognition using ConvNeXtBase and OAK-D Camera
Hardware Acceleration for AI - Final Project

## Group Members
- Carlos Cueto
- Henry Ascencio
- Vasista Kodumagulla
- Aman Vyas


## Project Description
Develop a CNN to classify hand gestures into the 26 letters of the American Sign Language Alphabet, and measure the performance of the CNN locally and on an API server.

## Requirements
- OAK-D Camera

## Project Structure
- `backend` - Contains the code for the API server. The API server is written in Python using Django and Django Rest Framework.
    - `models` - Contains the code for the models used in the API server.
    - `image_processing` - Contains the code for the image processing functions used in the API server.
- `client` - Contains the code for the client application. It contains two parts:
    - `local_prediction` - Contains the code for the local prediction application. It is written in Python using Keras and Tensorflow.
    - `server_prediction` - Contains the code for the server prediction application. It is written in Python using Keras and Tensorflow.
- `model` - Contains the Jupiter Notebook used to train the model. It will generate the directory `asl_model` which contains the model and the weights. You can find the model and the weights in the directory `backend/models/asl_model`.
    - `american_sign_language` - Contains the dataset used to train the model. It was obtanied from [here](https://www.kaggle.com/datasets/ayuraj/american-sign-language-dataset).

## Running the Project
- To run the API server, navigate to the `backend` directory and run the following commands:
    - `python manage.py makemigrations`
    - `python manage.py migrate`
    - `python manage.py runserver`
- To run the local prediction application, navigate to the `client` directory and run the following commands:
    - `python local_prediction.py`
- To run the server prediction application, navigate to the `client` directory and run the following commands:
    - `python server_prediction.py`

## References
- [Dataset](https://www.kaggle.com/datasets/ayuraj/american-sign-language-dataset)
- [ConvNeXtBase](https://www.tensorflow.org/api_docs/python/tf/keras/applications/convnext/ConvNeXtBase)
- [OAK-D Camera](https://docs.luxonis.com/en/latest/pages/tutorials/first_steps/)