from flask import Flask, request, render_template
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/team-writing-assistant/t5-base-c4jfleg"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    input_text = str(request.form['Input_text'])
    output = query({"inputs": "grammar: "+input_text, "wait_for_model":True})
    return render_template('index.html', prediction_text='{}'.format("Correct Setence: "+output[0]['generated_text']))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
