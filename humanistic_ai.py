"""
humanistic_ai.py - 人文AI引擎 v3.0

六模块集成：CBT + 概念澄清 + 伦理检查 + 论证分析 + 苏格拉底引擎 + 语义分析

作者：灵台未央
日期：2026-05-29
"""

from dataclasses import dataclass, field
from typing import List, Any, Optional
from datetime import datetime

from cognitive_distortion_detector import CognitiveDistortionDetector
from concept_clarifier import ConceptClarifier
from ethics_checker import EthicsChecker
from argument_analyzer import ArgumentAnalyzer
from socratic_engine import SocraticEngine


@dataclass
class HumanisticAnalysis:
    """人文AI分析结果"""
    original_text: str
    context: str = ""
    cognitive_distortions: List[Any] = field(default_factory=list)
    core_concepts: List[Any] = field(default_factory=list)
    assumptions: List[Any] = field(default_factory=list)
    ethical_risks: List[Any] = field(default_factory=list)
    ethics_passed: bool = True
    fallacies: List[Any] = field(default_factory=list)
    argument_score: float = 0.0
    overall_assessment: str = ""
    socratic_questions: List[str] = field(default_factory=list)
    semantic_result: Optional[Any] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class HumanisticAI:
    """
    人文AI引擎 v3.0
    
    用法：
        ai = HumanisticAI()
        response = ai.respond("我这次考试没考好，我真是个废物")
        report = ai.full_report("自由比平等更重要")
        dialogue = ai.dialogue_start("活着有什么意义？")
    """
    
    def __init__(self, enable_semantic: bool = False):
        self.cbt = CognitiveDistortionDetector()
        self.clarifier = ConceptClarifier()
        self.ethics = EthicsChecker()
        self.argument = ArgumentAnalyzer()
        self.socratic = SocraticEngine()
        self.enable_semantic = enable_semantic
        
        if enable_semantic:
            try:
                from semantic_analyzer import SemanticAnalyzer
                self.semantic = SemanticAnalyzer()
                self.enable_semantic = self.semantic.enabled
            except Exception:
                self.semantic = None
                self.enable_semantic = False
    
    def analyze(self, text: str, context: str = "") -> HumanisticAnalysis:
        """全面分析"""
        analysis = HumanisticAnalysis(original_text=text, context=context)
        
        analysis.cognitive_distortions = self.cbt.detect(text)
        analysis.core_concepts = self.clarifier.identify_concepts(text)
        analysis.assumptions = self.clarifier.extract_assumptions(text)
        
        ethics_report = self.ethics.full_check(text, context)
        analysis.ethical_risks = ethics_report.risks
        analysis.ethics_passed = ethics_report.passed
        
        arg_analysis = self.argument.analyze(text)
        analysis.fallacies = arg_analysis.fallacies
        analysis.argument_score = arg_analysis.overall_score
        
        analysis.overall_assessment = self._assess(analysis)
        analysis.socratic_questions = self._generate_questions(analysis)
        
        return analysis
    
    def respond(self, text: str, context: str = "") -> str:
        """生成人文AI回应"""
        analysis = self.analyze(text, context)
        parts = []
        
        parts.append(self._acknowledge(analysis))
        
        insight = self._insight(analysis)
        if insight:
            parts.append(insight)
        
        if analysis.socratic_questions:
            questions = "\n".join(f"• {q}" for q in analysis.socratic_questions[:3])
            parts.append(f"或许我们可以一起思考：\n{questions}")
        
        parts.append(self._encourage(analysis))
        return "\n\n".join(parts)
    
    def dialogue_start(self, text: str, context: str = "") -> Any:
        """开始苏格拉底式对话"""
        return self.socratic.start(text, context)
    
    def dialogue_continue(self, text: str) -> Any:
        """继续苏格拉底式对话"""
        return self.socratic.continue_dialogue(text)
    
    def full_report(self, text: str, context: str = "") -> str:
        """生成完整报告"""
        analysis = self.analyze(text, context)
        
        lines = [
            "=" * 50,
            "人文AI分析报告 v3.0",
            "=" * 50,
            "",
            f"输入: {text}",
        ]
        
        lines.extend(["", "[CBT]"])
        if analysis.cognitive_distortions:
            for d in analysis.cognitive_distortions:
                lines.append(f"  ! {d.distortion_type.value} ({d.confidence:.2f})")
        else:
            lines.append("  OK")
        
        lines.extend(["", "[Concepts]"])
        if analysis.core_concepts:
            for c in analysis.core_concepts[:5]:
                lines.append(f"  # {c.name} (ambiguity={c.ambiguity_score:.2f})")
        if analysis.assumptions:
            lines.append("  Assumptions:")
            for a in analysis.assumptions[:3]:
                lines.append(f"  - [{a.assumption_type}] {a.content}")
        
        lines.extend(["", "[Ethics]"])
        if analysis.ethical_risks:
            for r in analysis.ethical_risks:
                lines.append(f"  ! {r.risk_type.value}: {r.description}")
        else:
            lines.append("  OK")
        
        lines.extend(["", "[Argument]"])
        lines.append(f"  Score: {analysis.argument_score:.2f}")
        if analysis.fallacies:
            for f in analysis.fallacies:
                lines.append(f"  ! {f.type.value}: {f.description}")
        else:
            lines.append("  OK")
        
        lines.extend(["", "[Questions]"])
        if analysis.socratic_questions:
            for i, q in enumerate(analysis.socratic_questions[:5], 1):
                lines.append(f"  {i}. {q}")
        
        lines.extend(["", "=" * 50])
        return "\n".join(lines)
    
    def _assess(self, a: HumanisticAnalysis) -> str:
        parts = []
        if a.cognitive_distortions:
            types = [d.distortion_type.value for d in a.cognitive_distortions[:3]]
            parts.append(f"CBT: {', '.join(types)}")
        if a.core_concepts:
            names = [c.name for c in a.core_concepts[:3]]
            parts.append(f"Concepts: {', '.join(names)}")
        if a.fallacies:
            types = [f.type.value for f in a.fallacies[:3]]
            parts.append(f"Fallacies: {', '.join(types)}")
        if a.ethical_risks:
            parts.append("Ethics: risks detected")
        return "; ".join(parts) if parts else "No issues detected"
    
    def _generate_questions(self, a: HumanisticAnalysis) -> List[str]:
        questions = []
        for d in a.cognitive_distortions[:1]:
            questions.append(self.cbt.generate_response(d))
        for c in a.core_concepts[:1]:
            questions.append(f"What does '{c.name}' mean to you?")
        for assumption in a.assumptions[:1]:
            questions.append(f"Why do you believe '{assumption.content}'?")
        for f in a.fallacies[:1]:
            questions.append(f.suggestion)
        return questions[:5]
    
    def _acknowledge(self, a: HumanisticAnalysis) -> str:
        if a.cognitive_distortions:
            return "感谢你的分享。我能感受到你在这个问题上的困扰。"
        elif a.ethical_risks:
            return "谢谢你的坦诚。这是一个值得深入探讨的话题。"
        return "感谢你的分享。这是一个很有意思的观点。"
    
    def _insight(self, a: HumanisticAnalysis) -> str:
        if a.cognitive_distortions:
            d = a.cognitive_distortions[0]
            return f"我注意到你的思考中可能存在「{d.distortion_type.value}」的倾向。"
        if a.fallacies:
            f = a.fallacies[0]
            return f"这个论证中可能存在「{f.type.value}」的问题。"
        return ""
    
    def _encourage(self, a: HumanisticAnalysis) -> str:
        if a.cognitive_distortions:
            return "思维方式是可以改变的。通过觉察和练习，我们可以培养更灵活的思维模式。"
        return "保持开放和反思的态度，这对个人成长非常有帮助。"


def main():
    ai = HumanisticAI()
    
    print("=" * 50)
    print("人文AI引擎 v3.0")
    print("=" * 50)
    
    tests = [
        ("我这次考试没考好，我真是个废物，永远都这样了。", "CBT"),
        ("自由比平等更重要，因为自由是人的本质属性。", "Philosophy"),
        ("爱因斯坦说过神不掷骰子，所以量子力学是错的。", "Fallacy"),
        ("根据研究数据，城市通勤时间过长影响生活质量，因此建议优化公共交通。", "Good argument"),
        ("活着到底有什么意义？每天重复同样的事情，感觉很空虚。", "Existential"),
    ]
    
    for text, context in tests:
        print(f"\n{'='*50}")
        print(f"[{context}] {text}")
        print("=" * 50)
        response = ai.respond(text, context)
        print(response)
    
    # Dialogue test
    print(f"\n{'='*50}")
    print("[Dialogue Test]")
    print("=" * 50)
    r1 = ai.dialogue_start("我这次考试没考好，我真是个废物")
    print(f"AI: {r1.text[:200]}")
    r2 = ai.dialogue_continue("我觉得他们都在嘲笑我")
    print(f"\nUser: 觉得他们都在嘲笑我")
    print(f"AI: {r2.text[:200]}")


if __name__ == "__main__":
    main()
