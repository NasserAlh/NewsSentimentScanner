"""
Quick Comparison Script
Fast side-by-side comparison of VADER vs FinBERT
"""

import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentiment_analysis import analyze_sentiment as finbert_analyze

# Sample financial headlines for testing
test_headlines = [
    "Gold prices surge to record highs on strong demand",
    "ES futures tumble on recession fears and weak economic data",
    "Market remains neutral amid mixed signals from Fed",
    "Bitcoin rallies as institutional adoption accelerates",
    "Crude oil falls sharply on oversupply concerns",
    "S&P 500 futures point to higher open after strong earnings",
    "Gold drops on profit-taking after recent rally",
    "Treasury yields spike as inflation concerns mount",
    "Stocks extend gains on optimism about trade talks",
    "Dollar weakens against major currencies",
    "Commodities sell off amid strengthening dollar",
    "Tech stocks lead market recovery in afternoon trading",
    "Oil inventories rise more than expected, prices decline",
    "Gold maintains support near key technical levels",
    "Futures gap down on disappointing jobs report",
]


def vader_sentiment(text):
    """VADER analysis"""
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    polarity = scores['compound']

    if polarity > 0.05:
        sentiment = 'Positive'
    elif polarity < -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return polarity, sentiment


def compare_on_headline(headline, index):
    """Compare both methods on a single headline"""
    print(f"\n{'─' * 80}")
    print(f"[{index}] {headline}")
    print(f"{'─' * 80}")

    # VADER
    start = time.time()
    vader_score, vader_sentiment = vader_sentiment(headline)
    vader_time = (time.time() - start) * 1000

    # FinBERT
    start = time.time()
    finbert_score, finbert_sentiment = finbert_analyze(headline)
    finbert_time = (time.time() - start) * 1000

    # Display results
    print(f"{'Method':<15} {'Sentiment':<12} {'Score':<10} {'Time':<15} {'Match'}")
    print(f"{'-' * 80}")

    match = '✓' if vader_sentiment == finbert_sentiment else '✗ DISAGREE'

    print(f"{'VADER':<15} {vader_sentiment:<12} {vader_score:<10.3f} {vader_time:<13.2f}ms")
    print(f"{'FinBERT (GPU)':<15} {finbert_sentiment:<12} {finbert_score:<10.3f} {finbert_time:<13.2f}ms  {match}")

    if vader_sentiment != finbert_sentiment:
        print(f"\n⚠️  Methods disagree on this headline!")
        if abs(vader_score) < 0.15:
            print(f"   → VADER score is close to neutral threshold")
        if finbert_score < 0.7:
            print(f"   → FinBERT confidence is moderate")

    return {
        'headline': headline,
        'vader': {'sentiment': vader_sentiment, 'score': vader_score, 'time': vader_time},
        'finbert': {'sentiment': finbert_sentiment, 'score': finbert_score, 'time': finbert_time},
        'match': vader_sentiment == finbert_sentiment
    }


def main():
    """Run comparison"""
    print("=" * 80)
    print("VADER vs FinBERT - Quick Comparison")
    print("=" * 80)
    print(f"Testing with {len(test_headlines)} financial headlines\n")

    results = []

    # Warm up FinBERT
    print("Warming up FinBERT GPU...")
    finbert_analyze("warm up")
    print("✓ Ready\n")

    # Compare each headline
    for i, headline in enumerate(test_headlines, 1):
        result = compare_on_headline(headline, i)
        results.append(result)

    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    matches = sum(1 for r in results if r['match'])
    disagreements = len(results) - matches
    agreement_rate = (matches / len(results)) * 100

    vader_times = [r['vader']['time'] for r in results]
    finbert_times = [r['finbert']['time'] for r in results]

    print(f"\n📊 Agreement:")
    print(f"   Matches:       {matches}/{len(results)} ({agreement_rate:.1f}%)")
    print(f"   Disagreements: {disagreements}/{len(results)}")

    print(f"\n⏱️  Performance:")
    print(f"   VADER avg:     {sum(vader_times)/len(vader_times):.2f}ms")
    print(f"   FinBERT avg:   {sum(finbert_times)/len(finbert_times):.2f}ms")

    speedup = sum(vader_times) / sum(finbert_times)
    if speedup < 1:
        print(f"   🚀 FinBERT is {1/speedup:.1f}x FASTER (GPU acceleration!)")
    else:
        print(f"   ⚡ VADER is {speedup:.1f}x faster")

    # Sentiment distribution comparison
    vader_sentiments = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    finbert_sentiments = {'Positive': 0, 'Negative': 0, 'Neutral': 0}

    for r in results:
        vader_sentiments[r['vader']['sentiment']] += 1
        finbert_sentiments[r['finbert']['sentiment']] += 1

    print(f"\n💭 Sentiment Distribution:")
    print(f"   {'Sentiment':<12} {'VADER':<10} {'FinBERT':<10} {'Diff'}")
    print(f"   {'-' * 45}")
    for sentiment in ['Positive', 'Negative', 'Neutral']:
        vader_count = vader_sentiments[sentiment]
        finbert_count = finbert_sentiments[sentiment]
        diff = finbert_count - vader_count
        diff_str = f"{diff:+d}" if diff != 0 else "="
        print(f"   {sentiment:<12} {vader_count:<10} {finbert_count:<10} {diff_str}")

    # Show disagreements
    if disagreements > 0:
        print(f"\n⚠️  Headlines where methods disagreed:")
        print(f"   {'-' * 76}")
        for i, r in enumerate(results, 1):
            if not r['match']:
                print(f"\n   [{i}] {r['headline'][:70]}")
                print(f"       VADER: {r['vader']['sentiment']} ({r['vader']['score']:.2f})")
                print(f"       FinBERT: {r['finbert']['sentiment']} ({r['finbert']['score']:.2f})")

    print("\n" + "=" * 80)
    print("✅ Comparison Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
