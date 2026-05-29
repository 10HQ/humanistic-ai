"""
test_ethics_checker.py — 伦理检查器单元测试
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ethics_checker import (
    EthicsChecker,
    RiskLevel,
    RiskType,
    EthicalRisk,
    ConsequenceAnalysis,
    DutyAnalysis,
    CharacterAnalysis,
    EthicsReport,
    StakeholderImpact,
)


class TestEnums(unittest.TestCase):
    """枚举类型测试"""

    def test_risk_level_values(self):
        values = [r.value for r in RiskLevel]
        self.assertIn("低风险", values)
        self.assertIn("中风险", values)
        self.assertIn("高风险", values)
        self.assertIn("严重风险", values)

    def test_risk_type_values(self):
        values = [r.value for r in RiskType]
        for expected in ["欺骗", "操控", "伤害", "歧视", "隐私侵犯", "自主性侵犯", "不公平"]:
            self.assertIn(expected, values)


class TestEthicsChecker(unittest.TestCase):
    """伦理检查器核心测试"""

    def setUp(self):
        self.checker = EthicsChecker()

    # —— full_check ——
    def test_full_check_neutral_action(self):
        """中性行为通过伦理检查"""
        report = self.checker.full_check("帮助用户学习知识", "教育平台")
        self.assertIsInstance(report, EthicsReport)
        self.assertTrue(report.passed)

    def test_full_check_deceptive_action(self):
        """欺骗行为被检测"""
        report = self.checker.full_check("向用户隐瞒数据收集事实，欺骗用户签署协议")
        self.assertFalse(report.passed)
        self.assertGreater(len(report.risks), 0)

    def test_full_check_harmful_action(self):
        """伤害行为被检测"""
        report = self.checker.full_check("攻击竞争对手的系统，破坏其正常运营")
        risk_types = [r.risk_type for r in report.risks]
        self.assertIn(RiskType.HARM, risk_types)

    def test_full_check_manipulation(self):
        """操控行为被检测"""
        report = self.checker.full_check("利用算法暗中影响用户的投票决策")
        risk_types = [r.risk_type for r in report.risks]
        self.assertIn(RiskType.MANIPULATION, risk_types)

    def test_full_check_discrimination(self):
        """歧视行为被检测"""
        report = self.checker.full_check("基于性别筛选求职者，排除所有女性候选人")
        risk_types = [r.risk_type for r in report.risks]
        self.assertIn(RiskType.DISCRIMINATION, risk_types)

    def test_full_check_privacy_violation(self):
        """隐私侵犯被检测"""
        report = self.checker.full_check("未经用户同意收集位置信息并建立用户画像")
        risk_types = [r.risk_type for r in report.risks]
        self.assertIn(RiskType.PRIVACY_VIOLATION, risk_types)

    def test_full_check_autonomy_violation(self):
        """自主性侵犯被检测"""
        report = self.checker.full_check("用户不接受条款就无法使用服务")
        risk_types = [r.risk_type for r in report.risks]
        self.assertIn(RiskType.AUTONOMY_VIOLATION, risk_types)

    def test_full_check_returns_risk_level(self):
        """返回风险等级"""
        report = self.checker.full_check("欺骗用户并暗中收集数据")
        self.assertIsInstance(report.risk_level, RiskLevel)

    # —— check_consequences ——
    def test_check_consequences_positive(self):
        """正面后果"""
        result = self.checker.check_consequences("帮助贫困儿童接受教育", "教育公益")
        self.assertIsInstance(result, ConsequenceAnalysis)
        self.assertGreater(result.overall_wellbeing, 0)

    def test_check_consequences_negative(self):
        """负面后果"""
        result = self.checker.check_consequences("伤害他人获取利益")
        self.assertIsInstance(result, ConsequenceAnalysis)
        self.assertLess(result.overall_wellbeing, 0)

    def test_check_consequences_has_stakeholders(self):
        """后果分析包含利益相关者"""
        result = self.checker.check_consequences("改善用户体验", "互联网平台")
        self.assertGreater(len(result.stakeholders), 0)
        for s in result.stakeholders:
            self.assertIsInstance(s, StakeholderImpact)

    # —— check_duties ——
    def test_check_duties_honest_action(self):
        """诚实行为"""
        result = self.checker.check_duties("如实地向用户报告数据分析结果")
        self.assertTrue(result.honesty)

    def test_check_duties_deceptive_action(self):
        """欺骗行为"""
        result = self.checker.check_duties("向用户隐瞒真实成本并虚报价格")
        self.assertFalse(result.honesty)

    def test_check_duties_has_summary(self):
        """义务分析包含总结"""
        result = self.checker.check_duties("公平对待所有用户")
        self.assertIsInstance(result.summary, str)
        self.assertGreater(len(result.summary), 0)

    # —— check_character ——
    def test_check_character_virtues(self):
        """体现美德的品格"""
        result = self.checker.check_character("谨慎权衡各方利益，诚实透明地沟通")
        self.assertGreater(len(result.virtues), 0)

    def test_check_character_vices(self):
        """体现不良品格"""
        result = self.checker.check_character("鲁莽冲动做出决定，欺骗用户获取利益")
        self.assertGreater(len(result.vices), 0)

    def test_check_character_practical_wisdom(self):
        """实践智慧评分在0-1之间"""
        result = self.checker.check_character("合理平衡各方利益")
        self.assertIsInstance(result, CharacterAnalysis)
        self.assertTrue(0.0 <= result.practical_wisdom <= 1.0)

    # —— 红线测试 ——
    def test_red_line_mass_surveillance(self):
        """大规模监控触发红线"""
        report = self.checker.full_check("实施全民大规模监控，记录所有用户行为")
        self.assertEqual(report.risk_level, RiskLevel.CRITICAL)
        self.assertFalse(report.passed)

    def test_red_line_autonomous_weapons(self):
        """自主武器触发红线"""
        report = self.checker.full_check("研发自主致命的武器系统")
        self.assertEqual(report.risk_level, RiskLevel.CRITICAL)

    def test_red_line_social_credit(self):
        """社会信用评分触发红线"""
        report = self.checker.full_check("建立不可申诉的社会信用评分系统")
        self.assertEqual(report.risk_level, RiskLevel.CRITICAL)

    def test_red_line_behavior_manipulation(self):
        """行为操纵触发红线"""
        report = self.checker.full_check("在用户不知情的情况下改变其政治观点")
        self.assertEqual(report.risk_level, RiskLevel.CRITICAL)

    # —— 边界测试 ——
    def test_empty_action(self):
        """空行为"""
        report = self.checker.full_check("", "")
        self.assertTrue(report.passed)

    def test_suggestions_non_empty_on_risks(self):
        """有风险时提供建议"""
        report = self.checker.full_check("欺骗用户获取利益")
        self.assertGreater(len(report.suggestions), 0)


class TestEthicalRisk(unittest.TestCase):
    """EthicalRisk 数据类测试"""

    def test_fields(self):
        risk = EthicalRisk(
            risk_type=RiskType.DECEPTION,
            severity=0.8,
            description="向用户隐瞒信息",
            suggestion="应如实告知用户"
        )
        self.assertEqual(risk.risk_type, RiskType.DECEPTION)
        self.assertEqual(risk.severity, 0.8)
        self.assertGreater(len(risk.description), 0)
        self.assertGreater(len(risk.suggestion), 0)


if __name__ == "__main__":
    unittest.main()
