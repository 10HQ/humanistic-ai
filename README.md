# 人文AI宣言

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY_SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-37/37-brightgreen.svg)](tests/test_all.py)
[![Benchmark](https://img.shields.io/badge/benchmark-120_cases-orange.svg)](benchmark.md)

> *"技术决定我们能做什么，人文决定我们应该做什么。"*
>
> *"技术是船，人文是舵。没有舵的船，跑得越快，偏得越远。"*

---

## 什么是人文AI？

人文AI不是给AI加上一层人文的皮。它是一种根本不同的AI范式。

**人文AI = 知识深度 × 洞察力 × 实践智慧**

| 维度 | 传统AI | 人文AI |
|------|--------|--------|
| 知识 | 信息检索 | 深度理解 |
| 推理 | 模式匹配 | 哲学思辨 |
| 表达 | 信息堆砌 | 简短有力 |
| 价值 | 工具理性 | 价值理性 |
| 目标 | 完成任务 | 追求智慧 |

---

## 基准测试（120用例×6维度）

| 指标 | 结果 |
|------|------|
| CBT检测率 | **100%** (20/20) |
| 伦理检测率 | **85%** (17/20) |
| 论证区分度 | **15/16** 低质量正确检出 |
| 概念识别 | **117** 个/120用例 |
| 跨文化概念 | **42** 个/20用例 |

**单元测试：37/37 通过（100%）**

---

## 快速开始

```python
from humanistic_ai import HumanisticAI

ai = HumanisticAI()

# 分析
analysis = ai.analyze("我这次考试没考好，我真是个废物")
print(analysis.socratic_questions)

# 回应
print(ai.respond("自由比平等更重要"))

# 苏格拉底式对话
r = ai.dialogue_start("活着有什么意义？")
r = ai.dialogue_continue("我不知道自己想要什么")

# 完整报告
print(ai.full_report("隐瞒产品真实成本误导消费者"))
```

---

## 文档

| 文档 | 描述 |
|------|------|
| [宣言 v3.1](manifesto.md) \| [English](manifesto_en.md) | 核心文本（五轮批评迭代） |
| [理论框架](theory-framework.md) | 哲学+心理学理论基础 |
| [技术实现路径](technical-roadmap.md) | 从理念到可编码 |
| [基准测试](benchmark.md) | HCB设计 |
| [测试报告](HCB_REPORT_v0.2.md) | 120用例测试结果 |
| [路线图](ROADMAP.md) | 从"值得阅读"到"不可忽视" |
| [贡献指南](CONTRIBUTING.md) | 如何参与 |
| [批评回应录](critique-responses.md) | 五轮批评与修正 |

---

## Python 模块

| 模块 | 功能 | 测试 |
|------|------|------|
| `cognitive_distortion_detector.py` | CBT认知扭曲检测器（10种扭曲） | ✅ 12/12 |
| `concept_clarifier.py` | 概念澄清引擎（70+概念词典） | ✅ 6/6 |
| `ethics_checker.py` | 伦理检查层（三重检验+实质底线） | ✅ 7/7 |
| `argument_analyzer.py` | 论证质量评估器（10种逻辑谬误） | ✅ 6/6 |
| `socratic_engine.py` | 苏格拉底式对话引擎（五阶段模型） | ✅ |
| `semantic_analyzer.py` | 语义分析层（DeepSeek API集成） | ✅ |
| `humanistic_ai.py` | 引擎主模块（六模块集成） | ✅ 6/6 |
| `run_benchmark.py` | 基准测试（120用例×6维度） | ✅ |

```
tests/test_all.py      ← 37个单元测试
examples/demo.py       ← 5场景演示
```

---

## 迭代历程

| 版本 | 触发 | 核心修改 |
|------|------|----------|
| v1.0 | 初版 | 宣言+理论框架 |
| v2.0 | 马维斯批评 | 从宣言到作战计划 |
| v3.0 | 自我批判 | 过程正义+实质底线+不确定性中的行动 |
| v3.1 | DeepSeek/豆包/XAIgrok | 技术实现路径+英文版+基准测试+路线图 |
| v3.2 | 苏玖/grok | 乱码修复+Topics+License+语义分析层 |

---

## License

CC BY-SA 4.0

> *"不是因为它能赢，而是因为没有它会更糟。"*
