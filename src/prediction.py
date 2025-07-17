import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler

def prediction(db, model, scaler, is_aws):
    """Maneja la sección de predicción de fumadores."""
    st.header("Smoking Prediction :no_smoking:")
    st.subheader("Enter Your Data for Analysis")
    st.markdown('<div class="medical-badge">PATIENT ASSESSMENT</div>', unsafe_allow_html=True)
    
    with st.container():
        st.write("Enter patient biomarkers for smoking status prediction:")
        
        class_dict = {"0": "Non-Smoker", "1": "Smoker"}
        num_variables = ['gender', 'Gtp', 'hemoglobin', 'height(cm)', 'triglyceride', 'waist(cm)', 'LDL', 'HDL',
                         'Cholesterol', 'ALT', 'fasting blood sugar', 'systolic', 'AST', 'relaxation', 'weight(kg)',
                         'age', 'serum creatinine', 'eyesight(left)', 'eyesight(right)', 'tartar', 'dental caries',
                         'Urine protein', 'hearing(left)', 'hearing(right)']

        with st.form(key='prediction_form'):
            col1, col2 = st.columns(2)
            with col1:
                gender = st.selectbox("Gender", ["F", "M"])
                val2 = st.slider("Gtp", 1.0, 996.0, 100.0)
                val3 = st.slider("Hemoglobin", 7.4, 18.7, 12.0)
                val4 = st.slider("Height (cm)", 100.0, 230.0, 170.0)
            with col2:
                val5 = st.slider("Triglycerides", 31.0, 1029.0, 150.0)
                val6 = st.slider("Waist (cm)", 80.0, 102.0, 90.0)
                val7 = st.slider("LDL", 70.0, 300.0, 100.0)
            with col1:
                val8 = st.slider("HDL", 20.0, 300.0, 50.0)
                val9 = st.slider("Cholesterol", 300.0, 700.0, 200.0)
                val10 = st.slider("ALT", 1.0, 996.0, 20.0)
            with col2:
                val11 = st.slider("Fasting Blood Sugar", 0.0, 126.0, 90.0)
                val12 = st.slider("Systolic", 0.0, 140.0, 120.0)
                val13 = st.slider("AST", 10.0, 1543.0, 25.0)
            with col1:
                val14 = st.slider("Relaxation", 0.0, 120.0, 80.0)
                val15 = st.slider("Weight (kg)", 35.0, 300.0, 70.0)
                val16 = st.slider("Age", 0.0, 100.0, 30.0)
            with col2:
                val17 = st.slider("Serum Creatinine", 0.27, 6.81, 1.0)
                val18 = st.slider("Eyesight (Left)", 0.0, 2.0, 1.0)
                val19 = st.slider("Eyesight (Right)", 0.0, 2.0, 1.0)
                val20 = st.slider("Urine Protein", 1.0, 6.0, 1.0)

            hearing_left = st.selectbox("Hearing (Left)", ["Normal", "Difficulty"])
            hearing_right = st.selectbox("Hearing (Right)", ["Normal", "Difficulty"])
            tartar = st.selectbox("Tartar", ["No", "Yes"])
            dental_caries = st.selectbox("Dental Caries", ["No", "Yes"])

            if st.form_submit_button("Predict"):
                gender_value = 1 if gender == "M" else 0
                hearing_left_value = 1 if hearing_left == "Normal" else 2
                hearing_right_value = 1 if hearing_right == "Normal" else 2
                tartar_value = 0 if tartar == "No" else 1
                dental_caries_value = 0 if dental_caries == "No" else 1

                data = {
                    "gender": [gender_value],
                    "Gtp": [val2],
                    "hemoglobin": [val3],
                    "height(cm)": [val4],
                    "triglyceride": [val5],
                    "waist(cm)": [val6],
                    "LDL": [val7],
                    "HDL": [val8],
                    "Cholesterol": [val9],
                    "ALT": [val10],
                    "fasting blood sugar": [val11],
                    "systolic": [val12],
                    "AST": [val13],
                    "relaxation": [val14],
                    "weight(kg)": [val15],
                    "age": [val16],
                    "serum creatinine": [val17],
                    "eyesight(left)": [val18],
                    "eyesight(right)": [val19],
                    "tartar": [tartar_value],
                    "dental caries": [dental_caries_value],
                    "Urine protein": [val20],
                    "hearing(left)": [hearing_left_value],
                    "hearing(right)": [hearing_right_value]
                }
                df_scaled = pd.DataFrame(data, columns=num_variables)

                try:
                    if hasattr(model, 'feature_names_in_'):
                        if not all(col in model.feature_names_in_ for col in df_scaled.columns):
                            st.warning("Feature names may not match the trained model.")
                    data_normalized = scaler.transform(df_scaled)
                    prediction_result = model.predict(data_normalized)[0]
                    result_text = class_dict[str(prediction_result)]
                    st.success(f"Prediction: **{result_text}**")
                    db.save_prediction(gender, val3, result_text, is_aws)
                    st.session_state.predictions = st.session_state.get('predictions', 0) + 1
                    st.metric("Total Predictions", st.session_state.predictions)
                except Exception as e:
                    st.error(f"Prediction Error: {e}")