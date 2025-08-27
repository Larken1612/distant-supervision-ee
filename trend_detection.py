import numpy as np
from scipy.stats import poisson

def detect_trends_sliding(counts: list[int], z_threshold: float = 2, cusum_multiplier: float = 3, window_size: int = 2):
    """
    Detect trends using a sliding 2-day baseline window.
    
    :param counts: List of 7 daily event counts
    :param z_threshold: Z-score threshold for spikes (default=2)
    :param cusum_multiplier: Multiplier for CUSUM threshold (default=3)
    :param window_size: Number of days for sliding baseline (default=2)
    
    :return: Trend scores and flags for each day (Days 3–7)
    """
    counts = np.array(counts)
    results = []
    
    for t in range(window_size, len(counts)):
        # Sliding baseline (previous 2 days)
        baseline = counts[t-window_size:t]
        mu = np.mean(baseline)
        
        # --- Handle near-zero baselines ---
        if mu < 1:
            min_abs_increase = 1
            cusum_threshold = 1
        else:
            min_abs_increase = max(2, 0.5 * mu)
            cusum_threshold = cusum_multiplier * max(np.std(baseline, ddof=0), 1.0)
        
        # --- Poisson Significance ---
        poisson_p = 1 - poisson.cdf(counts[t] - 1, mu) if mu > 0 else 0
        
        # --- Z-score with σ flooring ---
        sigma = max(np.std(baseline, ddof=0), 1.0)
        z_score = (counts[t] - mu) / sigma
        
        # --- CUSUM (single-step deviation) ---
        delta = 0.5 * mu
        S = max(0, counts[t] - (mu + delta))
        
        # --- Trend Logic ---
        is_spike = (z_score > z_threshold) or (counts[t] >= mu + min_abs_increase + 0.1)
        is_trend = ((S >= cusum_threshold) or (poisson_p < 0.01)) and is_spike == True
        # print(is_spike, is_trend)
        
        trend_score = z_score + S / (cusum_threshold + 1e-6)
        
        results.append({
            'day': t + 1,  # Convert to 1-based index
            'trend_score': trend_score,
            'trend_confirmed': is_trend,
            'poisson_p': poisson_p,
            'z_score': z_score,
            'cusum': S,
            'baseline_mean': mu,
            'baseline_std': sigma
        })
    
    trending_day = None
    max_trending_score = -1

    for item in results:
        if item['trend_confirmed'] == True:
            if item['trend_score'] > max_trending_score:
                trending_day = item['day']
                max_trending_score = item['trend_score']

    return trending_day, max_trending_score

if __name__ == "__main__":
    print(detect_trends_sliding([0, 2, 6, 0, 0, 1, 0]))
