"""
concept_clarifier.py - 人文AI概念澄清引擎 v1.0

基于分析哲学、苏格拉底方法和胡塞尔现象学的结构化追问模块。
通过识别核心概念、提取隐含假设、生成追问来促进深度思考。

哲学基础：
- 分析哲学：概念澄清、语言分析
- 苏格拉底方法：通过追问揭示无知
- 胡塞尔现象学：悬置判断，回到事物本身

作者：灵台未央
日期：2026-05-29
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import re


@dataclass
class Concept:
    """核心概念"""
    name: str
    positions: List[Tuple[int, int]] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    is_abstract: bool = True
    ambiguity_score: float = 0.0


@dataclass
class Assumption:
    """隐含假设"""
    content: str
    is_explicit: bool = False
    challengeability: float = 0.5
    assumption_type: str = "unknown"  # causal, value, existence


@dataclass
class Meaning:
    """概念含义"""
    description: str
    context: str
    confidence: float = 0.5


class ConceptClarifier:
    """
    概念澄清引擎
    
    基于分析哲学和苏格拉底方法，通过结构化追问澄清概念和假设。
    
    用法：
        clarifier = ConceptClarifier()
        concepts = clarifier.identify_concepts("自由比平等更重要")
        questions = clarifier.generate_clarifying_questions("自由比平等更重要")
    """
    
    def __init__(self):
        self.abstract_concepts = {
            "自由", "平等", "正义", "公平", "真理", "美", "善", "恶",
            "道德", "伦理", "权利", "义务", "责任", "尊严", "价值",
            "幸福", "意义", "存在", "本质", "现象", "理性", "感性",
            "意识", "精神", "灵魂", "自我", "他者", "主体", "客体",
            "民主", "法治", "人权", "发展", "进步", "文明", "文化",
            "传统", "现代", "革命", "改革", "权力", "阶级", "民族",
            "国家", "社会", "集体", "个人", "公共", "私人",
            "理解", "认知", "知识", "智慧", "信念", "信仰", "怀疑",
            "确定", "不确定", "复杂", "简单", "系统", "整体", "部分",
            "原因", "结果", "目的", "手段", "可能", "必然", "偶然",
            "科学", "理论", "假设", "证据", "证明", "验证", "实验",
            "观察", "事实", "客观", "主观", "相对", "绝对", "普遍",
            "爱", "恨", "恐惧", "希望", "绝望", "痛苦", "快乐",
        }
        
        self.assumption_triggers = {
            'causal': ['因为', '所以', '因此', '导致', '引起', '由于', '从而', '只要', '如果', '那么'],
            'value': ['应该', '必须', '需要', '值得', '重要', '好', '坏', '对', '错', '正确', '错误'],
            'existence': ['存在', '有', '是', '在', '作为', '成为', '具有', '拥有'],
        }
        
        self.question_templates = {
            'concept': [
                "请问「{concept}」具体指的是什么？",
                "您能给出「{concept}」的明确定义吗？",
                "「{concept}」在什么意义上使用？",
                "有没有「{concept}」的反例？",
            ],
            'assumption': [
                "为什么您认为{assumption}？",
                "这个假设是否总是成立？",
                "有没有证据支持「{assumption}」？",
                "如果不成立，会怎样？",
            ],
            'premise': [
                "这个论证的前提是什么？",
                "有没有其他可能的解释？",
                "如果从相反前提开始，会得出什么？",
            ],
            'socratic': [
                "我们如何知道「{concept}」是真的？",
                "「{concept}」的本质是什么？",
                "如果悬置对「{concept}」的判断，会看到什么？",
            ],
        }
        
        self.disambiguation_dict = {
            "自由": [
                Meaning("消极自由：不受外部干涉", "政治哲学", 0.8),
                Meaning("积极自由：自主行动的能力", "政治哲学", 0.7),
                Meaning("意志自由：自由意志", "形而上学", 0.6),
                Meaning("言论自由：表达意见的权利", "法律", 0.9),
            ],
            "正义": [
                Meaning("分配正义：资源公平分配", "政治哲学", 0.8),
                Meaning("程序正义：规则公平执行", "法律", 0.7),
                Meaning("矫正正义：纠正不公", "伦理学", 0.6),
            ],
            "真理": [
                Meaning("符合论真理：与事实相符", "认识论", 0.8),
                Meaning("融贯论真理：与系统一致", "认识论", 0.6),
                Meaning("实用论真理：有用即真理", "实用主义", 0.5),
            ],
            "存在": [
                Meaning("实存：具体事物的存在", "形而上学", 0.7),
                Meaning("此在：人的存在方式", "存在主义", 0.8),
                Meaning("现象：显现出来的存在", "现象学", 0.7),
            ],
            "意识": [
                Meaning("现象意识：主观体验", "心灵哲学", 0.8),
                Meaning("自我意识：对自身的觉知", "心理学", 0.7),
            ],
        }
    
    def identify_concepts(self, text: str) -> List[Concept]:
        """识别文本中的核心概念"""
        concepts = []
        seen = set()
        
        for concept_name in self.abstract_concepts:
            positions = [(m.start(), m.end()) for m in re.finditer(re.escape(concept_name), text)]
            if positions and concept_name not in seen:
                seen.add(concept_name)
                ambiguity = min(1.0, len(self.disambiguation_dict.get(concept_name, [])) * 0.25)
                concepts.append(Concept(
                    name=concept_name,
                    positions=positions,
                    is_abstract=True,
                    ambiguity_score=ambiguity if concept_name in self.disambiguation_dict else 0.3
                ))
        
        # 识别相关概念
        for i, c1 in enumerate(concepts):
            for c2 in concepts[i+1:]:
                sentences = re.split(r'[。！？\n]', text)
                for sentence in sentences:
                    if c1.name in sentence and c2.name in sentence:
                        c1.related_concepts.append(c2.name)
                        c2.related_concepts.append(c1.name)
                        break
        
        concepts.sort(key=lambda c: c.positions[0][0] if c.positions else 0)
        return concepts
    
    def extract_assumptions(self, text: str) -> List[Assumption]:
        """提取文本中的隐含假设"""
        assumptions = []
        sentences = [s.strip() for s in re.split(r'[。！？\n]', text) if s.strip()]
        
        for sentence in sentences:
            for atype, triggers in self.assumption_triggers.items():
                for trigger in triggers:
                    if trigger in sentence:
                        parts = sentence.split(trigger)
                        if len(parts) >= 2:
                            before = parts[0][-15:] if len(parts[0]) > 15 else parts[0]
                            after = parts[1][:15] if len(parts[1]) > 15 else parts[1]
                            content = f"{before}{trigger}{after}"
                        else:
                            content = sentence[:40]
                        
                        challengeability = {'causal': 0.7, 'value': 0.8, 'existence': 0.6}.get(atype, 0.5)
                        assumptions.append(Assumption(
                            content=content,
                            is_explicit=False,
                            challengeability=challengeability,
                            assumption_type=atype
                        ))
                        break  # 每个句子每种类型只取一个
        
        # 去重
        seen = set()
        unique = []
        for a in assumptions:
            if a.content not in seen:
                seen.add(a.content)
                unique.append(a)
        return unique
    
    def generate_clarifying_questions(self, text: str) -> List[str]:
        """生成苏格拉底式追问"""
        questions = []
        concepts = self.identify_concepts(text)
        assumptions = self.extract_assumptions(text)
        
        for concept in concepts[:3]:
            for tpl in self.question_templates['concept'][:2]:
                questions.append(tpl.format(concept=concept.name))
            for tpl in self.question_templates['socratic'][:1]:
                questions.append(tpl.format(concept=concept.name))
        
        for assumption in assumptions[:2]:
            for tpl in self.question_templates['assumption'][:2]:
                questions.append(tpl.format(assumption=assumption.content))
        
        if concepts or assumptions:
            questions.extend(self.question_templates['premise'][:2])
        
        return list(dict.fromkeys(questions))[:12]
    
    def disambiguate(self, concept: str, context: str) -> List[Meaning]:
        """概念消歧"""
        if concept in self.disambiguation_dict:
            meanings = list(self.disambiguation_dict[concept])
        else:
            meanings = [Meaning(f"一般语境中的含义", "通用", 0.3)]
        
        # 根据上下文调整置信度
        for m in meanings:
            if any(kw in context for kw in m.context.split('/')):
                m.confidence = min(1.0, m.confidence + 0.2)
        
        meanings.sort(key=lambda m: m.confidence, reverse=True)
        return meanings
    
    def challenge_premises(self, text: str) -> List[str]:
        """挑战前提"""
        challenges = []
        assumptions = self.extract_assumptions(text)
        concepts = self.identify_concepts(text)
        
        for assumption in assumptions:
            if assumption.challengeability > 0.5:
                if assumption.assumption_type == 'causal':
                    challenges.append(f"「{assumption.content}」这个因果关系是否成立？")
                elif assumption.assumption_type == 'value':
                    challenges.append(f"「{assumption.content}」这个价值判断的根据是什么？")
                elif assumption.assumption_type == 'existence':
                    challenges.append(f"「{assumption.content}」这个存在判断如何验证？")
        
        for concept in concepts[:2]:
            challenges.append(f"如果悬置对「{concept.name}」的判断，会看到什么？")
        
        return list(dict.fromkeys(challenges))[:8]


def main():
    """测试用例"""
    clarifier = ConceptClarifier()
    
    print("=" * 60)
    print("人文AI · 概念澄清引擎 v1.0")
    print("=" * 60)
    
    test_text = """我认为自由比平等更重要，因为自由是人的本质属性。
只有保障个人自由，社会才能实现真正的正义。
如果为了平等而限制自由，就会导致极权主义。"""
    
    # 测试1: 概念识别
    print("\n【概念识别】")
    concepts = clarifier.identify_concepts(test_text)
    for c in concepts:
        related = f" (相关: {', '.join(c.related_concepts)})" if c.related_concepts else ""
        print(f"  - {c.name} | 歧义度: {c.ambiguity_score:.2f}{related}")
    
    # 测试2: 假设提取
    print("\n【假设提取】")
    assumptions = clarifier.extract_assumptions(test_text)
    for a in assumptions:
        print(f"  - [{a.assumption_type}] {a.content}")
    
    # 测试3: 追问生成
    print("\n【苏格拉底式追问】")
    questions = clarifier.generate_clarifying_questions(test_text)
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")
    
    # 测试4: 概念消歧
    print("\n【概念消歧】")
    for name in ["自由", "正义"]:
        print(f"\n  「{name}」的可能含义:")
        meanings = clarifier.disambiguate(name, test_text)
        for m in meanings:
            print(f"    - {m.description} ({m.context}, {m.confidence:.2f})")
    
    # 测试5: 前提挑战
    print("\n【前提挑战】")
    challenges = clarifier.challenge_premises(test_text)
    for i, c in enumerate(challenges, 1):
        print(f"  {i}. {c}")
    
    # 测试6: 哲学名句
    print("\n" + "=" * 60)
    print("哲学名句测试")
    print("=" * 60)
    
    quotes = [
        "人天生是自由的，但却无往不在枷锁之中。",
        "存在先于本质，人首先存在，然后定义自己。",
        "意识总是关于某物的意识，这就是意向性。",
    ]
    
    for text in quotes:
        print(f"\n文本: {text}")
        concepts = clarifier.identify_concepts(text)
        print(f"  概念: {[c.name for c in concepts]}")
        questions = clarifier.generate_clarifying_questions(text)
        print(f"  追问: {questions[0] if questions else '无'}")


if __name__ == "__main__":
    main()
