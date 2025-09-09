import argparse, pandas as pd, pathlib
from sklearn.model_selection import train_test_split
from collections import Counter

def can_stratify(labels):
    c = Counter(labels)
    return all(v >= 2 for v in c.values())

def main(out: str):
    raw_dir = pathlib.Path("data/raw")
    fake = pd.read_csv(raw_dir / "fake.csv"); fake["label"] = "fake"
    real = pd.read_csv(raw_dir / "true.csv"); real["label"] = "real"

    df = pd.concat([fake, real], ignore_index=True)
    df["title"] = df["title"].astype(str).fillna("")
    df["text"]  = df["text"].astype(str).fillna("")
    df["body"]  = (df["title"].str.strip() + " " + df["text"].str.strip()).str.strip()

    # Only dedup if we have a reasonable amount of data; otherwise keep all rows
    # to avoid collapsing tiny toy datasets back to 2 samples.
    if len(df) > 200:
        df = df.drop_duplicates(subset=["body", "label"]).reset_index(drop=True)

    strat1 = df["label"] if can_stratify(df["label"]) else None
    train, temp = train_test_split(df, test_size=0.30, random_state=42, stratify=strat1)

    strat2 = temp["label"] if can_stratify(temp["label"]) else None
    val, test = train_test_split(temp, test_size=0.50, random_state=42, stratify=strat2)

    out_dir = pathlib.Path(out); out_dir.mkdir(parents=True, exist_ok=True)
    train.to_parquet(out_dir / "train.parquet", index=False)
    val.to_parquet(out_dir / "val.parquet", index=False)
    test.to_parquet(out_dir / "test.parquet", index=False)

    print("Counts:")
    print("  train:", train["label"].value_counts().to_dict())
    print("  val  :",   val["label"].value_counts().to_dict())
    print("  test :",  test["label"].value_counts().to_dict())

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    args = p.parse_args()
    main(args.out)


