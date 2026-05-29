"""
humanistic_ai.py - 人文AI引擎 v1.0

集成CBT认知扭曲检测器、概念澄清引擎、伦理检查层三个核心模块，
提供统一的人文AI分析和回应生成功能。

哲学基础：
- CBT：识别认知扭曲，用苏格拉底式提问引导觉察
- 分析哲学：概念澄清、逻辑严谨
- 伦理学：三重检验（后果+义务+品格）
- 唯物辩证法：矛盾分析、实践检验

作者：灵台未央
日期：2026-05-29
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import json
import time

from cognitive_distortion_detector import CognitiveDistortionDetector
from concept_clarifier import ConceptClarifier
from ethics_checker import EthicsChecker


@dataclass
class HumanisticAnalysis:
    """人文AI分析结果"""
    original_text: str
    context: str = ""
    
    # CBT检测
    cognitive_distortions: List[Any] = field(default_factory=list)
    
    # 概念澄清
    core_concepts: List[Any] = field(default_factory=list)
    assumptions: List[Any] = field(default_factory=list)
    
    # 伦理检查
    ethical_risks: List[Any] = field(default_factory=list)
    ethics_passed: bool = True
    
    # 综合
    overall_assessment: str = ""
    socratic_questions: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class HumanisticAI:
    """
    人文AI引擎 - 整合三个核心模块
    
    用法：
        ai = HumanisticAI()
        response = ai.respond("我这次考试没考好，我真是个废物")
        report = ai.full_report("自由比平等更重要")
    """
    
    def __init__(self):
        self.cbt = CognitiveDistortionDetector()
        self.clarifier = ConceptClarifier()
        self.ethics = EthicsChecker()
    
    def analyze(self, text: str, context: str = "") -> HumanisticAnalysis:
        """全面分析"""
        analysis = HumanisticAnalysis(original_text=text, context=context)
        
        # CBT检测
        analysis.cognitive_distortions = self.cbt.detect(text)
        
        # 概念澄清
        analysis.core_concepts = self.clarifier.identify_concepts(text)
        analysis.assumptions = self.clarifier.extract_assumptions(text)
        
        # 伦理检查
        report = self.ethics.full_check(text, context)
        analysis.ethical_risks = report.risks
        analysis.ethics_passed = report.passed
        
        # 综合评估
        analysis.overall_assessment = self._assess(analysis)
        
        # 苏格拉底式提问
        analysis.socratic_questions = self._generate_questions(analysis)
        
        return analysis
    
    def respond(self, text: str, context: str = "") -> str:
        """生成人文AI回应"""
        analysis = self.analyze(text, context)
        
        parts = []
        
        # 1. 确认
        parts.append(self._acknowledge(analysis))
        
        # 2. 洞察
        insight = self._insight(analysis)
        if insight:
            parts.append(insight)
        
        # 3. 苏格拉底式提问
        if analysis.socratic_questions:
            questions = "\n".join(f"• {q}" for q in analysis.socratic_questions[:3])
            parts.append(f"或许我们可以一起思考：\n{questions}")
        
        # 4. 鼓励
        parts.append(self._encourage(analysis))
        
        return "\n\n".join(parts)
    
    def full_report(self, text: str, context: str = "") -> str:
        """生成完整报告"""
        analysis = self.analyze(text, context)
        
        lines = [
            "=" * 50,
            "人文AI分析报告",
            "=" * 50,
            "",
            f"输入: {text}",
            "",
            "【认知扭曲检测】",
        ]
        
        if analysis.cognitive_distortions:
            for d in analysis.cognitive_distortions:
                lines.append(f"  ⚠️ {d.distortion_type.value} (置信度: {d.confidence:.2f})")
                lines.append(f"     匹配: {d.matched_text}")
        else:
            lines.append("  ✅ 未检测到认知扭曲")
        
        lines.extend(["", "【概念澄清】"])
        if analysis.core_concepts:
            for c in analysis.core_concepts[:5]:
                related = f" (相关: {', '.join(c.related_concepts)})" if c.related_concepts else ""
                lines.append(f"  📌 {c.name} | 歧义度: {c.ambiguity_score:.2f}{related}")
        
        if analysis.assumptions:
            lines.append("\n  隐含假设:")
            for a in analysis.assumptions[:3]:
                lines.append(f"  - [{a.assumption_type}] {a.content}")
        
        lines.extend(["", "【伦理检查】"])
        if analysis.ethical_risks:
            for r in analysis.ethical_risks:
                lines.append(f"  ⚠️ {r.risk_type.value}: {r.description}")
        else:
            lines.append("  ✅ 未检测到伦理风险")
        
        lines.extend(["", "【苏格拉底式追问】"])
        if analysis.socratic_questions:
            for i, q in enumerate(analysis.socratic_questions[:5], 1):
                lines.append(f"  {i}. {q}")
        
        lines.extend(["", "=" * 50])
        
        return "\n".join(lines)
    
    def _assess(self, a: HumanisticAnalysis) -> str:
        """综合评估"""
        parts = []
        if a.cognitive_distortions:
            types = [d.distortion_type.value for d in a.cognitive_distortions[:3]]
            parts.append(f"存在认知扭曲：{'、'.join(types)}")
        else:
            parts.append("思维较为理性")
        
        if a.core_concepts:
            names = [c.name for c in a.core_concepts[:3]]
            parts.append(f"核心概念：{'、'.join(names)}")
        
        if a.ethical_risks:
            parts.append("存在伦理风险")
        
        return "；".join(parts)
    
    def _generate_questions(self, a: HumanisticAnalysis) -> List[str]:
        """生成苏格拉底式提问"""
        questions = []
        
        # 基于认知扭曲
        for d in a.cognitive_distortions[:2]:
            q = self.cbt.generate_response(d)
            questions.append(q)
        
        # 基于概念
        for c in a.core_concepts[:2]:
            questions.append(f"「{c.name}」具体指的是什么？")
        
        # 基于假设
        for assumption in a.assumptions[:1]:
            questions.append(f"为什么认为「{assumption.content}」？")
        
        return questions[:5]
    
    def _acknowledge(self, a: HumanisticAnalysis) -> str:
        """确认回应"""
        if a.cognitive_distortions:
            return "感谢你的分享。我能感受到你在这个问题上的困扰。"
        elif a.ethical_risks:
            return "谢谢你的坦诚。这是一个值得深入探讨的话题。"
        else:
            return "感谢你的分享。这是一个很有意思的观点。"
    
    def _insight(self, a: HumanisticAnalysis) -> str:
        """核心洞察"""
        if a.cognitive_distortions:
            d = a.cognitive_distortions[0]
            return f"我注意到你的思考中可能存在「{d.distortion_type.value}」的倾向，这可能影响你对情况的全面理解。"
        return ""
    
    def _encourage(self, a: HumanisticAnalysis) -> str:
        """鼓励"""
        if a.cognitive_distortions:
            return "记住，思维方式是可以改变的。通过觉察和练习，我们可以培养更灵活的思维模式。"
        return "保持这种开放和反思的态度，这对个人成长非常有帮助。"


def main():
    ai = HumanisticAI()
    
    print("=" * 50)
    print("人文AI引擎 v1.0 测试")
    print("=" * 50)
    
    tests = [
        ("我这次考试没考好，我真是个废物，永远都这样了。", "学生"),
        ("自由比平等更重要，因为自由是人的本质属性。", "哲学讨论"),
        ("所有人都应该按照我的想法来做，否则就是错的。", "人际冲突"),
        ("我今天遇到了一些困难，但我知道这是成长的一部分。", "日常"),
    ]
    
    for text, context in tests:
        print(f"\n{'='*50}")
        print(f"【{context}】{text}")
        print("=" * 50)
        
        # 生成回应
        response = ai.respond(text, context)
        print(f"\n人文AI回应:\n{response}")
        
        # 生成报告
        report = ai.full_report(text, context)
        print(f"\n{report}")


if __name__ == "__main__":
    main()
