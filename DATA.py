from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
import os

app = Flask(__name__)
CORS(app)

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

def analyze_blood_pressure(bp, age):
    if 90 <= bp <= 120:
        return {
            "message": "Your blood pressure looks great! Keep up the good work!",
            "lifestyle": [],
            "medications": []
        }
    elif bp > 120:
        return {
            "message": "Hmm, your blood pressure is a bit high. Consider relaxing and consulting a doctor if needed.",
            "lifestyle": [
                "Reduce salt intake.",
                "Exercise regularly (e.g., walking, jogging).",
                "Maintain a healthy weight.",
                "Avoid smoking and limit alcohol consumption.",
                "Manage stress through meditation or yoga."
            ],
            "medications": ["ACE inhibitors", "Beta blockers", "Calcium channel blockers"]
        }
    else:
        return {
            "message": "Oh no, your blood pressure is a bit low. Make sure to stay hydrated and eat well.",
            "lifestyle": [
                "Increase fluid intake.",
                "Eat small, frequent meals.",
                "Avoid standing for long periods.",
                "Wear compression stockings if needed."
            ],
            "medications": ["Fludrocortisone", "Midodrine"]
        }

def analyze_blood_sugar(sugar, age):
    if 70 <= sugar <= 140:
        return {
            "message": "Your blood sugar level is perfectly normal. Great job!",
            "lifestyle": [],
            "medications": []
        }
    elif sugar > 140:
        return {
            "message": "Oops, your blood sugar is on the higher side. Watch your diet and consult a doctor if necessary.",
            "lifestyle": [
                "Follow a low-carb, balanced diet.",
                "Exercise regularly to improve insulin sensitivity.",
                "Monitor blood sugar levels frequently.",
                "Avoid sugary drinks and processed foods."
            ],
            "medications": ["Metformin", "Sulfonylureas", "Insulin"]
        }
    else:
        return {
            "message": "Your blood sugar is a bit low. Have a snack and take care of yourself!",
            "lifestyle": [
                "Carry quick sugar sources like glucose tablets or candy.",
                "Eat regular meals and snacks.",
                "Avoid skipping meals."
            ],
            "medications": ["Glucose tablets", "Glucagon (for emergencies)"]
        }

def analyze_body_temperature(temp, age):
    if 97.0 <= temp <= 99.0:
        return {
            "message": "Your body temperature is normal. You're doing fine!",
            "lifestyle": [],
            "medications": []
        }
    elif temp > 99.0:
        return {
            "message": "It seems like you have a fever. Rest up and stay hydrated!",
            "lifestyle": [
                "Drink plenty of fluids.",
                "Rest and avoid strenuous activities.",
                "Use a cool compress to reduce fever."
            ],
            "medications": ["Paracetamol", "Ibuprofen"],
            "types": [
                {
                    "type": "Viral Fever",
                    "description": "Caused by viral infections.",
                    "common_symptoms": ["Fatigue", "Body aches", "Runny nose", "Sore throat"]
                },
                {
                    "type": "Bacterial Fever",
                    "description": "Caused by bacterial infections.",
                    "common_symptoms": ["High fever", "Chills", "Sweating", "Localized pain"]
                },
                {
                    "type": "Malaria",
                    "description": "Caused by mosquito-borne parasites.",
                    "common_symptoms": ["High fever", "Chills", "Sweating", "Headache"]
                },
                {
                    "type": "Typhoid",
                    "description": "Caused by Salmonella bacteria.",
                    "common_symptoms": ["Prolonged fever", "Abdominal pain", "Weakness", "Loss of appetite"]
                },
                {
                    "type": "Dengue",
                    "description": "Caused by dengue virus transmitted by mosquitoes.",
                    "common_symptoms": ["High fever", "Severe headache", "Pain behind the eyes", "Skin rash"]
                }
            ]
        }
    else:
        return {
            "message": "Your body temperature is low. Keep warm and take care of yourself.",
            "lifestyle": [
                "Wear warm clothing.",
                "Use blankets and heating pads.",
                "Drink warm beverages."
            ],
            "medications": ["Warm fluids", "Vitamin C supplements"]
        }

def analyze_symptom(symptom):
    symptom_medications = {
        "fever": {
            "medications": ["Paracetamol", "Ibuprofen"],
            "types": [
                "Viral Fever: Caused by viral infections.",
                "Bacterial Fever: Caused by bacterial infections.",
                "Malaria: Caused by mosquito-borne parasites.",
                "Typhoid: Caused by Salmonella bacteria.",
                "Dengue: Caused by dengue virus transmitted by mosquitoes."
            ]
        },
        "cold": {
            "medications": ["Antihistamines", "Decongestants"]
        },
        "headache": {
            "medications": ["Aspirin", "Ibuprofen"]
        },
        "cough": {
            "medications": ["Cough syrups", "Lozenges"]
        },
        "stomach pain": {
            "medications": ["Antacids", "Proton pump inhibitors"]
        },
        "body pain": {
            "medications": ["Pain relievers", "Muscle relaxants"]
        },
        "other": {
            "medications": ["Consult a doctor for specific medications"]
        }
    }
    return symptom_medications.get(symptom.lower(), {"medications": ["Consult a doctor for specific medications"]})

@app.route('/')
def home():
    app.logger.debug("Home route accessed")
    return jsonify({"message": "Backend is running!"})

@app.route('/analyze', methods=['POST'])
def analyze_health():
    try:
        data = request.get_json()
        app.logger.debug(f"Received data: {data}")

        bp = int(data.get("bp", 0))
        sugar = int(data.get("sugar", 0))
        temp = float(data.get("temp", 0.0))
        age = int(data.get("age", 0))
        symptom = data.get("symptom", "")

        symptom_analysis = analyze_symptom(symptom)
        body_temp_analysis = analyze_body_temperature(temp, age)
        response = {
            "Blood Pressure": analyze_blood_pressure(bp, age),
            "Blood Sugar": analyze_blood_sugar(sugar, age),
            "Body Temperature": body_temp_analysis,
            "Symptom Analysis": symptom_analysis
        }
        app.logger.debug(f"Response: {response}")
        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable or default to 5000
    app.run(debug=True, host='0.0.0.0', port=port)  # Bind to 0.0.0.0 to make it accessible externally