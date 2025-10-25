"""
Benchmark Comparison: VADER vs FinBERT
Provides comprehensive observability and performance metrics
"""

import time
import torch
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentiment_analysis import fetch_news
import psutil
import json
from datetime import datetime
from collections import defaultdict

# GPU setup for FinBERT
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load models
print("Loading models...")
vader_analyzer = SentimentIntensityAnalyzer()

finbert_model = AutoModelForSequenceClassification.from_pretrained(
    "yiyanghkust/finbert-tone"
).to(device)
finbert_tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
labels = ['Positive', 'Negative', 'Neutral']

print("Models loaded!\n")


def analyze_sentiment_vader(text):
    """VADER sentiment analysis"""
    scores = vader_analyzer.polarity_scores(text)
    polarity = scores['compound']

    if polarity > 0.05:
        sentiment = 'Positive'
    elif polarity < -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return polarity, sentiment


def analyze_sentiment_finbert(text):
    """FinBERT sentiment analysis"""
    if not text.strip():
        return 0.0, 'Neutral'

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

    return confidence, sentiment


class PerformanceMetrics:
    """Track performance metrics for each method"""

    def __init__(self, name):
        self.name = name
        self.timings = []
        self.memory_samples = []
        self.gpu_memory_samples = []
        self.results = []
        self.start_time = None
        self.end_time = None

    def start(self):
        """Start timing"""
        self.start_time = time.time()
        self.memory_samples.append(psutil.Process().memory_info().rss / 1e6)
        if torch.cuda.is_available():
            self.gpu_memory_samples.append(torch.cuda.memory_allocated() / 1e6)

    def record_single(self, elapsed, result):
        """Record single operation"""
        self.timings.append(elapsed)
        self.results.append(result)

    def end(self):
        """End timing"""
        self.end_time = time.time()
        self.memory_samples.append(psutil.Process().memory_info().rss / 1e6)
        if torch.cuda.is_available():
            self.gpu_memory_samples.append(torch.cuda.memory_allocated() / 1e6)

    def get_stats(self):
        """Calculate statistics"""
        total_time = self.end_time - self.start_time
        timings_array = np.array(self.timings) * 1000  # Convert to ms

        # Sentiment distribution
        sentiment_counts = defaultdict(int)
        for _, sentiment in self.results:
            sentiment_counts[sentiment] += 1

        stats = {
            'name': self.name,
            'total_time_sec': total_time,
            'num_samples': len(self.timings),
            'avg_time_ms': np.mean(timings_array),
            'median_time_ms': np.median(timings_array),
            'min_time_ms': np.min(timings_array),
            'max_time_ms': np.max(timings_array),
            'std_time_ms': np.std(timings_array),
            'throughput_per_sec': len(self.timings) / total_time,
            'ram_usage_mb': max(self.memory_samples) - min(self.memory_samples),
            'sentiment_distribution': dict(sentiment_counts),
        }

        if torch.cuda.is_available() and self.gpu_memory_samples:
            stats['gpu_memory_mb'] = max(self.gpu_memory_samples) - min(self.gpu_memory_samples)

        return stats


def benchmark_method(method_name, analyze_func, articles):
    """Benchmark a single method"""
    print(f"{'='*70}")
    print(f"Benchmarking: {method_name}")
    print(f"{'='*70}")

    metrics = PerformanceMetrics(method_name)
    metrics.start()

    for i, article in enumerate(articles):
        text = article['title']

        # Time individual analysis
        start = time.time()
        score, sentiment = analyze_func(text)
        elapsed = time.time() - start

        metrics.record_single(elapsed, (score, sentiment))

        # Print first 5 and progress
        if i < 5:
            print(f"  [{i+1}] {sentiment} ({score:.2f}): {text[:60]}...")
        elif i % 20 == 0:
            print(f"  Progress: {i}/{len(articles)} articles analyzed...")

    metrics.end()

    print(f"  ✅ Complete: {len(articles)} articles in {metrics.end_time - metrics.start_time:.2f}s\n")

    return metrics


def compare_results(vader_metrics, finbert_metrics, articles):
    """Compare results between methods"""
    print(f"\n{'='*70}")
    print("RESULT COMPARISON")
    print(f"{'='*70}\n")

    agreements = 0
    disagreements = []

    for i, article in enumerate(articles):
        vader_result = vader_metrics.results[i]
        finbert_result = finbert_metrics.results[i]

        if vader_result[1] == finbert_result[1]:
            agreements += 1
        else:
            disagreements.append({
                'title': article['title'],
                'vader': vader_result,
                'finbert': finbert_result
            })

    agreement_rate = (agreements / len(articles)) * 100

    print(f"Agreement Rate: {agreement_rate:.1f}% ({agreements}/{len(articles)})")
    print(f"Disagreements: {len(disagreements)}\n")

    if disagreements:
        print(f"Sample Disagreements (first 10):")
        print(f"{'-'*70}")
        for i, item in enumerate(disagreements[:10]):
            print(f"\n{i+1}. {item['title'][:65]}...")
            print(f"   VADER:   {item['vader'][1]} (score: {item['vader'][0]:.2f})")
            print(f"   FinBERT: {item['finbert'][1]} (confidence: {item['finbert'][0]:.2f})")

    return agreement_rate, disagreements


def print_performance_report(vader_stats, finbert_stats):
    """Print detailed performance comparison"""
    print(f"\n{'='*70}")
    print("PERFORMANCE METRICS REPORT")
    print(f"{'='*70}\n")

    # Performance comparison table
    print(f"{'Metric':<30} {'VADER':<20} {'FinBERT':<20} {'Winner'}")
    print(f"{'-'*70}")

    metrics_comparison = [
        ('Total Time', f"{vader_stats['total_time_sec']:.3f}s",
         f"{finbert_stats['total_time_sec']:.3f}s",
         'VADER' if vader_stats['total_time_sec'] < finbert_stats['total_time_sec'] else 'FinBERT'),

        ('Avg Time per Article', f"{vader_stats['avg_time_ms']:.2f}ms",
         f"{finbert_stats['avg_time_ms']:.2f}ms",
         'VADER' if vader_stats['avg_time_ms'] < finbert_stats['avg_time_ms'] else 'FinBERT'),

        ('Median Time', f"{vader_stats['median_time_ms']:.2f}ms",
         f"{finbert_stats['median_time_ms']:.2f}ms",
         'VADER' if vader_stats['median_time_ms'] < finbert_stats['median_time_ms'] else 'FinBERT'),

        ('Throughput', f"{vader_stats['throughput_per_sec']:.1f}/sec",
         f"{finbert_stats['throughput_per_sec']:.1f}/sec",
         'FinBERT' if finbert_stats['throughput_per_sec'] > vader_stats['throughput_per_sec'] else 'VADER'),

        ('RAM Usage', f"{vader_stats['ram_usage_mb']:.1f}MB",
         f"{finbert_stats['ram_usage_mb']:.1f}MB",
         'VADER' if vader_stats['ram_usage_mb'] < finbert_stats['ram_usage_mb'] else 'FinBERT'),
    ]

    if 'gpu_memory_mb' in finbert_stats:
        metrics_comparison.append(
            ('GPU Memory', 'N/A', f"{finbert_stats['gpu_memory_mb']:.1f}MB", 'VADER')
        )

    for metric, vader_val, finbert_val, winner in metrics_comparison:
        winner_marker = ' ⭐' if winner else ''
        print(f"{metric:<30} {vader_val:<20} {finbert_val:<20} {winner}{winner_marker}")

    # Speed comparison
    print(f"\n{'='*70}")
    print("SPEED ANALYSIS")
    print(f"{'='*70}\n")

    speedup = vader_stats['avg_time_ms'] / finbert_stats['avg_time_ms']
    if speedup > 1:
        print(f"⚡ FinBERT is {speedup:.1f}x FASTER than VADER!")
        print(f"   (This is unusual - likely due to GPU acceleration)")
    else:
        slowdown = finbert_stats['avg_time_ms'] / vader_stats['avg_time_ms']
        print(f"🐌 FinBERT is {slowdown:.1f}x SLOWER than VADER")

    # Sentiment distribution comparison
    print(f"\n{'='*70}")
    print("SENTIMENT DISTRIBUTION")
    print(f"{'='*70}\n")

    print(f"{'Sentiment':<15} {'VADER':<20} {'FinBERT':<20} {'Difference'}")
    print(f"{'-'*70}")

    for sentiment in ['Positive', 'Negative', 'Neutral']:
        vader_count = vader_stats['sentiment_distribution'].get(sentiment, 0)
        finbert_count = finbert_stats['sentiment_distribution'].get(sentiment, 0)
        vader_pct = (vader_count / vader_stats['num_samples']) * 100
        finbert_pct = (finbert_count / finbert_stats['num_samples']) * 100
        diff = finbert_pct - vader_pct

        diff_str = f"{diff:+.1f}%"
        print(f"{sentiment:<15} {vader_count:>4} ({vader_pct:>5.1f}%)      {finbert_count:>4} ({finbert_pct:>5.1f}%)      {diff_str}")


def save_results(vader_stats, finbert_stats, agreement_rate, disagreements, filename=None):
    """Save results to JSON file"""
    if filename is None:
        filename = f"benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    results = {
        'timestamp': datetime.now().isoformat(),
        'device': str(device),
        'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A',
        'vader_stats': vader_stats,
        'finbert_stats': finbert_stats,
        'agreement_rate': agreement_rate,
        'num_disagreements': len(disagreements),
        'sample_disagreements': disagreements[:20]  # Save first 20
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📊 Results saved to: {filename}")


def main():
    """Main benchmark function"""
    print("="*70)
    print("VADER vs FinBERT - Comprehensive Benchmark")
    print("="*70)
    print(f"Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Version: {torch.version.cuda}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    # Fetch articles
    print("\n📰 Fetching articles...")
    queries = ["gold market", "gold price", "gold forecast"]
    articles = []

    for query in queries:
        print(f"   Fetching: '{query}'...")
        articles.extend(fetch_news(query, num_articles=20))

    print(f"   Total articles fetched: {len(articles)}\n")

    # Benchmark VADER
    vader_metrics = benchmark_method("VADER", analyze_sentiment_vader, articles)

    # Small delay
    time.sleep(1)

    # Benchmark FinBERT
    finbert_metrics = benchmark_method("FinBERT (GPU)", analyze_sentiment_finbert, articles)

    # Get statistics
    vader_stats = vader_metrics.get_stats()
    finbert_stats = finbert_metrics.get_stats()

    # Compare results
    agreement_rate, disagreements = compare_results(vader_metrics, finbert_metrics, articles)

    # Print report
    print_performance_report(vader_stats, finbert_stats)

    # Save results
    save_results(vader_stats, finbert_stats, agreement_rate, disagreements)

    print("\n" + "="*70)
    print("✅ Benchmark Complete!")
    print("="*70)


if __name__ == "__main__":
    main()
