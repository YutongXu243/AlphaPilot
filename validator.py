"""
Agent 2: Quant Validator
执行回测、统计检验并给出结论
Uses scipy for paired t-tests to ensure statistical significance of Alpha.
"""
import pandas as pd
import numpy as np
from scipy import stats
import tushare as ts
from config import TUSHARE_TOKEN, BACKTEST_START, BACKTEST_END
from rich.console import Console

console = Console()

class MockDataError(Exception):
    pass

class QuantValidator:
    def __init__(self):
        self.is_mock = False
        if not TUSHARE_TOKEN:
            self.is_mock = True
            console.print("[yellow]⚠️ 未检测到 Tushare Token，切换至演示模式（模拟数据）[/yellow]")
        else:
            try:
                ts.set_token(TUSHARE_TOKEN)
                self.pro = ts.pro_api()
            except:
                self.is_mock = True

    def _get_mock_data(self, field: str, threshold: float = 1.0) -> pd.DataFrame:
        """生成用于演示的模拟数据 (Optimized for Demo Storyline)
        
        故事线设计：
        - PB < 1.0 时：策略收益低于基准（Excess Return < 0）→ 触发 Advisor 建议
        - PB < 0.8 时：策略收益显著高于基准（Excess Return > 0, p < 0.05）→ 验证成功
        
        关键设计：
        - 使用自相关PB序列，确保信号与alpha对齐
        - PB < 0.8 区间注入强正Alpha
        - 0.8 <= PB < 1.0 区间注入负Alpha
        """
        dates = pd.date_range(start="2023-01-01", end="2025-12-31", freq='D')
        np.random.seed(42) 
        
        # 1. 构造基准价格 (Benchmark)
        benchmark_returns = np.full(len(dates), 0.0005)  # 每日固定 +0.05%
        prices = 5.0 * np.cumprod(1 + benchmark_returns)
        
        # 2. 构造自相关PB序列（减少信号错位）
        pb_values = np.zeros(len(dates))
        pb_values[0] = 1.0  # 起始值
        for i in range(1, len(dates)):
            # 高自相关：今天的PB ≈ 昨天的PB + 小扰动
            pb_values[i] = pb_values[i-1] + np.random.normal(0, 0.02)
            # 限制在合理范围
            pb_values[i] = np.clip(pb_values[i], 0.6, 1.5)
        
        # 3. 构造 Alpha 成分
        alpha_values = np.zeros(len(dates))
        for i in range(len(pb_values)):
            if pb_values[i] < 0.8:
                # 极低估区间：注入强正 Alpha (+0.008 每日)
                alpha_values[i] = 0.008
            elif pb_values[i] < 1.0:
                # 一般低估区间：注入负 Alpha (-0.005 每日)
                alpha_values[i] = -0.005
        
        df = pd.DataFrame({
            'trade_date': dates,
            'close': prices,
            'pb': pb_values,
            'alpha': alpha_values 
        })
        return df

    def load_data(self, stock_code: str, field: str, threshold: float = 1.0) -> pd.DataFrame:
        """加载数据"""
        if self.is_mock:
            return self._get_mock_data(field, threshold)
            
        try:
            ts.set_token(TUSHARE_TOKEN)
            self.pro = ts.pro_api()
            df_daily = self.pro.daily(ts_code=stock_code, start_date=BACKTEST_START, end_date=BACKTEST_END)
            df_daily['trade_date'] = pd.to_datetime(df_daily['trade_date'])
            df_daily.sort_values('trade_date', inplace=True)
            df_fina = self.pro.fina_indicator(ts_code=stock_code)
            df_fina['end_date'] = pd.to_datetime(df_fina['end_date'])
            df_fina.sort_values('end_date', inplace=True)
            df = pd.merge_asof(
                df_daily[['trade_date', 'close']],
                df_fina[['end_date', field]],
                left_on='trade_date',
                right_on='end_date',
                direction='backward'
            )
            return df.dropna(subset=[field])
        except Exception as e:
            console.print(f"[red]数据加载失败: {e}，切换至模拟数据[/red]")
            self.is_mock = True
            return self._get_mock_data(field, threshold)

    def run_validation(self, hypothesis: dict) -> dict:
        """执行验证流程"""
        stock = hypothesis['stock_code']
        field = hypothesis['field']
        threshold = hypothesis['threshold']
        
        console.print(f"\n[bold blue]🔍 正在验证: {stock} {hypothesis['signal_desc']}[/bold blue]")
        console.print("[dim]加载历史数据...[/dim]")
        
        data = self.load_data(stock, field, threshold)
        if data.empty:
            return {"error": "无有效数据"}
            
        console.print(f"[dim]数据量: {len(data)} 个交易日[/dim]")
        
        # 1. 生成信号
        data['signal'] = (data[field] < threshold).astype(int)
        
        # 2. 计算收益
        if self.is_mock:
            # 演示模式：基准收益是原始市场收益
            daily_returns = np.full(len(data), 0.0005)  # 固定每日 +0.05%
            data['daily_ret'] = daily_returns
            # 策略收益 = 基准收益 + Alpha
            data['strategy_daily_ret'] = daily_returns + data['alpha'].values
        else:
            data['daily_ret'] = data['close'].pct_change()
            data['strategy_daily_ret'] = data['daily_ret']
            
        # 关键点：策略收益 = 信号 * (基准 + Alpha)
        # 使用 shift(1) 确保信号在交易前一日产生，避免未来函数
        data['final_strategy_ret'] = data['signal'].shift(1) * data['strategy_daily_ret']
        
        # 3. 计算核心指标
        clean_data = data.dropna()
        
        # 策略总收益和年化（基于整个回测期，更稳健的评估方式）
        strategy_cum = (1 + clean_data['final_strategy_ret']).prod()
        total_days = len(clean_data)
        total_strategy_ret = strategy_cum ** (252 / total_days) - 1
            
        # 基准年化（整个回测期）
        benchmark_cum = (1 + clean_data['daily_ret']).prod()
        total_benchmark_ret = benchmark_cum ** (252 / total_days) - 1
        
        # 超额收益 = 策略年化 - 基准年化
        excess_ret = total_strategy_ret - total_benchmark_ret
        
        # 4. 统计检验 (paired t-test) - 比较策略日收益与基准日收益
        if len(clean_data) > 10:
            t_stat, p_value = stats.ttest_rel(clean_data['final_strategy_ret'], clean_data['daily_ret'])
        else:
            p_value = 1.0
            
        # 5. 最大回撤
        cum_ret = (1 + clean_data['final_strategy_ret']).cumprod()
        rolling_max = cum_ret.cummax()
        drawdown = (cum_ret - rolling_max) / rolling_max
        max_dd = drawdown.min()
        
        # 6. 结论
        is_significant = p_value < 0.05
        is_profitable = excess_ret > 0
        
        if is_significant and is_profitable:
            conclusion = "✅ 有效 (Significant Alpha)"
            color = "green"
        elif is_profitable:
            conclusion = "⚠️ 收益为正但不显著 (Luck?)"
            color = "yellow"
        else:
            conclusion = "❌ 无效 (Invalid Hypothesis)"
            color = "red"
            
        return {
            "strategy_annual": total_strategy_ret,
            "benchmark_annual": total_benchmark_ret,
            "excess_return": excess_ret,
            "p_value": p_value,
            "max_drawdown": max_dd,
            "conclusion": conclusion,
            "color": color,
            "is_mock": self.is_mock
        }

    def suggest_optimization(self, hypothesis: dict, result: dict) -> dict:
        """如果失败，尝试建议优化（Hardcode 演示逻辑）"""
        # 只有在第一次验证失败且是 PB 指标时才建议优化
        if result['excess_return'] <= 0 and hypothesis['field'] == 'pb' and hypothesis['threshold'] == 1.0:
            new_threshold = 0.8
            console.print(f"\n[yellow]💡 AI 建议: 原阈值可能太宽松，尝试 {hypothesis['field'].upper()} < {new_threshold}[/yellow]")
            
            # 递归验证新阈值
            new_hyp = hypothesis.copy()
            new_hyp['threshold'] = new_threshold
            new_hyp['signal_desc'] = f"{hypothesis['field'].upper()} < {new_threshold}"
            return self.run_validation(new_hyp)
        return None
