# utils/data_processor.py
from typing import Dict, List, Any
import json
import os
import pandas as pd
from evaluation.scoring import ScoringAnalyzer


# def process_results(results: List[Dict[str, Any]], output_dir: str, include_themes: bool = True) -> Dict[str, Any]:
#     """
#     Process and analyze results
#     """
#     # Ensure output directory exists
#     os.makedirs(output_dir, exist_ok=True)
#
#     # Save complete results
#     with open(f"{output_dir}/complete_results.json", "w") as f:
#         json.dump(results, f, indent=2)
#
#     # Extract scores
#     scores_data = []
#     for result in results:
#         case = result.get("case", {})
#         scores = result.get("scores", {})
#
#         scores_data.append({
#             "case_id": case.get("case_id", ""),
#             "theme": case.get("theme", ""),
#             "subtheme": case.get("subtheme", ""),
#             "query": case.get("query", ""),
#             "risk_level": case.get("risk_level", ""),
#             "overall_score": scores.get("overall", 0),
#             "principle_1": scores.get("principle_1", 0),
#             "principle_2": scores.get("principle_2", 0),
#             "principle_3": scores.get("principle_3", 0),
#             "principle_4": scores.get("principle_4", 0),
#             "principle_5": scores.get("principle_5", 0),
#             "principle_6": scores.get("principle_6", 0),
#             "principle_7": scores.get("principle_7", 0),
#             "principle_8": scores.get("principle_8", 0),
#             "principle_9": scores.get("principle_9", 0),
#             "safety_level": scores.get("safety_level", "Unknown")
#         })
#
#     # Create scores DataFrame
#     df_scores = pd.DataFrame(scores_data)
#     df_scores.to_csv(f"{output_dir}/scores_summary.csv", index=False)
#
#     # Calculate basic statistics
#     stats = {
#         "total_cases": len(results),
#         "average_overall_score": df_scores["overall_score"].mean(),
#         "min_score": df_scores["overall_score"].min(),
#         "max_score": df_scores["overall_score"].max(),
#         "std_dev": df_scores["overall_score"].std(),
#         "safety_levels": df_scores["safety_level"].value_counts().to_dict()
#     }
#
#     with open(f"{output_dir}/basic_statistics.json", "w") as f:
#         json.dump(stats, f, indent=2)
#
#     # Analyze by theme if needed
#     if include_themes:
#         analyzer = ScoringAnalyzer(results, f"{output_dir}/analysis")
#         theme_analysis = analyzer.analyze_by_theme()
#
#         with open(f"{output_dir}/theme_analysis.json", "w") as f:
#             json.dump(theme_analysis, f, indent=2)
#
#         stats.update({"theme_analysis": theme_analysis})
#
#     return stats

# utils/data_processor.py 修改部分

from typing import Dict, List, Any
import json
import os
import pandas as pd
import numpy as np
from evaluation.scoring import ScoringAnalyzer

# def convert_numpy_types(obj):
#     """
#     Recursively convert NumPy types to standard Python types for JSON serialization
#     """
#     if isinstance(obj, dict):
#         return {key: convert_numpy_types(value) for key, value in obj.items()}
#     elif isinstance(obj, list):
#         return [convert_numpy_types(item) for item in obj]
#     elif isinstance(obj, tuple):
#         return tuple(convert_numpy_types(item) for item in obj)
#     elif isinstance(obj, np.integer):
#         return int(obj)
#     elif isinstance(obj, np.floating):
#         return float(obj)
#     elif isinstance(obj, np.ndarray):
#         return convert_numpy_types(obj.tolist())
#     elif isinstance(obj, pd.DataFrame):
#         return convert_numpy_types(obj.to_dict())
#     elif isinstance(obj, pd.Series):
#         return convert_numpy_types(obj.to_dict())
#     else:
#         return obj
def convert_numpy_types(obj):
    """
    Recursively convert NumPy types to standard Python types for JSON serialization
    """
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_numpy_types(item) for item in obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return convert_numpy_types(obj.tolist())
    elif isinstance(obj, pd.DataFrame):
        return convert_numpy_types(obj.to_dict())
    elif isinstance(obj, pd.Series):
        return convert_numpy_types(obj.to_dict())
    elif isinstance(obj, pd.Index):
        return convert_numpy_types(list(obj))
    else:
        return obj
def process_results(results: List[Dict[str, Any]], output_dir: str, include_themes: bool = True) -> Dict[str, Any]:
    """
    Process and analyze results
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save complete results
    with open(f"{output_dir}/complete_results.json", "w") as f:
        json.dump(convert_numpy_types(results), f, indent=2)

    # Extract scores for full and truncated evaluations
    full_scores_data = []
    truncated_scores_data = []

    for result in results:
        case = result.get("case", {})
        evaluations = result.get("evaluation", {})

        full_evaluation = evaluations.get("full", {})
        truncated_evaluation = evaluations.get("truncated", {})

        full_scores = full_evaluation.get("scores", {}) if full_evaluation else {}
        truncated_scores = truncated_evaluation.get("scores", {}) if truncated_evaluation else {}

        # Process full evaluation data
        if full_scores:
            full_scores_data.append({
                "case_id": case.get("case_id", ""),
                "theme": case.get("theme", ""),
                "subtheme": case.get("subtheme", ""),
                "query": case.get("query", ""),
                "risk_level": case.get("risk_level", ""),
                "overall_score": full_scores.get("overall", 0),
                "principle_1": full_scores.get("principle_1", 0),
                "principle_2": full_scores.get("principle_2", 0),
                "principle_3": full_scores.get("principle_3", 0),
                "principle_4": full_scores.get("principle_4", 0),
                "principle_5": full_scores.get("principle_5", 0),
                "principle_6": full_scores.get("principle_6", 0),
                "principle_7": full_scores.get("principle_7", 0),
                "principle_8": full_scores.get("principle_8", 0),
                "principle_9": full_scores.get("principle_9", 0),
                "safety_level": full_scores.get("safety_level", "Unknown"),
                "evaluation_type": "full"
            })

        # Process truncated evaluation data
        if truncated_scores:
            truncated_scores_data.append({
                "case_id": case.get("case_id", ""),
                "theme": case.get("theme", ""),
                "subtheme": case.get("subtheme", ""),
                "query": case.get("query", ""),
                "risk_level": case.get("risk_level", ""),
                "overall_score": truncated_scores.get("overall", 0),
                "principle_1": truncated_scores.get("principle_1", 0),
                "principle_2": truncated_scores.get("principle_2", 0),
                "principle_3": truncated_scores.get("principle_3", 0),
                "principle_4": truncated_scores.get("principle_4", 0),
                "principle_5": truncated_scores.get("principle_5", 0),
                "principle_6": truncated_scores.get("principle_6", 0),
                "principle_7": truncated_scores.get("principle_7", 0),
                "principle_8": truncated_scores.get("principle_8", 0),
                "principle_9": truncated_scores.get("principle_9", 0),
                "safety_level": truncated_scores.get("safety_level", "Unknown"),
                "evaluation_type": "truncated"
            })

    # Combine all score data for comparison
    all_scores_data = full_scores_data + truncated_scores_data

    # Create separate DataFrames
    if full_scores_data:
        df_full_scores = pd.DataFrame(full_scores_data)
        df_full_scores.to_csv(f"{output_dir}/full_scores_summary.csv", index=False)

    if truncated_scores_data:
        df_truncated_scores = pd.DataFrame(truncated_scores_data)
        df_truncated_scores.to_csv(f"{output_dir}/truncated_scores_summary.csv", index=False)

    # Create DataFrame with all scores (for comparison)
    if all_scores_data:
        df_all_scores = pd.DataFrame(all_scores_data)
        df_all_scores.to_csv(f"{output_dir}/all_scores_summary.csv", index=False)

    # Calculate basic statistics
    stats = {
        "total_cases": len(results),
    }

    if full_scores_data:
        df_full = pd.DataFrame(full_scores_data)
        stats["full"] = {
            "average_overall_score": df_full["overall_score"].mean(),
            "min_score": df_full["overall_score"].min(),
            "max_score": df_full["overall_score"].max(),
            "std_dev": df_full["overall_score"].std(),
            "safety_levels": df_full["safety_level"].value_counts().to_dict()
        }

    if truncated_scores_data:
        df_truncated = pd.DataFrame(truncated_scores_data)
        stats["truncated"] = {
            "average_overall_score": df_truncated["overall_score"].mean(),
            "min_score": df_truncated["overall_score"].min(),
            "max_score": df_truncated["overall_score"].max(),
            "std_dev": df_truncated["overall_score"].std(),
            "safety_levels": df_truncated["safety_level"].value_counts().to_dict()
        }

    # Calculate differences if both evaluation types are present
    if full_scores_data and truncated_scores_data:
        # Create comparison DataFrame to analyze differences
        comparison_data = []
        for i, result in enumerate(results):
            case = result.get("case", {})
            evaluations = result.get("evaluation", {})

            full_scores = evaluations.get("full", {}).get("scores", {}) if "full" in evaluations else {}
            truncated_scores = evaluations.get("truncated", {}).get("scores", {}) if "truncated" in evaluations else {}

            if full_scores and truncated_scores:
                comparison_data.append({
                    "case_id": case.get("case_id", i),
                    "theme": case.get("theme", ""),
                    "subtheme": case.get("subtheme", ""),
                    "full_score": full_scores.get("overall", 0),
                    "truncated_score": truncated_scores.get("overall", 0),
                    "score_difference": full_scores.get("overall", 0) - truncated_scores.get("overall", 0),
                    "full_safety": full_scores.get("safety_level", "Unknown"),
                    "truncated_safety": truncated_scores.get("safety_level", "Unknown")
                })

        if comparison_data:
            df_comparison = pd.DataFrame(comparison_data)
            df_comparison.to_csv(f"{output_dir}/comparison_summary.csv", index=False)

            # Add difference statistics to overall stats
            stats["comparison"] = {
                "average_difference": df_comparison["score_difference"].mean(),
                "max_difference": df_comparison["score_difference"].max(),
                "min_difference": df_comparison["score_difference"].min(),
                "std_dev_difference": df_comparison["score_difference"].std(),
                "cases_with_significant_difference": len(df_comparison[df_comparison["score_difference"].abs() >= 1])
            }

    with open(f"{output_dir}/basic_statistics.json", "w") as f:
        json.dump(convert_numpy_types(stats), f, indent=2)

    # Analyze by theme if requested
    theme_analysis = {}
    if include_themes and all_scores_data:
        analyzer = ScoringAnalyzer(results, f"{output_dir}/analysis")
        theme_analysis = analyzer.analyze_by_theme()

        with open(f"{output_dir}/theme_analysis.json", "w") as f:
            json.dump(convert_numpy_types(theme_analysis), f, indent=2)

        stats.update({"theme_analysis": theme_analysis})

    return convert_numpy_types(stats)