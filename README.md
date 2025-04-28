```
medical_llm_agents/
│
├── config/
│   ├── models_config.yaml       # 主要LLM模型的配置
│   └── evaluator_config.yaml    # GPT-4o评估器的配置
│
├── structures/
│   ├── shared_pool_voting.py    # 共享信息池+无leader投票结构
│   ├── layer_structure.py       # Layer型结构
│   ├── centralized.py           # 中心化结构
│   └── decentralized.py         # 去中心化结构
│
├── agents/
│   ├── base_agent.py            # 基础智能体类
│   ├── specialist_agent.py      # 专科医生智能体
│   └── dark_agent.py            # 黑暗人格智能体
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
│
├── results/                     # 结果保存目录
│
├── run_shared_pool.py           # 运行共享信息池结构的脚本
├── run_layer.py                 # 运行Layer型结构的脚本
├── run_centralized.py           # 运行中心化结构的脚本
├── run_decentralized.py         # 运行去中心化结构的脚本
├── requirements.txt             # 项目依赖
└── README.md                    # 项目说明
```

### 运行以下四个结构单独实现

├── run_shared_pool.py           # 运行共享信息池结构的脚本

├── run_layer.py                 # 运行Layer型结构的脚本

├── run_centralized.py           # 运行中心化结构的脚本

├── run_decentralized.py         # 运行去中心化结构的脚本

#### 现在存在的问题
1.数据集主题和子主题是中文导致图片显示不正常；

2.没有加入防御方法；