from transformers import pipeline

classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

THRESHOLD = 0.6  # you can change this later

def classify_prompt(text):
    result = classifier(text)[0]
    
    label = result['label']
    score = result['score']
    
    if label == "NEGATIVE" and score > THRESHOLD:
        verdict = "UNSAFE"
    else:
        verdict = "SAFE"
    
    return {
        "text": text,
        "verdict": verdict,
        "confidence": score
    }

# test
while True:
    prompt = input("\nEnter prompt: ")
    output = classify_prompt(prompt)
    print(output)