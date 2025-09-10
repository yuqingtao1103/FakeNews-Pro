import argparse, joblib, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, f1_score
from src.features.tfidf import build_vectorizer

def load_xy(path):
    df = pd.read_parquet(path)
    return df["body"].tolist(), df["label"].tolist()

def main(train, val, out):
    Xtr, ytr = load_xy(train)
    Xva, yva = load_xy(val)
    pipe = Pipeline([("tfidf", build_vectorizer()), ("clf", LogisticRegression(max_iter=200, C=3.0, solver="liblinear"))])
    pipe.fit(Xtr, ytr)
    ypred = pipe.predict(Xva)
    f1 = f1_score(yva, ypred, average="weighted")
    print(classification_report(yva, ypred))
    joblib.dump(pipe, out)
    print(f"Saved model → {out}. Val weighted F1: {f1:.3f}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--train", required=True)
    p.add_argument("--val", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    main(args.train, args.val, args.out)
