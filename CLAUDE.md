# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NewsSentimentScanner is a Python-based sentiment analysis tool that fetches news articles from Google News RSS feeds and analyzes their sentiment using multiple NLP approaches. The primary use case is analyzing market sentiment for specific topics (e.g., gold market trends).

## Architecture

The project uses a pipeline architecture:
1. **News Fetching** ([sentiment_analysis.py:18-37](sentiment_analysis.py#L18-L37)) - Uses Google News RSS feeds via feedparser
2. **Content Extraction** ([sentiment_analysis.py:39-49](sentiment_analysis.py#L39-L49)) - Scrapes article content using BeautifulSoup
3. **Sentiment Analysis** ([sentiment_analysis.py:51-67](sentiment_analysis.py#L51-L67)) - Currently uses VADER; FinBERT implementation available but commented out
4. **Aggregation** ([sentiment_analysis.py:86-106](sentiment_analysis.py#L86-L106)) - Summarizes sentiment across all articles

### Sentiment Analysis Approaches

The codebase supports two sentiment analysis methods:
- **Active: VADER** ([sentiment_analysis.py:51-67](sentiment_analysis.py#L51-L67)) - Fast, lexicon-based approach using vaderSentiment
- **Commented: FinBERT** ([sentiment_analysis.py:69-83](sentiment_analysis.py#L69-L83)) - Transformer-based model (yiyanghkust/finbert-tone) specialized for financial text

The FinBERT model is loaded at module level ([sentiment_analysis.py:13-14](sentiment_analysis.py#L13-L14)) but not currently used in the active implementation. Switch between methods by uncommenting the preferred `analyze_sentiment()` function.

## Development Setup

This project uses UV for package management (per CLAUDE.md standards):

```bash
# Initialize UV environment
uv venv
.venv\Scripts\activate

# Install dependencies from requirements.txt
uv pip install -r requirements.txt

# Run the main scanner
uv run python sentiment_analysis.py
```

## Running the Code

**Main script:**
```bash
uv run python sentiment_analysis.py
```

The script will:
- Fetch articles for predefined queries ([sentiment_analysis.py:109-117](sentiment_analysis.py#L109-L117))
- Analyze sentiment for each article
- Print individual results and aggregate summary

**Jupyter notebook testing:**
The [test.ipynb](test.ipynb) notebook contains VADER polarity testing for sample headlines.

## Key Configuration Points

- **Search queries:** Defined in `main()` ([sentiment_analysis.py:109-117](sentiment_analysis.py#L109-L117))
- **Articles per query:** `num_articles_per_query = 10` ([sentiment_analysis.py:118](sentiment_analysis.py#L118))
- **Sentiment thresholds:** Polarity > 0.05 = Positive, < -0.05 = Negative ([sentiment_analysis.py:60-65](sentiment_analysis.py#L60-L65))
- **Article content timeout:** 10 seconds ([sentiment_analysis.py:41](sentiment_analysis.py#L41))

## Important Implementation Notes

- Sentiment analysis currently runs on **titles only**, not full content ([sentiment_analysis.py:98](sentiment_analysis.py#L98), [sentiment_analysis.py:131](sentiment_analysis.py#L131))
- Article content is fetched but not used in analysis (to avoid noise and improve speed)
- FinBERT model loads at import time, consuming ~400MB memory even when not used
- No rate limiting on news fetching or content scraping
- Error handling for content fetching returns "Content not retrieved." string ([sentiment_analysis.py:49](sentiment_analysis.py#L49))

## Dependencies Migration Note

The project currently uses `requirements.txt`. To migrate to UV's native dependency management:
```bash
# Convert to pyproject.toml
uv init
uv add feedparser requests beautifulsoup4 textblob vaderSentiment transformers torch numpy
```
