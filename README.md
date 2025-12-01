# Student Placement Prediction System

A professional, end-to-end machine learning web application designed to predict the likelihood of student placement based on resume content. This tool is particularly useful for academic institutions and students aiming to assess employability and receive actionable feedback for improvement.

## Overview

This project allows users to upload resumes in PDF format, extract key information using NLP techniques, and predict placement chances using a trained ML model. Based on the extracted features, it also provides personalized recommendations to improve a candidate's job prospects.

## Key Features

* PDF Resume Parsing using `PyMuPDF`
* Feature Extraction and formatting
* Placement Prediction using a trained `RandomForestClassifier`
* Recommendation Engine to suggest improvements
* Web Interface powered by `Flask`

## Project Structure

```
├── app.py                      # Flask backend logic
├── parse_resume.py             # Resume parsing and ML processing
├── placementdata.csv           # Training dataset for the ML model
├── templates/
│   ├── index.html              # Upload and input page
│   └── result.html             # Results and recommendations display
├── static/
│   └── style.css               # Optional frontend styles
├── uploads/                    # Temporary storage for uploaded resumes
├── README.md                   # Project documentation
```

## Setup Instructions

### Prerequisites

* Python 3.7 or higher

### Install Dependencies

It’s recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

Install required Python packages:

```bash
pip install Flask Werkzeug PyMuPDF pandas numpy scikit-learn
```

### Run the Application

```bash
python app.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000) to access the app.

## ML Model Details

* Model Used: `RandomForestClassifier`
* Dataset: `placementdata.csv`
* Features: CGPA, skills, projects, internships, certifications
* Preprocessing: Label encoding, imputation, scaling
* Target Variable: Placement Status (Placed / Not Placed)

## Recommendations Module

Based on deficiencies found in resumes, the system provides improvement suggestions such as:

* Increase CGPA or GPA consistency
* Complete more internships or hands-on projects
* Gain relevant certifications or training
* Boost extracurricular participation or leadership

## Future Enhancements

* Support for `.docx` resume format
* Better resume section classification (education, experience, skills)
* Enhanced frontend experience with animations and feedback
* PDF report generation for placement readiness score

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Licensed under the [MIT License](LICENSE).

## Author

**Bharath Harihara Sudhan**. 
GitHub: [@Bharath-Bobby](https://github.com/Bharath-Bobby)
