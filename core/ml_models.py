import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from .models import PlacementRecord
import joblib
from pathlib import Path
from django.conf import settings
MODEL_PATH = Path(settings.BASE_DIR) / "ml_models" / "placement_model.joblib"
def train_placement_model():
    records = PlacementRecord.objects.all().values(
        "cgpa",
        "skill_count",
        "project_count",
        "application_count",
        "placement_status",
    )

    df = pd.DataFrame(list(records))

    X = df[
        [
            "cgpa",
            "skill_count",
            "project_count",
            "application_count",
        ]
    ]

    y = df["placement_status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy
def train_and_save_model():
    model, accuracy = train_placement_model()

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "accuracy": accuracy,
        },
        MODEL_PATH,
    )

    return model, accuracy
def load_placement_model():
    if not MODEL_PATH.exists():
        return train_and_save_model()

    data = joblib.load(MODEL_PATH)

    return data["model"], data["accuracy"]
def predict_placement(student):
    model, accuracy = load_placement_model()

    features = pd.DataFrame([{
        "cgpa": student.cgpa,
        "skill_count": student.skills.count(),
        "project_count": student.projects.count(),
        "application_count": student.application_set.count(),
    }])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0].max()

    return {
        "placement_prediction": bool(prediction),
        "confidence": round(float(probability) * 100, 2),
        "model_accuracy": round(float(accuracy) * 100, 2),
    }