# AlphaPilot Architecture

## Multi-Agent Investment Research Copilot

### Mermaid Diagram (README Ready)

```mermaid
flowchart TD
    User[👤 User<br/>Investment Hypothesis] --> Researcher
    
    subgraph Agents["🤖 AlphaPilot Multi-Agent System"]
        direction TB
        
        Researcher[🔍 Researcher Agent<br/>Extract Investment Hypothesis]
        Critic[⚖️ Critic Agent<br/>Check Logic & Risks]
        Validator[📊 Validator Agent<br/>Backtest + Statistical Test]
        Advisor[💡 Advisor Agent<br/>Generate Optimization]
        
        Researcher --> Critic
        Critic --> Validator
        Validator --> Advisor
    end
    
    Advisor --> ValidationCard
    
    subgraph Output["📋 Validation Card"]
        direction TB
        StrategyRet[📈 Strategy Annualized Return]
        BenchmarkRet[📉 Benchmark Return]
        ExcessRet[✨ Excess Return / Alpha]
        PValue[🎯 p-value / Statistical Significance]
        Conclusion[✅ Final Conclusion]
    end
    
    ValidationCard --> Output

    classDef user fill:#f9f,stroke:#333,stroke-width:2px
    classDef agent fill:#fff,stroke:#333,stroke-width:2px
    classDef output fill:#ff9,stroke:#333,stroke-width:2px
    classDef container fill:#f0f0f0,stroke:#666,stroke-width:1px,stroke-dasharray: 5 5
    
    class User user
    class Researcher,Critic,Validator,Advisor agent
    class ValidationCard,StrategyRet,BenchmarkRet,ExcessRet,PValue,Conclusion output
    class Agents,Output container
```

### Simplified Version (Better for GitHub README)

```mermaid
graph LR
    A[👤 User Input] --> B[🔍 Researcher<br/>Parse Hypothesis]
    B --> C[⚖️ Critic<br/>Logic Check]
    C --> D[📊 Validator<br/>Backtest & Stats]
    D --> E[💡 Advisor<br/>Optimization]
    E --> F[📋 Validation Card<br/>Returns + p-value + Conclusion]
    
    style A fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    style B fill:#fff4e6,stroke:#ff9900,stroke-width:2px
    style C fill:#fff4e6,stroke:#ff9900,stroke-width:2px
    style D fill:#fff4e6,stroke:#ff9900,stroke-width:2px
    style E fill:#fff4e6,stroke:#ff9900,stroke-width:2px
    style F fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
```

### Vertical Flow (Professional Documentation)

```mermaid
flowchart TB
    Start([🚀 User submits<br/>investment hypothesis]) --> R[🔍 Researcher Agent]
    
    R -->|"Extract structured signal<br/>(e.g., PB < 1.0)"| C[⚖️ Critic Agent]
    C -->|"Validate logic<br/& check biases"| V[📊 Validator Agent]
    
    V -->|"Run backtest<br/>Calculate returns<br/>Statistical test"| A[💡 Advisor Agent]
    A -->|"Analyze results<br/>Suggest optimization"| Result{Validation<br/>Result}
    
    Result -->|"Success ✅<br/>p < 0.05, Alpha > 0"| Success[🎯 Valid Hypothesis<br/>Significant Alpha Found]
    Result -->|"Failure ❌<br/>Alpha ≤ 0"| Optimize[🔄 Suggest stricter threshold<br/>e.g., PB < 0.8]
    
    Optimize -->|"Re-validate"| V
    
    Success --> End([📊 Generate<br/>Validation Card])
    
    classDef startend fill:#4CAF50,color:#fff,stroke:#333,stroke-width:2px
    classDef process fill:#2196F3,color:#fff,stroke:#333,stroke-width:2px
    classDef decision fill:#FF9800,color:#fff,stroke:#333,stroke-width:2px
    
    class Start,End startend
    class R,C,V,A process
    class Result,Optimize decision
```

## Usage Instructions

### For GitHub README.md

Copy the "Simplified Version" mermaid code block above and paste it into your README.md file. GitHub natively renders mermaid diagrams.

### Example README Integration

```markdown
## 🏗️ Architecture

AlphaPilot uses a multi-agent workflow to validate investment hypotheses:

```mermaid
graph LR
    A[👤 User Input] --> B[🔍 Researcher<br/>Parse Hypothesis]
    B --> C[⚖️ Critic<br/>Logic Check]
    C --> D[📊 Validator<br/>Backtest & Stats]
    D --> E[💡 Advisor<br/>Optimization]
    E --> F[📋 Validation Card<br/>Returns + p-value + Conclusion]
    
    style A fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    style B fill:#fff4e6,stroke:#ff9900,stroke-width:2px
    style C fill:#fff4e6,stroke:#ff9900,stroke-width:2px
    style D fill:#fff4e6,stroke:#ff9900,stroke-width:2px
    style E fill:#fff4e6,stroke:#ff9900,stroke-width:2px
    style F fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
```

### Agent Roles

- **🔍 Researcher**: Parses natural language into structured signals
- **⚖️ Critic**: Checks for logical flaws and look-ahead bias
- **📊 Validator**: Runs historical backtests with statistical rigor
- **💡 Advisor**: Provides optimization suggestions when hypotheses fail
```

## Key Design Principles

1. **Minimalist Black & White**: Clean lines, high contrast
2. **Emoji Icons**: Visual hierarchy without color dependency
3. **Clear Flow**: Left-to-right or top-to-bottom progression
4. **Professional Labels**: Concise, technical terminology
5. **GitHub Compatible**: Native mermaid rendering support
