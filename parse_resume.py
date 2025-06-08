import fitz  # PyMuPDF
import re
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Load and preprocess the dataset
df = pd.read_csv("placementdata.csv")
df = df.drop(columns="StudentID", errors="ignore")

imputer = SimpleImputer(strategy="most_frequent")
df[df.columns] = imputer.fit_transform(df)

label_encoders = {}
for column in df.select_dtypes(include=['object']).columns:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

target_encoder = LabelEncoder()
df['PlacementStatus'] = target_encoder.fit_transform(df['PlacementStatus'])

X = df.drop(columns=['PlacementStatus'])
y = df['PlacementStatus']
X_columns = X.columns

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ------------------------
# PDF and Resume Parsing
# ------------------------

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def parse_resume(text):
    result = {
        "CGPA": 0.0,
        "Internships": 0,
        "Projects": 0,
        "Workshops/Certifications": 0,
        "AptitudeTestScore": 70,
        "SoftSkillsRating": 5,
        "ExtracurricularActivities": 0,
        "PlacementTraining": 1,
        "SSC_Marks": 0,
        "HSC_Marks": 0
    }

    cgpa_match = re.search(r'CGPA[:\s]*([0-9.]+)', text, re.I)
    if cgpa_match:
        result['CGPA'] = float(cgpa_match.group(1))

    marks_matches = re.findall(r'(?:Class\s*1[02]|S\.?S\.?C\.?|H\.?S\.?C\.?)[^\d]*(\d{2,3})[%]?', text, re.I)
    if len(marks_matches) >= 2:
        result['HSC_Marks'] = int(marks_matches[0])
        result['SSC_Marks'] = int(marks_matches[1])

    result["Internships"] = text.lower().count("internship")
    result["Projects"] = text.lower().count("project")
    result["Workshops/Certifications"] = text.lower().count("certificate") + \
        sum(k in text.lower() for k in ["competition", "symposium", "hackathon", "award"])

    result["ExtracurricularActivities"] = 1 if any(k in text.lower() for k in [
        "volunteer", "sports", "club", "football", "public relations", "nso"
    ]) else 0

    if "no placement training" in text.lower():
        result["PlacementTraining"] = 0

    return result

# ------------------------
# Prediction
# ------------------------

def predict_placement(input_data):
    input_df = pd.DataFrame([input_data], columns=X_columns)
    input_df.fillna(dict(zip(X_columns, imputer.statistics_)), inplace=True)

    for column in input_df.select_dtypes(include=['object']).columns:
        if column in label_encoders:
            if input_df[column].iloc[0] in label_encoders[column].classes_:
                input_df[column] = label_encoders[column].transform(input_df[column])
            else:
                input_df[column] = -1

    input_df = input_df[X_columns]
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)

    return "Placed" if prediction[0] == 1 else "Not Placed"

# ------------------------
# Recommendation Generator
# ------------------------

def generate_recommendations(data, prediction):
    tips = []

    if data["CGPA"] < 7.0:
        tips.append("Improve your CGPA to at least 7.0 to enhance academic standing.")
    if data["Internships"] < 1:
        tips.append("Gain real-world experience by pursuing internships.")
    if data["Projects"] < 2:
        tips.append("Work on more hands-on projects to showcase technical skills.")
    if data["Workshops/Certifications"] < 2:
        tips.append("Attend workshops or earn certifications to boost your resume.")
    if data["AptitudeTestScore"] < 75:
        tips.append("Practice aptitude tests to improve logical and quantitative skills.")
    if data["SoftSkillsRating"] < 7:
        tips.append("Consider improving your soft skills through communication workshops.")
    if data["ExtracurricularActivities"] == 0:
        tips.append("Join extracurricular activities to show a well-rounded profile.")
    if data["PlacementTraining"] == 0:
        tips.append("Participate in placement training to prepare for interviews.")
    if data["SSC_Marks"] < 60:
        tips.append("Highlight improvements made since school to address low SSC marks.")
    if data["HSC_Marks"] < 60:
        tips.append("Emphasize higher education performance to compensate for HSC scores.")

    if prediction == "Placed":
        tips.append("Great work! Keep building your portfolio with internships or research.")
    else:
        tips.append("Don't be discouraged. Focus on upskilling and consistent effort.")

    return tips