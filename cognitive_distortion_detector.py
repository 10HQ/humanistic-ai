"""
CBT认知扭曲检测器 - 人文AI核心模块 v1.0

基于规则引擎的认知扭曲识别与苏格拉底式提问生成

哲学基础：
- Beck认知模型：自动思维→中间信念→核心信念
- CBT原则：通过苏格拉底式提问引导觉察，而非直接反驳
- 唯物主义立场：心理现象是脑功能的表现，症状是适应不良的信号

作者：灵台未央
日期：2026-05-29
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class DistortionType(Enum):
    """认知扭曲类型枚举"""
    CATASTROPHIZING = "灾难化"
    BLACK_AND_WHITE = "非黑即白"
    OVERGENERALIZATION = "过度概括"
    SELECTIVE_ABSTRACTION = "选择性抽象"
    PERSONALIZATION = "个人化"
    MIND_READING = "读心术"
    EMOTIONAL_REASONING = "情绪推理"
    LABELING = "贴标签"
    SHOULD_STATEMENTS = "应该思维"
    MAGNIFICATION_MINIMIZATION = "放大/缩小"


@dataclass
class DistortionPattern:
    """认知扭曲模式定义"""
    type: DistortionType
    name: str
    description: str
    keywords: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    questioning_templates: List[str] = field(default_factory=list)


@dataclass
class DistortionResult:
    """检测结果"""
    distortion_type: DistortionType
    matched_text: str
    matched_pattern: str
    confidence: float
    start_pos: int
    end_pos: int


@dataclass
class ConversationAnalysis:
    """对话分析结果"""
    total_messages: int
    distortions_found: List[DistortionResult]
    distortion_frequency: Dict[DistortionType, int]
    dominant_distortion: Optional[DistortionType]
    pattern_sequence: List[DistortionType]


class CognitiveDistortionDetector:
    """
    认知扭曲检测器
    
    使用正则表达式+关键词匹配+模式识别的纯规则引擎，
    无需LLM API即可运行。
    
    用法：
        detector = CognitiveDistortionDetector()
        results = detector.detect("我这次彻底完蛋了")
        for r in results:
            print(detector.generate_response(r))
    """
    
    def __init__(self):
        self.patterns: Dict[DistortionType, DistortionPattern] = {}
        self._load_patterns()
        
    def _load_patterns(self) -> None:
        """加载所有认知扭曲模式定义"""
        
        self.patterns[DistortionType.CATASTROPHIZING] = DistortionPattern(
            type=DistortionType.CATASTROPHIZING,
            name="灾难化",
            description="将事情想象成最糟糕的结果，夸大负面后果",
            keywords=["完蛋", "完了", "糟了", "最坏", "灾难", "毁灭",
                      "无法承受", "受不了", "死定了", "没救了",
                      "彻底失败", "全完了", "世界末日", "这辈子都没希望"],
            patterns=[
                r"(如果|要是).*?就(完蛋|完了|糟了)",
                r"(一定|肯定|绝对).*?(失败|完蛋|不行)",
                r"最(坏|差|糟糕).*?(情况|结果|可能)",
                r"(无法|不能).*?(承受|忍受|面对)",
                r"这(是|就是).*?(灾难|毁灭|末日)",
                r"(彻底|完全).*?(完蛋|失败|没希望)"
            ],
            questioning_templates=[
                "最坏的情况发生的概率有多大？有没有其他可能性？",
                "如果最坏的情况真的发生了，你能做些什么来应对？",
                "过去遇到类似情况时，实际结果通常如何？",
                "有没有证据表明情况真的会这么糟糕？",
                "如果朋友遇到同样的情况，你会怎么安慰他/她？"
            ]
        )
        
        self.patterns[DistortionType.BLACK_AND_WHITE] = DistortionPattern(
            type=DistortionType.BLACK_AND_WHITE,
            name="非黑即白",
            description="用极端的两极化方式看待事物，没有中间地带",
            keywords=["总是", "从不", "永远", "绝对", "完全",
                      "要么", "不是...就是", "全部", "所有", "没有一个"],
            patterns=[
                r"(要么|不是).*?(就是|要么)",
                r"(总是|从不|永远).*?(这样|如此)",
                r"(完全|绝对).*?(没有|不行|错误)",
                r"所有.*?都.*?(不好|不行|错误)",
                r"没有(一个|任何).*?(好的|对的)"
            ],
            questioning_templates=[
                "事情真的只有两种可能吗？中间有没有其他选择？",
                "有没有例外的情况？",
                "如果用0-100分来评价，你会打多少分？",
                "有没有部分做得好、部分需要改进的地方？",
                "这种非此即彼的想法对你有什么影响？"
            ]
        )
        
        self.patterns[DistortionType.OVERGENERALIZATION] = DistortionPattern(
            type=DistortionType.OVERGENERALIZATION,
            name="过度概括",
            description="基于单一事件得出普遍性结论",
            keywords=["总是", "每次都", "从来都", "所有人",
                      "所有事", "每次", "永远", "全都"],
            patterns=[
                r"(每次|总是|从来).*?(都|就).*?(这样|如此)",
                r"(所有|全部).*?(人|事|情况).*?(都|就)",
                r"一(次|个).*?(就|都).*?(说明|代表|证明)",
                r"从(来|没有).*?(成功|做好|对过)"
            ],
            questioning_templates=[
                "这个结论是基于多少证据？有没有反例？",
                "一次经历就能代表所有情况吗？",
                "如果朋友遇到同样的事，你会给出同样的结论吗？",
                "过去有没有不同的经历？",
                "这种概括对你解决问题有帮助吗？"
            ]
        )
        
        self.patterns[DistortionType.SELECTIVE_ABSTRACTION] = DistortionPattern(
            type=DistortionType.SELECTIVE_ABSTRACTION,
            name="选择性抽象",
            description="只关注负面细节，忽视整体情况",
            keywords=["只有", "唯一", "就只", "仅仅", "只看到"],
            patterns=[
                r"(只|仅|就).*?(看到|关注|注意).*?(不好|错误|问题)",
                r"(虽然|尽管).*?(但是|可是|然而).*?(失败|不好)",
            ],
            questioning_templates=[
                "除了这个问题，还有没有其他方面值得关注？",
                "如果从整体来看，情况真的那么糟糕吗？",
                "你关注的这个方面占整体的多大比例？",
                "有没有被你忽略的积极信息？",
                "换个角度看，这个情况还有什么其他意义？"
            ]
        )
        
        self.patterns[DistortionType.PERSONALIZATION] = DistortionPattern(
            type=DistortionType.PERSONALIZATION,
            name="个人化",
            description="将外部事件归因于自己，过度承担责任",
            keywords=["都怪我", "是我的错", "因为我", "都是我的",
                      "我害的", "我造成的", "是我的责任"],
            patterns=[
                r"(都|全|就).*?怪我",
                r"因为(我|自己).*?(才|所以|导致)",
                r"如果(我|自己).*?不.*?就(不会|没有)",
                r"是我.*?(害|导致|造成|引起)",
            ],
            questioning_templates=[
                "这件事真的完全由你控制吗？还有没有其他因素？",
                "如果朋友遇到同样情况，你会认为全是他的责任吗？",
                "你能区分哪些是你能控制的，哪些不是？",
                "有没有其他可能的原因？",
                "过度承担责任对你有什么影响？"
            ]
        )
        
        self.patterns[DistortionType.MIND_READING] = DistortionPattern(
            type=DistortionType.MIND_READING,
            name="读心术",
            description="在没有充分证据的情况下，断定他人的想法或意图",
            keywords=["他觉得", "他认为", "他们觉得", "别人认为",
                      "肯定是想", "一定是觉得", "看不起", "讨厌我"],
            patterns=[
                r"(他|她|他们|别人).*?(觉得|认为|想).*?(肯定|一定|绝对)",
                r"(肯定|一定|绝对).*?(看不起|讨厌|不喜欢|嫌弃)",
                r"明摆着.*?(是|就是).*?(想|要|觉得)",
            ],
            questioning_templates=[
                "你有什么证据支持这个判断？",
                "有没有其他可能的解释？",
                "如果直接去问对方，结果会怎样？",
                "你以前猜测别人想法时，准确率有多高？",
                "这种猜测对你的人际关系有什么影响？"
            ]
        )
        
        self.patterns[DistortionType.EMOTIONAL_REASONING] = DistortionPattern(
            type=DistortionType.EMOTIONAL_REASONING,
            name="情绪推理",
            description="将情绪感受当作事实依据",
            keywords=["感觉", "觉得", "感到", "直觉", "心里觉得", "预感"],
            patterns=[
                r"(感觉|觉得|感到).*?(就是|一定是|肯定是)",
                r"因为.*?(害怕|担心|焦虑).*?所以.*?(一定|肯定)",
                r"心里.*?(觉得|感觉).*?(肯定|一定)"
            ],
            questioning_templates=[
                "感觉和事实是一回事吗？有没有感觉不好但实际很好的例子？",
                "你的这种感觉有多少事实依据？",
                "如果换个心情，你会怎么看待这件事？",
                "情绪通常持续多久？它真的能预测结果吗？",
                "有没有办法验证你的感觉是否准确？"
            ]
        )
        
        self.patterns[DistortionType.LABELING] = DistortionPattern(
            type=DistortionType.LABELING,
            name="贴标签",
            description="给自己或他人贴上笼统的负面标签",
            keywords=["我是个", "我就是个", "废物", "失败者", "没用",
                      "差劲", "笨蛋", "蠢货", "loser"],
            patterns=[
                r"(我|他|她).*?就(是|是个).*?(废物|失败|没用|差劲|笨蛋)",
                r"就是.*?个.*?(没用|废物|失败)"
            ],
            questioning_templates=[
                "用标签来描述一个人是否太简单化了？",
                "这个标签能涵盖这个人的全部吗？",
                "如果朋友这样评价自己，你会怎么回应？",
                "有没有不符合这个标签的行为或特质？",
                "把行为和人分开来看，具体是什么行为让你这样评价？"
            ]
        )
        
        self.patterns[DistortionType.SHOULD_STATEMENTS] = DistortionPattern(
            type=DistortionType.SHOULD_STATEMENTS,
            name="应该思维",
            description="用僵化的'应该'、'必须'要求自己或他人",
            keywords=["应该", "必须", "一定要", "不得不", "理应", "本该"],
            patterns=[
                r"(应该|必须|一定要).*?(这样|那样|做到|完成)",
                r"(理应|本该|应当).*?(如此|这样|更好)",
                r"怎么(能|可以).*?(这样|那样|如此)",
            ],
            questioning_templates=[
                "这个'应该'是从哪里来的？是合理的期望吗？",
                "如果做不到，最坏的结果是什么？",
                "有没有灵活处理的空间？",
                "这个标准对所有人都适用吗？",
                "如果放下这个'应该'，你会感觉轻松一些吗？"
            ]
        )
        
        self.patterns[DistortionType.MAGNIFICATION_MINIMIZATION] = DistortionPattern(
            type=DistortionType.MAGNIFICATION_MINIMIZATION,
            name="放大/缩小",
            description="夸大负面事件的重要性，缩小正面事件的价值",
            keywords=["太严重", "太可怕", "太糟糕", "微不足道",
                      "不值一提", "没什么", "小意思"],
            patterns=[
                r"(太|非常|极其).*?(严重|可怕|糟糕|恐怖)",
                r"(不过|只是|就).*?(小事|小问题|没什么)",
                r"(谁|大家|所有人).*?(都|也).*?(会|能).*?(做到|这样)",
            ],
            questioning_templates=[
                "这件事真的有那么严重吗？还是被放大了？",
                "如果朋友遇到同样的事，你会觉得是大事还是小事？",
                "你的成就是否被低估了？",
                "用1-10分来评价，这件事到底有多重要？",
                "这种放大或缩小的思维方式对你有什么影响？"
            ]
        )
    
    def detect(self, text: str) -> List[DistortionResult]:
        """检测文本中的认知扭曲"""
        results: List[DistortionResult] = []
        
        if not text or not text.strip():
            return results
        
        for distortion_type, pattern in self.patterns.items():
            # 关键词匹配
            for keyword in pattern.keywords:
                if keyword in text:
                    start = text.find(keyword)
                    end = start + len(keyword)
                    confidence = min(0.5 + len(keyword) * 0.05, 0.8)
                    
                    results.append(DistortionResult(
                        distortion_type=distortion_type,
                        matched_text=keyword,
                        matched_pattern=f"关键词: {keyword}",
                        confidence=confidence,
                        start_pos=start,
                        end_pos=end
                    ))
            
            # 正则表达式匹配
            for regex_pattern in pattern.patterns:
                matches = re.finditer(regex_pattern, text)
                for match in matches:
                    matched_text = match.group()
                    start = match.start()
                    end = match.end()
                    confidence = min(0.6 + len(matched_text) * 0.03, 0.95)
                    
                    is_duplicate = any(
                        r.start_pos == start and r.end_pos == end and r.distortion_type == distortion_type
                        for r in results
                    )
                    
                    if not is_duplicate:
                        results.append(DistortionResult(
                            distortion_type=distortion_type,
                            matched_text=matched_text,
                            matched_pattern=f"正则: {regex_pattern}",
                            confidence=confidence,
                            start_pos=start,
                            end_pos=end
                        ))
        
        results.sort(key=lambda x: x.confidence, reverse=True)
        return results
    
    def generate_response(self, distortion: DistortionResult) -> str:
        """生成苏格拉底式提问"""
        pattern = self.patterns.get(distortion.distortion_type)
        if not pattern or not pattern.questioning_templates:
            return "请尝试换个角度思考这个问题。"
        
        if distortion.confidence > 0.8:
            question = pattern.questioning_templates[0]
        elif distortion.confidence > 0.6:
            question = pattern.questioning_templates[len(pattern.questioning_templates) // 2]
        else:
            question = pattern.questioning_templates[-1]
        
        return f"我注意到「{distortion.matched_text}」可能是{pattern.name}的思维方式。{question}"
    
    def analyze_conversation(self, messages: List[str]) -> ConversationAnalysis:
        """分析对话历史中的扭曲模式"""
        all_distortions: List[DistortionResult] = []
        distortion_frequency: Dict[DistortionType, int] = {dt: 0 for dt in DistortionType}
        
        for message in messages:
            distortions = self.detect(message)
            all_distortions.extend(distortions)
            for d in distortions:
                distortion_frequency[d.distortion_type] += 1
        
        dominant_distortion = max(distortion_frequency, key=distortion_frequency.get)
        if distortion_frequency[dominant_distortion] == 0:
            dominant_distortion = None
        
        pattern_sequence = [d.distortion_type for d in all_distortions]
        
        return ConversationAnalysis(
            total_messages=len(messages),
            distortions_found=all_distortions,
            distortion_frequency=distortion_frequency,
            dominant_distortion=dominant_distortion,
            pattern_sequence=pattern_sequence
        )


def main():
    """测试用例"""
    detector = CognitiveDistortionDetector()
    
    print("=" * 60)
    print("人文AI · CBT认知扭曲检测器 v1.0")
    print("=" * 60)
    
    tests = [
        ("灾难化", "如果这次面试失败，我就彻底完蛋了，这辈子都没希望了。"),
        ("非黑即白", "要么成功，要么失败，没有中间道路可走。"),
        ("个人化", "都怪我，如果不是我，项目就不会失败，都是我的错。"),
        ("读心术", "他肯定觉得我很差劲，一定在背后嘲笑我。"),
        ("应该思维", "我应该做得更好，我必须成功，怎么能失败呢。"),
        ("贴标签", "我就是个废物，什么都做不好。"),
        ("情绪推理", "我感觉这件事一定会搞砸，心里觉得肯定不行。"),
        ("过度概括", "我每次都失败，从来都没有成功过。"),
    ]
    
    for name, text in tests:
        print(f"\n【{name}】")
        print(f"输入: {text}")
        results = detector.detect(text)
        for r in results:
            print(f"  → {r.distortion_type.value} (置信度: {r.confidence:.2f})")
            print(f"    {detector.generate_response(r)}")
    
    print("\n" + "=" * 60)
    print("对话分析测试")
    print("=" * 60)
    
    conversation = [
        "我这次考试没考好，我真是个废物。",
        "他们肯定都在笑话我。",
        "以后每次考试我都会失败，永远都这样了。",
        "都怪我太笨了，如果我不这么蠢就好了。"
    ]
    
    analysis = detector.analyze_conversation(conversation)
    print(f"\n总消息数: {analysis.total_messages}")
    print(f"扭曲总数: {len(analysis.distortions_found)}")
    print(f"主导扭曲: {analysis.dominant_distortion.value if analysis.dominant_distortion else '无'}")
    print("\n频率统计:")
    for dt, freq in analysis.distortion_frequency.items():
        if freq > 0:
            print(f"  {dt.value}: {freq}次")


if __name__ == "__main__":
    main()