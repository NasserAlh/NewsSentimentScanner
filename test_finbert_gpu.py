import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time
import numpy as np

print("="*60)
print("FinBERT GPU Test")
print("="*60)

# GPU setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"\n🚀 Device: {device}")

if torch.cuda.is_available():
    print(f"   GPU: {torch.cuda.get_device_name(0)}")
    print(f"   Initial VRAM: {torch.cuda.memory_allocated() / 1e9:.2f} GB")

# Load model
print("\n📦 Loading FinBERT model...")
finbert_model = AutoModelForSequenceClassification.from_pretrained(
    "yiyanghkust/finbert-tone"
).to(device)
finbert_tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
labels = ['Positive', 'Negative', 'Neutral']

if torch.cuda.is_available():
    print(f"   After loading: {torch.cuda.memory_allocated() / 1e9:.2f} GB")

# Test sentences
test_sentences = [
    "Gold prices surge to record highs on strong demand",
    "ES futures tumble on recession fears and weak data",
    "Market remains neutral amid mixed economic signals",
    "Bitcoin rallies as institutional adoption accelerates",
    "Crude oil falls on oversupply concerns",
] * 10  # 50 sentences total

print(f"\n🧪 Testing with {len(test_sentences)} sentences...")
print("   (Watch nvidia-smi in another window - GPU should spike!)\n")

# Warm up GPU
inputs = finbert_tokenizer("warmup", return_tensors="pt", truncation=True, max_length=512).to(device)
with torch.no_grad():
    _ = finbert_model(**inputs)

# Benchmark
start_time = time.time()

for i, text in enumerate(test_sentences):
    inputs = finbert_tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(device)

    with torch.no_grad():
        outputs = finbert_model(**inputs)

    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]
    max_index = np.argmax(probabilities)
    sentiment = labels[max_index]
    confidence = probabilities[max_index]

    if i < 5:  # Print first 5
        print(f"   [{i+1}] {sentiment} ({confidence:.2f}): {text[:50]}...")

elapsed = time.time() - start_time

print(f"\n⏱️  Performance:")
print(f"   Total time: {elapsed:.2f} seconds")
print(f"   Per sentence: {(elapsed/len(test_sentences))*1000:.1f} ms")
print(f"   Throughput: {len(test_sentences)/elapsed:.1f} sentences/sec")

if torch.cuda.is_available():
    print(f"\n💾 Peak VRAM: {torch.cuda.max_memory_allocated() / 1e9:.2f} GB")
    print(f"   Current VRAM: {torch.cuda.memory_allocated() / 1e9:.2f} GB")

print("\n" + "="*60)
print("✅ Test complete! Check nvidia-smi - GPU usage should have spiked.")
print("="*60)
