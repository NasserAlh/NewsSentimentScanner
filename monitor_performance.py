"""
Real-time Performance Monitor
Shows live metrics while processing articles
"""

import time
import sys
from datetime import datetime
from sentiment_analysis import fetch_news, analyze_sentiment


class PerformanceMonitor:
    """Real-time performance monitoring with live display"""

    def __init__(self):
        self.start_time = None
        self.article_count = 0
        self.timings = []
        self.sentiments = {'Positive': 0, 'Negative': 0, 'Neutral': 0}

    def start(self):
        """Start monitoring"""
        self.start_time = time.time()
        self.clear_screen()
        print("🚀 Starting News Sentiment Analysis with Performance Monitoring")
        print("=" * 80)

    def clear_screen(self):
        """Clear screen for live updates"""
        # Use print newlines instead of os.system for cross-platform
        print("\n" * 2)

    def update(self, article_title, sentiment, score, elapsed):
        """Update metrics with new article analysis"""
        self.article_count += 1
        self.timings.append(elapsed * 1000)  # Convert to ms
        self.sentiments[sentiment] += 1

        # Display live stats
        self.display_dashboard(article_title, sentiment, score, elapsed)

    def display_dashboard(self, last_title, last_sentiment, last_score, last_time):
        """Display real-time dashboard"""
        elapsed_total = time.time() - self.start_time
        avg_time = sum(self.timings) / len(self.timings) if self.timings else 0
        throughput = self.article_count / elapsed_total if elapsed_total > 0 else 0

        # Clear previous output (simple version)
        print("\r" + " " * 80, end='\r')

        # Header
        print(f"\n{'=' * 80}")
        print(f"📊 REAL-TIME PERFORMANCE DASHBOARD - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'=' * 80}\n")

        # Performance metrics
        print(f"⏱️  PERFORMANCE METRICS:")
        print(f"   Articles Processed:  {self.article_count}")
        print(f"   Total Time:          {elapsed_total:.2f}s")
        print(f"   Avg Time/Article:    {avg_time:.2f}ms")
        print(f"   Last Article Time:   {last_time*1000:.2f}ms")
        print(f"   Throughput:          {throughput:.1f} articles/sec")

        # Create simple progress bar
        if self.article_count > 0:
            bar_width = 50
            progress = min(self.article_count / 60, 1.0)  # Assume 60 articles target
            filled = int(bar_width * progress)
            bar = '█' * filled + '░' * (bar_width - filled)
            print(f"   Progress:            [{bar}] {self.article_count}/60")

        # Sentiment distribution
        total = sum(self.sentiments.values())
        print(f"\n💭 SENTIMENT DISTRIBUTION:")
        for sentiment, count in self.sentiments.items():
            pct = (count / total * 100) if total > 0 else 0
            bar_length = int(pct / 2)  # Scale to 50 chars max
            bar = '█' * bar_length
            emoji = '🟢' if sentiment == 'Positive' else '🔴' if sentiment == 'Negative' else '⚪'
            print(f"   {emoji} {sentiment:<10} {count:>3} ({pct:>5.1f}%) {bar}")

        # Last analyzed article
        print(f"\n📰 LAST ANALYZED:")
        print(f"   Title:     {last_title[:65]}...")
        print(f"   Sentiment: {last_sentiment}")
        print(f"   Score:     {last_score:.2f}")

        print(f"\n{'=' * 80}")

        # Flush output
        sys.stdout.flush()

    def summary(self):
        """Display final summary"""
        elapsed_total = time.time() - self.start_time

        print("\n\n" + "=" * 80)
        print("📊 FINAL PERFORMANCE SUMMARY")
        print("=" * 80)

        print(f"\n⏱️  TIMING:")
        print(f"   Total Articles: {self.article_count}")
        print(f"   Total Time:     {elapsed_total:.2f}s")
        print(f"   Average Time:   {sum(self.timings)/len(self.timings):.2f}ms per article")
        print(f"   Fastest:        {min(self.timings):.2f}ms")
        print(f"   Slowest:        {max(self.timings):.2f}ms")
        print(f"   Throughput:     {self.article_count/elapsed_total:.1f} articles/sec")

        print(f"\n💭 SENTIMENT BREAKDOWN:")
        total = sum(self.sentiments.values())
        for sentiment, count in sorted(self.sentiments.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total * 100) if total > 0 else 0
            print(f"   {sentiment}: {count} ({pct:.1f}%)")

        # Market signal
        positive_pct = (self.sentiments['Positive'] / total * 100) if total > 0 else 0
        negative_pct = (self.sentiments['Negative'] / total * 100) if total > 0 else 0

        print(f"\n📈 MARKET SIGNAL:")
        if positive_pct > 40:
            signal = "🟢 BULLISH"
        elif negative_pct > 35:
            signal = "🔴 BEARISH"
        else:
            signal = "⚪ NEUTRAL"

        print(f"   {signal}")
        print(f"   Positive: {positive_pct:.1f}% | Negative: {negative_pct:.1f}%")

        print("\n" + "=" * 80)


def main():
    """Run monitored sentiment analysis"""
    monitor = PerformanceMonitor()
    monitor.start()

    # Configure queries
    queries = [
        "gold market",
        "gold price",
        "gold forecast"
    ]

    print(f"📡 Fetching articles for {len(queries)} queries...\n")

    all_articles = []
    for query in queries:
        print(f"   Fetching: '{query}'...")
        articles = fetch_news(query, num_articles=20)
        all_articles.extend(articles)
        print(f"   ✓ Got {len(articles)} articles")

    print(f"\n📊 Starting analysis of {len(all_articles)} articles...\n")
    time.sleep(1)

    # Analyze with monitoring
    for article in all_articles:
        start = time.time()
        score, sentiment = analyze_sentiment(article['title'])
        elapsed = time.time() - start

        monitor.update(article['title'], sentiment, score, elapsed)

        # Small delay to see the updates (remove in production)
        time.sleep(0.05)

    # Display summary
    monitor.summary()


if __name__ == "__main__":
    main()
