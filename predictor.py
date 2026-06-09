TRAINING_DATA = [
    {"glucose": 85, "haemoglobin": 13.5, "cholesterol": 170, "label": "Normal range"},
    {"glucose": 92, "haemoglobin": 14.2, "cholesterol": 185, "label": "Normal range"},
    {"glucose": 110, "haemoglobin": 13.1, "cholesterol": 190, "label": "Prediabetes risk"},
    {"glucose": 121, "haemoglobin": 12.8, "cholesterol": 205, "label": "Prediabetes risk"},
    {"glucose": 140, "haemoglobin": 13.7, "cholesterol": 210, "label": "Diabetes risk"},
    {"glucose": 165, "haemoglobin": 14.5, "cholesterol": 220, "label": "Diabetes risk"},
    {"glucose": 88, "haemoglobin": 10.5, "cholesterol": 175, "label": "Anaemia risk"},
    {"glucose": 95, "haemoglobin": 11.2, "cholesterol": 190, "label": "Anaemia risk"},
    {"glucose": 96, "haemoglobin": 13.8, "cholesterol": 235, "label": "Cholesterol risk"},
    {"glucose": 104, "haemoglobin": 14.0, "cholesterol": 260, "label": "Cholesterol risk"},
    {"glucose": 142, "haemoglobin": 10.8, "cholesterol": 245, "label": "Multiple risk indicators"},
    {"glucose": 155, "haemoglobin": 11.0, "cholesterol": 270, "label": "Multiple risk indicators"},
]


def normalise(value, minimum, maximum):
    return (value - minimum) / (maximum - minimum)


def calculate_distance(patient, sample):
    glucose_distance = normalise(patient["glucose"], 70, 180) - normalise(
        sample["glucose"], 70, 180
    )
    haemoglobin_distance = normalise(
        patient["haemoglobin"], 8, 18
    ) - normalise(sample["haemoglobin"], 8, 18)
    cholesterol_distance = normalise(patient["cholesterol"], 120, 300) - normalise(
        sample["cholesterol"], 120, 300
    )

    return (
        glucose_distance**2
        + haemoglobin_distance**2
        + cholesterol_distance**2
    ) ** 0.5


def predict_health_condition(glucose, haemoglobin, cholesterol):
    patient = {
        "glucose": glucose,
        "haemoglobin": haemoglobin,
        "cholesterol": cholesterol,
    }

    closest_sample = min(
        TRAINING_DATA,
        key=lambda sample: calculate_distance(patient, sample),
    )

    return closest_sample["label"]


def generate_health_remark(glucose, haemoglobin, cholesterol):
    prediction = predict_health_condition(glucose, haemoglobin, cholesterol)

    advice = {
        "Normal range": "Values look normal based on the custom ML model.",
        "Prediabetes risk": "Possible prediabetes risk. Please monitor glucose levels.",
        "Diabetes risk": "Possible diabetes risk. Please consult a doctor.",
        "Anaemia risk": "Possible anaemia risk. Please check haemoglobin levels with a doctor.",
        "Cholesterol risk": "Possible cholesterol risk. Please review diet and consult a doctor.",
        "Multiple risk indicators": "Multiple possible health risks detected. Please consult a doctor.",
    }

    return f"ML Prediction: {prediction}. {advice[prediction]}"
