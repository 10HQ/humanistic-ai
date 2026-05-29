"""
test_cognitive_distortion_detector.py — CBT认知扭曲检测器单元测试
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cognitive_distortion_detector import (
    CognitiveDistortionDetector,
    DistortionType,
    DistortionResult,
    DistortionPattern,
    ConversationAnalysis,
)


class TestDistortionType(unittest.TestCase):
    """认知扭曲类型枚举测试"""

    def test_all_types_exist(self):
        """验证10种认知扭曲类型均已定义"""
        expected = [
            "灾难化", "非黑即白", "过度概括", "选择性抽象",
            "个人化", "读心术", "情绪推理", "贴标签",
            "应该思维", "放大/缩小",
        ]
        for name in expected:
            self.assertIn(name, [d.value for d in DistortionType])

    def test_enum_uniqueness(self):
        """验证枚举值唯一"""
        values = [d.value for d in DistortionType]
        self.assertEqual(len(values), len(set(values)))


class TestCognitiveDistortionDetector(unittest.TestCase):
    """认知扭曲检测器核心测试"""

    def setUp(self):
        self.detector = CognitiveDistortionDetector()

    # —— 灾难化 ——
    def test_catastrophizing_basic(self):
        """灾难化：如果X就完蛋了"""
        results = self.detector.detect("如果这次面试失败，我就彻底完蛋了。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.CATASTROPHIZING, types)

    def test_catastrophizing_life_ruined(self):
        """灾难化：人生完了"""
        results = self.detector.detect("失去这份工作，我的人生就完了。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.CATASTROPHIZING, types)

    def test_catastrophizing_lonely_forever(self):
        """灾难化：孤独终老"""
        results = self.detector.detect("如果分手了，我这辈子都会孤独终老。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.CATASTROPHIZING, types)

    # —— 非黑即白 ——
    def test_black_and_white_either_or(self):
        """非黑即白：要么X要么Y"""
        results = self.detector.detect("要么成功，要么失败，没有中间道路可走。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.BLACK_AND_WHITE, types)

    def test_black_and_white_always(self):
        """非黑即白：总是如此"""
        results = self.detector.detect("我总是把事情搞得一团糟。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.BLACK_AND_WHITE, types)

    # —— 过度概括 ——
    def test_overgeneralization_every_time(self):
        """过度概括：每次都失败"""
        results = self.detector.detect("我每次都失败，从来都没有成功过。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.OVERGENERALIZATION, types)

    def test_overgeneralization_single_event(self):
        """过度概括：一次代表全部"""
        results = self.detector.detect("一个项目失败，说明我没有做任何事的才能。")
        types = [r.distortion_type for r in results]
        # 可能匹配过度概括或灾难化
        self.assertTrue(len(results) > 0)

    # —— 个人化 ——
    def test_personalization_blame_self(self):
        """个人化：都怪我"""
        results = self.detector.detect("都怪我，如果不是我，项目就不会失败。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.PERSONALIZATION, types)

    # —— 读心术 ——
    def test_mind_reading_others_thoughts(self):
        """读心术：他肯定觉得"""
        results = self.detector.detect("他肯定觉得我很差劲，一定在背后嘲笑我。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.MIND_READING, types)

    def test_mind_reading_no_reply(self):
        """读心术：没回消息就是生气了"""
        results = self.detector.detect("她没有回我消息，一定是生我的气了。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.MIND_READING, types)

    # —— 贴标签 ——
    def test_labeling_self(self):
        """贴标签：我就是个废物"""
        results = self.detector.detect("我就是个废物，什么都做不好。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.LABELING, types)

    def test_labeling_others(self):
        """贴标签：他是人渣"""
        results = self.detector.detect("他是个人渣，完全不值得信任。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.LABELING, types)

    # —— 应该思维 ——
    def test_should_statements(self):
        """应该思维：我应该做得更好"""
        results = self.detector.detect("我应该做得更好，我必须成功。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.SHOULD_STATEMENTS, types)

    def test_should_age_pressure(self):
        """应该思维：三十岁必须"""
        results = self.detector.detect("三十岁了必须有房有车，否则就是失败人生。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.SHOULD_STATEMENTS, types)

    # —— 情绪推理 ——
    def test_emotional_reasoning(self):
        """情绪推理：我感觉会搞砸"""
        results = self.detector.detect("我感觉这件事一定会搞砸。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.EMOTIONAL_REASONING, types)

    # —— 放大/缩小 ——
    def test_magnification_minimization(self):
        """放大/缩小：这点成绩不值一提"""
        results = self.detector.detect("这点成绩不值一提，谁都能做到。")
        types = [r.distortion_type for r in results]
        self.assertIn(DistortionType.MAGNIFICATION_MINIMIZATION, types)

    # —— 边界测试 ——
    def test_no_distortion_neutral_text(self):
        """中性文本不触发检测"""
        results = self.detector.detect("今天天气不错，适合出去走走。")
        self.assertEqual(len(results), 0)

    def test_empty_text(self):
        """空文本不触发检测"""
        results = self.detector.detect("")
        self.assertEqual(len(results), 0)

    def test_multiple_distortions(self):
        """多认知扭曲同时检测"""
        results = self.detector.detect("我就是个废物，这次面试肯定失败，我的人生完了。")
        self.assertGreater(len(results), 1)

    # —— DistortionResult 字段测试 ——
    def test_result_has_confidence(self):
        """检测结果包含置信度"""
        results = self.detector.detect("我彻底完蛋了。")
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertTrue(0.0 <= r.confidence <= 1.0)

    def test_result_has_positions(self):
        """检测结果包含起止位置"""
        results = self.detector.detect("我彻底完蛋了。")
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertLess(r.start_pos, r.end_pos)

    # —— generate_response 测试 ——
    def test_generate_response_returns_string(self):
        """generate_response 返回字符串"""
        results = self.detector.detect("我彻底完蛋了。")
        self.assertGreater(len(results), 0)
        response = self.detector.generate_response(results[0])
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    # —— 对话分析 ——
    def test_conversation_analysis(self):
        """对话分析正常运作"""
        messages = [
            "我彻底完蛋了。",
            "他们都在嘲笑我。",
            "我应该做得更好。",
            "今天天气不错。",
        ]
        analysis = self.detector.analyze_conversation(messages)
        self.assertIsInstance(analysis, ConversationAnalysis)
        self.assertEqual(analysis.total_messages, 4)
        self.assertGreater(len(analysis.distortions_found), 0)


class TestDistortionPattern(unittest.TestCase):
    """认知扭曲模式定义测试"""

    def setUp(self):
        self.detector = CognitiveDistortionDetector()

    def test_all_patterns_have_templates(self):
        """每种模式都有苏格拉底式提问模板"""
        for dtype, pattern in self.detector.patterns.items():
            self.assertGreater(
                len(pattern.questioning_templates), 0,
                f"{dtype.value} 缺少提问模板"
            )

    def test_all_patterns_have_description(self):
        """每种模式都有描述"""
        for dtype, pattern in self.detector.patterns.items():
            self.assertGreater(len(pattern.description), 0)
            self.assertGreater(len(pattern.keywords), 0)


if __name__ == "__main__":
    unittest.main()
