import joblib
from typing import List

class BaselineModel:
    def __init__(self, model_path: str):
        self.pipe = joblib.load(model_path)
        self.vectorizer = self.pipe.named_steps["tfidf"]
        self.clf = self.pipe.named_steps["clf"]
        self.feature_names = self.vectorizer.get_feature_names_out()

    def predict(self, text: str):
        if hasattr(self.pipe, "predict_proba"):
            proba = self.pipe.predict_proba([text])[0]
            conf = float(max(proba))
        else:
            conf = 1.0
        label = self.pipe.predict([text])[0]
        return label, conf

    def top_features(self, text: str, k: int = 10) -> List[str]:
        vec = self.vectorizer.transform([text])
        # Align positive weights with 'real' for readability
        weights = self.clf.coef_[0] if self.clf.classes_[1] == "real" else -self.clf.coef_[0]
        scores = vec.multiply(weights).toarray()[0]
        idx = scores.argsort()[::-1][:k]
        feats = [self.feature_names[i] for i in idx if scores[i] > 0]
        return feats[:k]
