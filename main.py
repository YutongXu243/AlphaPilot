"""
AlphaPilot MVP Entry Point
"""
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from parser import parse_hypothesis
from validator import QuantValidator

console = Console()

def print_card(result: dict, title: str):
    """打印验证卡片"""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="bold")
    
    table.add_row("策略年化", f"{result['strategy_annual']*100:.2f}%")
    table.add_row("基准年化", f"{result['benchmark_annual']*100:.2f}%")
    table.add_row("超额收益", f"{result['excess_return']*100:.2f}%", 
                  style="green" if result['excess_return'] > 0 else "red")
    table.add_row("p-value", f"{result['p_value']:.3f}", 
                  style="green" if result['p_value'] < 0.05 else "dim")
    table.add_row("最大回撤", f"{result['max_drawdown']*100:.2f}%")
    
    panel = Panel(table, title=f"[bold]{title}[/bold]", 
                  border_style=result['color'], expand=False)
    console.print(panel)
    console.print(f"[bold {result['color']}]{result['conclusion']}[/bold {result['color']}]")

def main():
    console.rule("[bold green]AlphaPilot: Investment Hypothesis Validator[/bold green]")
    console.print("[dim]让每一个投资观点都经得起历史检验[/dim]\n")
    
    validator = QuantValidator()
    
    # 演示模式：自动运行两个案例
    if len(sys.argv) == 1:
        console.print("[bold]🎬 启动 Demo 模式...[/bold]\n")
        
        # Case 1: 失败案例
        hyp1 = parse_hypothesis("京东方A PB低于1倍时买入")
        res1 = validator.run_validation(hyp1)
        print_card(res1, "Case 1: 原观点验证")
        
        # Case 2: 优化建议
        res2 = validator.suggest_optimization(hyp1, res1)
        if res2:
            print_card(res2, "Case 2: AI 优化后验证")
            
    else:
        # 交互模式
        user_input = " ".join(sys.argv[1:])
        hyp = parse_hypothesis(user_input)
        res = validator.run_validation(hyp)
        print_card(res, "验证结果")

if __name__ == "__main__":
    main()