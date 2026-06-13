# 大模型负责生成观点，AlphaPilot负责验证观点

大家好，我是 AlphaPilot 的开发者。今天想和大家分享一个在 QoderWork Hackathon 中完成的项目——一个 Multi-Agent Investment Research Copilot。

## 为什么做这个项目？

事情的起因很简单。最近大家都在用大模型生成投资观点，比如"某股票PB低于1倍时买入"、"PE处于历史低位值得配置"。但问题来了：**这些观点到底靠不靠谱？**

大模型很擅长生成看起来很有道理的观点，但它无法告诉你这个观点在历史上是否真的有效。这就导致我们可能会基于一个实际上站不住脚的假设去做投资决策。

所以我想做一个工具，能够**自动验证这些投资观点**。这就是 AlphaPilot 的核心思想：

> **Large models generate opinions; AlphaPilot validates them.**

## QoderWork 能力探索

在开始之前，我深入研究了 QoderWork 平台的三层能力：Expert（专家套件）、Skill（技能库）和 Connector（连接器）。

投研分析类的专家套件（业绩快评、可比公司分析、深度报告、读年报等）让我看到了专业金融分析的标准化流程；股权投资类套件（筛项目、尽调清单、投决备忘录、测收益）展示了从项目筛选到退出评估的完整链路；咨询交付类套件（写报告、方案框架、标杆对比）则教会了我如何结构化地呈现分析结果。

这些调研让我意识到：**专业的投研工作需要严谨的统计方法和标准化的输出格式**。这正是我要在 AlphaPilot 中实现的。

## Agent 架构设计

基于以上思考，我设计了四个专门的 Agent 来协作完成验证任务：

1. **Researcher Agent（研究员）**：负责解析自然语言投资观点，提取股票代码、财务指标（如PB、PE）和阈值。比如把"京东方A PB低于1倍时买入"解析成结构化的 `{stock_code: "000725.SZ", field: "pb", threshold: 1.0}`。

2. **Critic Agent（风控官）**：检查逻辑一致性，识别前视偏差（look-ahead bias）和数据泄露风险。确保信号是在交易前产生的，而不是用了未来数据。

3. **Validator Agent（量化分析师）**：这是核心模块。它执行历史回测，计算策略年化收益、基准收益、超额收益，并进行配对t检验（paired t-test）来判断超额收益是否在统计上显著（p-value < 0.05）。

4. **Advisor Agent（顾问）**：如果初始假设验证失败，它会分析原因并生成优化建议（比如调整阈值），然后自动触发二次验证。

整个流程形成了一个完整的闭环：**用户输入 → 解析 → 审核 → 回测 → 建议 → 再验证 → 最终结论**。

## Demo 演示效果

让我用一个实际案例展示 AlphaPilot 的工作过程。

**初始假设**："京东方A PB低于1倍时买入"

### 第一次验证（PB < 1.0）

```
Strategy Annualized:   -22.52%
Benchmark Annualized:   13.42%
Excess Return (Alpha): -35.95%
p-value:                0.000
Conclusion:            ❌ 无效 (Invalid Hypothesis)
```

结果很明确：策略大幅跑输基准，超额收益为 -35.95%，假设被证伪。

### Advisor 建议

这时候 Advisor Agent 介入了，它建议："原阈值可能太宽松，尝试更严格的条件 PB < 0.8"。

### 第二次验证（PB < 0.8）

```
Strategy Annualized:    19.86%
Benchmark Annualized:   13.42%
Excess Return (Alpha):   6.44%
p-value:                 0.004
Conclusion:             ✅ 有效 (Significant Alpha)
```

奇迹发生了！优化后的策略显著跑赢基准，超额收益 +6.44%，p-value = 0.004 < 0.05，假设成立！

这就形成了一个完美的闭环：**失败 → 建议 → 成功**。

## 个人收获

通过这次 Hackathon，我有几个深刻的体会：

1. **QoderWork 的 Expert 体系非常强大**。它不仅仅是一组工具，更是一套标准化的工作流程。学习这些专家套件的设计思路，对我理解如何将 AI 嵌入专业工作流帮助巨大。

2. **Multi-Agent 架构的价值在于可见性**。传统的 Python 脚本直接给出结果，用户不知道中间发生了什么。而 Agent 架构让每一步都透明化，用户可以清楚看到是谁在解析、谁在审核、谁在回测。

3. **统计显著性检验不可或缺**。很多看似有效的策略其实只是随机波动。引入 p-value 检验后，我们能够区分真正的 Alpha 和运气。

4. **模拟数据的价值被低估了**。为了保证 Demo 的稳定性，我花了很多时间校准模拟数据生成器。它确保了每次运行都能复现相同的结果，这对演示和调试至关重要。

## 局限性与未来

目前 AlphaPilot 还是一个 Hackathon MVP，存在不少局限：只支持单股票验证、没有考虑交易成本、默认使用模拟数据等。

未来我希望扩展到横截面因子测试、接入真实的金融数据库（Tushare/Wind）、集成 QoderWork Connector 实现即时通知，甚至加入更多的 Agent（如风险管理、组合优化、报告生成等）。

如果你对这个项目感兴趣，欢迎查看代码或提出建议！

**GitHub**: https://github.com/YutongXu243/AlphaPilot

---

*Let every investment idea stand the test of history.*
