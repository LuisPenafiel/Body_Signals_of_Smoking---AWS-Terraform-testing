import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler

# FIX: Add is_aws parameter to function signature
def prediction(db, model, scaler, is_aws):  # <-- IMPORTANT CHANGE HERE
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
                gender = st.selectbox("Gender", ["F", "M"], help="Select your gender")
                val2 = st.slider("Gtp", min_value=1.0, max_value=996.0, step=0.1, value=100.0)
                val3 = st.slider("Hemoglobin", min_value=7.4, max_value=18.7, step=0.1, value=12.0)
                val4 = st.slider("Height (cm)", min_value=100.0, max_value=230.0, step=0.1, value=170.0)
            with col2:
                val5 = st.slider("Triglycerides", min_value=31.0, max_value=1029.0, step=0.1, value=150.0)
                val6 = st.slider("Waist (cm)", min_value=80.0, max_value=102.0, step=0.1, value=90.0)
                val7 = st.slider("LDL", min_value=70.0, max_value=300.0, step=0.1, value=100.0)
            with col1:
                val8 = st.slider("HDL", min_value=20.0, max_value=300.0, step=0.1, value=50.0)
                val9 = st.slider("Cholesterol", min_value=300.0, max_value=700.0, step=0.1, value=200.0)
                val10 = st.slider("ALT", min_value=1.0, max_value=996.0, step=0.1, value=20.0)
            with col2:
                val11 = st.slider("Fasting Blood Sugar", min_value=0.0, max_value=126.0, step=0.1, value=90.0)
                val12 = st.slider("Systolic", min_value=0.0, max_value=140.0, step=0.1, value=120.0)
                val13 = st.slider("AST", min_value=10.0, max_value=1543.0, step=0.1, value=25.0)
            with col1:
                val14 = st.slider("Relaxation", min_value=0.0, max_value=120.0, step=0.1, value=80.0)
                val15 = st.slider("Weight (kg)", min_value=35.0, max_value=300.0, step=0.1, value=70.0)
                val16 = st.slider("Age", min_value=0.0, max_value=100.0, step=0.1, value=30.0)
            with col2:
                val17 = st.slider("Serum Creatinine", min_value=0.27, max_value=6.81, step=0.01, value=1.0)
                val18 = st.slider("Eyesight (Left)", min_value=0.0, max_value=2.0, step=0.1, value=1.0)
                val19 = st.slider("Eyesight (Right)", min_value=0.0, max_value=2.0, step=0.1, value=1.0)
                val20 = st.slider("Urine Protein", min_value=1.0, max_value=6.0, step=0.1, value=1.0)

            hearing_left = st.selectbox("Hearing (Left)", ["Normal", "Difficulty"])
            hearing_right = st.selectbox("Hearing (Right)", ["Normal", "Difficulty"])
            tartar = st.selectbox("Tartar", ["No", "Yes"])
            dental_caries = st.selectbox("Dental Caries", ["No", "Yes"])

            if st.form_submit_button("Predict", help="Get your smoking prediction"):
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
                    # Ajuste para coincidir con nombres de características del modelo
                    if hasattr(model, 'feature_names_in_'):
                        if not all(col in model.feature_names_in_ for col in df_scaled.columns):
                            st.warning("Feature names may not match the trained model. Please verify training data in your notebook.")
                    data_normalized = scaler.transform(df_scaled)
                    prediction_result = model.predict(data_normalized)[0]
                    result_text = class_dict[str(prediction_result)]
                    st.success(f"Prediction: **{result_text}**", icon="✅")
                    # FIX: Use the passed is_aws parameter instead of undefined IS_AWS
                    db.save_prediction(gender, val3, result_text, is_aws)  # <-- IMPORTANT CHANGE HERE
                    st.session_state.predictions = st.session_state.get('predictions', 0) + 1
                    st.metric("Total Predictions", st.session_state.predictions)
                except Exception as e:
                    st.error(f"Prediction Error: {e}")