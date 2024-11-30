from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import cv2
from dotenv import load_dotenv
import numpy as np
from tensorflow.keras.models import load_model
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable CORS
UPLOAD_FOLDER = '/Users/kunalsangwan/Violence_detection/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the trained model
model = load_model("/Users/kunalsangwan/Downloads/modelnew.h5")

# Email configuration


def send_email_notification(frame_path):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

    subject = "Violence Detected Alert!"
    body = "Alert: Violence has been detected in the uploaded video."

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the violence frame
    with open(frame_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        f'attachment; filename={os.path.basename(frame_path)}')
        msg.attach(part)

    # Connect to the SMTP server and send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

# Process video


def detect_violence(video_path):
    cap = cv2.VideoCapture(video_path)
    violence_detected = False
    frame_path = ""

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocess the frame for the model
        resized_frame = cv2.resize(frame, (128, 128))
        normalized_frame = resized_frame / 255.0
        input_frame = np.expand_dims(normalized_frame, axis=0)

        # Predict violence
        prediction = model.predict(input_frame)
        if prediction[0][0] > 0.5:  # Threshold of 0.5 for violence
            print("Violence detected!")
            frame_path = os.path.join(UPLOAD_FOLDER, "violence_frame.jpg")
            cv2.imwrite(frame_path, frame)
            violence_detected = True
            send_email_notification(frame_path)
            break

    cap.release()
    return violence_detected, "violence_frame.jpg"


@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        violence_detected, frame_path = detect_violence(file_path)
        response = {
            "violence_detected": violence_detected,
            "frame_path": frame_path if violence_detected else None
        }
        return jsonify(response), 200  # Explicitly return a 200 status
    except Exception as e:
        print(f"Error processing video: {e}")
        return jsonify({"error": str(e)}), 500

# Serve uploaded files


@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
