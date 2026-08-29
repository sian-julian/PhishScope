import pandas as pd
import random
import uuid
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
from backend.analyzer.feature_extractor import extract_features

def generate_safe_urls(count=150):
    bases = [
        "https://github.com/",
        "https://chatgpt.com/c/",
        "https://youtube.com/watch?v=",
        "https://notion.so/",
        "https://discord.com/channels/",
        "https://docs.google.com/document/d/",
        "https://drive.google.com/file/d/",
        "https://aws.amazon.com/console/home?region=us-east-1#",
        "https://zoom.us/j/",
        "https://teams.microsoft.com/l/meetup-join/"
    ]
    
    urls = []
    for _ in range(count):
        base = random.choice(bases)
        if "youtube.com" in base:
            suffix = str(uuid.uuid4())[:11]
        else:
            suffix = str(uuid.uuid4())
            if random.random() > 0.5:
                suffix += "/" + str(uuid.uuid4())
        
        urls.append(base + suffix)
    return urls

def append_to_split(split_file, count=150):
    file_path = os.path.join(PROJECT_ROOT, "datasets", "splits", split_file)
    try:
        df = pd.read_csv(file_path, low_memory=False)
    except FileNotFoundError:
        print(f"{file_path} not found.")
        return

    urls = generate_safe_urls(count)
    new_rows = []
    
    for url in urls:
        features = extract_features(url)
        if not features.get("valid"):
            continue
            
        row = {"url": url, "label": "0", "source": "augmented_v1"}
        for k in df.columns:
            if k in ["url", "label", "source"]:
                continue
            v = features.get(k, 0)
            if isinstance(v, bool):
                v = 1 if v else 0
            row[k] = v
        new_rows.append(row)
        
    new_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(file_path, index=False)
    print(f"Appended {len(new_rows)} rows to {split_file}")

if __name__ == "__main__":
    print("Augmenting train.csv...")
    append_to_split("train.csv", count=200)
    print("Augmenting test.csv...")
    append_to_split("test.csv", count=50)
    print("Done.")
