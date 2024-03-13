from flask import Flask, request, render_template
from pickle import load
import numpy as np
import joblib as joblib
import os

# Set Webpage Title
st.set_page_config(page_title="Body signals that predict whether you are a smoker or non-smoker")

# Load the Model
model=joblib.load('')


app=Flask(__name__)
IMG_FOLDER=os.path.join('static','IMG')
app.config['UPLOAD_FOLDER']=IMG_FOLDER
@app.route('/')
def index():
    return render_template('index.html')
class_dict = {
    "0": "Non Smoking"
    "1": "Smoking",
}
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Obtener los valores de todas las variables del formulario
        gender = float(request.form['gender'])
        hemoglobin = float(request.form['hemoglobin'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        triglyceride = float(request.form['triglyceride'])
        Gtp = float(request.form['Gtp'])
        waist = float(request.form['waist'])
        serum_creatinine = float(request.form['serum_creatinine'])
        relaxation = float(request.form['relaxation'])
        dental_caries = float(request.form['dental_caries'])
        fasting_blood_sugar = float(request.form['fasting_blood_sugar'])
        ALT = float(request.form['ALT'])
        systolic = float(request.form['systolic'])
        eyesight_right = float(request.form['eyesight_right'])
        eyesight_left = float(request.form['eyesight_left'])
        AST = float(request.form['AST'])
        urine_protein = float(request.form['urine_protein'])
        hearing_right = float(request.form['hearing_right'])
        hearing_left = float(request.form['hearing_left'])
        cholesterol = float(request.form['cholesterol'])
        LDL = float(request.form['LDL'])
        tartar = float(request.form['tartar'])
        age = float(request.form['age'])
        HDL = float(request.form['HDL'])
        # Crear una lista con los valores de todas las variables
        data = [[gender, hemoglobin, height, weight, triglyceride, Gtp, waist, serum_creatinine,
                 relaxation, dental_caries, fasting_blood_sugar, ALT, systolic, eyesight_right,
                 eyesight_left, AST, urine_protein, hearing_right, hearing_left, cholesterol,
                 LDL, tartar, age, HDL]]
        # Realizar la predicción usando el modelo
        prediction = str(model.predict(data)[0])
        pred_class = class_dict[prediction]
    else:
        pred_class = None
    return render_template('index.html', prediction=pred_class)
if __name__ == '__main__':
    app.run(debug=True)