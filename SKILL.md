---
name: compliance-checker-zx
displayName: 行业合规工具
summary: 10个合规工具：合同分析/法规检索/风险评估/合规清单/隐私审计/脱敏/术语解释/条款生成/义务追踪/报告生成
tags:
  - compliance
  - legal
  - risk
  - audit
version: 1.0.0
language: python
---

# 行业合规工具 (compliance-checker-zx)

## 描述

提供10个行业合规相关的工具函数，覆盖合同条款分析、法规检索、风险评估、合规检查清单、数据隐私审计、敏感信息脱敏、法律术语解释、条款生成、义务追踪和合规报告生成等场景。

## 功能

1. **合同条款分析** - 检查合同中的关键条款和潜在风险
2. **法规检索** - 按关键词、行业、管辖区检索法规
3. **风险评估** - 基于风险因素矩阵评估整体风险等级
4. **合规检查清单** - 按行业生成合规检查项
5. **数据隐私审计** - 审计数据流和处理活动合规性
6. **敏感信息脱敏** - 正则识别并脱敏敏感数据
7. **法律术语解释** - 内置法律术语知识库
8. **条款生成器** - 生成标准合同条款文本
9. **义务追踪器** - 追踪义务履行状态和截止日期
10. **合规报告生成** - 支持文本/JSON/Markdown格式

## 使用

```python
from main import contract_analyzer, compliance_report_generator

result = contract_analyzer("合同文本", ["付款条件", "违约责任"])
report = compliance_report_generator({"findings": [...]}, "markdown")
```

## 依赖

无外部依赖，仅使用Python标准库。
