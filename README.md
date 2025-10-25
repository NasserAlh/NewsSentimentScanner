# News Sentiment Scanner

A Python tool that fetches news articles from Google News RSS feeds and analyzes their sentiment using natural language processing. Designed for tracking market sentiment on specific topics like commodities, stocks, or market trends.

## Features

- **Multi-source news aggregation** - Fetches articles from Google News using multiple search queries
- **Dual sentiment analysis engines**:
  - VADER (active) - Fast, lexicon-based sentiment analysis
  - FinBERT (available) - Transformer-based model specialized for financial text
- **Article content extraction** - Scrapes full article text using BeautifulSoup
- **Aggregate sentiment reporting** - Summarizes overall sentiment across all analyzed articles

## Installation

This project uses UV for package management:

```bash
# Create virtual environment
uv venv

# Activate environment (Windows)
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

## Usage

Run the sentiment scanner:

```bash
uv run python sentiment_analysis.py
```

The script will:
1. Fetch articles for predefined queries (default: gold market-related topics)
2. Analyze sentiment for each article title
3. Display individual article results
4. Print aggregate sentiment summary

### Example Output

```
Fetching news articles for 'gold market'...

Article 1: Gold Bull Market: Trading Expert Issues Warning
Link: https://...
Published: Fri, 24 Oct 2025 10:30:00 GMT
Sentiment: Positive (Polarity: 0.40)

--- Market Sentiment Summary ---
Total articles analyzed: 70
Positive: 28 (40.00%)
Negative: 15 (21.43%)
Neutral: 27 (38.57%)
```

## Configuration

### Customizing Search Topics

Edit the `queries` list in `main()` ([sentiment_analysis.py:109-117](sentiment_analysis.py#L109-L117)):

```python
queries = [
    "your topic here",
    "related search",
]
```

### Adjusting Article Count

Modify `num_articles_per_query` ([sentiment_analysis.py:118](sentiment_analysis.py#L118)):

```python
num_articles_per_query = 20  # Default: 10
```

### Switching to FinBERT

For more accurate financial sentiment analysis, switch to FinBERT by:
1. Commenting out the VADER implementation ([sentiment_analysis.py:51-67](sentiment_analysis.py#L51-L67))
2. Uncommenting the FinBERT implementation ([sentiment_analysis.py:69-83](sentiment_analysis.py#L69-L83))

Note: FinBERT requires ~400MB memory and is slower but more accurate for financial text.

## Dependencies

- **feedparser** - RSS feed parsing
- **requests** - HTTP requests
- **beautifulsoup4** - HTML content extraction
- **vaderSentiment** - Lexicon-based sentiment analysis
- **textblob** - NLP library (currently unused)
- **transformers** - Hugging Face transformers for FinBERT
- **torch** - PyTorch for FinBERT model
- **numpy** - Numerical operations

## Project Structure

```
NewsSentimentScanner/
├── sentiment_analysis.py      # Main scanner implementation
├── benchmark_comparison.py    # Comprehensive VADER vs FinBERT benchmark
├── monitor_performance.py     # Real-time performance monitoring
├── quick_compare.py          # Quick side-by-side comparison
├── check_gpu.py              # GPU configuration checker
├── test_finbert_gpu.py       # FinBERT GPU acceleration test
├── test.ipynb                # Jupyter notebook for testing
├── requirements.txt          # Python dependencies
├── USER_MANUAL.md            # Comprehensive user manual
└── README.md                 # This file
```

## How It Works

1. **Fetch News** - Queries Google News RSS feeds for specified topics
2. **Extract Content** - Scrapes article content from source URLs (with 10s timeout)
3. **Analyze Sentiment** - Processes article titles using VADER or FinBERT
4. **Aggregate Results** - Calculates percentage breakdown of positive/negative/neutral sentiment

## Current Limitations

- Only analyzes article **titles**, not full content (for speed and accuracy)
- No rate limiting on requests
- No caching mechanism
- Basic error handling for failed content fetches

## Performance Benchmarking & Observability

### 1. Comprehensive Benchmark (Recommended)

Compare VADER vs FinBERT with detailed metrics:

```bash
uv run python benchmark_comparison.py
```

**Features:**
- Side-by-side performance comparison
- Agreement rate analysis
- Sentiment distribution comparison
- Memory usage tracking
- GPU utilization metrics
- Saves results to JSON file

**Output includes:**
- Total processing time
- Average time per article
- Throughput (articles/sec)
- RAM and GPU memory usage
- Disagreement analysis with examples

### 2. Real-Time Performance Monitor

Watch live metrics as articles are analyzed:

```bash
uv run python monitor_performance.py
```

**Features:**
- Live dashboard updates
- Real-time sentiment distribution
- Progress bar
- Instant throughput calculation
- Market signal indicator (Bullish/Bearish/Neutral)

### 3. Quick Comparison

Fast comparison on predefined headlines:

```bash
uv run python quick_compare.py
```

**Features:**
- Tests 15 financial headlines
- Side-by-side results
- Highlights disagreements
- Performance comparison
- No internet required (uses test data)

### 4. GPU Verification

Check GPU configuration:

```bash
uv run python check_gpu.py
```

Confirms CUDA availability, GPU model, and VRAM.

### Performance Expectations (RTX 4090)

| Method | Articles | Time | Speed per Article | Throughput |
|--------|----------|------|-------------------|------------|
| VADER | 70 | ~1s | ~14ms | 70/sec |
| FinBERT (GPU) | 70 | ~0.7s | ~9ms | 100+/sec |
| FinBERT (CPU) | 70 | ~60s | ~800ms | 1.2/sec |

## License

MIT

## Contributing

Contributions welcome! Please ensure code follows existing patterns and includes appropriate error handling.
