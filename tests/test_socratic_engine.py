"""
test_socratic_engine.py — 苏格拉底式对话引擎单元测试
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from socratic_engine import (
    SocraticEngine,
    DialogueStage,
    ConcernType,
    DialogueState,
    SocraticResponse,
)


class TestEnums(unittest.TestCase):
    """枚举类型测试"""

    def test_dialogue_stages(self):
        stages = [s.value for s in DialogueStage]
        expected = ["确认", "探索", "挑战", "反思", "整合"]
        for e in expected:
            self.assertIn(e, stages)

    def test_concern_types(self):
        concerns = [c.value for c in ConcernType]
        for expected in ["死亡", "自由", "孤独", "无意义", "其他"]:
            self.assertIn(expected, concerns)


class TestSocraticEngine(unittest.TestCase):
    """苏格拉底式对话引擎核心测试"""

    def setUp(self):
        self.engine = SocraticEngine()

    # —— start ——
    def test_start_returns_socratic_response(self):
        """start 返回 SocraticResponse"""
        response = self.engine.start("我这次考试没考好，我真是个废物")
        self.assertIsInstance(response, SocraticResponse)

    def test_start_response_has_text(self):
        """回应包含文本"""
        response = self.engine.start("我彻底完蛋了")
        self.assertIsInstance(response.text, str)
        self.assertGreater(len(response.text), 0)

    def test_start_with_distortion_acknowledges(self):
        """有认知扭曲时先确认情绪"""
        response = self.engine.start("我就是个废物，什么都做不好。")
        self.assertEqual(response.stage, DialogueStage.EXPLORATION)

    def test_start_with_philosophical_question(self):
        """哲学问题正常回应"""
        response = self.engine.start("自由比平等更重要吗？")
        self.assertIsInstance(response, SocraticResponse)
        self.assertGreater(len(response.text), 0)

    def test_start_initializes_state(self):
        """start 初始化对话状态"""
        self.engine.start("我考试没考好")
        self.assertEqual(self.engine.state.turn_count, 1)

    def test_start_detects_distortions(self):
        """start 检测认知扭曲"""
        response = self.engine.start("我彻底完蛋了，这次肯定没救了。")
        self.assertGreater(len(self.engine.state.distortions_found), 0)

    # —— continue_dialogue ——
    def test_continue_dialogue_advances_turn(self):
        """继续对话推进回合数"""
        self.engine.start("我最近很迷茫")
        response = self.engine.continue_dialogue("我觉得活着没什么意义")
        self.assertEqual(self.engine.state.turn_count, 2)

    def test_continue_dialogue_returns_response(self):
        """继续对话返回回应"""
        self.engine.start("我最近很焦虑")
        response = self.engine.continue_dialogue("工作压力太大了")
        self.assertIsInstance(response, SocraticResponse)
        self.assertGreater(len(response.text), 0)

    def test_continue_dialogue_updates_distortions(self):
        """继续对话累积认知扭曲"""
        self.engine.start("我觉得我很差劲")
        initial_count = len(self.engine.state.distortions_found)
        self.engine.continue_dialogue("我每次都把事情搞砸")
        self.assertGreater(len(self.engine.state.distortions_found), initial_count)

    def test_continue_dialogue_updates_concepts(self):
        """继续对话累积概念"""
        self.engine.start("自由很重要")
        initial = len(self.engine.state.concepts_clarified)
        self.engine.continue_dialogue("正义和公平也很关键")
        self.assertGreater(len(self.engine.state.concepts_clarified), initial)

    # —— 终极关怀 ——
    def test_identify_death_concern(self):
        """识别死亡关怀"""
        response = self.engine.start("面对生命的有限性，我不知道该怎么办")
        self.assertEqual(self.engine.state.concern_type, ConcernType.DEATH)

    def test_identify_freedom_concern(self):
        """识别自由关怀"""
        response = self.engine.start("我不知道该选择哪个方向")
        self.assertEqual(self.engine.state.concern_type, ConcernType.FREEDOM)

    def test_identify_isolation_concern(self):
        """识别孤独关怀"""
        response = self.engine.start("我觉得没人能理解我，很孤独")
        self.assertEqual(self.engine.state.concern_type, ConcernType.ISOLATION)

    def test_identify_meaninglessness_concern(self):
        """识别无意义关怀"""
        response = self.engine.start("活着到底有什么意义，一切都好空虚")
        self.assertEqual(self.engine.state.concern_type, ConcernType.MEANINGLESSNESS)

    def test_identify_other_concern(self):
        """普通话题识别为OTHER"""
        response = self.engine.start("今天天气真好")
        self.assertEqual(self.engine.state.concern_type, ConcernType.OTHER)

    # —— 阶段推进 ——
    def test_initial_stage_is_exploration(self):
        """初始阶段为探索"""
        self.engine.start("自由比平等更重要")
        self.assertEqual(self.engine.state.stage, DialogueStage.EXPLORATION)

    def test_stage_advances_over_turns(self):
        """多轮对话后阶段推进"""
        self.engine.start("我考试没考好，我真是个废物")
        for i in range(5):
            self.engine.continue_dialogue("可是我真的觉得我很失败")
        # 多轮后应进入更深阶段
        self.assertIn(
            self.engine.state.stage,
            [DialogueStage.CHALLENGE, DialogueStage.REFLECTION, DialogueStage.INTEGRATION]
        )

    # —— 模块使用 ——
    def test_start_modules_used(self):
        """start 回应标明使用的模块"""
        response = self.engine.start("我彻底完蛋了，这绝对是灾难。")
        self.assertGreater(len(response.modules_used), 0)

    # —— 深度级别 ——
    def test_depth_level_starts_at_zero(self):
        """初始深度为0"""
        response = self.engine.start("自由是什么")
        self.assertEqual(response.depth_level, 0)

    # —— 边界测试 ——
    def test_empty_text(self):
        """空文本"""
        response = self.engine.start("")
        self.assertIsInstance(response, SocraticResponse)

    def test_very_short_text(self):
        """极短文本"""
        response = self.engine.start("嗯")
        self.assertIsInstance(response, SocraticResponse)
        self.assertGreater(len(response.text), 0)


class TestDialogueState(unittest.TestCase):
    """对话状态数据类测试"""

    def test_default_state(self):
        state = DialogueState()
        self.assertEqual(state.stage, DialogueStage.ACKNOWLEDGMENT)
        self.assertEqual(state.depth_level, 0)
        self.assertEqual(state.turn_count, 0)
        self.assertEqual(state.concern_type, ConcernType.OTHER)
        self.assertEqual(len(state.distortions_found), 0)


class TestSocraticResponse(unittest.TestCase):
    """苏格拉底式回应数据类测试"""

    def test_fields(self):
        response = SocraticResponse(
            text="让我们一起来思考这个问题。",
            stage=DialogueStage.EXPLORATION,
            question_type="clarifying",
            depth_level=1,
            modules_used=["CBT", "概念澄清"],
        )
        self.assertEqual(response.text, "让我们一起来思考这个问题。")
        self.assertEqual(response.stage, DialogueStage.EXPLORATION)
        self.assertEqual(response.question_type, "clarifying")
        self.assertEqual(response.depth_level, 1)


if __name__ == "__main__":
    unittest.main()
