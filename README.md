# 3M-Bench
This is the official repository for the paper *3M-Bench: Measurable Evaluation and Improvement of Multi-Agent Safety in Medical Domain*.

## :rocket: Quick Start
```
# Run script for SharedPool Structure
python run_shared_pool.py           

# Run script for Layer Structure
python run_layer.py                 

# Run script for Centralized Structure
python run_centralized.py

# Run script for Decentralized Structure
python run_decentralized.py        
```
The results are saved by default under the ```results```folder.


```
medical_llm_agents/
│
├── config/
│   ├── models_config.yaml       # 主要LLM模型的配置
│   └── evaluator_config.yaml    # GPT-4o评估器的配置
│
├── evaluation/
│   ├── evaluator.py             # GPT-4o评估器实现
│   └── scoring.py               # 基于医疗伦理原则的评分实现
│
├── utils/
│   ├── llm_interface.py         # LLM API接口封装
│   ├── data_processor.py        # 数据处理和结果统计
│   └── shared_memory.py         # 共享信息池实现（被shared_pool_voting.py调用）
│
├── data/
│   └── MAS_Med_safe_bench.csv   # 测试数据集
```
