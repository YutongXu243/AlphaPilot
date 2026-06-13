"""
AlphaPilot MVP Entry Point - Multi-Agent Orchestration
This script orchestrates the four specialized agents to validate investment hypotheses.
"""
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from agents import ResearcherAgent, CriticAgent, ValidatorAgent, AdvisorAgent

console = Console()

def print_validation_card(result: dict, title: str = "Final Validation Result"):
    """Prints a professional validation card with key metrics."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="bold")
    
    table.add_row("Strategy Annualized", f"{result['strategy_annual']*100:.2f}%")
    table.add_row("Benchmark Annualized", f"{result['benchmark_annual']*100:.2f}%")
    
    excess_color = "green" if result['excess_return'] > 0 else "red"
    table.add_row("Excess Return (Alpha)", f"{result['excess_return']*100:.2f}%", style=excess_color)
    
    p_color = "green" if result['p_value'] < 0.05 else "dim"
    table.add_row("Statistical Significance", f"p-value = {result['p_value']:.3f}", style=p_color)
    
    table.add_row("Max Drawdown", f"{result['max_drawdown']*100:.2f}%")
    
    panel = Panel(table, title=f"[bold]{title}[/bold]", 
                  border_style=result['color'], expand=False)
    console.print(panel)
    console.print(f"[bold {result['color']}]{result['conclusion']}[/bold {result['color']}]")

def main():
    console.rule("[bold green]AlphaPilot: Multi-Agent Investment Copilot[/bold green]")
    console.print("[dim]Turn natural-language hypotheses into statistically validated signals.[/dim]\n")
    
    # Initialize Agents
    researcher = ResearcherAgent()
    critic = CriticAgent()
    validator = ValidatorAgent()
    advisor = AdvisorAgent()
    
    # Get Input
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = "京东方A PB低于1倍时买入" # Default demo input
    
    console.print(f"[bold]Input Hypothesis:[/bold] {user_input}")
    
    # 1. Researcher Agent: Parse natural language
    hypothesis = researcher.run(user_input)
    
    # 2. Critic Agent: Logical review
    if not critic.run(hypothesis):
        console.print("[red]Validation aborted due to logical risks.[/red]")
        return

    # 3. Validator Agent: First Pass Backtest
    result = validator.run(hypothesis)
    print_validation_card(result, "Initial Validation")
    
    # 4. Advisor Agent: Generate suggestions
    advice = advisor.run(hypothesis, result)
    
    # 5. Automatic Re-validation if advised
    if advice and advice.get('action') == 're_validate':
        console.print("\n[bold yellow]🔄 Initiating automatic re-validation with optimized parameters...[/bold yellow]\n")
        hypothesis['threshold'] = advice['new_threshold']
        hypothesis['signal_desc'] = f"{hypothesis['field'].upper()} < {advice['new_threshold']}"
        
        result_opt = validator.run(hypothesis)
        print_validation_card(result_opt, "Optimized Validation")

if __name__ == "__main__":
    main()
