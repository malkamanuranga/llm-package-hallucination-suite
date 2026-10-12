"""
Metrics Aggregator & Statistical Evaluator for LLM Slopsquatting Research.
Computes empirical hallucination rates, risk distribution, and threat summaries from JSONL logs.
"""

import json
from pathlib import Path

LOG_PATH = Path(__file__).parent / "async_hallucinations_log.jsonl"

def compute_metrics():
    """Reads the JSONL log and compiles statistical research metrics."""
    if not LOG_PATH.exists():
        print(f"[!] Threat log not found at {LOG_PATH}. Run async_pipeline.py first.")
        return

    total_records = 0
    model_stats = {}

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            total_records += 1
            
            model = record.get("model", "unknown")
            is_hallucination = record.get("is_hallucination", False)
            
            if model not in model_stats:
                model_stats[model] = {
                    "total_packages": 0,
                    "safe_packages": 0,
                    "hallucinated_packages": 0
                }
            
            model_stats[model]["total_packages"] += 1
            if is_hallucination:
                model_stats[model]["hallucinated_packages"] += 1
            else:
                model_stats[model]["safe_packages"] += 1

    print("\n" + "="*50)
    print("📊 EMPIRICAL SLOPQUATTING RESEARCH REPORT")
    print("="*50)
    print(f"Total Audit Entries Evaluated: {total_records}\n")

    for model, stats in model_stats.items():
        total = stats["total_packages"]
        halls = stats["hallucinated_packages"]
        safe = stats["safe_packages"]
        rate = (halls / total * 100) if total > 0 else 0
        
        print(f"Model Engine: {model}")
        print(f"  -> Total Packages Scanned : {total}")
        print(f"  -> Verified Safe (Real)   : {safe}")
        print(f"  -> Hallucinated (Danger)  : {halls}")
        print(f"  -> Hallucination Rate     : {rate:.2f}%")
        print("-" * 50)

if __name__ == "__main__":
    compute_metrics()