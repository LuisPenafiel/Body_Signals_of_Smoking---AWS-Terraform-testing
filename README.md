# Body Signals of Smoking - Data Science Project

This project aims to predict smoking habits using bodily signals and biomarkers. By leveraging a Random Forest Classifier trained on biomedical data—such as hemoglobin, cholesterol, and blood pressure—the system classifies individuals as smokers or non-smokers. A user-friendly Streamlit application allows users to input their data via sliders and dropdowns, delivering real-time predictions. This tool supports early detection of smoking behaviors and contributes to public health initiatives for smoking prevention.

---

## Project Overview

- **Objective**: Develop a machine learning model to predict smoking status based on health markers and provide an interactive interface for users.
- **Dataset**: Biomedical data from individuals, including demographic and physiological features (e.g., age, gender, hemoglobin levels).
- **Model**: Random Forest Classifier with an accuracy of 83.22%, sensitivity of 79.76%, and specificity of 85.36%.
- **Application**: A Streamlit-based UI for inputting data and receiving predictions.
- **Source**: [Kaggle - Body Signal of Smoking](https://www.kaggle.com/datasets/kukuroo3/body-signal-of-smoking)

---

## Project Structure

```
Body_Signals_of_Smoking/
├── app.py                  # Main script to run the Streamlit application
├── Project_smoking_Body_Signals.ipynb  # Jupyter notebook for EDA, cleaning, and model development
├── requirements.txt        # List of required Python packages
├── models/                 # Directory for trained models
│   └── randomforest_default_42.pkl  # Example saved Random Forest model
├── data/                   # Directory for datasets
│   ├── raw/               # Raw, unprocessed data (e.g., smoking.csv)
│   └── processed/         # Processed data ready for modeling
└── README.md              # Project documentation (this file)
```

---

## Setup Instructions

### Prerequisites
- **Python**: Version 3.11 or higher
- **pip**: Package installer for Python
- **Git**: For cloning the repository (optional)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/Body_Signals_of_Smoking.git
   cd Body_Signals_of_Smoking
   ```
2. **Install Dependencies**:
   Install all required packages in one go:
   ```bash
   pip install -r requirements.txt
   ```
   If issues arise, install key libraries individually:
   ```bash
   pip install matplotlib seaborn streamlit pandas numpy scikit-learn xgboost pycaret scipy
   ```
3. **Font Fix (Optional)**:
   If you encounter font-related warnings in Matplotlib:
   ```bash
   sudo apt-get install ttf-mscorefonts-installer  # For Linux systems
   ```

### Running the Application
Launch the Streamlit app from the project root:
```bash
streamlit run app.py
```
- Access the app in your browser at `http://localhost:8501`.

---

## Usage

1. **Home**: Learn about the project and its goals.
2. **Relevant Data**: Explore visualizations of key insights (e.g., gender differences, biomarker trends).
3. **Prediction**: Input your biomedical data using sliders and dropdowns to predict smoking status.
4. **Limitations**: Review dataset limitations and future improvement ideas.

### Adding Models
To save a trained model:
```python
from pickle import dump
dump(rf_model, open('models/randomforest_default_42.pkl', 'wb'))
```

### Working with Data
- Place raw datasets in `data/raw/`.
- Store processed datasets in `data/processed/`.
- Modify `app.py` or the notebook for custom data processing using pandas.

---

## Key Features

- **Interactive UI**: Input data via sliders and dropdowns for instant predictions.
- **Data Visualization**: Insights into smoking-related trends (e.g., hemoglobin, triglycerides).
- **Scalable Design**: Easily extendable with additional models or features.

---

## Model Performance

The Random Forest Classifier achieved:
- **Accuracy**: 83.22%
- **Sensitivity**: 79.76% (correctly identifies smokers)
- **Specificity**: 85.36% (correctly identifies non-smokers)

See `Project_smoking_Body_Signals.ipynb` for confusion matrix and detailed evaluation.

---

## Notebook Breakdown: `Project_smoking_Body_Signals.ipynb`

The Jupyter notebook (`Project_smoking_Body_Signals.ipynb`) is the core exploratory and modeling environment for this project. Below is a detailed breakdown of its sections and what was accomplished in each:

1. **Introduction and Objective**:
   - Defines the project's goal: predicting smoking status using health markers.
   - Links to the Kaggle dataset and outlines the purpose of the analysis.

2. **Imports**:
   - Loads essential Python libraries for:
     - **EDA and Visualization**: `pandas`, `numpy`, `matplotlib`, `seaborn`.
     - **Machine Learning**: `scikit-learn` (e.g., `RandomForestClassifier`, `StandardScaler`), `xgboost`, `pycaret`.
   - Includes fixes for font issues in Matplotlib visualizations.

3. **Loading Data**:
   - Reads the raw dataset (`smoking.csv`) from `data/raw/` into a pandas DataFrame.
   - Displays initial rows (`head()`) to inspect the data structure.

4. **First Blick (Exploratory Data Analysis - EDA)**:
   - **Overview**: Examines data format, features (e.g., gender, hemoglobin), and target variable (`smoking`).
   - **Actions**:
     - Checks dataset shape (55,692 rows, 27 columns) and data types (`info()`).
     - Identifies categorical (e.g., `gender`, `tartar`) and numerical features.
     - Flags potential preprocessing needs (e.g., encoding categoricals, handling missing values).
   - **Insights**: Confirms no missing values and highlights the need for further visualization.

5. **Data Visualization**:
   - **Purpose**: Visualizes relationships between features and smoking status.
   - **Actions**:
     - Generates plots (e.g., heatmaps, bar charts) to explore correlations and distributions.
     - Highlights trends like higher hemoglobin or triglyceride levels in smokers.
   - **Output**: Visuals used in the Streamlit app’s "Relevant Data" section.

6. **Preprocessing and Feature Engineering**:
   - **Actions**:
     - Encodes categorical variables (e.g., `gender`: F/M to 0/1, `tartar`: N/Y to 0/1).
     - Scales numerical features using `StandardScaler` for model compatibility.
     - Splits data into training and testing sets (`train_test_split`).
   - **Output**: Prepares `total_data_c2.csv` in `data/processed/` for modeling.

7. **Model Development**:
   - **Approach**: Tests multiple models (e.g., Logistic Regression, SVM, Random Forest) using `scikit-learn` and `pycaret`.
   - **Focus**: Optimizes a Random Forest Classifier as the final model.
   - **Actions**:
     - Trains the model on scaled data.
     - Saves the trained model as `randomforest_default_42.pkl` in `models/`.
   - **Tools**: Uses `GridSearchCV` for hyperparameter tuning (if applicable).

8. **Model Evaluation**:
   - **Actions**:
     - Generates predictions (`y_pred_random`) on the test set.
     - Computes a confusion matrix using `confusion_matrix`.
     - Calculates metrics: Accuracy (83.22%), Sensitivity (79.76%), Specificity (85.36%).
   - **Visualization**: Creates a heatmap of the confusion matrix with true positives (TP), false positives (FP), etc.
   - **Conclusions**: Confirms Random Forest as the best performer for this dataset.

9. **Conclusions**:
   - Summarizes model performance and its implications for smoking prediction.
   - Notes the balance between sensitivity and specificity, indicating reliable classification.

---

## Limitations & Future Improvements

### Current Limitations
- No temporal or geographic context for the data.
- Limited demographic and behavioral variables.

### Potential Enhancements
1. Add demographic data (e.g., education, income).
2. Include physiological markers (e.g., exhaled CO levels).
3. Incorporate behavioral data (e.g., smoking frequency).
4. Account for cultural and environmental factors.
5. Use user feedback to refine the model and UI.

---

## Contributors

- **Paola Reyna**
- **Luis Peñafiel**

---

## License

This project is unlicensed and open for educational use. Please attribute the contributors if reused.

