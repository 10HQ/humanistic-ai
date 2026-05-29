"""
test_humanistic_ai.py — 人文AI引擎单元测试
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from humanistic_ai import HumanisticAI, HumanisticAnalysis


class TestHumanisticAI(unittest.TestCase):
    """人文AI引擎核心测试"""

    def setUp(self):
        self.ai = HumanisticAI()

    # —— 初始化 ——
    def test_init_without_semantic(self):
        """默认不启用语义分析"""
        ai = HumanisticAI()
        self.assertFalse(ai.enable_semantic)

    def test_init_submodules_initialized(self):
        """子模块正确初始化"""
        self.assertIsNotNone(self.ai.cbt)
        self.assertIsNotNone(self.ai.clarifier)
        self.assertIsNotNone(self.ai.ethics)
        self.assertIsNotNone(self.ai.argument)
        self.assertIsNotNone(self.ai.socratic)

    # —— analyze ——
    def test_analyze_returns_analysis(self):
        """analyze 返回 HumanisticAnalysis"""
        result = self.ai.analyze("自由比平等更重要")
        self.assertIsInstance(result, HumanisticAnalysis)

    def test_analyze_preserves_original_text(self):
        """保留原始文本"""
        text = "自由是人的本质属性"
        result = self.ai.analyze(text)
        self.assertEqual(result.original_text, text)

    def test_analyze_has_timestamp(self):
        """分析结果包含时间戳"""
        result = self.ai.analyze("正义就是给每个人以其应得的东西")
        self.assertIsInstance(result.timestamp, str)
        self.assertGreater(len(result.timestamp), 0)

    def test_analyze_with_context(self):
        """带上下文分析"""
        result = self.ai.analyze("我认为这个方案不合适", "商业决策评审会")
        self.assertEqual(result.context, "商业决策评审会")

    def test_analyze_detects_distortions(self):
        """检测认知扭曲"""
        result = self.ai.analyze("我彻底完蛋了，这次肯定失败了。")
        self.assertGreater(len(result.cognitive_distortions), 0)

    def test_analyze_identifies_concepts(self):
        """识别概念"""
        result = self.ai.analyze("自由比平等更重要，正义需要法律保障")
        self.assertGreater(len(result.core_concepts), 0)

    def test_analyze_extracts_assumptions(self):
        """提取假设"""
        result = self.ai.analyze("因为人天生自由，所以任何限制都不合理")
        self.assertGreater(len(result.assumptions), 0)

    def test_analyze_detects_fallacies(self):
        """检测论证谬误"""
        result = self.ai.analyze("所有政客都不诚实，因为政客都不诚实。")
        self.assertGreater(len(result.fallacies), 0)

    def test_analyze_has_argument_score(self):
        """包含论证评分"""
        result = self.ai.analyze("自由是人的本质属性")
        self.assertTrue(0.0 <= result.argument_score <= 1.0)

    def test_analyze_has_overall_assessment(self):
        """包含总体评估"""
        result = self.ai.analyze("自由比平等更重要")
        self.assertIsInstance(result.overall_assessment, str)

    def test_analyze_generates_socratic_questions(self):
        """生成苏格拉底式提问"""
        result = self.ai.analyze("我考试没考好，我真是个废物")
        self.assertIsInstance(result.socratic_questions, list)

    # —— respond ——
    def test_respond_returns_string(self):
        """respond 返回字符串"""
        response = self.ai.respond("我最近感觉很迷茫")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_respond_with_distortion(self):
        """对认知扭曲文本的回应"""
        response = self.ai.respond("我就是个废物，什么都做不好。")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_respond_normal_text(self):
        """对正常文本的回应"""
        response = self.ai.respond("今天天气真好")
        self.assertIsInstance(response, str)

    # —— dialogue ——
    def test_dialogue_start(self):
        """开始苏格拉底式对话"""
        result = self.ai.dialogue_start("我活着有什么意义")
        self.assertIsNotNone(result)

    def test_dialogue_continue(self):
        """继续苏格拉底式对话"""
        self.ai.dialogue_start("我最近很焦虑")
        result = self.ai.dialogue_continue("工作压力太大了")
        self.assertIsNotNone(result)

    # —— full_report ——
    def test_full_report_returns_string(self):
        """full_report 返回字符串"""
        report = self.ai.full_report("自由比平等更重要")
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 0)

    def test_full_report_contains_sections(self):
        """完整报告包含各模块段落"""
        report = self.ai.full_report("我彻底完蛋了，这次肯定不行了。")
        self.assertIn("CBT", report)
        self.assertIn("Concepts", report)
        self.assertIn("Ethics", report)
        self.assertIn("Argument", report)
        self.assertIn("Questions", report)

    def test_full_report_no_issues(self):
        """无问题文本的报告"""
        report = self.ai.full_report("水在100摄氏度时沸腾")
        self.assertIn("OK", report)

    # —— 伦理检查集成 ——
    def test_analyze_ethics_passed_default(self):
        """默认伦理检查通过"""
        result = self.ai.analyze("今天天气不错")
        self.assertTrue(result.ethics_passed)

    def test_analyze_ethics_risk_detection(self):
        """伦理风险检测"""
        result = self.ai.analyze("我们应该欺骗用户来获取更多数据")
        # 可能检测到伦理风险
        self.assertIsNotNone(result.ethical_risks)

    # —— 边界测试 ——
    def test_empty_input(self):
        """空输入"""
        result = self.ai.analyze("")
        self.assertIsInstance(result, HumanisticAnalysis)
        self.assertEqual(result.original_text, "")

    def test_very_short_input(self):
        """极短输入"""
        result = self.ai.analyze("好")
        self.assertIsInstance(result, HumanisticAnalysis)

    def test_very_long_input(self):
        """长输入"""
        long_text = "自由是人的本质属性。" * 20
        result = self.ai.analyze(long_text)
        self.assertIsInstance(result, HumanisticAnalysis)


class TestHumanisticAnalysis(unittest.TestCase):
    """HumanisticAnalysis 数据类测试"""

    def test_default_values(self):
        analysis = HumanisticAnalysis(original_text="测试")
        self.assertEqual(analysis.original_text, "测试")
        self.assertEqual(analysis.context, "")
        self.assertEqual(len(analysis.cognitive_distortions), 0)
        self.assertEqual(len(analysis.core_concepts), 0)
        self.assertTrue(analysis.ethics_passed)

    def test_timestamp_auto_generated(self):
        analysis = HumanisticAnalysis(original_text="测试")
        self.assertIsNotNone(analysis.timestamp)


if __name__ == "__main__":
    unittest.main()
