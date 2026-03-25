import json
from transformers import pipeline

# ------------------ KEYWORD FILTER ------------------
bad_words = ["hack", "bomb", "attack", "bypass"]

def keyword_filter(text):
    for word in bad_words:
        if word in text.lower():
            return "unsafe"
    return "safe"


# ------------------ MODEL ------------------
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

THRESHOLD = 0.6

def classify_prompt(text):
    result = classifier(text)[0]
    
    label = result['label']
    score = result['score']
    
    if label == "NEGATIVE" and score > THRESHOLD:
        verdict = "unsafe"
    else:
        verdict = "safe"
    
    return verdict, score


# ------------------ LOAD DATA ------------------
with open("dataset.json", "r") as f:
    data = json.load(f)

correct = 0
total = len(data)

results = []

# ------------------ EVALUATION LOOP ------------------
for item in data:
    text = item["text"]
    true_label = item["label"]

    predicted, score = classify_prompt(text)
    keyword_pred = keyword_filter(text)

    # map labels
    actual = "safe" if true_label == "safe" else "unsafe"

    if predicted == actual:
        correct += 1

    results.append({
        "text": text,
        "actual": actual,
        "model_pred": predicted,
        "keyword_pred": keyword_pred,
        "confidence": score
    })


# ------------------ METRICS ------------------
accuracy = correct / total

print("\n===== RESULTS =====")
print("Total:", total)
print("Correct:", correct)
print("Accuracy:", accuracy)


# ------------------ FAILURES ------------------
print("\n===== MODEL FAILURES =====")
for r in results:
    if r["actual"] != r["model_pred"]:
        print(r)


# ------------------ COMPARISON ------------------
print("\n===== MODEL vs KEYWORD DIFFERENCES =====")
for r in results:
    if r["model_pred"] != r["keyword_pred"]:
        print(r)