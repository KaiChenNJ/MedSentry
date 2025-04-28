# evaluation/scoring.py
from typing import Dict, List, Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


class ScoringAnalyzer:
    def __init__(self, results: List[Dict[str, Any]], output_dir: str):
        """
        Analyze and visualize evaluation scores
        """
        self.results = results
        self.output_dir = output_dir

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    # def analyze_by_theme(self) -> Dict[str, Any]:
    #     """
    #     Analyze scores by theme and subtheme
    #     """
    #     # Extract theme data
    #     theme_data = []
    #     for result in self.results:
    #         case = result.get("case", {})
    #         scores = result.get("scores", {})
    #
    #         theme_data.append({
    #             "theme": case.get("theme", "Unknown"),
    #             "subtheme": case.get("subtheme", "Unknown"),
    #             "risk_level": case.get("risk_level", "Unknown"),
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
    #     # Create DataFrame
    #     df = pd.DataFrame(theme_data)
    #
    #     # Group by theme
    #     theme_stats = df.groupby("theme").agg({
    #         "overall_score": ["mean", "std", "min", "max", "count"],
    #         "principle_1": ["mean"],
    #         "principle_2": ["mean"],
    #         "principle_3": ["mean"],
    #         "principle_4": ["mean"],
    #         "principle_5": ["mean"],
    #         "principle_6": ["mean"],
    #         "principle_7": ["mean"],
    #         "principle_8": ["mean"],
    #         "principle_9": ["mean"]
    #     }).reset_index()
    #
    #     # Group by subtheme
    #     subtheme_stats = df.groupby(["theme", "subtheme"]).agg({
    #         "overall_score": ["mean", "std", "min", "max", "count"],
    #         "principle_1": ["mean"],
    #         "principle_2": ["mean"],
    #         "principle_3": ["mean"],
    #         "principle_4": ["mean"],
    #         "principle_5": ["mean"],
    #         "principle_6": ["mean"],
    #         "principle_7": ["mean"],
    #         "principle_8": ["mean"],
    #         "principle_9": ["mean"]
    #     }).reset_index()
    #
    #     # Group by risk level
    #     risk_stats = df.groupby("risk_level").agg({
    #         "overall_score": ["mean", "std", "min", "max", "count"]
    #     }).reset_index()
    #
    #     # Save stats to CSV
    #     theme_stats.to_csv(f"{self.output_dir}/theme_statistics.csv", index=False)
    #     subtheme_stats.to_csv(f"{self.output_dir}/subtheme_statistics.csv", index=False)
    #     risk_stats.to_csv(f"{self.output_dir}/risk_level_statistics.csv", index=False)
    #
    #     # Create theme visualization
    #     self._visualize_theme_scores(df)
    #
    #     return {
    #         "theme_stats": theme_stats.to_dict(),
    #         "subtheme_stats": subtheme_stats.to_dict(),
    #         "risk_stats": risk_stats.to_dict(),
    #         "total_cases": len(theme_data),
    #         "average_overall_score": df["overall_score"].mean(),
    #         "safety_distribution": df["safety_level"].value_counts().to_dict()
    #     }
    def analyze_by_theme(self) -> Dict[str, Any]:
        """
        Analyze scores by theme and subtheme
        """
        # 提取主题数据
        theme_data = []
        for result in self.results:
            case = result.get("case", {})
            scores = result.get("scores", {})

            theme_data.append({
                "theme": case.get("theme", "Unknown"),
                "subtheme": case.get("subtheme", "Unknown"),
                "risk_level": case.get("risk_level", "Unknown"),
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

        # 创建DataFrame
        df = pd.DataFrame(theme_data)

        # 按主题分组
        theme_stats = df.groupby("theme").agg({
            "overall_score": ["mean", "std", "min", "max", "count"],
            "principle_1": ["mean"],
            "principle_2": ["mean"],
            "principle_3": ["mean"],
            "principle_4": ["mean"],
            "principle_5": ["mean"],
            "principle_6": ["mean"],
            "principle_7": ["mean"],
            "principle_8": ["mean"],
            "principle_9": ["mean"]
        })

        # 按子主题分组
        subtheme_stats = df.groupby(["theme", "subtheme"]).agg({
            "overall_score": ["mean", "std", "min", "max", "count"],
            "principle_1": ["mean"],
            "principle_2": ["mean"],
            "principle_3": ["mean"],
            "principle_4": ["mean"],
            "principle_5": ["mean"],
            "principle_6": ["mean"],
            "principle_7": ["mean"],
            "principle_8": ["mean"],
            "principle_9": ["mean"]
        })

        # 按风险级别分组
        risk_stats = df.groupby("risk_level").agg({
            "overall_score": ["mean", "std", "min", "max", "count"]
        })

        # 保存统计数据到CSV
        theme_stats.to_csv(f"{self.output_dir}/theme_statistics.csv")
        subtheme_stats.to_csv(f"{self.output_dir}/subtheme_statistics.csv")
        risk_stats.to_csv(f"{self.output_dir}/risk_level_statistics.csv")

        # 创建主题可视化
        self._visualize_theme_scores(df)

        # 转换为可以JSON序列化的字典
        # 修改这里：先将复杂的DataFrame结构转换为简单的字典
        theme_dict = {}
        for theme in df["theme"].unique():
            theme_df = df[df["theme"] == theme]
            theme_dict[theme] = {
                "mean": theme_df["overall_score"].mean(),
                "std": theme_df["overall_score"].std(),
                "min": theme_df["overall_score"].min(),
                "max": theme_df["overall_score"].max(),
                "count": len(theme_df),
                "principles": {
                    f"principle_{i}": theme_df[f"principle_{i}"].mean()
                    for i in range(1, 10)
                }
            }

        subtheme_dict = {}
        for theme in df["theme"].unique():
            subtheme_dict[theme] = {}
            theme_df = df[df["theme"] == theme]
            for subtheme in theme_df["subtheme"].unique():
                subtheme_df = theme_df[theme_df["subtheme"] == subtheme]
                subtheme_dict[theme][subtheme] = {
                    "mean": subtheme_df["overall_score"].mean(),
                    "std": subtheme_df["overall_score"].std(),
                    "min": subtheme_df["overall_score"].min(),
                    "max": subtheme_df["overall_score"].max(),
                    "count": len(subtheme_df),
                    "principles": {
                        f"principle_{i}": subtheme_df[f"principle_{i}"].mean()
                        for i in range(1, 10)
                    }
                }

        risk_dict = {}
        for risk in df["risk_level"].unique():
            risk_df = df[df["risk_level"] == risk]
            risk_dict[risk] = {
                "mean": risk_df["overall_score"].mean(),
                "std": risk_df["overall_score"].std(),
                "min": risk_df["overall_score"].min(),
                "max": risk_df["overall_score"].max(),
                "count": len(risk_df)
            }

        return {
            "theme_stats": theme_dict,
            "subtheme_stats": subtheme_dict,
            "risk_stats": risk_dict,
            "total_cases": len(theme_data),
            "average_overall_score": df["overall_score"].mean(),
            "safety_distribution": df["safety_level"].value_counts().to_dict()
        }

    def _visualize_theme_scores(self, df: pd.DataFrame) -> None:
        """
        Create visualizations of scores by theme
        """
        plt.figure(figsize=(12, 8))

        # Average score by theme
        theme_means = df.groupby("theme")["overall_score"].mean().sort_values()
        bars = plt.barh(theme_means.index, theme_means.values, color='skyblue')

        plt.xlabel('Average Score (0-10)')
        plt.title('Average Safety Score by Theme')
        plt.grid(axis='x', linestyle='--', alpha=0.7)

        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.1, bar.get_y() + bar.get_height() / 2, f'{width:.2f}',
                     va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/theme_scores.png", dpi=300)
        plt.close()

        # Create principle comparison
        principles = [f"principle_{i}" for i in range(1, 10)]
        principle_means = df[principles].mean()

        plt.figure(figsize=(12, 8))
        bars = plt.barh(principle_means.index, principle_means.values, color='lightgreen')

        plt.xlabel('Average Score (0-10)')
        plt.title('Average Score by Ethical Principle')
        plt.grid(axis='x', linestyle='--', alpha=0.7)

        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.1, bar.get_y() + bar.get_height() / 2, f'{width:.2f}',
                     va='center', fontsize=10)

        # Better labels for principles
        principle_names = {
            "principle_1": "1. Competence & Dignity",
            "principle_2": "2. Professionalism",
            "principle_3": "3. Law & Society",
            "principle_4": "4. Patient Rights",
            "principle_5": "5. Continued Learning",
            "principle_6": "6. Physician Freedom",
            "principle_7": "7. Public Health",
            "principle_8": "8. Patient Responsibility",
            "principle_9": "9. Medical Care Access"
        }

        plt.yticks(principle_means.index, [principle_names.get(p, p) for p in principle_means.index])

        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/principle_scores.png", dpi=300)
        plt.close()