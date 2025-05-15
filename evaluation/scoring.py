
# evaluation/scoring.py
from typing import Dict, List, Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns


class ScoringAnalyzer:
    def __init__(self, results: List[Dict[str, Any]], output_dir: str):
        """
        Analyze and visualize evaluation scores
        """
        self.results = results
        self.output_dir = output_dir

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def analyze_by_theme(self) -> Dict[str, Any]:
        """
        Analyze scores by theme and subtheme
        """
        theme_data = []
        for result in self.results:
            case = result.get("case", {})
            scores = result.get("scores", {})

            # 检查是否有评估类型区分
            if "full" in scores and "truncated" in scores:
                # 处理完整评估
                full_scores = scores.get("full", {})
                if full_scores:
                    theme_data.append({
                        "theme": case.get("theme", "Unknown"),
                        "subtheme": case.get("subtheme", "Unknown"),
                        "risk_level": case.get("risk_level", "Unknown"),
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

                # 处理截断评估
                truncated_scores = scores.get("truncated", {})
                if truncated_scores:
                    theme_data.append({
                        "theme": case.get("theme", "Unknown"),
                        "subtheme": case.get("subtheme", "Unknown"),
                        "risk_level": case.get("risk_level", "Unknown"),
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
            else:
                # 兼容旧的数据结构（无评估类型区分）
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

        # 添加调试信息
        print(f"Theme data count: {len(theme_data)}")

        # 创建DataFrame
        df = pd.DataFrame(theme_data)

        # 检查数据框是否为空
        if df.empty:
            print("WARNING: Empty DataFrame - no data to visualize")
            return {
                "total_cases": 0,
                "average_overall_score": 0,
                "error": "No data available for analysis"
            }

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
                "mean": float(theme_df["overall_score"].mean()),
                "std": float(theme_df["overall_score"].std()),
                "min": float(theme_df["overall_score"].min()),
                "max": float(theme_df["overall_score"].max()),
                "count": int(len(theme_df)),
                "principles": {
                    f"principle_{i}": float(theme_df[f"principle_{i}"].mean())
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
                    "mean": float(subtheme_df["overall_score"].mean()),
                    "std": float(subtheme_df["overall_score"].std()),
                    "min": float(subtheme_df["overall_score"].min()),
                    "max": float(subtheme_df["overall_score"].max()),
                    "count": int(len(subtheme_df)),
                    "principles": {
                        f"principle_{i}": float(subtheme_df[f"principle_{i}"].mean())
                        for i in range(1, 10)
                    }
                }

        risk_dict = {}
        for risk in df["risk_level"].unique():
            risk_df = df[df["risk_level"] == risk]
            risk_dict[risk] = {
                "mean": float(risk_df["overall_score"].mean()),
                "std": float(risk_df["overall_score"].std()),
                "min": float(risk_df["overall_score"].min()),
                "max": float(risk_df["overall_score"].max()),
                "count": int(len(risk_df))
            }

        return {
            "theme_stats": theme_dict,
            "subtheme_stats": subtheme_dict,
            "risk_stats": risk_dict,
            "total_cases": len(theme_data),
            "average_overall_score": float(df["overall_score"].mean()),
            "safety_distribution": {k: int(v) for k, v in df["safety_level"].value_counts().to_dict().items()}
        }

    def _visualize_theme_scores(self, df: pd.DataFrame) -> None:
        """
        Create visualizations of scores by theme
        """
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

        # 添加调试信息
        print(f"Visualization data shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Theme values: {df['theme'].unique().tolist()}")

        if 'evaluation_type' in df.columns:
            print(f"Evaluation types: {df['evaluation_type'].unique().tolist()}")
            self._visualize_by_evaluation_type(df)
        else:
            self._visualize_single_evaluation(df)

    def _visualize_single_evaluation(self, df: pd.DataFrame) -> None:
        """创建单一评估类型的可视化"""
        try:
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
        except Exception as e:
            print(f"ERROR in single evaluation visualization: {e}")
            import traceback
            traceback.print_exc()

    def _visualize_by_evaluation_type(self, df: pd.DataFrame) -> None:
        """创建按评估类型分组的可视化"""
        # 确保有足够的数据可用
        if df.empty or 'evaluation_type' not in df.columns:
            print("WARNING: Not enough data for evaluation type visualization")
            return

        # 检查每种评估类型是否有足够数据
        type_counts = df['evaluation_type'].value_counts()
        print(f"Evaluation type counts: {type_counts.to_dict()}")

        if type_counts.empty or type_counts.max() < 1:
            print("WARNING: Insufficient data for each evaluation type")
            return

        try:

            theme_scores = df.groupby(["theme", "evaluation_type"])["overall_score"].mean().unstack()

            # 确保有数据可用
            if theme_scores.empty:
                print("WARNING: No theme scores data available")
                return

            # 排序主题
            theme_scores = theme_scores.sort_values(
                by="full" if "full" in theme_scores.columns else theme_scores.columns[0])

            # 设置X轴
            x = np.arange(len(theme_scores.index))
            width = 0.35

            # 创建条形图
            fig, ax = plt.subplots(figsize=(14, 10))

            if "full" in theme_scores.columns:
                rects1 = ax.barh(x - width / 2, theme_scores["full"], width, label='Full Evaluation', color='skyblue')

            if "truncated" in theme_scores.columns:
                rects2 = ax.barh(x + width / 2, theme_scores["truncated"], width, label='Truncated Evaluation',
                                 color='salmon')

            # 添加标签和图例
            ax.set_xlabel('Average Score (0-10)')
            ax.set_title('Average Safety Score by Theme and Evaluation Type')
            ax.set_yticks(x)
            ax.set_yticklabels(theme_scores.index)
            ax.legend()
            ax.grid(axis='x', linestyle='--', alpha=0.7)

            # 添加数值标签
            if "full" in theme_scores.columns:
                for bar in rects1:
                    width = bar.get_width()
                    ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2, f'{width:.2f}',
                            va='center', fontsize=9)

            if "truncated" in theme_scores.columns:
                for bar in rects2:
                    width = bar.get_width()
                    ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2, f'{width:.2f}',
                            va='center', fontsize=9)

            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/theme_scores_comparison.png", dpi=300)
            plt.close()

            # 创建原则分数比较 - 修改为垂直分组条形图
            principles = [f"principle_{i}" for i in range(1, 10)]

            # 更好的原则标签
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

            # 按评估类型和原则分组计算平均分
            principles_df = pd.DataFrame()
            for eval_type in df["evaluation_type"].unique():
                eval_df = df[df["evaluation_type"] == eval_type]
                principles_df[eval_type] = eval_df[principles].mean()

            # 创建分组条形图
            fig, ax = plt.subplots(figsize=(12, 8))

            # 定义原则名称和位置
            labels = [principle_names.get(p, p) for p in principles]
            x = np.arange(len(labels))
            width = 0.35  # 条形宽度

            eval_types = principles_df.columns
            colors = ['#5DA5DA', '#FAA43A', '#60BD68', '#F17CB0']

            for i, eval_type in enumerate(eval_types):
                offset = width * i - width * (len(eval_types) - 1) / 2
                rects = ax.bar(x + offset, principles_df[eval_type], width,
                               label=f'{eval_type.capitalize()} Evaluation',
                               color=colors[i % len(colors)])

                for rect in rects:
                    height = rect.get_height()
                    ax.annotate(f'{height:.1f}',
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(0, 3),  #
                                textcoords="offset points",
                                ha='center', va='bottom',
                                fontsize=8)

            ax.set_ylabel('Average Score (0-10)')
            ax.set_title('Average Score by Ethical Principle and Evaluation Type')
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45, ha='right')
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=len(eval_types))
            ax.set_ylim(0, 10.5)  # 设置Y轴范围，留出标签空间
            ax.grid(axis='y', linestyle='--', alpha=0.7)

            # 确保布局合适
            fig.tight_layout()
            plt.savefig(f"{self.output_dir}/principle_scores_comparison.png", dpi=300, bbox_inches='tight')
            plt.close()

            # 创建差异分布图
            if len(eval_types) >= 2 and "full" in eval_types and "truncated" in eval_types:
                # 计算每个案例的差异
                case_diffs = []
                for theme in df["theme"].unique():
                    theme_df = df[df["theme"] == theme]
                    full_scores = theme_df[theme_df["evaluation_type"] == "full"]["overall_score"]
                    truncated_scores = theme_df[theme_df["evaluation_type"] == "truncated"]["overall_score"]

                    # 需要确保索引匹配
                    if len(full_scores) > 0 and len(truncated_scores) > 0:
                        # 重置索引以便配对计算
                        full_scores = full_scores.reset_index(drop=True)
                        truncated_scores = truncated_scores.reset_index(drop=True)

                        # 确保长度相同
                        min_len = min(len(full_scores), len(truncated_scores))
                        diffs = full_scores.iloc[:min_len].values - truncated_scores.iloc[:min_len].values

                        for diff in diffs:
                            case_diffs.append({"theme": theme, "difference": diff})

                if case_diffs:
                    diff_df = pd.DataFrame(case_diffs)

                    # 创建差异箱线图（按主题）
                    plt.figure(figsize=(14, 10))
                    sns.boxplot(x="difference", y="theme", data=diff_df, orient="h")
                    plt.axvline(x=0, color='r', linestyle='--')
                    plt.title('Difference Between Full and Truncated Evaluation (Full - Truncated)')
                    plt.xlabel('Score Difference')
                    plt.grid(axis='x', linestyle='--', alpha=0.7)
                    plt.tight_layout()
                    plt.savefig(f"{self.output_dir}/score_difference_by_theme.png", dpi=300)
                    plt.close()

                    # 创建总体差异直方图
                    plt.figure(figsize=(12, 8))
                    sns.histplot(diff_df["difference"], kde=True)
                    plt.axvline(x=0, color='r', linestyle='--')
                    plt.title('Distribution of Score Differences (Full - Truncated)')
                    plt.xlabel('Score Difference')
                    plt.ylabel('Count')
                    plt.grid(axis='x', linestyle='--', alpha=0.7)
                    plt.tight_layout()
                    plt.savefig(f"{self.output_dir}/score_difference_distribution.png", dpi=300)
                    plt.close()
        except Exception as e:
            print(f"ERROR in evaluation type visualization: {e}")
            import traceback
            traceback.print_exc()

