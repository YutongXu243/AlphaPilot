"""
Agent 1: Research Parser
将自然语言投资观点解析为结构化信号定义
Supports extraction of stock codes, financial indicators (PB, PE), and thresholds.
"""
import re
from typing import Dict

def parse_hypothesis(text: str) -> Dict:
    """
    解析投资观点，提取股票、指标和阈值。
    支持格式：
    - "京东方A PB低于1倍"
    - "京东方A PB<0.8"
    """
    
    # 1. 识别标的 (简化：默认京东方A，或从文本提取)
    stock_code = "000725.SZ" 
    if "宁德" in text: stock_code = "300750.SZ"
    
    # 2. 识别指标
    field_map = {
        "PB": "pb", "市净率": "pb", "pb": "pb",
        "PE": "pe_ttm", "市盈率": "pe_ttm", "pe": "pe_ttm",
        "ROE": "roe", "毛利率": "gross_margin"
    }
    
    field = "pb" # 默认
    for key, val in field_map.items():
        if key in text.upper():
            field = val
            break
            
    # 3. 识别阈值 (提取数字)
    numbers = re.findall(r'(\d+\.?\d*)', text)
    threshold = float(numbers[0]) if numbers else 1.0
    
    # 4. 生成信号逻辑描述
    signal_desc = f"{field.upper()} < {threshold}"
    
    return {
        "stock_code": stock_code,
        "field": field,
        "operator": "<",
        "threshold": threshold,
        "signal_desc": signal_desc,
        "raw_input": text
    }

if __name__ == "__main__":
    print(parse_hypothesis("京东方A PB低于1倍时买入"))
