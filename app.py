from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from parse_resume import extract_text_from_pdf, parse_resume, predict_placement, generate_recommendations

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return 'No file part in the request.'

    file = request.files['resume']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        resume_text = extract_text_from_pdf(filepath)
        input_data = parse_resume(resume_text)
        prediction = predict_placement(input_data)
        recommendations = generate_recommendations(input_data, prediction)

        return render_template('result.html', prediction=prediction, recommendations=recommendations)
    else:
        return 'Invalid file type. Please upload a PDF.'

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    app.run(debug=True)
