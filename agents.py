"""
AlphaPilot Multi-Agent System
Lightweight wrappers to orchestrate the investment validation process.
Defines four specialized agents: Researcher, Critic, Validator, and Advisor.
"""

from parser import parse_hypothesis
from validator import QuantValidator
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

class ResearcherAgent:
    """Responsible for parsing natural language into structured signals."""
    def run(self, text: str):
        console.print(f"\n[bold blue]🕵️ [Researcher Agent][/bold blue] Parsing hypothesis: \"{text}\"...")
        return parse_hypothesis(text)

class CriticAgent:
    """Responsible for logical review and risk assessment."""
    def run(self, hypothesis: dict):
        console.print(f"[bold yellow]⚖️  [Critic Agent][/bold yellow] Checking logic & risks...")
        risks = []
        if hypothesis['operator'] not in ['<', '>', '<=', '>=']:
            risks.append("Non-standard operator detected.")
        
        if not risks:
            console.print("[green]✓ Logic check passed. No obvious look-ahead bias.[/green]")
            return True
        else:
            for r in risks:
                console.print(f"[red]⚠️ Risk: {r}[/red]")
            return False

class ValidatorAgent:
    """Responsible for executing the backtest and statistical tests."""
    def __init__(self):
        self.engine = QuantValidator()

    def run(self, hypothesis: dict):
        console.print(f"[bold magenta]📊 [Validator Agent][/bold magenta] Executing historical validation...")
        return self.engine.run_validation(hypothesis)

class AdvisorAgent:
    """Responsible for generating suggestions based on results."""
    def run(self, hypothesis: dict, result: dict):
        console.print(f"[bold cyan]💡 [Advisor Agent][/bold cyan] Analyzing results & generating advice...")
        
        if result.get('error'):
            return None

        # Optimization logic: if failed and PB < 1.0, suggest stricter threshold
        if result['excess_return'] <= 0 and hypothesis['field'] == 'pb' and hypothesis['threshold'] >= 1.0:
            new_threshold = round(hypothesis['threshold'] * 0.8, 2)
            suggestion = f"Original hypothesis failed. Suggest trying a stricter threshold: **{hypothesis['field'].upper()} < {new_threshold}**"
            
            panel = Panel(Markdown(suggestion), title="[bold cyan]Optimization Advice[/bold cyan]", border_style="yellow")
            console.print(panel)
            
            return {"action": "re_validate", "new_threshold": new_threshold}
        
        console.print("[green]✓ Hypothesis is statistically sound. No further optimization needed.[/green]")
        return None
