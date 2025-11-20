# classifier/predict.py
from joblib import load
MODEL_PATH = "classifier/model.joblib"

def load_model():
    try:
        model = load(MODEL_PATH)
        return model
    except Exception as e:
        raise RuntimeError("Model not trained. Run classifier/train_model.py first.") from e

def is_relevant(text: str, threshold_label="relevant"):
    model = load_model()
    pred = model.predict([text])[0]
    # model predict returns label: "relevant" or "not_relevant"
    return pred == threshold_label
