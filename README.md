# Readme

This Readme is designed to kickstart data science projects by providing a basic setup for database connections, data processing, and machine learning model development. It includes a structured folder organization for your datasets and a set of pre-defined Python packages necessary for most data science tasks.

# Data Science Project Body Signals Of Smoking
Body Signals of Smoking" project aims to develop a system for predicting smoking habits using bodily signals and biomarkers. To achieve this, biomedical data from individuals are collected, including values such as hemoglobin, cholesterol, and blood pressure, among others. These data are used to train a machine learning model, specifically a random forest classifier, which can predict whether a person is a smoker or non-smoker. The application utilizes Streamlit to create a user-friendly interface where users can input their biomedical data through sliders and a dropdown menu. Once the data is entered, the model classifies the user as a smoker or non-smoker. The project seeks to provide a useful tool for early detection of smoking behaviors and potentially contribute to public health initiatives for smoking prevention.

## Structure

The project is organized as follows:

- `app.py` - The main Python script that you run for the project.
- `Project_smoking_Body_Signals.py` - A notebook to explore data, play around, visualize, clean and model definition.
- `utils.py` - This file contains utility code for operations like database connections.
- `requirements.txt` - This file contains the list of necessary python packages.
- `models/` - This directory should contain Models to Predict the data.
- `data/` - This directory contains the following subdirectories:
  - `processed/` - For the final data to be used for modeling and streamlit.
  - `raw/` - For raw data without any processing.
 
    
## Setup

**Prerequisites**
Make sure you have Python 3.11+ installed on your system. You will also need pip to install the Python packages. Running requirements.txt should be enough, but you can install the libraries individually if needed.

**Installation**

Clone the project repository to your local machine.

Navigate to the project directory and install the required Python packages:

```bash
pip install -r /workspaces/Final_Project_Body_Signals/src/requirements.txt
```
```bash
pip install streamlit
```
```bash
pip install seaborn
```
```bash
pip install pycaret
```
```bash
pip install --upgrade pip
```
Errors realated with new versions could give Warnings
```
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
```
```bash
sudo apt-get install ttf-mscorefonts-installer
```

## Running the Application

To run the application, execute the app.py script from the root of the project directory:

```bash
python app.py
```

## Adding Models

```
from pickle import dump

dump(rf_model, open('../models/randomforest_default_42.pkl', 'wb'))
```

## Working with Data

You can place your raw datasets in the data/raw directory and the processed datasets ready for analysis in data/processed.

To process data, you can modify the app.py script to include your data processing steps, utilizing pandas for data manipulation and analysis.

## Contributors

Paola Reyna & Luis Peñafiel
