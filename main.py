from flask import Flask, request, flash, redirect, jsonify
import os
from Color import filtering
from Recommender import hybrid


UPLOAD_FOLDER = '/image'

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/", methods=['GET'])
def healthcheck():
    return("Hello World")

@app.route("/recommend", methods=['POST'])
def recommend_furniture():    
    file = request.files['image']
    height = request.form.get('height')
    length = request.form.get('length')
    breath = request.form.get('breath')
    category = request.form.get('category')
    
    if file:
        filename = "background.jpg"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    suggestions = filtering(category, int(length), int(breath), int(height), file_path)
    os.remove(file_path)
    return suggestions

@app.route("/hybrid", methods=["POST"])
def get_recommendations():
    furniture = request.form.get('furniture').split(" ")
    user_id = request.form.get('user_id')
    return hybrid(furniture, int(user_id))



