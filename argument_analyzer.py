"""
argument_analyzer.py - 人文AI论证质量评估器 v1.0

基于分析哲学、非形式逻辑和修辞学的论证分析工具。

哲学基础：
- 分析哲学：逻辑分析、概念澄清
- 非形式逻辑：谬误分类与论证评估
- 修辞学：论证策略与说服技巧分析

作者：灵台未央
日期：2026-05-29
"""

from dataclasses import dataclass, field
from typing import List, Tuple
from enum import Enum
import re


class FallacyType(Enum):
    CIRCULAR_REASONING = "循环论证"
    EQUIVOCATION = "偷换概念"
    APPEAL_TO_AUTHORITY = "诉诸权威"
    SLIPPERY_SLOPE = "滑坡谬误"
    FALSE_DILEMMA = "虚假二分"
    AD_HOMINEM = "人身攻击"
    STRAW_MAN = "稻草人"
    APPEAL_TO_EMOTION = "诉诸情感"
    HASTY_GENERALIZATION = "以偏概全"
    APPEAL_TO_IGNORANCE = "诉诸无知"


@dataclass
class Fallacy:
    type: FallacyType
    position: Tuple[int, int]
    description: str
    severity: float  # 0.0 - 1.0
    suggestion: str


@dataclass
class ArgumentStructure:
    premises: List[str] = field(default_factory=list)
    conclusion: str = ""
    reasoning_type: str = ""
    validity: float = 0.0
    strength: float = 0.0


@dataclass
class ArgumentAnalysis:
    fallacies: List[Fallacy] = field(default_factory=list)
    structure: ArgumentStructure = field(default_factory=ArgumentStructure)
    overall_score: float = 0.0
    improvement_suggestions: List[str] = field(default_factory=list)


class ArgumentAnalyzer:
    """
    论证质量评估器
    
    用法：
        analyzer = ArgumentAnalyzer()
        analysis = analyzer.analyze("所有政客都是不诚实的，因为政客都不诚实")
        print(analyzer.generate_critique(analysis))
    """
    
    def __init__(self):
        self.circular_patterns = [
            (r'因为\s*(.+?)\s*，所以\s*\1', '前提和结论相同'),
            (r'之所以\s*(.+?)\s*是因为\s*\1', '循环解释'),
        ]
        
        self.authority_patterns = [
            (r'(专家|教授|博士|权威|研究|科学家|大佬|学者|大师)\s*(说|认为|指出|表示|证明|讲过|说过)', '引用权威但未提供具体证据'),
            (r'(某某|某位|很多|不少)\s*(专家|学者|权威|大佬)', '模糊引用权威'),
            (r'权威.*?指出|研究.*?表明.*?所以', '用研究结论代替论证'),
            (r'(爱因斯坦|牛顿|达尔文|霍金|孔子|亚里士多德|柏拉图)\s*(说过|讲过|说过)', '引用名人名言替代论证'),
        ]
        
        self.slippery_slope_patterns = [
            (r'(如果|一旦)\s*(.+?)\s*，\s*(就|便会|必将)\s*(.+?)(，\s*(进而|最终|导致)\s*(.+)){1,}', '因果链缺乏中间环节'),
        ]
        
        self.false_dilemma_patterns = [
            (r'(要么|不是)\s*(.+?)\s*(要么|就是)\s*(.+?)\s*，\s*(没有|不存在)\s*(其他|别的)', '排除中间选项'),
            (r'(只有|唯一)\s*(两种|两个)\s*(选择|可能|选项)', '限制选项数量'),
        ]
        
        self.ad_hominem_patterns = [
            (r'(你|他|她|他们|对方)\s*(就是|不过|只是|也就)\s*(一个|个|这种)\s*(.*?)(人|家伙|货|的)', '攻击人格特质'),
            (r'(你|他|她)\s*(懂什么|有什么资格|凭什么|你算|他算)\s*(说|评论|批评|讨论|讲|来)|一个连.*?都没有的人', '以身份否定论点'),
            (r'(离婚|没上过|小学|没学历|没文化|菜鸟|外行|门外汉).*?(的人|来着|也配|也敢)', '用身份标签否定观点'),
        ]
        
        self.straw_man_patterns = [
            (r'(你|你们|对方)\s*(的意思|的观点|的看法|的逻辑)\s*(就是|无非是|不过是|说白了就是|等于说)\s*(.+?)(，|。|但|然而|所以)', '歪曲对方观点'),
            (r'这无非是|说白了就是|这不就等于|这等于说', '将对方观点极端化'),
            (r'按你这么说|照你那么说|那你是不是|按你的逻辑|照这样讲', '将对方立场推导到极端'),
            (r'(你是想让|你是说|你的意思是)\s*(所有人|大家都)\s*(.*?)(吗|？|吧)', '将对方观点极端化'),
        ]
        
        self.equivocation_patterns = [
            (r'(自然|本质|真正|纯粹|绝对)\s*(的\s*)?(自由|正义|平等|民主|安全|权利)', '抽象概念被重新定义'),
            (r'昨天.*?说.*?今天.*?说', '在同一论证中使用概念的不同含义'),
            (r'所谓.*?就是', '重新定义概念以支持论点'),
        ]
        
        self.emotion_patterns = [
            (r'(难道|怎能|岂能)\s*(不|没有)\s*(.*?)(吗|呢|？)', '修辞性反问替代论证'),
            (r'(想想|试想|想象一下|想一想)\s*(.*?)(的|之)\s*(后果|结果|遭遇)', '诉诸恐惧'),
            (r'(那些|多少).*?(孩子|老人|穷人|病人).*?(你怎么|你们怎么|怎么能)', '诉诸怜悯'),
        ]
        
        self.generalization_patterns = [
            (r'(所有|全部|每个|总是|从来|永远)\s*(.*?)\s*(都|均|皆)', '绝对化表述'),
            (r'(几个|少数|个别)\s*(.*?)\s*(就|便)\s*(代表|说明|证明)', '样本不足概括'),
        ]
        
        self.ignorance_patterns = [
            (r'(没有|无法)\s*(证明|证实|证伪)\s*(.*?)\s*，\s*(所以|因此)\s*(.*?)(存在|成立|正确)', '无法证伪即成立'),
        ]
        
        self.premise_indicators = ['因为', '由于', '鉴于', '基于', '根据', '首先', '第一', '其一']
        self.conclusion_indicators = ['所以', '因此', '因而', '故', '于是', '从而', '可见', '总之', '综上所述', '由此可知']
    
    def analyze(self, text: str) -> ArgumentAnalysis:
        """综合分析"""
        fallacies = self.detect_fallacies(text)
        structure = self.evaluate_argument_structure(text)
        score = self._calculate_score(fallacies, structure)
        suggestions = self._generate_suggestions(fallacies, structure)
        
        return ArgumentAnalysis(
            fallacies=fallacies,
            structure=structure,
            overall_score=score,
            improvement_suggestions=suggestions
        )
    
    def detect_fallacies(self, text: str) -> List[Fallacy]:
        """检测逻辑谬误"""
        fallacies = []
        
        detectors = [
            (self.circular_patterns, FallacyType.CIRCULAR_REASONING, 0.8, "避免用结论本身来证明结论"),
            (self.equivocation_patterns, FallacyType.EQUIVOCATION, 0.7, "明确概念的定义，确保同一概念在论证中含义一致"),
            (self.authority_patterns, FallacyType.APPEAL_TO_AUTHORITY, 0.6, "提供具体证据，而非仅依赖权威"),
            (self.slippery_slope_patterns, FallacyType.SLIPPERY_SLOPE, 0.7, "提供因果链中每个环节的证据"),
            (self.false_dilemma_patterns, FallacyType.FALSE_DILEMMA, 0.7, "考虑更多可能的选项"),
            (self.ad_hominem_patterns, FallacyType.AD_HOMINEM, 0.8, "聚焦于论点本身而非提出论点的人"),
            (self.straw_man_patterns, FallacyType.STRAW_MAN, 0.8, "准确理解并呈现对方观点"),
            (self.emotion_patterns, FallacyType.APPEAL_TO_EMOTION, 0.6, "用逻辑和证据替代情感诉求"),
            (self.generalization_patterns, FallacyType.HASTY_GENERALIZATION, 0.7, "避免基于有限样本做出普遍性结论"),
            (self.ignorance_patterns, FallacyType.APPEAL_TO_IGNORANCE, 0.7, "提供正面证据支持论点"),
        ]
        
        for patterns, ftype, severity, suggestion in detectors:
            for pattern, desc in patterns:
                for match in re.finditer(pattern, text):
                    fallacies.append(Fallacy(
                        type=ftype,
                        position=(match.start(), match.end()),
                        description=desc,
                        severity=severity,
                        suggestion=suggestion
                    ))
        
        fallacies.sort(key=lambda f: f.position[0])
        return fallacies
    
    def evaluate_argument_structure(self, text: str) -> ArgumentStructure:
        """评估论证结构"""
        sentences = [s.strip() for s in re.split(r'[。！？；\n]', text) if s.strip()]
        
        premises = []
        conclusion = ""
        
        for sentence in sentences:
            if any(ind in sentence for ind in self.premise_indicators):
                premises.append(sentence)
            if any(ind in sentence for ind in self.conclusion_indicators):
                conclusion = sentence
        
        if not conclusion and sentences:
            conclusion = sentences[-1]
        
        # 推理类型
        reasoning_type = "未识别"
        if re.search(r'(所有|凡是|任何)\s*(.+?)\s*(都|均)', text):
            reasoning_type = "演绎推理"
        elif re.search(r'(多数|大部分|通常|往往|统计|数据)', text):
            reasoning_type = "归纳推理"
        elif re.search(r'(就像|如同|好比|类似)', text):
            reasoning_type = "类比推理"
        
        # 有效性
        validity = 0.0
        if premises and conclusion:
            validity = 0.5
            if any(c in conclusion for c in self.conclusion_indicators):
                validity += 0.2
            if len(premises) >= 2:
                validity += 0.1
        
        # 强度
        strength = 0.0
        if premises:
            strength = min(len(premises) * 0.15, 0.5)
            if any(kw in ' '.join(premises) for kw in ['数据', '统计', '研究', '证据']):
                strength += 0.3
        
        return ArgumentStructure(premises, conclusion, reasoning_type, min(validity, 1.0), min(strength, 1.0))
    
    def generate_critique(self, analysis: ArgumentAnalysis) -> str:
        """生成批判性评论"""
        parts = []
        
        if analysis.overall_score >= 0.8:
            parts.append("论证质量较高，逻辑较为严密。")
        elif analysis.overall_score >= 0.6:
            parts.append("论证质量中等，存在一些逻辑问题。")
        else:
            parts.append("论证质量较低，存在较多逻辑缺陷。")
        
        s = analysis.structure
        if s.premises:
            parts.append(f"论证包含{len(s.premises)}个前提，推理类型为{s.reasoning_type}。")
        else:
            parts.append("论证结构不清晰，缺乏明确的前提。")
        
        if analysis.fallacies:
            parts.append(f"检测到{len(analysis.fallacies)}个逻辑谬误：")
            for f in analysis.fallacies:
                parts.append(f"  - {f.type.value}：{f.description}")
                parts.append(f"    建议：{f.suggestion}")
        
        if analysis.improvement_suggestions:
            parts.append("\n改进建议：")
            for i, s in enumerate(analysis.improvement_suggestions, 1):
                parts.append(f"  {i}. {s}")
        
        return "\n".join(parts)
    
    def _calculate_score(self, fallacies: List[Fallacy], structure: ArgumentStructure) -> float:
        """计算总体评分"""
        score = 0.7
        for f in fallacies:
            score -= f.severity * 0.15
        if structure.premises:
            score += structure.validity * 0.1
            score += structure.strength * 0.1
        if structure.reasoning_type != "未识别":
            score += 0.1
        return max(0.0, min(score, 1.0))
    
    def _generate_suggestions(self, fallacies: List[Fallacy], structure: ArgumentStructure) -> List[str]:
        """生成改进建议"""
        suggestions = []
        if fallacies:
            suggestions.append("注意避免逻辑谬误，确保论证的严谨性。")
        if not structure.premises:
            suggestions.append("明确列出论证的前提，使论证结构更清晰。")
        if structure.validity < 0.5:
            suggestions.append("加强前提与结论之间的逻辑联系。")
        if structure.strength < 0.5:
            suggestions.append("提供更多具体证据和数据支持。")
        suggestions.append("考虑可能的反例和反驳，完善论证的全面性。")
        return suggestions


def main():
    analyzer = ArgumentAnalyzer()
    
    print("=" * 50)
    print("人文AI · 论证质量评估器 v1.0")
    print("=" * 50)
    
    tests = [
        ("循环论证", "所有政客都是不诚实的，因为政客都是不诚实的人。"),
        ("虚假二分+滑坡", "要么支持我们的政策，要么就是反对进步，没有其他选择。如果允许这项政策通过，最终会导致社会崩溃。"),
        ("人身攻击+稻草人", "对方认为应该增加教育投入，这无非是想让政府多花钱。你一个连孩子都没有的人，有什么资格讨论教育政策？"),
        ("高质量论证", "根据2023年的统计数据，城市居民的平均通勤时间为45分钟。由于通勤时间过长会影响工作效率，因此建议优化公共交通系统。"),
        ("诉诸权威+诉诸无知", "专家说我们的方案是最好的，所以我们应该采纳它。没有人能证明这个方案有问题，所以它一定是正确的。"),
    ]
    
    for name, text in tests:
        print(f"\n【{name}】")
        print(f"文本: {text}")
        analysis = analyzer.analyze(text)
        print(f"评分: {analysis.overall_score:.2f}")
        if analysis.fallacies:
            for f in analysis.fallacies:
                print(f"  ⚠️ {f.type.value}: {f.description}")
        else:
            print("  ✅ 未检测到谬误")
        print(f"  前提: {len(analysis.structure.premises)} | 推理: {analysis.structure.reasoning_type}")


if __name__ == "__main__":
    main()
