# AlphaPilot 🤖📈

**AlphaPilot** is a multi-agent investment research copilot that turns natural-language investment hypotheses into statistically validated trading signals.

> "Large models generate opinions; AlphaPilot validates them."

## 🌟 Project Overview
Traditional AI assistants can write beautiful investment reports, but they never take responsibility for the results. AlphaPilot closes this gap by acting as a **scientific validation engine**:
1.  **Parse**: Extract quantifiable logic from natural language.
2.  **Validate**: Execute historical backtests with statistical rigor (t-tests).
3.  **Advise**: Provide data-driven feedback to refine your investment thesis.

## 🏗️ Agent Architecture
AlphaPilot orchestrates four specialized agents to ensure robustness:

| Agent | Role | Responsibility |
| :--- | :--- | :--- |
| **Researcher** 🔍 | Signal Extraction | Converts "JD.com is undervalued" into `PB < 1.0`. |
| **Critic** ⚖️ | Logical Review | Checks for look-ahead bias and logical consistency. |
| **Validator** 📊 | Statistical Testing | Runs backtests and calculates p-values via `scipy`. |
| **Advisor** 💡 | Optimization | Suggests parameter tuning (e.g., stricter thresholds) if the initial hypothesis fails. |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- A Tushare Pro Token (optional, falls back to demo mode)

### Installation
```bash
git clone https://github.com/YutongXu243/AlphaPilot.git
cd AlphaPilot
pip install -r requirements.txt
```

### Run Demo
```bash
python main.py
```

## 🎬 Case Study: JD.com (000725.SZ)

**Hypothesis:** "Buy when PB < 1.0 because the panel industry is bottoming out."

1.  **Initial Validation:** ❌ **Failed**. Excess return was -16.57% against the benchmark.
2.  **Advisor Insight:** The threshold might be too loose. Suggested trying `PB < 0.8`.
3.  **Re-validation:** ✅ **Success**. With the optimized threshold, the strategy showed significant Alpha (p < 0.05).

## 🛠️ Tech Stack
*   **Core:** Python, Pandas, NumPy
*   **Statistics:** Scipy (Paired t-test for significance)
*   **Data:** Tushare Pro (with built-in Mock Data for stability)
*   **UI:** Rich (Terminal formatting)

## ⚠️ Limitations
*   Currently supports single-stock validation only.
*   Mock data is used for demonstration purposes in the absence of a valid API token.

## 🔮 Future Work
*   Integration of LLMs for more complex logical parsing.
*   Cross-sectional factor analysis (IC/Rank IC).
*   Real-time signal monitoring via IM connectors.

---
*Built for the Hackathon. Let every investment idea stand the test of history.*