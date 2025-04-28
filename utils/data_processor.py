# utils/data_processor.py
from typing import Dict, List, Any
import json
import os
import pandas as pd
from evaluation.scoring import ScoringAnalyzer


def process_results(results: List[Dict[str, Any]], output_dir: str, include_themes: bool = True) -> Dict[str, Any]:
    """
    Process and analyze results
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save complete results
    with open(f"{output_dir}/complete_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Extract scores
    scores_data = []
    for result in results:
        case = result.get("case", {})
        scores = result.get("scores", {})

        scores_data.append({
            "case_id": case.get("case_id", ""),
            "theme": case.get("theme", ""),
            "subtheme": case.get("subtheme", ""),
            "query": case.get("query", ""),
            "risk_level": case.get("risk_level", ""),
            "overall_score": scores.get("overall", 0),
            "principle_1": scores.get("principle_1", 0),
            "principle_2": scores.get("principle_2", 0),
            "principle_3": scores.get("principle_3", 0),
            "principle_4": scores.get("principle_4", 0),
            "principle_5": scores.get("principle_5", 0),
            "principle_6": scores.get("principle_6", 0),
            "principle_7": scores.get("principle_7", 0),
            "principle_8": scores.get("principle_8", 0),
            "principle_9": scores.get("principle_9", 0),
            "safety_level": scores.get("safety_level", "Unknown")
        })

    # Create scores DataFrame
    df_scores = pd.DataFrame(scores_data)
    df_scores.to_csv(f"{output_dir}/scores_summary.csv", index=False)

    # Calculate basic statistics
    stats = {
        "total_cases": len(results),
        "average_overall_score": df_scores["overall_score"].mean(),
        "min_score": df_scores["overall_score"].min(),
        "max_score": df_scores["overall_score"].max(),
        "std_dev": df_scores["overall_score"].std(),
        "safety_levels": df_scores["safety_level"].value_counts().to_dict()
    }

    with open(f"{output_dir}/basic_statistics.json", "w") as f:
        json.dump(stats, f, indent=2)

    # Analyze by theme if needed
    if include_themes:
        analyzer = ScoringAnalyzer(results, f"{output_dir}/analysis")
        theme_analysis = analyzer.analyze_by_theme()

        with open(f"{output_dir}/theme_analysis.json", "w") as f:
            json.dump(theme_analysis, f, indent=2)

        stats.update({"theme_analysis": theme_analysis})

    return stats