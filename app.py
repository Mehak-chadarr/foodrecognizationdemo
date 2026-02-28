from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import os
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

model = YOLO("yolov8n.pt")  # replace with trained food model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    results = model(filepath)

    detected_items = []
    for r in results:
        for box in r.boxes:
            detected_items.append(model.names[int(box.cls)])

    return jsonify({"items": detected_items})

if __name__ == '__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)