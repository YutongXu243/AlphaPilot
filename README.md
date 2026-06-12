# AlphaPilot

AlphaPilot is a multi-agent research demo for the QoderWork Hackathon. It turns a natural-language research hypothesis into a simple testable signal and shows a validation card.

> Large models generate opinions; AlphaPilot validates them.

## Project Overview

This project demonstrates a lightweight agent workflow:

1. Parse a research hypothesis.
2. Convert it into a structured signal.
3. Compare the signal result with a simple benchmark.
4. Produce a clear validation card and next-step suggestion.

## Agent Architecture

| Agent | Role | Responsibility |
| :--- | :--- | :--- |
| Researcher | Signal extraction | Converts a sentence about BOE Technology into a condition such as `PB < 1.0`. |
| Critic | Logic review | Checks basic consistency and validation risks. |
| Validator | Historical check | Runs the numerical validation and statistical test. |
| Advisor | Iteration | Suggests a stricter threshold if the first hypothesis fails. |

## Quick Start

```bash
git clone https://github.com/YutongXu243/AlphaPilot.git
cd AlphaPilot
pip install -r requirements.txt
python main.py
```

## Case Study: BOE Technology / Jingdongfang A (000725.SZ)

Demo hypothesis: `BOE Technology PB < 1.0`.

AlphaPilot first checks the broad threshold, then asks whether a stricter threshold such as `PB < 0.8` gives a cleaner result.

## Tech Stack

- Python
- Pandas
- NumPy
- SciPy
- Tushare, optional
- Rich

## Limitations

- This is a Hackathon MVP, not financial advice.
- The default mode uses deterministic demo data when no Tushare token is configured.
- Current validation is single-company and demonstration-oriented.

## Future Work

- LLM-based parsing for complex research logic.
- Broader universe testing.
- Transaction-cost-aware validation.
- QoderWork connector integration.
