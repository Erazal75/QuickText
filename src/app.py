from flask import Flask, request, jsonify
import pickle
import numpy as np

# Charger le modèle entraîné (par exemple, un modèle sauvegardé avec joblib)
filename = '/Users/lazaregrail/Documents/QuickText/venv/Jupiter NoteBook/Gaussian Process_model.sav'
model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({"species": prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
