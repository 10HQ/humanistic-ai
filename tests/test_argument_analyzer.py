"""
test_argument_analyzer.py — 论证分析器单元测试
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from argument_analyzer import (
    ArgumentAnalyzer,
    FallacyType,
    Fallacy,
    ArgumentStructure,
    ArgumentAnalysis,
)


class TestFallacyType(unittest.TestCase):
    """谬误类型枚举测试"""

    def test_all_types_exist(self):
        expected = [
            "循环论证", "偷换概念", "诉诸权威", "滑坡谬误",
            "虚假二分", "人身攻击", "稻草人", "诉诸情感",
            "以偏概全", "诉诸无知",
        ]
        values = [f.value for f in FallacyType]
        for e in expected:
            self.assertIn(e, values)


class TestArgumentAnalyzer(unittest.TestCase):
    """论证分析器核心测试"""

    def setUp(self):
        self.analyzer = ArgumentAnalyzer()

    # —— 循环论证 ——
    def test_circular_reasoning(self):
        """循环论证：「因为政客都不诚实，所以所有政客不诚实」"""
        analysis = self.analyzer.analyze("所有政客都是不诚实的，因为政客都不诚实。")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.CIRCULAR_REASONING, types)

    # —— 诉诸权威 ——
    def test_appeal_to_authority(self):
        """诉诸权威：引用专家但无证据"""
        analysis = self.analyzer.analyze("专家说这样是对的，所以一定没错。")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.APPEAL_TO_AUTHORITY, types)

    def test_appeal_to_authority_famous_name(self):
        """诉诸权威：引用爱因斯坦"""
        analysis = self.analyzer.analyze("爱因斯坦说过宇宙是永恒的，所以宇宙一定是永恒的。")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.APPEAL_TO_AUTHORITY, types)

    # —— 滑坡谬误 ——
    def test_slippery_slope(self):
        """滑坡谬误：如果允许X就会导致Y"""
        analysis = self.analyzer.analyze("如果允许学生用手机，接下来他们就会整天玩游戏，最终成绩一落千丈。")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.SLIPPERY_SLOPE, types)

    # —— 虚假二分 ——
    def test_false_dilemma(self):
        """虚假二分：要么X要么Y"""
        analysis = self.analyzer.analyze("要么支持这项政策，要么就是不爱这个国家，没有别的选择。")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.FALSE_DILEMMA, types)

    # —— 人身攻击 ——
    def test_ad_hominem(self):
        """人身攻击"""
        analysis = self.analyzer.analyze("你一个连大学都没上过的人，有什么资格谈教育？")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.AD_HOMINEM, types)

    # —— 稻草人 ——
    def test_straw_man(self):
        """稻草人谬误：歪曲对方观点"""
        analysis = self.analyzer.analyze("你的意思无非是说，所有人都应该听你的话，这不就是独裁吗？")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.STRAW_MAN, types)

    # —— 偷换概念 ——
    def test_equivocation(self):
        """偷换概念"""
        analysis = self.analyzer.analyze("你昨天说我们应该保护自由，今天却说要限制自由，这不是自相矛盾吗？")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.EQUIVOCATION, types)

    # —— 诉诸情感 ——
    def test_appeal_to_emotion(self):
        """诉诸情感"""
        analysis = self.analyzer.analyze("想想那些贫困山区的孩子们，你怎么能不支持这项政策呢？")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.APPEAL_TO_EMOTION, types)

    def test_appeal_to_emotion_rhetorical(self):
        """诉诸情感：反问句"""
        analysis = self.analyzer.analyze("难道你能忍心看着这些老人无家可归吗？")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.APPEAL_TO_EMOTION, types)

    # —— 以偏概全 ——
    def test_hasty_generalization(self):
        """以偏概全"""
        analysis = self.analyzer.analyze("我认识的几个北方人都很豪爽，所以所有北方人都豪爽。")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.HASTY_GENERALIZATION, types)

    # —— 诉诸无知 ——
    def test_appeal_to_ignorance(self):
        """诉诸无知"""
        analysis = self.analyzer.analyze("没有人能证明外星人不存在，所以外星人一定存在。")
        types = [f.type for f in analysis.fallacies]
        self.assertIn(FallacyType.APPEAL_TO_IGNORANCE, types)

    # —— 无谬误 ——
    def test_no_fallacy_clean_argument(self):
        """无谬误的清晰论证"""
        analysis = self.analyzer.analyze("水在100摄氏度时沸腾，这是经过反复实验验证的物理事实。")
        self.assertEqual(len(analysis.fallacies), 0)

    # —— 整体评分 ——
    def test_overall_score_range(self):
        """整体评分在0-1区间"""
        analysis = self.analyzer.analyze("因为所有运动员都应该遵守规则，所以足球运动员也不例外。")
        self.assertIsInstance(analysis, ArgumentAnalysis)
        self.assertTrue(0.0 <= analysis.overall_score <= 1.0)

    def test_fallacy_lowers_score(self):
        """谬误降低评分"""
        clean = self.analyzer.analyze("经过反复验证的实验结果表明，该药物对90%的患者有效。")
        fallacious = self.analyzer.analyze("所有政客都是不诚实的，因为政客都不诚实。")
        self.assertGreater(clean.overall_score, fallacious.overall_score)

    # —— 论证结构 ——
    def test_argument_structure_has_premises(self):
        """论证结构包含前提识别"""
        analysis = self.analyzer.analyze("因为人都会死，苏格拉底是人，所以苏格拉底会死。")
        self.assertIsInstance(analysis.structure, ArgumentStructure)

    def test_argument_structure_validity_and_strength(self):
        """论证结构包含有效性和力度"""
        analysis = self.analyzer.analyze("因为水往低处流，所以放在高处的水会往下流。")
        s = analysis.structure
        self.assertTrue(0.0 <= s.validity <= 1.0)
        self.assertTrue(0.0 <= s.strength <= 1.0)

    # —— generate_critique ——
    def test_generate_critique_returns_string(self):
        """generate_critique 返回批评估"""
        analysis = self.analyzer.analyze("所有政客都是不诚实的，因为政客都不诚实。")
        critique = self.analyzer.generate_critique(analysis)
        self.assertIsInstance(critique, str)
        self.assertGreater(len(critique), 0)

    # —— 改进建议 ——
    def test_improvement_suggestions_on_fallacies(self):
        """有谬误时提供改进建议"""
        analysis = self.analyzer.analyze("所有政客都是不诚实的，因为政客都不诚实。")
        self.assertGreater(len(analysis.improvement_suggestions), 0)

    # —— Fallacy dataclass ——
    def test_fallacy_has_severity(self):
        """谬误包含严重程度"""
        analysis = self.analyzer.analyze("所有政客都是不诚实的，因为政客都不诚实。")
        for f in analysis.fallacies:
            self.assertTrue(0.0 <= f.severity <= 1.0)

    def test_fallacy_has_position(self):
        """谬误包含位置"""
        analysis = self.analyzer.analyze("专家说对就是对。")
        for f in analysis.fallacies:
            start, end = f.position
            self.assertLess(start, end)


if __name__ == "__main__":
    unittest.main()
