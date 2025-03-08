# Body Signals of Smoking on AWS with Terraform

This project predicts smoking habits using biomedical health markers, leveraging a Random Forest model and an interactive Streamlit interface, deployed on AWS using Infrastructure as Code (IaC) with Terraform.

## Deployment on AWS with Terraform

- **Cloud Infrastructure**:
  - **AWS S3**: Stores `smoking.csv` and files in `smoking-body-signals-data-dev`.
  - **AWS EC2**: A t2.micro instance runs the Streamlit app (accessible at `http://<public_ip>`).
  - **AWS RDS (optional)**: MySQL database for model metrics in `eu-central-1`.
- **Terraform**:
  - **main.tf**: Configures AWS resources (S3, EC2, RDS) for the deployment.
  - **variables.tf**: Defines variables like the region (`eu-central-1`), environment (`dev`), and RDS password.
  - **outputs.tf**: Provides outputs such as the S3 bucket name (`smoking-body-signals-data-dev`), EC2 public IP, and RDS endpoint.

## AWS Deployment Instructions

1. Configure AWS CLI with `aws configure` using the `eu-central-1` region.
2. Clone this repository and run `terraform init`, `terraform plan`, `terraform apply` from the `/terraform` folder.
3. Upload `smoking.csv` and files to S3 with `aws s3 cp data/raw/smoking.csv s3://smoking-body-signals-data-dev/data/raw/` and `aws s3 cp src/ s3://smoking-body-signals-data-dev/src/ --recursive`.
4. Connect to EC2, install dependencies, and run `streamlit run src/app.py --server.port 80 --server.address 0.0.0.0`.

## Screenshots
- [Images of the app on EC2 (http://<public_ip>), S3 bucket, terraform apply output].

---

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

## Setup Instructions

### Prerequisites
- **Python**: Version 3.11 or higher
- **pip**: Package installer for Python
- **Git**: For cloning the repository (optional)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LuisPenafiel/Body_Signals_of_Smoking.git
   cd Body_Signals_of_Smoking

---

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

## Setup Instructions

### Prerequisites
- **Python**: Version 3.11 or higher
- **pip**: Package installer for Python
- **Git**: For cloning the repository (optional)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LuisPenafiel/Body_Signals_of_Smoking.git
   cd Body_Signals_of_Smoking


---

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

## Setup Instructions

### Prerequisites
- **Python**: Version 3.11 or higher
- **pip**: Package installer for Python
- **Git**: For cloning the repository (optional)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LuisPenafiel/Body_Signals_of_Smoking.git
   cd Body_Signals_of_Smoking


---



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
.
.
├── .devcontainer/               # Dev container configuration (for VSCode)
├── .vscode/                     # VSCode workspace settings
├── data/                        # Data directory
│   ├── interim/                 # Intermediate data (e.g., cleaned or transformed data)
│   ├── processed/               # Processed data (e.g., final datasets for modeling)
│       └── total_data_c2.csv    # Processed dataset
│   └── raw/                     # Raw data (e.g., original datasets)
│       └── smoking.csv          # Raw dataset
├── models/                      # Trained models
│   └── random_forest_model_Default.pkl  # Saved model
├── src/                         # Source code
│   ├── GTP.png                  # Image/plot
│   ├── Gender_smoking.png       # Image/plot
│   ├── Project_Smoking_Body_Signals.ipynb  # Jupyter Notebook
│   ├── Triglyceride.png         # Image/plot
│   ├── app.py                   # Python script (e.g., Flask app)
│   ├── body.jpg                 # Image
│   ├── hemoglobine_gender.png   # Image/plot
│   ├── logs.log                 # Log file
│   ├── outliers.png             # Image/plot
│   ├── random_forest_model_Default.pkl  # Duplicate model (consider removing)
│   ├── scaler.pkl               # Saved scaler object
│   └── total_data_c2.csv        # Duplicate dataset (consider removing)
├── terraform/                   # Terraform configuration
│   ├── main.tf                  # Main Terraform configuration
│   ├── outputs.tf               # Terraform outputs
│   ├── variables.tf             # Terraform variables
│   └── LICENSE.txt              # License file
├── .gitignore                   # Git ignore file
├── README.md                    # Project documentation
└── requirements.txt             # Python dependencies
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

