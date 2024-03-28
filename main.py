from flask import Flask, request, flash, redirect, jsonify
import os
from Color import filtering

UPLOAD_FOLDER = '/image'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/recommend", methods=['POST'])
def recommend_furniture():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    height = request.form.get('height')
    length = request.form.get('length')
    breath = request.form.get('breath')
    category = request.form.get('category')

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        filename = "background"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    suggestions = filtering(category, length, breath, height, file_path)
    os.remove(file_path)
    return suggestions

