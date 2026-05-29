"""
humanistic_ai.py - 人文AI引擎 v2.0

集成五个核心模块：
1. CBT认知扭曲检测器
2. 概念澄清引擎
3. 伦理检查层
4. 论证质量评估器（新增）
5. 苏格拉底式对话引擎（新增）

作者：灵台未央
日期：2026-05-29
"""

from dataclasses import dataclass, field
from typing import List, Any
from datetime import datetime
import time

from cognitive_distortion_detector import CognitiveDistortionDetector
from concept_clarifier import ConceptClarifier
from ethics_checker import EthicsChecker
from argument_analyzer import ArgumentAnalyzer


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
    
    # 论证分析（新增）
    fallacies: List[Any] = field(default_factory=list)
    argument_score: float = 0.0
    
    # 综合
    overall_assessment: str = ""
    socratic_questions: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class HumanisticAI:
    """
    人文AI引擎 v2.0 - 五模块集成
    
    用法：
        ai = HumanisticAI()
        response = ai.respond("我这次考试没考好，我真是个废物")
        report = ai.full_report("自由比平等更重要")
    """
    
    def __init__(self):
        self.cbt = CognitiveDistortionDetector()
        self.clarifier = ConceptClarifier()
        self.ethics = EthicsChecker()
        self.argument = ArgumentAnalyzer()
    
    def analyze(self, text: str, context: str = "") -> HumanisticAnalysis:
        """全面分析"""
        analysis = HumanisticAnalysis(original_text=text, context=context)
        
        # CBT检测
        analysis.cognitive_distortions = self.cbt.detect(text)
        
        # 概念澄清
        analysis.core_concepts = self.clarifier.identify_concepts(text)
        analysis.assumptions = self.clarifier.extract_assumptions(text)
        
        # 伦理检查
        ethics_report = self.ethics.full_check(text, context)
        analysis.ethical_risks = ethics_report.risks
        analysis.ethics_passed = ethics_report.passed
        
        # 论证分析
        arg_analysis = self.argument.analyze(text)
        analysis.fallacies = arg_analysis.fallacies
        analysis.argument_score = arg_analysis.overall_score
        
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
            "人文AI分析报告 v2.0",
            "=" * 50,
            "",
            f"输入: {text}",
        ]
        
        # 认知扭曲
        lines.extend(["", "【认知扭曲检测】"])
        if analysis.cognitive_distortions:
            for d in analysis.cognitive_distortions:
                lines.append(f"  ⚠️ {d.distortion_type.value} (置信度: {d.confidence:.2f})")
        else:
            lines.append("  ✅ 未检测到认知扭曲")
        
        # 概念澄清
        lines.extend(["", "【概念澄清】"])
        if analysis.core_concepts:
            for c in analysis.core_concepts[:5]:
                lines.append(f"  📌 {c.name} | 歧义度: {c.ambiguity_score:.2f}")
        if analysis.assumptions:
            lines.append("  隐含假设:")
            for a in analysis.assumptions[:3]:
                lines.append(f"  - [{a.assumption_type}] {a.content}")
        
        # 伦理检查
        lines.extend(["", "【伦理检查】"])
        if analysis.ethical_risks:
            for r in analysis.ethical_risks:
                lines.append(f"  ⚠️ {r.risk_type.value}: {r.description}")
        else:
            lines.append("  ✅ 未检测到伦理风险")
        
        # 论证分析
        lines.extend(["", "【论证质量】"])
        lines.append(f"  评分: {analysis.argument_score:.2f}")
        if analysis.fallacies:
            for f in analysis.fallacies:
                lines.append(f"  ⚠️ {f.type.value}: {f.description}")
        else:
            lines.append("  ✅ 未检测到逻辑谬误")
        
        # 苏格拉底式追问
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
            parts.append(f"认知扭曲：{'、'.join(types)}")
        else:
            parts.append("思维较为理性")
        
        if a.core_concepts:
            names = [c.name for c in a.core_concepts[:3]]
            parts.append(f"核心概念：{'、'.join(names)}")
        
        if a.fallacies:
            types = [f.type.value for f in a.fallacies[:3]]
            parts.append(f"逻辑谬误：{'、'.join(types)}")
        
        if a.ethical_risks:
            parts.append("存在伦理风险")
        
        return "；".join(parts)
    
    def _generate_questions(self, a: HumanisticAnalysis) -> List[str]:
        """生成苏格拉底式提问"""
        questions = []
        
        # 基于认知扭曲
        for d in a.cognitive_distortions[:1]:
            questions.append(self.cbt.generate_response(d))
        
        # 基于概念
        for c in a.core_concepts[:1]:
            questions.append(f"「{c.name}」具体指的是什么？")
        
        # 基于假设
        for assumption in a.assumptions[:1]:
            questions.append(f"为什么认为「{assumption.content}」？")
        
        # 基于论证谬误
        for f in a.fallacies[:1]:
            questions.append(f.suggestion)
        
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
            return f"我注意到你的思考中可能存在「{d.distortion_type.value}」的倾向。"
        if a.fallacies:
            f = a.fallacies[0]
            return f"这个论证中可能存在「{f.type.value}」的问题。"
        return ""
    
    def _encourage(self, a: HumanisticAnalysis) -> str:
        """鼓励"""
        if a.cognitive_distortions:
            return "思维方式是可以改变的。通过觉察和练习，我们可以培养更灵活的思维模式。"
        return "保持开放和反思的态度，这对个人成长非常有帮助。"


def main():
    ai = HumanisticAI()
    
    print("=" * 50)
    print("人文AI引擎 v2.0 测试")
    print("=" * 50)
    
    tests = [
        ("我这次考试没考好，我真是个废物，永远都这样了。", "学生"),
        ("所有政客都是不诚实的，因为政客都是不诚实的人。", "政治讨论"),
        ("自由比平等更重要，因为自由是人的本质属性。", "哲学讨论"),
        ("根据研究数据，城市通勤时间过长影响生活质量，因此建议优化公共交通。", "政策分析"),
    ]
    
    for text, context in tests:
        print(f"\n{'='*50}")
        print(f"【{context}】")
        print(f"输入: {text}")
        print("=" * 50)
        
        response = ai.respond(text, context)
        print(f"\n{response}")
        
        report = ai.full_report(text, context)
        print(f"\n{report}")


if __name__ == "__main__":
    main()
