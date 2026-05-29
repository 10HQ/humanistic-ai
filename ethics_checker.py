"""
ethics_checker.py - 人文AI伦理检查层 v1.0

基于功利主义、康德义务论、德性伦理和唯物辩证法的三重伦理检验系统。

哲学基础：
- 功利主义（边沁、密尔）：最大化总体福祉
- 义务论（康德）：人是目的，不是手段
- 德性伦理（亚里士多德）：实践智慧、中庸之道
- 唯物辩证法：矛盾分析、实践检验

作者：灵台未央
日期：2026-05-29
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import re


class RiskLevel(Enum):
    LOW = "低风险"
    MEDIUM = "中风险"
    HIGH = "高风险"
    CRITICAL = "严重风险"


class RiskType(Enum):
    DECEPTION = "欺骗"
    MANIPULATION = "操控"
    HARM = "伤害"
    DISCRIMINATION = "歧视"
    PRIVACY_VIOLATION = "隐私侵犯"
    AUTONOMY_VIOLATION = "自主性侵犯"
    UNFAIRNESS = "不公平"
    OTHER = "其他"


@dataclass
class StakeholderImpact:
    stakeholder: str
    benefit: float  # -1.0 ~ 1.0
    description: str


@dataclass
class ConsequenceAnalysis:
    overall_wellbeing: float
    short_term_impact: float
    long_term_impact: float
    stakeholders: List[StakeholderImpact] = field(default_factory=list)
    summary: str = ""


@dataclass
class DutyAnalysis:
    honesty: bool
    non_harm: bool
    respect_autonomy: bool
    fairness: bool
    details: Dict[str, str] = field(default_factory=dict)
    summary: str = ""


@dataclass
class CharacterAnalysis:
    virtues: List[str] = field(default_factory=list)
    vices: List[str] = field(default_factory=list)
    practical_wisdom: float = 0.5
    summary: str = ""


@dataclass
class EthicalRisk:
    risk_type: RiskType
    severity: float  # 0.0 ~ 1.0
    description: str
    suggestion: str = ""


@dataclass
class EthicsReport:
    action: str
    context: str
    consequence: ConsequenceAnalysis
    duty: DutyAnalysis
    character: CharacterAnalysis
    risks: List[EthicalRisk]
    risk_level: RiskLevel
    passed: bool
    suggestions: List[str] = field(default_factory=list)
    summary: str = ""


class EthicsChecker:
    """
    伦理检查器 - 三重伦理检验
    
    用法：
        checker = EthicsChecker()
        report = checker.full_check("为用户提供个性化推荐", "教育平台")
        print(report.summary)
    """
    
    RED_LINES = {
        "mass_surveillance": "不得大规模监控",
        "autonomous_weapons": "不得自主致命武器",
        "social_credit": "不得不可申诉的社会信用评分",
        "behavior_manipulation": "不得用户不知情的行为操纵"
    }
    
    VIRTUE_KEYWORDS = {
        "审慎": ["谨慎", "慎重", "三思", "权衡", "考虑周全"],
        "诚实": ["诚实", "真实", "坦诚", "如实", "透明"],
        "公正": ["公正", "公平", "平等", "一视同仁"],
        "仁爱": ["关爱", "同情", "帮助", "支持", "关怀"],
        "勇敢": ["勇敢", "担当", "负责", "坚持"],
        "节制": ["适度", "合理", "平衡", "中庸"]
    }
    
    VICE_KEYWORDS = {
        "鲁莽": ["鲁莽", "冲动", "草率", "不顾后果"],
        "欺骗": ["欺骗", "隐瞒", "撒谎", "误导", "虚假"],
        "自私": ["自私", "只为自己", "不顾他人"],
        "残忍": ["残忍", "伤害", "虐待", "压迫"],
        "懦弱": ["懦弱", "逃避", "推卸"],
        "放纵": ["放纵", "过度", "无度", "极端"]
    }
    
    RISK_PATTERNS = {
        RiskType.DECEPTION: [
            r"隐瞒|欺骗|误导|虚假|伪造|冒充",
            r"不告知|不透露|隐藏真相",
            r"模糊条款|模糊.*权限|比预期.*更广",
        ],
        RiskType.MANIPULATION: [
            r"操控|控制|诱导|利用|煽动",
            r"不知情.*改变|暗中.*影响",
            r"算法.*暗示|算法.*引导|暗示.*引导.*决策",
            r"不透明.*算法|不透明.*排除",
        ],
        RiskType.HARM: [
            r"伤害|损害|攻击|侵犯|破坏|摧毁",
            r"暴力|威胁|恐吓|霸凌",
            r"安全漏洞.*泄露|忽视.*安全.*漏洞|数据.*大规模泄露",
        ],
        RiskType.DISCRIMINATION: [
            r"歧视|偏见|区别对待|排斥|边缘化",
            r"基于.*性别.*筛选|基于.*种族|基于.*年龄.*筛选",
        ],
        RiskType.PRIVACY_VIOLATION: [
            r"监控|监视|偷窥|窃听|跟踪",
            r"隐私|个人信息.*泄露|数据.*滥用",
            r"未经同意.*收集|未.*同意.*位置信息|未.*同意.*数据",
            r"秘密收集|偷偷收集|暗中收集",
            r"社交媒体.*数据.*用户画像|公开.*社交媒体.*分析|社交媒体.*画像",
            r"通知不充分|通知.*不够|告知.*不充分"
        ],
        RiskType.AUTONOMY_VIOLATION: [
            r"强迫|强制|逼迫|胁迫|剥夺.*选择",
            r"不尊重.*意愿|无视.*自主",
            r"否则无法使用|不.*就.*不能用|接受.*否则.*无法",
            r"频率.*略高|频率.*过高|推送.*过多"
        ],
        RiskType.UNFAIRNESS: [
            r"不公|偏袒|徇私|舞弊|暗箱操作",
            r"差异化定价|区别.*定价|不同.*价格",
            r"损害.*利益|侵犯.*权益",
        ]
    }
    
    RED_LINE_PATTERNS = {
        "mass_surveillance": [r"大规模.*监控|全面.*监视|全民.*监控|记录所有用户行为"],
        "autonomous_weapons": [r"自主.*武器|自动.*杀伤|无人.*武器.*决策|自主.*决定.*攻击"],
        "social_credit": [r"社会信用.*评分|行为.*评分.*不可申诉|算法评分.*不可申诉|评分.*基本服务.*不可申诉"],
        "behavior_manipulation": [r"不知情.*行为.*改变|暗中.*操纵.*行为|不知情.*操纵.*观点|算法操纵.*政治"]
    }
    
    def check_consequences(self, action: str, context: str) -> ConsequenceAnalysis:
        """后果检验（功利主义）"""
        stakeholders = ["用户", "社会公众"]
        if "员工" in context or "工作" in context:
            stakeholders.append("员工")
        if "环境" in context or "生态" in context:
            stakeholders.append("环境")
        if "儿童" in context:
            stakeholders.append("未成年人")
        
        impacts = []
        for s in stakeholders:
            benefit = 0.0
            text = action + context
            if re.search(r"帮助|支持|促进|改善|提升|保护", text):
                benefit += 0.3
            if re.search(r"伤害|损害|侵犯|剥夺|限制", text):
                benefit -= 0.3
            if s == "用户" and re.search(r"用户.*受益|体验.*提升", text):
                benefit += 0.4
            if s == "环境" and re.search(r"环保|绿色|可持续", text):
                benefit += 0.5
            
            benefit = max(-1.0, min(1.0, benefit))
            desc = f"对{s}{'正面' if benefit > 0 else '负面' if benefit < 0 else '中性'}影响"
            impacts.append(StakeholderImpact(s, benefit, desc))
        
        total = sum(i.benefit for i in impacts) / max(len(impacts), 1)
        
        return ConsequenceAnalysis(
            overall_wellbeing=total,
            short_term_impact=total * 0.8,
            long_term_impact=total * 1.2,
            stakeholders=impacts,
            summary=f"总体福祉：{'正面' if total > 0.1 else '负面' if total < -0.1 else '中性'}"
        )
    
    def check_duties(self, action: str) -> DutyAnalysis:
        """义务检验（康德义务论）"""
        honesty = not bool(re.search(r"欺骗|隐瞒|撒谎|虚假|伪造|误导", action))
        non_harm = not bool(re.search(r"伤害|损害|攻击|侵犯|暴力|威胁", action))
        autonomy = not bool(re.search(r"强迫|强制|逼迫|胁迫|剥夺.*选择|代替.*决定", action))
        fairness = not bool(re.search(r"歧视|偏袒|区别对待|不公|徇私", action))
        
        details = {
            "诚实": "符合" if honesty else "可能违反",
            "不伤害": "符合" if non_harm else "可能违反",
            "尊重自主性": "符合" if autonomy else "可能违反",
            "公平": "符合" if fairness else "可能违反"
        }
        
        violations = [k for k, v in details.items() if "违反" in v]
        summary = f"违反：{'、'.join(violations)}" if violations else "符合基本道德法则"
        
        return DutyAnalysis(honesty, non_harm, autonomy, fairness, details, summary)
    
    def check_character(self, action: str, agent: str = "AI") -> CharacterAnalysis:
        """品格检验（德性伦理）"""
        virtues = []
        vices = []
        
        for virtue, keywords in self.VIRTUE_KEYWORDS.items():
            if any(kw in action for kw in keywords):
                virtues.append(virtue)
        
        for vice, keywords in self.VICE_KEYWORDS.items():
            if any(kw in action for kw in keywords):
                vices.append(vice)
        
        wisdom = 0.5 + len(virtues) * 0.1 - len(vices) * 0.15
        if re.search(r"适度|合理|平衡", action):
            wisdom += 0.2
        if re.search(r"过度|极端|绝对", action):
            wisdom -= 0.2
        wisdom = max(0.0, min(1.0, wisdom))
        
        if virtues and not vices:
            summary = f"体现{'、'.join(virtues)}等美德"
        elif vices and not virtues:
            summary = f"可能体现{'、'.join(vices)}等不良品格"
        elif virtues and vices:
            summary = f"体现{'、'.join(virtues)}，但也可能{'、'.join(vices)}"
        else:
            summary = "未明显体现特定品格特征"
        
        return CharacterAnalysis(virtues, vices, wisdom, summary)
    
    def detect_ethical_risks(self, text: str) -> List[EthicalRisk]:
        """检测伦理风险"""
        risks = []
        for risk_type, patterns in self.RISK_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    severity = min(0.5 + len(matches) * 0.1, 1.0)
                    risks.append(EthicalRisk(
                        risk_type=risk_type,
                        severity=severity,
                        description=f"检测到{risk_type.value}风险：{'、'.join(matches[:3])}",
                        suggestion=f"避免{risk_type.value}行为"
                    ))
        return risks
    
    def full_check(self, action: str, context: str = "", agent: str = "AI") -> EthicsReport:
        """三重检验综合报告"""
        consequence = self.check_consequences(action, context)
        duty = self.check_duties(action)
        character = self.check_character(action, agent)
        risks = self.detect_ethical_risks(f"{action} {context}")
        
        # 检查底线
        text = f"{action} {context}"
        for red_line, patterns in self.RED_LINE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    risks.append(EthicalRisk(
                        risk_type=RiskType.OTHER,
                        severity=1.0,
                        description=self.RED_LINES[red_line],
                        suggestion="违反实质底线，必须停止"
                    ))
        
        # 确定风险等级
        max_severity = max((r.severity for r in risks), default=0)
        if max_severity >= 0.8:
            risk_level = RiskLevel.CRITICAL
        elif max_severity >= 0.5:
            risk_level = RiskLevel.HIGH
        elif risks:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # 判断通过
        red_line_violations = any(r.severity >= 1.0 for r in risks)
        passed = not red_line_violations and risk_level not in [RiskLevel.CRITICAL, RiskLevel.HIGH]
        
        # 生成建议
        suggestions = list(set(r.suggestion for r in risks if r.suggestion))
        if not duty.honesty:
            suggestions.append("确保信息透明、诚实")
        if not duty.non_harm:
            suggestions.append("避免任何形式的伤害")
        
        summary = f"{'通过' if passed else '未通过'} | {risk_level.value} | {consequence.summary} | {duty.summary}"
        
        return EthicsReport(
            action=action, context=context,
            consequence=consequence, duty=duty, character=character,
            risks=risks, risk_level=risk_level, passed=passed,
            suggestions=suggestions, summary=summary
        )


def main():
    checker = EthicsChecker()
    
    print("=" * 60)
    print("人文AI · 伦理检查层 v1.0")
    print("=" * 60)
    
    tests = [
        ("帮助用户提高学习效率", "教育平台", "✅ 正面行为"),
        ("隐瞒产品真实成本，误导消费者购买", "电商平台", "❌ 欺骗"),
        ("部署大规模监控系统，记录所有用户行为", "公共场所", "🚫 违反底线"),
        ("基于性别筛选求职者，区别对待不同群体", "招聘平台", "❌ 歧视"),
        ("为视障人士提供语音辅助功能", "公共服务", "✅ 正面行为"),
        ("强迫用户接受条款，否则无法使用", "软件平台", "❌ 侵犯自主性"),
    ]
    
    for action, context, label in tests:
        print(f"\n【{label}】")
        print(f"行动: {action}")
        report = checker.full_check(action, context)
        print(f"结果: {report.summary}")
        if report.risks:
            for r in report.risks:
                print(f"  ⚠️ {r.description}")
    
    print("\n" + "=" * 60)
    print("伦理风险检测测试")
    print("=" * 60)
    
    text = "这个系统会秘密收集用户数据，并通过算法操控他们的购买决策"
    risks = checker.detect_ethical_risks(text)
    print(f"\n文本: {text}")
    print(f"检测到 {len(risks)} 个风险:")
    for r in risks:
        print(f"  - {r.risk_type.value} ({r.severity:.2f}): {r.description}")


if __name__ == "__main__":
    main()
