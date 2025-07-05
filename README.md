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
- [Images of the app on EC2 (http://3.66.168.76:8501/), S3 bucket, terraform apply output].

## Improvements
1. Needs to improve the security with https://
2. Needs to be able to connect RDS and with MySQL 

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

-------------------------------------------------------------------------------------


markdown
# Body Signals of Smoking Project

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

A machine learning application for detecting smoking signals deployed on AWS using Terraform infrastructure as code.

## Project Overview

**Goal**: Build and deploy a Streamlit application with machine learning models on AWS, managed with Terraform.

**Start Date**: July 5, 2025  
**Duration**: 14 days  
**Status**: In Progress 🚧

## Daily Progress Log

### Day 1 (Saturday, July 5, 2025)
✅ **Tasks Completed**:
- Set up Codespaces environment with custom `devcontainer.json`
- Configured `post-create.sh` to auto-install:
  - AWS CLI
  - Terraform 1.12.2
- Created IAM user `aws-examples` with AdministratorAccess policy
- Securely stored AWS credentials as GitHub Secrets
- Verified installations:

  ```bash
  aws --version
  terraform --version
  ```
📝 Notes:

Successful AWS identity verification:


### Upcoming Days

#### Day 2 (Monday, July 7, 2025)
🔜 **Planned Tasks**:
- Configure Terraform Cloud backend
- Link GitHub repository to Terraform Cloud
- Set up workspace variables
- Test remote state management

#### Day 3 (Tuesday, July 8, 2025)
🔜 **Planned Tasks**:
- Adapt Terraform templates from reference architecture
- Configure AWS provider settings
- Initialize VPC module
- Set up security groups

#### Day 4 (Wednesday, July 9, 2025)
🔜 **Planned Tasks**:
- Implement basic Streamlit application skeleton
- Add data ingestion functionality
- Configure basic visualization
- Set up project structure

#### Day 5 (Thursday, July 10, 2025)
🔜 **Planned Tasks**:
- Modularize application code
- Separate concerns:
- Data processing
- Model inference
- UI components
- Implement configuration management

#### Day 6 (Friday, July 11, 2025)
🔜 **Planned Tasks**:
- Implement comprehensive logging
- Add error handling middleware
- Set up monitoring alerts
- Configure application insights

#### Day 7 (Saturday, July 12, 2025)
🔜 **Planned Tasks**:
- Create EC2 deployment package
- Configure AMI with dependencies
- Prepare user data scripts
- Test local deployment

#### Day 8 (Monday, July 14, 2025)
🔜 **Planned Tasks**:
- Write unit tests for core functionality
- Implement test fixtures
- Configure pytest framework
- Set up code coverage tracking

#### Day 9 (Tuesday, July 15, 2025)
🔜 **Planned Tasks**:
- Perform integration tests
- Test AWS service integrations
- Validate end-to-end workflow
- Stress test application

#### Day 10 (Wednesday, July 16, 2025)
🔜 **Planned Tasks**:
- Deploy core infrastructure:
- EC2 instances
- S3 buckets
- IAM roles
- Configure auto-scaling
- Set up load balancing

#### Day 11 (Thursday, July 17, 2025)
🔜 **Planned Tasks**:
- Verify EC2 deployment
- Test application accessibility
- Monitor resource utilization
- Optimize instance sizing

#### Day 12 (Friday, July 18, 2025)
🔜 **Planned Tasks**:
- Adapt application for serverless
- Package for Lambda deployment
- Configure layer dependencies
- Test cold start performance

#### Day 13 (Saturday, July 19, 2025)
🔜 **Planned Tasks**:
- Deploy Lambda functions
- Configure API Gateway
- Set up route mappings
- Implement authorization

#### Day 14 (Sunday, July 20, 2025)
🔜 **Planned Tasks**:
- Conduct final API testing
- Document all endpoints
- Prepare user guide
- Complete project documentation

## Project Roadmap

```mermaid
gantt
    title Project Development Timeline
    dateFormat  YYYY-MM-DD
    axisFormat %b %d
    
    section Infrastructure
    Environment Setup        :done, env1, 2025-07-05, 1d
    Terraform Configuration :active, env2, 2025-07-07, 2d
    Cloud Deployment        : crit, env3, 2025-07-16, 3d
    
    section Application
    Core Development       : dev1, 2025-07-09, 5d
    Testing Phase          : dev2, after dev1, 3d
    
    section Finalization
    Documentation         : doc1, 2025-07-19, 2d
    API Integration       : doc2, after doc1, 1d

```

### Project Setup
- Prerequisites
- GitHub account with Codespaces access
- AWS account with IAM permissions
- Terraform Cloud account (optional)

Installation
Clone the repository:

```bash
git clone <repository-url>
Open in GitHub Codespaces or configure local environment using the provided devcontainer.json
```

### Configure AWS credentials:

Set as GitHub Secrets:

- AWS_ACCESS_KEY_ID

- AWS_SECRET_ACCESS_KEY

Or configure locally:

```bash
aws configure
Initialize Terraform:
```

```bash
cd terraform/
terraform init
terraform plan
```

Future Updates
This README will be updated daily with progress. Check back for the latest developments!

Last Updated: July 5, 2025

text

This version includes:
1. Professional badges for technologies used
2. Clear project status indication
3. Well-organized progress log with emoji visuals
4. Responsive table for upcoming tasks
5. Clean setup instructions
6. Consistent formatting and spacing
7. Last updated timestamp
8. Clear section headings

