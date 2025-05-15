# run_shared_pool.py
import argparse
import os
import yaml
import json
import pandas as pd
import time
from structures.shared_pool_voting import SharedPoolVotingSystem
from evaluation.evaluator import Evaluator
from utils.data_processor import process_results


def main():
    """
    Run the shared pool voting system
    """
    parser = argparse.ArgumentParser(description="Run shared pool voting system")
    parser.add_argument("--use_dark_agent", action="store_true", default=False, help="Include a dark agent in the team")
    parser.add_argument("--model", type=str, default="deepseek", help="Model to use (from config)")
    parser.add_argument("--output_dir", type=str, default="results/shared_pool", help="Output directory")
    parser.add_argument("--data_path", type=str, default="data/3M_Bench_sub.csv", help="Path to dataset")
    parser.add_argument("--num_cases", type=int, default=1, help="Number of cases to process (-1 for all)")
    parser.add_argument("--num_agents", type=int, default=5, help="Number of agents in the team")
    parser.add_argument("--query_source", type=str, default="gpt4o", choices=["gpt4o", "claude", "both"],
                        help="Source of queries to use (gpt4o, claude, or both)")
    parser.add_argument("--evaluation_mode", type=str, default="both",
                        choices=["full", "truncated", "both"],
                        help="Evaluation mode: full, truncated, or both")
    args = parser.parse_args()
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Load configurations
    with open("config/models_config.yaml", "r") as f:
        models_config = yaml.safe_load(f)["models"]

    with open("config/evaluator_config.yaml", "r") as f:
        evaluator_config = yaml.safe_load(f)["evaluator"]

    # Load dataset
    dataset = pd.read_csv(args.data_path)
    if args.num_cases > 0:
        dataset = dataset.head(args.num_cases)

    # Initialize system
    system = SharedPoolVotingSystem(
        num_agents=args.num_agents,
        use_dark_agent=args.use_dark_agent,
        models_config=models_config,
        model_name=args.model
    )

    # Initialize evaluator
    evaluator = Evaluator(evaluator_config)

    # Store results
    all_results = []

    # Track total token usage and time
    total_tokens_used = 0
    total_start_time = time.time()

    # Token usage by case
    token_usage_by_case = []

    # Process each case
    for idx, row in dataset.iterrows():
        case_number = idx + 1
        print(f"\n{'*' * 100}")
        print(f"Processing case {case_number}/{len(dataset)}: {row.get('Topic', 'Unknown theme')}")
        print(f"{'*' * 100}")

        # Run discussion
        try:
            case_start_time = time.time()

            print(f"\n[Case {case_number}] Starting discussion...")
            result = system.run_discussion(row.to_dict(), query_source=args.query_source)

            print(f"\n[Case {case_number}] Discussion completed. Starting evaluation...")
            evaluation = evaluator.evaluate(result, truncate_mode=args.evaluation_mode)

            scores = {}
            if "full" in evaluation:
                scores["full"] = evaluation["full"]["scores"]
            if "truncated" in evaluation:
                scores["truncated"] = evaluation["truncated"]["scores"]

            result["evaluation"] = evaluation
            result["scores"] = scores

            # Calculate token usage for this case
            agent_tokens = 0
            for agent in system.agents:
                agent_tokens += sum(agent.get_token_usage().values())

            evaluator_tokens = sum(evaluator.get_token_usage().values())
            case_tokens = agent_tokens + evaluator_tokens

            # Track time for this case
            case_end_time = time.time()
            case_duration = case_end_time - case_start_time

            # Add token and time info to result
            result["performance"] = {
                "agent_tokens": agent_tokens,
                "evaluator_tokens": evaluator_tokens,
                "total_tokens": case_tokens,
                "duration_seconds": case_duration
            }

            # Update totals
            total_tokens_used += case_tokens

            # Add to token usage by case
            token_usage_by_case.append({
                "case_number": case_number,
                "theme": row.get('Topic', 'Unknown'),
                "subtheme": row.get('Subtopic', 'Unknown'),
                "risk_level": row.get('（low/medium/high）', 'Unknown'),
                "agent_tokens": agent_tokens,
                "evaluator_tokens": evaluator_tokens,
                "total_tokens": case_tokens,
                "duration_seconds": case_duration
            })

            all_results.append(result)

            # Save individual result
            with open(f"{args.output_dir}/case_{case_number}.json", "w") as f:
                json.dump(result, f, indent=2)

            print(f"\n[Case {case_number}] Evaluation complete")
            if "full" in scores:
                print(f"Full evaluation score: {scores['full'].get('overall', 'N/A')}")
            if "truncated" in scores:
                print(f"Truncated evaluation score: {scores['truncated'].get('overall', 'N/A')}")
            if "full" in scores and "truncated" in scores:
                diff = scores["full"].get("overall", 0) - scores["truncated"].get("overall", 0)
                print(f"Score difference (Full - Truncated): {diff:.2f}")

            print(f"\n[Case {case_number}] Completed in {case_duration:.2f} seconds")
            print(f"Token usage: {case_tokens} tokens")

        except Exception as e:
            print(f"Error processing case {case_number}: {e}")
            continue

    # Calculate total time
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time

    # Save token usage by case
    with open(f"{args.output_dir}/token_usage_by_case.json", "w") as f:
        json.dump(token_usage_by_case, f, indent=2)

    # Create a CSV for token usage
    token_df = pd.DataFrame(token_usage_by_case)
    token_df.to_csv(f"{args.output_dir}/token_usage_by_case.csv", index=False)

    # Process and save aggregate results
    summary = process_results(all_results, args.output_dir)

    # Add performance metrics to summary
    performance_summary = {
        "total_tokens_used": total_tokens_used,
        "total_duration_seconds": total_duration,
        "average_tokens_per_case": total_tokens_used / len(all_results) if all_results else 0,
        "average_duration_per_case": total_duration / len(all_results) if all_results else 0,
    }

    with open(f"{args.output_dir}/performance_summary.json", "w") as f:
        json.dump(performance_summary, f, indent=2)

    # Print summary
    print("\n" + "=" * 50)
    print("EVALUATION COMPLETE!")
    print("=" * 50)
    print(f"Total cases processed: {len(all_results)}")
    print(f"Total time: {total_duration:.2f} seconds")
    print(f"Total tokens used: {total_tokens_used}")
    print(f"Average tokens per case: {performance_summary['average_tokens_per_case']:.2f}")
    print(f"Average time per case: {performance_summary['average_duration_per_case']:.2f} seconds")

    if "full" in summary:
        print(f"Average full evaluation score: {summary.get('full', {}).get('average_overall_score', 'N/A')}")
    if "truncated" in summary:
        print(f"Average truncated evaluation score: {summary.get('truncated', {}).get('average_overall_score', 'N/A')}")
    if "comparison" in summary:
        print(f"Average score difference: {summary.get('comparison', {}).get('average_difference', 'N/A')}")

    print(f"Results saved to: {args.output_dir}")
    print("=" * 50)


if __name__ == "__main__":
    main()