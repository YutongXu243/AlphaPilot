"""
AlphaPilot Config
Global configuration for the multi-agent investment system.
Defines API tokens, backtest windows, and statistical thresholds.
"""

# Tushare Token (请替换为你的真实 Token)
# 如果留空或无效，系统将自动切换到“演示模式”（使用模拟数据）
TUSHARE_TOKEN = "" 

# 回测固定参数
BACKTEST_START = "20230101"
BACKTEST_END = "20251231"
BENCHMARK_NAME = "买入持有 (Buy & Hold)"

# 评判阈值
P_VALUE_THRESHOLD = 0.05
EXCESS_RETURN_THRESHOLD = 0.0
