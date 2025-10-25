# News Sentiment Scanner - User Manual

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Understanding the Application](#understanding-the-application)
5. [Configuration & Usage](#configuration--usage)
6. [Switching Between Sentiment Engines](#switching-between-sentiment-engines)
7. [GPU Acceleration Setup](#gpu-acceleration-setup)
8. [Multi-Market Analysis](#multi-market-analysis)
9. [Interpreting Results](#interpreting-results)
10. [Advanced Usage](#advanced-usage)
11. [Troubleshooting](#troubleshooting)
12. [Best Practices](#best-practices)

---

## Overview

### What This Application Does

The News Sentiment Scanner is a Python-based tool designed to help traders, investors, and market analysts gauge market sentiment by analyzing news headlines and articles. It:

- **Fetches** news articles from Google News RSS feeds based on your search queries
- **Analyzes** sentiment using advanced NLP (Natural Language Processing) techniques
- **Aggregates** results to show overall market sentiment (Positive/Negative/Neutral)
- **Supports** any market: stocks, futures, commodities, forex, crypto

### Use Cases

1. **Pre-Market Analysis**: Check sentiment before trading day starts
2. **Event-Driven Trading**: Monitor sentiment around earnings, Fed announcements, etc.
3. **Multi-Market Comparison**: Compare sentiment across gold, ES futures, oil, etc.
4. **Research & Backtesting**: Analyze historical sentiment trends
5. **Risk Management**: Identify negative sentiment shifts early

### Key Features

- Two sentiment analysis engines: VADER (fast) and FinBERT (accurate)
- GPU acceleration support for FinBERT (RTX 4090, 3090, etc.)
- Customizable search queries for any market
- Batch processing of multiple queries
- Real-time sentiment aggregation

---

## System Requirements

### Minimum Requirements

- **OS**: Windows 10/11, Linux, or macOS
- **Python**: 3.8 or higher
- **RAM**: 4GB (8GB recommended for FinBERT)
- **Storage**: 2GB free space
- **Internet**: Required for fetching news articles

### Recommended for FinBERT

- **GPU**: NVIDIA RTX 3060 or better (RTX 4090 ideal)
- **VRAM**: 6GB minimum, 24GB for advanced usage
- **RAM**: 16GB
- **CUDA**: 11.8 or 12.x

### Recommended for VADER Only

- **CPU**: Any modern processor
- **RAM**: 4GB
- **No GPU required**

---

## Installation Guide

### Step 1: Install UV Package Manager

UV is the recommended package manager for this project.

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Clone or Download the Project

```bash
cd C:\Users\YourName\Dev
git clone <repository-url> NewsSentimentScanner
cd NewsSentimentScanner
```

Or download and extract the ZIP file.

### Step 3: Create Virtual Environment

```bash
uv venv
```

### Step 4: Activate Virtual Environment

**Windows:**
```powershell
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 5: Install Dependencies

```bash
uv pip install -r requirements.txt
```

**Dependencies installed:**
- `feedparser` - RSS feed parsing
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `vaderSentiment` - VADER sentiment analyzer
- `transformers` - Hugging Face transformers for FinBERT
- `torch` - PyTorch for deep learning
- `numpy` - Numerical operations

### Step 6: Verify Installation

```bash
uv run python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"
```

**Expected output:**
```
PyTorch: 2.7.0
CUDA Available: True  # If you have GPU
```

### Step 7: GPU Setup (Optional but Recommended)

If you have an NVIDIA GPU:

**Check CUDA version:**
```bash
nvidia-smi
```

**Install PyTorch with CUDA support:**
```bash
# For CUDA 12.1
uv pip install torch --index-url https://download.pytorch.org/whl/cu121

# For CUDA 11.8
uv pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---

## Understanding the Application

### Application Architecture

The application follows a 4-stage pipeline:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│ 1. Fetch    │────▶│ 2. Extract   │────▶│ 3. Analyze  │────▶│ 4. Aggregate │
│    News     │     │    Content   │     │  Sentiment  │     │   Results    │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
```

#### Stage 1: News Fetching
- Constructs Google News RSS URL from your query
- Fetches article metadata (title, link, published date)
- Retrieves multiple articles per query

#### Stage 2: Content Extraction
- Visits each article URL
- Extracts text from HTML using BeautifulSoup
- Handles timeouts and errors gracefully

#### Stage 3: Sentiment Analysis
- Analyzes text using VADER or FinBERT
- Returns polarity score (-1 to +1) and sentiment label
- Currently analyzes **titles only** for speed and accuracy

#### Stage 4: Aggregation
- Counts Positive/Negative/Neutral articles
- Calculates percentages
- Displays summary

### VADER vs FinBERT

| Feature | VADER | FinBERT |
|---------|-------|---------|
| **Type** | Lexicon-based | Transformer-based AI |
| **Speed** | Very fast (~1ms/article) | Slower (~800ms/article CPU, ~50ms GPU) |
| **Accuracy** | Good for obvious sentiment | Excellent for nuanced financial text |
| **Size** | ~1MB | ~439MB |
| **GPU** | Not needed | Recommended |
| **Best For** | Quick scans, social media | Financial news, trading decisions |
| **Context Understanding** | Limited | Excellent |

**When to use VADER:**
- Quick prototyping
- High-volume real-time processing without GPU
- Social media analysis
- Simple, clear sentiment

**When to use FinBERT:**
- You have a GPU (especially RTX 4090)
- Analyzing financial reports, earnings calls
- Making trading decisions
- Need contextual understanding

---

## Configuration & Usage

### Basic Usage - Gold Market (Default)

The application comes pre-configured for gold market analysis:

```bash
uv run python sentiment_analysis.py
```

**What happens:**
1. Fetches 10 articles each for 7 gold-related queries (70 total articles)
2. Analyzes sentiment of each article title
3. Prints individual results
4. Shows aggregate sentiment summary

**Expected output:**
```
Fetching news articles for 'gold market'...

Article 1: Gold prices surge to record highs
Link: https://...
Published: Fri, 24 Oct 2025 10:30:00 GMT
Sentiment: Positive (Polarity: 0.76)

Article 2: Gold falls on strong dollar
Link: https://...
Published: Fri, 24 Oct 2025 09:15:00 GMT
Sentiment: Negative (Polarity: -0.65)

...

--- Market Sentiment Summary ---
Total articles analyzed: 70
Positive: 15 (21.43%)
Negative: 10 (14.29%)
Neutral: 45 (64.29%)
```

### Customizing for Different Markets

#### ES Futures Example

Edit `sentiment_analysis.py` at lines 109-117:

```python
queries = [
    "ES futures",
    "S&P 500 futures",
    "E-mini S&P",
    "stock index futures",
    "equity futures market",
    "S&P futures analysis",
    "index futures forecast"
]
```

#### Bitcoin Example

```python
queries = [
    "bitcoin price",
    "BTC futures",
    "cryptocurrency market",
    "bitcoin forecast",
    "crypto sentiment",
    "bitcoin analysis",
    "BTC news"
]
```

#### Crude Oil Example

```python
queries = [
    "crude oil futures",
    "WTI price",
    "oil market",
    "CL futures",
    "oil forecast",
    "energy market",
    "petroleum news"
]
```

### Adjusting Article Count

Change `num_articles_per_query` at line 118:

```python
num_articles_per_query = 20  # Default: 10
```

**Considerations:**
- More articles = better statistical confidence
- More articles = longer processing time
- Recommended: 10-20 per query for real-time use

### Modifying Sentiment Thresholds

Edit thresholds at lines 60-65:

```python
# Default thresholds
if polarity > 0.05:
    sentiment = 'Positive'
elif polarity < -0.05:
    sentiment = 'Negative'
else:
    sentiment = 'Neutral'
```

**Stricter thresholds (fewer neutrals):**
```python
if polarity > 0.15:
    sentiment = 'Positive'
elif polarity < -0.15:
    sentiment = 'Negative'
else:
    sentiment = 'Neutral'
```

**Looser thresholds (more positives/negatives):**
```python
if polarity > 0.01:
    sentiment = 'Positive'
elif polarity < -0.01:
    sentiment = 'Negative'
else:
    sentiment = 'Neutral'
```

---

## Switching Between Sentiment Engines

### Currently Active: VADER

Lines 51-67 are uncommented (active).

### To Switch to FinBERT

**Step 1:** Comment out VADER implementation (lines 51-67):

```python
# def analyze_sentiment(text):
#     analyzer = SentimentIntensityAnalyzer()
#     scores = analyzer.polarity_scores(text)
#     polarity = scores['compound']
#
#     if polarity > 0.05:
#         sentiment = 'Positive'
#     elif polarity < -0.05:
#         sentiment = 'Negative'
#     else:
#         sentiment = 'Neutral'
#
#     return polarity, sentiment
```

**Step 2:** Uncomment FinBERT implementation (lines 69-83):

```python
def analyze_sentiment(text):
    if not text.strip():
        return 0.0, 'Neutral'

    inputs = finbert_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = finbert_model(**inputs)

    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).numpy()[0]
    max_index = np.argmax(probabilities)
    sentiment = labels[max_index]
    confidence = probabilities[max_index]

    return confidence, sentiment
```

**Step 3:** Run the script:

```bash
uv run python sentiment_analysis.py
```

**First run:** Downloads FinBERT model (~439MB) - happens once, cached locally.

---

## GPU Acceleration Setup

### Step 1: Verify GPU is Detected

```bash
nvidia-smi
```

**Expected output:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xx       Driver Version: 535.xx       CUDA Version: 12.x    |
|-------------------------------+----------------------+----------------------+
| GPU  Name                     | Bus-Id        Disp.A | Volatile Uncorr. ECC |
|   0  NVIDIA GeForce RTX 4090  | 00000000:01:00.0  On |                  N/A |
+-------------------------------+----------------------+----------------------+
```

### Step 2: Modify Code for GPU Support

Add at the top of `sentiment_analysis.py` (after imports):

```python
import torch

# GPU setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
```

Modify model loading (lines 13-14):

```python
finbert_model = AutoModelForSequenceClassification.from_pretrained(
    "yiyanghkust/finbert-tone"
).to(device)  # ← Add this

finbert_tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
```

Modify FinBERT analyze_sentiment function:

```python
def analyze_sentiment(text):
    if not text.strip():
        return 0.0, 'Neutral'

    inputs = finbert_tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(device)  # ← Add this

    with torch.no_grad():
        outputs = finbert_model(**inputs)

    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]  # ← Add .cpu()
    max_index = np.argmax(probabilities)
    sentiment = labels[max_index]
    confidence = probabilities[max_index]

    return confidence, sentiment
```

### Step 3: Monitor GPU Usage

Run in a separate terminal:

```bash
nvidia-smi -l 1
```

Watch for:
- **Memory-Usage**: Should be ~2GB when model loaded
- **GPU-Util**: Should spike to 80-100% during analysis

### Performance Comparison

**RTX 4090 Results:**

| Configuration | 70 Articles | 1000 Articles |
|---------------|-------------|---------------|
| VADER (CPU) | ~1 second | ~15 seconds |
| FinBERT (CPU) | ~60 seconds | ~14 minutes |
| FinBERT (GPU) | ~3 seconds | ~40 seconds |

---

## Multi-Market Analysis

### Example: Compare 4 Markets Simultaneously

Create a new file `multi_market_analysis.py`:

```python
from sentiment_analysis import fetch_news, analyze_sentiment

def multi_market_scanner():
    markets = {
        "Gold": [
            "gold market",
            "gold price",
            "gold forecast"
        ],
        "ES Futures": [
            "ES futures",
            "S&P 500 futures",
            "stock index futures"
        ],
        "Crude Oil": [
            "crude oil futures",
            "WTI price",
            "oil market"
        ],
        "Bitcoin": [
            "bitcoin price",
            "BTC futures",
            "crypto market"
        ]
    }

    results = {}

    for market_name, queries in markets.items():
        print(f"\n{'='*60}")
        print(f"Analyzing {market_name}")
        print(f"{'='*60}\n")

        all_articles = []
        for query in queries:
            print(f"Fetching: '{query}'...")
            articles = fetch_news(query, num_articles=10)
            all_articles.extend(articles)

        # Analyze sentiment
        positive = negative = neutral = 0
        for article in all_articles:
            _, sentiment = analyze_sentiment(article['title'])
            if sentiment == 'Positive':
                positive += 1
            elif sentiment == 'Negative':
                negative += 1
            else:
                neutral += 1

        total = len(all_articles)
        results[market_name] = {
            'Positive': (positive / total) * 100,
            'Negative': (negative / total) * 100,
            'Neutral': (neutral / total) * 100,
            'Total': total
        }

    # Display comparison
    print("\n" + "="*60)
    print("MARKET SENTIMENT COMPARISON")
    print("="*60)
    print(f"{'Market':<15} {'Positive':<12} {'Negative':<12} {'Neutral':<12}")
    print("-" * 60)

    for market, data in results.items():
        print(f"{market:<15} {data['Positive']:>6.1f}%     {data['Negative']:>6.1f}%     {data['Neutral']:>6.1f}%")

    # Identify most bullish/bearish
    print("\n" + "="*60)
    most_bullish = max(results.items(), key=lambda x: x[1]['Positive'])
    most_bearish = max(results.items(), key=lambda x: x[1]['Negative'])

    print(f"Most Bullish:  {most_bullish[0]} ({most_bullish[1]['Positive']:.1f}% positive)")
    print(f"Most Bearish:  {most_bearish[0]} ({most_bearish[1]['Negative']:.1f}% negative)")

if __name__ == "__main__":
    multi_market_scanner()
```

**Run:**
```bash
uv run python multi_market_analysis.py
```

**Example Output:**
```
============================================================
MARKET SENTIMENT COMPARISON
============================================================
Market          Positive     Negative     Neutral
------------------------------------------------------------
Gold              21.4%        14.3%        64.3%
ES Futures        45.0%        12.0%        43.0%
Crude Oil         18.0%        35.0%        47.0%
Bitcoin           62.0%         8.0%        30.0%

============================================================
Most Bullish:  Bitcoin (62.0% positive)
Most Bearish:  Crude Oil (35.0% negative)
```

---

## Interpreting Results

### Understanding Sentiment Scores

#### VADER Polarity Scale

```
-1.0 ←────────────── 0 ──────────────→ +1.0
Very Negative      Neutral      Very Positive
```

**Examples:**
- `0.76` - Strong positive (e.g., "Gold surges to record highs!")
- `0.15` - Mild positive (e.g., "Gold edges higher")
- `0.00` - Neutral (e.g., "Gold trading unchanged")
- `-0.32` - Mild negative (e.g., "Gold dips slightly")
- `-0.85` - Strong negative (e.g., "Gold crashes on selloff")

#### FinBERT Confidence

FinBERT returns confidence (0-1) for its classification:
- `> 0.9` - Very confident
- `0.7-0.9` - Confident
- `0.5-0.7` - Moderate confidence
- `< 0.5` - Low confidence (treat with caution)

### Statistical Significance

**Sample size matters:**

| Articles Analyzed | Reliability |
|-------------------|-------------|
| 10-20 | Low - use for quick checks only |
| 30-50 | Moderate - reasonable snapshot |
| 70-100 | Good - reliable for decision-making |
| 200+ | Excellent - high statistical confidence |

### Sentiment as Trading Signal

**Bullish Signals:**
- Positive sentiment > 40%
- Negative sentiment < 15%
- Increasing positive trend over time

**Bearish Signals:**
- Negative sentiment > 35%
- Positive sentiment < 20%
- Increasing negative trend

**Neutral/Uncertain:**
- Neutral > 60%
- Positive ≈ Negative
- Mixed signals

**Important:** Sentiment is **one indicator** - combine with:
- Technical analysis (charts, indicators)
- Fundamental analysis (economic data)
- Price action
- Volume

---

## Advanced Usage

### 1. Scheduled Automated Analysis

**Windows Task Scheduler:**

Create `run_scanner.bat`:
```batch
@echo off
cd C:\Users\YourName\Dev\NewsSentimentScanner
call .venv\Scripts\activate
python sentiment_analysis.py > output_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.txt
```

Schedule to run daily at 8:00 AM before market open.

**Linux/macOS Cron:**
```bash
# Edit crontab
crontab -e

# Add line (runs daily at 8 AM)
0 8 * * * cd /home/user/NewsSentimentScanner && .venv/bin/python sentiment_analysis.py >> logs/$(date +\%Y\%m\%d).log 2>&1
```

### 2. Export Results to CSV

Add to `sentiment_analysis.py`:

```python
import csv
from datetime import datetime

def export_to_csv(articles, filename=None):
    if filename is None:
        filename = f"sentiment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Title', 'Link', 'Published', 'Polarity', 'Sentiment'])

        for article in articles:
            polarity, sentiment = analyze_sentiment(article['title'])
            writer.writerow([
                datetime.now().isoformat(),
                article['title'],
                article['link'],
                article['published'],
                polarity,
                sentiment
            ])

    print(f"Results exported to {filename}")

# In main(), add:
export_to_csv(all_articles)
```

### 3. Real-Time Monitoring Dashboard

Combine with a web framework:

```python
from flask import Flask, jsonify
import threading
import time

app = Flask(__name__)
latest_results = {}

def background_scanner():
    global latest_results
    while True:
        # Run analysis
        articles = []
        for query in queries:
            articles.extend(fetch_news(query, num_articles=10))

        # Calculate sentiment
        positive = sum(1 for a in articles if analyze_sentiment(a['title'])[1] == 'Positive')
        negative = sum(1 for a in articles if analyze_sentiment(a['title'])[1] == 'Negative')

        latest_results = {
            'timestamp': time.time(),
            'positive': positive,
            'negative': negative,
            'total': len(articles)
        }

        # Wait 30 minutes
        time.sleep(1800)

@app.route('/sentiment')
def get_sentiment():
    return jsonify(latest_results)

if __name__ == '__main__':
    scanner_thread = threading.Thread(target=background_scanner, daemon=True)
    scanner_thread.start()
    app.run(host='0.0.0.0', port=5000)
```

Access at `http://localhost:5000/sentiment`

### 4. Batch Processing with GPU

For maximum GPU efficiency:

```python
def batch_analyze_sentiment(texts, batch_size=32):
    """Analyze multiple texts at once using GPU"""
    results = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]

        inputs = finbert_tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(device)

        with torch.no_grad():
            outputs = finbert_model(**inputs)

        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).cpu().numpy()

        for probs in probabilities:
            max_index = np.argmax(probs)
            results.append((probs[max_index], labels[max_index]))

    return results

# Usage in main():
titles = [article['title'] for article in all_articles]
sentiments = batch_analyze_sentiment(titles, batch_size=32)
```

**Performance gain:** 3-5x faster with GPU when processing 100+ articles.

---

## Troubleshooting

### Issue: "CUDA not available" with GPU installed

**Solution:**
```bash
# Reinstall PyTorch with CUDA
uv pip uninstall torch
uv pip install torch --index-url https://download.pytorch.org/whl/cu121
```

Verify:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

### Issue: Model downloads every time

**Cause:** Hugging Face cache not persisted.

**Solution:**
Set cache directory:
```python
import os
os.environ['TRANSFORMERS_CACHE'] = 'C:/Users/YourName/.cache/huggingface'
```

### Issue: "Content not retrieved" for many articles

**Causes:**
- Website blocking scrapers
- Rate limiting
- Timeout too short

**Solutions:**

1. Increase timeout (line 41):
```python
response = requests.get(url, timeout=20)  # Increased from 10
```

2. Add user agent:
```python
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
response = requests.get(url, headers=headers, timeout=10)
```

3. Add delay between requests:
```python
import time
time.sleep(1)  # Wait 1 second between articles
```

### Issue: RSS feed returns no results

**Cause:** Query too specific or Google News has no articles.

**Solution:** Broaden query:
```python
# Too specific
"ES futures CME December contract"

# Better
"ES futures"
```

### Issue: Memory error with FinBERT

**Cause:** Insufficient RAM or VRAM.

**Solutions:**

1. Reduce batch size:
```python
# Process one at a time instead of batches
```

2. Clear CUDA cache periodically:
```python
torch.cuda.empty_cache()
```

3. Switch to VADER if no GPU available

### Issue: Slow performance on CPU

**Expected behavior:** FinBERT is slow on CPU (~800ms per article).

**Solutions:**
1. Use VADER instead (100x faster)
2. Get a GPU
3. Process overnight for large datasets
4. Reduce number of articles analyzed

---

## Best Practices

### 1. Query Design

**Good queries:**
- Specific enough: "ES futures" not just "futures"
- Market-relevant: "gold price forecast" not "gold jewelry"
- Multiple variations: "bitcoin", "BTC", "cryptocurrency"

**Poor queries:**
- Too broad: "market", "news"
- Ambiguous: "ES" (could mean Spain in Spanish)
- Single query only (get diverse sources)

### 2. Sample Size

- **Minimum:** 30 articles for any conclusion
- **Recommended:** 70-100 articles
- **Multiple time periods:** Run analysis over several days to spot trends

### 3. Combining with Other Data

Sentiment works best when combined with:

```
Trading Decision = 40% Technical + 30% Fundamental + 30% Sentiment
```

Never trade on sentiment alone.

### 4. Update Frequency

- **Pre-market:** Once before market open
- **Intraday:** Every 1-2 hours if volatility high
- **Post-event:** After major news (Fed, earnings, etc.)
- **Avoid:** Constant updates (noise vs signal)

### 5. Data Hygiene

- Archive results to CSV for historical analysis
- Delete old logs periodically
- Monitor for API changes in Google News RSS
- Validate results spot-check against manual reading

### 6. Model Selection

**Use VADER for:**
- Development and testing
- Quick daily scans
- Social media sentiment
- When you don't have GPU

**Use FinBERT for:**
- Live trading decisions
- Deep market analysis
- Research and backtesting
- When GPU available

### 7. Ethical Considerations

- **Respect robots.txt** and website terms of service
- **Don't spam requests** - add delays between fetches
- **Attribute sources** - news belongs to publishers
- **No guarantees** - sentiment is informational, not financial advice

---

## Appendix: Full Example Workflow

### Complete ES Futures Pre-Market Analysis

**Objective:** Analyze ES futures sentiment before 9:30 AM market open.

**Step 1:** Activate environment
```bash
cd C:\Users\nasser\Dev\NewsSentimentScanner
.venv\Scripts\activate
```

**Step 2:** Configure for ES futures (edit `sentiment_analysis.py`)
```python
queries = [
    "ES futures",
    "S&P 500 futures",
    "stock index futures",
    "equity futures",
    "S&P futures overnight"
]
num_articles_per_query = 15  # 75 total articles
```

**Step 3:** Ensure FinBERT is enabled (with GPU)
```python
# Uncomment FinBERT implementation (lines 69-83)
# Comment out VADER (lines 51-67)
```

**Step 4:** Run analysis
```bash
uv run python sentiment_analysis.py > es_sentiment_$(date +%Y%m%d).log
```

**Step 5:** Review results
```
--- Market Sentiment Summary ---
Total articles analyzed: 75
Positive: 34 (45.33%)
Negative: 9 (12.00%)
Neutral: 32 (42.67%)
```

**Step 6:** Interpret
- **45% positive, 12% negative** → Bullish bias
- **Consider long bias** for ES futures
- **Confirm with:** Price action, overnight futures levels, economic calendar

**Step 7:** Monitor throughout day
- Re-run at 12:00 PM if major news
- Compare morning vs afternoon sentiment
- Track sentiment shifts

---

## Support & Resources

### Documentation
- **VADER**: https://github.com/cjhutto/vaderSentiment
- **FinBERT**: https://huggingface.co/yiyanghkust/finbert-tone
- **Transformers**: https://huggingface.co/docs/transformers

### Community
- Open issues at project repository
- Share strategies in discussions
- Contribute improvements via pull requests

### Disclaimer

This tool is for informational purposes only. Sentiment analysis does not guarantee trading profits. Always:
- Do your own research
- Use proper risk management
- Never risk more than you can afford to lose
- Consult a financial advisor for investment advice

---

**Version:** 1.0
**Last Updated:** October 2025
**License:** MIT
