"""
socratic_engine.py - 人文AI苏格拉底式对话引擎 v1.0

基于苏格拉底方法的深度对话系统，整合CBT、概念澄清、伦理检查、论证分析。

哲学基础：
- 苏格拉底方法：通过追问揭示无知，引导自我发现
- CBT：苏格拉底式提问引导认知重构
- 现象学：悬置判断，回到事物本身
- 存在主义：面对终极关怀（死亡、自由、孤独、无意义）

作者：灵台未央
日期：2026-05-29
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import re

from cognitive_distortion_detector import CognitiveDistortionDetector
from concept_clarifier import ConceptClarifier
from ethics_checker import EthicsChecker
from argument_analyzer import ArgumentAnalyzer


class DialogueStage(Enum):
    """对话阶段"""
    ACKNOWLEDGMENT = "确认"
    EXPLORATION = "探索"
    CHALLENGE = "挑战"
    REFLECTION = "反思"
    INTEGRATION = "整合"


class ConcernType(Enum):
    """关怀类型（亚隆四终极关怀）"""
    DEATH = "死亡"
    FREEDOM = "自由"
    ISOLATION = "孤独"
    MEANINGLESSNESS = "无意义"
    OTHER = "其他"


@dataclass
class DialogueState:
    """对话状态"""
    stage: DialogueStage = DialogueStage.ACKNOWLEDGMENT
    concern_type: ConcernType = ConcernType.OTHER
    distortions_found: List[str] = field(default_factory=list)
    concepts_clarified: List[str] = field(default_factory=list)
    assumptions_challenged: List[str] = field(default_factory=list)
    fallacies_detected: List[str] = field(default_factory=list)
    depth_level: int = 0  # 0-4, 追问深度
    turn_count: int = 0


@dataclass
class SocraticResponse:
    """苏格拉底式回应"""
    text: str
    stage: DialogueStage
    question_type: str  # clarifying, probing, reflective, synthesizing
    depth_level: int
    modules_used: List[str] = field(default_factory=list)


class SocraticEngine:
    """
    苏格拉底式对话引擎
    
    整合四个模块，通过五阶段对话引导深度思考。
    
    用法：
        engine = SocraticEngine()
        response = engine.start("我这次考试没考好，我真是个废物")
        followup = engine.continue_dialogue("我觉得他们都在嘲笑我")
    """
    
    def __init__(self):
        self.cbt = CognitiveDistortionDetector()
        self.clarifier = ConceptClarifier()
        self.ethics = EthicsChecker()
        self.argument = ArgumentAnalyzer()
        self.state = DialogueState()
        
        # 终极关怀关键词
        self.concern_patterns = {
            ConcernType.DEATH: [r"死|死亡|临终|绝症|生命.*有限|时间.*不多"],
            ConcernType.FREEDOM: [r"选择.*困难|不知道.*该.*怎么|自由.*负担|必须.*决定"],
            ConcernType.ISOLATION: [r"孤独|没人.*理解|一个人|被.*抛弃|被.*忽视"],
            ConcernType.MEANINGLESSNESS: [r"没.*意义|空虚|无聊|活着.*为什么|一切.*都没"],
        }
        
        # 五阶段问题模板
        self.stage_templates = {
            DialogueStage.ACKNOWLEDGMENT: {
                "distortion": [
                    "我能感受到你在这个问题上的困扰。",
                    "谢谢你愿意分享这些。",
                    "这听起来确实不容易。",
                ],
                "normal": [
                    "感谢你的分享。",
                    "这是一个很有意思的观点。",
                    "我理解你的想法。",
                ]
            },
            DialogueStage.EXPLORATION: {
                "concept": [
                    "你说的「{concept}」具体指的是什么？",
                    "「{concept}」对你来说意味着什么？",
                    "能举一个「{concept}」的具体例子吗？",
                ],
                "assumption": [
                    "你似乎假设了「{assumption}」，这个假设是怎么来的？",
                    "如果这个假设不成立，你会怎么看？",
                    "有没有人可能不同意这个假设？",
                ],
                "emotion": [
                    "这种感觉是什么时候开始的？",
                    "当你说这些的时候，身体有什么感觉？",
                    "这种情绪背后，你最担心的是什么？",
                ]
            },
            DialogueStage.CHALLENGE: {
                "distortion": [
                    "如果用0-100分来评价，你会打多少分？",
                    "有没有例外的情况？",
                    "如果朋友遇到同样的事，你会对他说什么？",
                    "有没有证据支持/反对这个想法？",
                ],
                "assumption": [
                    "为什么认为「{assumption}」总是成立的？",
                    "有没有反例？",
                    "这个推理是否依赖于某个未经验证的前提？",
                ],
                "argument": [
                    "这个论证的前提是什么？",
                    "有没有其他可能的解释？",
                    "如果从相反的前提开始，会得出什么？",
                ]
            },
            DialogueStage.REFLECTION: {
                "general": [
                    "经过这些思考，你有什么新的发现？",
                    "你的想法有没有发生变化？",
                    "现在回头看，你最初的说法还成立吗？",
                ],
                "concern": {
                    ConcernType.DEATH: "面对生命的有限性，什么对你来说最重要？",
                    ConcernType.FREEDOM: "在众多选择中，你真正想要的是什么？",
                    ConcernType.ISOLATION: "在孤独中，你发现了什么关于自己的真相？",
                    ConcernType.MEANINGLESSNESS: "如果意义需要被创造，你想创造什么样的意义？",
                }
            },
            DialogueStage.INTEGRATION: {
                "general": [
                    "从这次对话中，你最大的收获是什么？",
                    "如果要把今天的思考总结成一句话，你会怎么说？",
                    "接下来你打算怎么做？",
                ]
            }
        }
    
    def start(self, text: str, context: str = "") -> SocraticResponse:
        """开始对话"""
        self.state = DialogueState(turn_count=1)
        
        # 全面分析
        cbt_results = self.cbt.detect(text)
        concepts = self.clarifier.identify_concepts(text)
        assumptions = self.clarifier.extract_assumptions(text)
        arg_analysis = self.argument.analyze(text)
        ethics_report = self.ethics.full_check(text, context)
        
        # 更新状态
        self.state.distortions_found = [d.distortion_type.value for d in cbt_results]
        self.state.concepts_clarified = [c.name for c in concepts]
        self.state.assumptions_challenged = [a.content for a in assumptions]
        self.state.fallacies_detected = [f.type.value for f in arg_analysis.fallacies]
        
        # 识别终极关怀
        self.state.concern_type = self._identify_concern(text)
        
        # 生成初始回应
        response_text = self._generate_initial_response(
            text, cbt_results, concepts, assumptions, arg_analysis, ethics_report
        )
        
        # 确定阶段
        if cbt_results or arg_analysis.fallacies:
            self.state.stage = DialogueStage.EXPLORATION
        else:
            self.state.stage = DialogueStage.EXPLORATION
        
        modules = []
        if cbt_results: modules.append("CBT")
        if concepts: modules.append("概念澄清")
        if arg_analysis.fallacies: modules.append("论证分析")
        if ethics_report.risks: modules.append("伦理检查")
        
        return SocraticResponse(
            text=response_text,
            stage=self.state.stage,
            question_type="clarifying",
            depth_level=0,
            modules_used=modules
        )
    
    def continue_dialogue(self, text: str) -> SocraticResponse:
        """继续对话"""
        self.state.turn_count += 1
        
        # 分析新输入
        cbt_results = self.cbt.detect(text)
        concepts = self.clarifier.identify_concepts(text)
        assumptions = self.clarifier.extract_assumptions(text)
        arg_analysis = self.argument.analyze(text)
        
        # 更新状态
        if cbt_results:
            self.state.distortions_found.extend([d.distortion_type.value for d in cbt_results])
        if concepts:
            self.state.concepts_clarified.extend([c.name for c in concepts])
        if assumptions:
            self.state.assumptions_challenged.extend([a.content for a in assumptions])
        if arg_analysis.fallacies:
            self.state.fallacies_detected.extend([f.type.value for f in arg_analysis.fallacies])
        
        # 推进阶段
        self._advance_stage()
        
        # 生成回应
        response_text = self._generate_stage_response(text, cbt_results, concepts, assumptions, arg_analysis)
        
        return SocraticResponse(
            text=response_text,
            stage=self.state.stage,
            question_type=self._get_question_type(),
            depth_level=self.state.depth_level,
            modules_used=[]
        )
    
    def _identify_concern(self, text: str) -> ConcernType:
        """识别终极关怀"""
        for concern, patterns in self.concern_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return concern
        return ConcernType.OTHER
    
    def _generate_initial_response(self, text, cbt_results, concepts, assumptions, arg_analysis, ethics_report):
        """生成初始回应"""
        parts = []
        
        # 确认
        if cbt_results or arg_analysis.fallacies:
            templates = self.stage_templates[DialogueStage.ACKNOWLEDGMENT]["distortion"]
            parts.append(templates[0])
        else:
            templates = self.stage_templates[DialogueStage.ACKNOWLEDGMENT]["normal"]
            parts.append(templates[0])
        
        # 核心洞察
        if cbt_results:
            d = cbt_results[0]
            parts.append(f"我注意到你的思考中可能存在「{d.distortion_type.value}」的倾向。")
        
        if arg_analysis.fallacies:
            f = arg_analysis.fallacies[0]
            parts.append(f"这个论证中可能存在「{f.type.value}」的问题。")
        
        # 苏格拉底式提问
        questions = []
        
        if cbt_results:
            questions.append(self.cbt.generate_response(cbt_results[0]))
        
        if concepts:
            c = concepts[0]
            questions.append(f"「{c.name}」具体指的是什么？")
        
        if assumptions:
            questions.append(f"为什么认为「{assumptions[0].content}」？")
        
        if not questions:
            questions.append("能告诉我更多关于这个想法的背景吗？")
        
        if questions:
            parts.append("或许我们可以一起思考：")
            for q in questions[:2]:
                parts.append(f"• {q}")
        
        # 终极关怀
        if self.state.concern_type != ConcernType.OTHER:
            concern_question = self.stage_templates[DialogueStage.REFLECTION]["concern"].get(self.state.concern_type)
            if concern_question:
                parts.append(f"\n更深层的问题：{concern_question}")
        
        return "\n\n".join(parts)
    
    def _generate_stage_response(self, text, cbt_results, concepts, assumptions, arg_analysis):
        """根据阶段生成回应"""
        parts = []
        
        if self.state.stage == DialogueStage.EXPLORATION:
            # 探索阶段：追问概念和假设
            if concepts:
                c = concepts[0]
                templates = self.stage_templates[DialogueStage.EXPLORATION]["concept"]
                parts.append(templates[0].format(concept=c.name))
            elif assumptions:
                templates = self.stage_templates[DialogueStage.EXPLORATION]["assumption"]
                parts.append(templates[0].format(assumption=assumptions[0].content))
            else:
                templates = self.stage_templates[DialogueStage.EXPLORATION]["emotion"]
                parts.append(templates[0])
        
        elif self.state.stage == DialogueStage.CHALLENGE:
            # 挑战阶段：挑战扭曲和假设
            if cbt_results:
                templates = self.stage_templates[DialogueStage.CHALLENGE]["distortion"]
                parts.append(templates[self.state.depth_level % len(templates)])
            elif assumptions:
                templates = self.stage_templates[DialogueStage.CHALLENGE]["assumption"]
                parts.append(templates[0].format(assumption=assumptions[0].content))
            elif arg_analysis.fallacies:
                templates = self.stage_templates[DialogueStage.CHALLENGE]["argument"]
                parts.append(templates[0])
        
        elif self.state.stage == DialogueStage.REFLECTION:
            # 反思阶段
            templates = self.stage_templates[DialogueStage.REFLECTION]["general"]
            parts.append(templates[self.state.depth_level % len(templates)])
            
            if self.state.concern_type != ConcernType.OTHER:
                concern_q = self.stage_templates[DialogueStage.REFLECTION]["concern"].get(self.state.concern_type)
                if concern_q:
                    parts.append(concern_q)
        
        elif self.state.stage == DialogueStage.INTEGRATION:
            # 整合阶段
            templates = self.stage_templates[DialogueStage.INTEGRATION]["general"]
            parts.append(templates[self.state.depth_level % len(templates)])
        
        return "\n\n".join(parts) if parts else "请继续说，我在听。"
    
    def _advance_stage(self):
        """推进对话阶段"""
        if self.state.stage == DialogueStage.ACKNOWLEDGMENT:
            self.state.stage = DialogueStage.EXPLORATION
        elif self.state.stage == DialogueStage.EXPLORATION:
            if self.state.turn_count >= 3:
                self.state.stage = DialogueStage.CHALLENGE
                self.state.depth_level = 0
        elif self.state.stage == DialogueStage.CHALLENGE:
            self.state.depth_level += 1
            if self.state.depth_level >= 3:
                self.state.stage = DialogueStage.REFLECTION
                self.state.depth_level = 0
        elif self.state.stage == DialogueStage.REFLECTION:
            self.state.depth_level += 1
            if self.state.depth_level >= 2:
                self.state.stage = DialogueStage.INTEGRATION
                self.state.depth_level = 0
    
    def _get_question_type(self) -> str:
        """获取当前问题类型"""
        mapping = {
            DialogueStage.ACKNOWLEDGMENT: "acknowledging",
            DialogueStage.EXPLORATION: "clarifying",
            DialogueStage.CHALLENGE: "probing",
            DialogueStage.REFLECTION: "reflective",
            DialogueStage.INTEGRATION: "synthesizing",
        }
        return mapping.get(self.state.stage, "clarifying")
    
    def get_state_summary(self) -> str:
        """获取状态摘要"""
        return (
            f"Stage: {self.state.stage.value} | "
            f"Turn: {self.state.turn_count} | "
            f"Depth: {self.state.depth_level} | "
            f"Concern: {self.state.concern_type.value} | "
            f"Distortions: {len(self.state.distortions_found)} | "
            f"Concepts: {len(self.state.concepts_clarified)}"
        )


def main():
    """测试苏格拉底对话引擎"""
    engine = SocraticEngine()
    
    print("=" * 50)
    print("人文AI · 苏格拉底式对话引擎 v1.0")
    print("=" * 50)
    
    # 测试1：认知扭曲对话
    print("\n[Test 1: Cognitive Distortion Dialogue]")
    print("-" * 40)
    
    r1 = engine.start("我这次考试没考好，我真是个废物，永远都这样了。")
    print(f"AI: {r1.text}")
    print(f"[{engine.get_state_summary()}]")
    
    r2 = engine.continue_dialogue("我觉得他们都在嘲笑我，所有人都看不起我。")
    print(f"\nUser: 觉得他们都在嘲笑我，所有人都看不起我。")
    print(f"AI: {r2.text}")
    print(f"[{engine.get_state_summary()}]")
    
    r3 = engine.continue_dialogue("我不知道该怎么办，感觉一切都完了。")
    print(f"\nUser: 我不知道该怎么办，感觉一切都完了。")
    print(f"AI: {r3.text}")
    print(f"[{engine.get_state_summary()}]")
    
    # 测试2：存在主义对话
    print("\n\n[Test 2: Existential Dialogue]")
    print("-" * 40)
    
    engine2 = SocraticEngine()
    r1 = engine2.start("活着到底有什么意义？每天重复同样的事情，感觉很空虚。")
    print(f"AI: {r1.text}")
    print(f"[{engine2.get_state_summary()}]")
    
    r2 = engine2.continue_dialogue("我不知道自己真正想要什么。")
    print(f"\nUser: 我不知道自己真正想要什么。")
    print(f"AI: {r2.text}")
    print(f"[{engine2.get_state_summary()}]")
    
    # 测试3：哲学讨论
    print("\n\n[Test 3: Philosophical Discussion]")
    print("-" * 40)
    
    engine3 = SocraticEngine()
    r1 = engine3.start("自由比平等更重要，因为自由是人的本质属性。")
    print(f"AI: {r1.text}")
    print(f"[{engine3.get_state_summary()}]")
    
    r2 = engine3.continue_dialogue("我认为如果没有自由，平等毫无意义。")
    print(f"\nUser: 我认为如果没有自由，平等毫无意义。")
    print(f"AI: {r2.text}")
    print(f"[{engine3.get_state_summary()}]")


if __name__ == "__main__":
    main()
