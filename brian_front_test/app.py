import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import mysql.connector
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load your trained model
model = load_model('bt_model.h5')

# Create uploads directory if not exists
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# MySQL database config using environment variables
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "tumor_detection_db")
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.method == 'POST':
            # Debug: Log form data
            print("Form data received:", request.form)

            name = request.form.get('name')
            gender = request.form.get('gender')
            phone = request.form.get('phone')
            img_file = request.files.get('image')

            # Debug: Log uploaded file info
            print("Uploaded file:", img_file)

            if not img_file:
                return {"error": "No image uploaded"}, 400

            # Save the uploaded file
            filename = secure_filename(img_file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            img_file.save(file_path)

            # Debug: Log file path
            print("File saved at:", file_path)

            # Preprocess image
            img = image.load_img(file_path, target_size=(240, 240   ))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0

            # Debug: Log preprocessed image shape
            print("Image array shape:", img_array.shape)

            # Prediction
            prediction = model.predict(img_array)
            print("Raw prediction output:", prediction)

            result = "Tumor Detected" if prediction[0][0] > 0.5 else "No Tumor"

            # Debug: Log prediction result
            print("Prediction result:", result)

            # Save to MySQL
            insert_query = """
                INSERT INTO patients (name, gender, phone, image_path, prediction)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (name, gender, phone, file_path, result)
            cursor.execute(insert_query, values)
            db.commit()

            # Debug: Log successful database insertion
            print("Data inserted into database successfully.")

            return {"result": result}
    except Exception as e:
        # Debug: Log the error
        print("Error occurred:", e)
        return {"error": str(e)}, 500

@app.route('/patients', methods=['GET'])
def patients():
    try:
        # Fetch all patient records from the database
        query = "SELECT id, name, gender, phone, image_path, prediction, timestamp FROM patients"
        cursor.execute(query)
        patients = cursor.fetchall()

        # Debug: Log fetched patient data
        print("Fetched patients:", patients)

        # Pass the patient data to the template
        return render_template('patients.html', patients=patients)
    except Exception as e:
        # Debug: Log the error
        print("Error occurred:", e)
        return {"error": str(e)}, 500

@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    try:
        # Delete the patient record from the database
        delete_query = "DELETE FROM patients WHERE id = %s"
        cursor.execute(delete_query, (patient_id,))
        db.commit()

        # Debug: Log successful deletion
        print(f"Patient with ID {patient_id} deleted successfully.")

        return {"success": True}, 200
    except Exception as e:
        # Debug: Log the error
        print("Error occurred while deleting patient:", e)
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
