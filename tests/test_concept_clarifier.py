"""
test_concept_clarifier.py — 概念澄清引擎单元测试
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from concept_clarifier import ConceptClarifier, Concept, Assumption, Meaning


class TestConceptClarifier(unittest.TestCase):
    """概念澄清引擎核心测试"""

    def setUp(self):
        self.clarifier = ConceptClarifier()

    # —— identify_concepts ——
    def test_identify_single_abstract_concept(self):
        """识别单个抽象概念"""
        concepts = self.clarifier.identify_concepts("自由是人的本质属性")
        names = [c.name for c in concepts]
        self.assertIn("自由", names)

    def test_identify_multiple_concepts(self):
        """识别多个抽象概念"""
        concepts = self.clarifier.identify_concepts("自由比平等更重要，正义是社会的基石")
        names = [c.name for c in concepts]
        self.assertIn("自由", names)
        self.assertIn("平等", names)
        self.assertIn("正义", names)

    def test_no_concept_in_concrete_text(self):
        """无抽象概念的文本返回空列表"""
        concepts = self.clarifier.identify_concepts("今天吃了晚饭，然后去散步了")
        self.assertEqual(len(concepts), 0)

    def test_concept_has_positions(self):
        """识别到的概念包含位置信息"""
        concepts = self.clarifier.identify_concepts("自由很重要")
        self.assertGreater(len(concepts), 0)
        c = concepts[0]
        self.assertGreater(len(c.positions), 0)

    def test_concept_ambiguity_score(self):
        """可消歧的概念 ambiguity_score > 0"""
        concepts = self.clarifier.identify_concepts("自由比平等更重要")
        for c in concepts:
            if c.name == "自由":
                self.assertGreater(c.ambiguity_score, 0)
            if c.name == "平等":
                self.assertGreater(c.ambiguity_score, 0)

    def test_concept_is_abstract_flag(self):
        """抽象概念标记 is_abstract=True"""
        concepts = self.clarifier.identify_concepts("道德和法律")
        for c in concepts:
            self.assertTrue(c.is_abstract)

    def test_related_concepts_in_same_sentence(self):
        """同一句中的多个概念互相关联"""
        concepts = self.clarifier.identify_concepts("自由和平等是民主的基石")
        # 找相关概念
        related_count = sum(len(c.related_concepts) for c in concepts)
        self.assertGreater(related_count, 0)

    # —— extract_assumptions ——
    def test_extract_causal_assumption(self):
        """提取因果假设"""
        assumptions = self.clarifier.extract_assumptions("因为科技进步，所以社会必然进步")
        types = [a.assumption_type for a in assumptions]
        self.assertIn("causal", types)

    def test_extract_value_assumption(self):
        """提取价值假设"""
        assumptions = self.clarifier.extract_assumptions("每个人都应该追求幸福")
        types = [a.assumption_type for a in assumptions]
        self.assertIn("value", types)

    def test_extract_existence_assumption(self):
        """提取存在假设"""
        assumptions = self.clarifier.extract_assumptions("存在先于本质")
        types = [a.assumption_type for a in assumptions]
        self.assertIn("existence", types)

    def test_assumption_has_content(self):
        """假设包含内容"""
        assumptions = self.clarifier.extract_assumptions("因为人天生自由，所以不应受限")
        self.assertGreater(len(assumptions), 0)
        for a in assumptions:
            self.assertGreater(len(a.content), 0)

    def test_assumption_has_challengeability(self):
        """假设包含可挑战度"""
        assumptions = self.clarifier.extract_assumptions("人应该追求真理")
        self.assertGreater(len(assumptions), 0)
        for a in assumptions:
            self.assertTrue(0.0 <= a.challengeability <= 1.0)

    def test_empty_text_no_assumptions(self):
        """空文本无假设"""
        assumptions = self.clarifier.extract_assumptions("")
        self.assertEqual(len(assumptions), 0)

    # —— generate_clarifying_questions ——
    def test_generate_clarifying_questions(self):
        """生成澄清问题"""
        questions = self.clarifier.generate_clarifying_questions("自由比平等更重要")
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        for q in questions:
            self.assertIsInstance(q, str)

    def test_clarify_concept_questions(self):
        """澄清概念问题包含具体概念"""
        questions = self.clarifier.generate_clarifying_questions("正义很重要")
        # 应包含「正义」相关的追问
        found = any("正义" in q for q in questions)
        self.assertTrue(found, f"未找到包含「正义」的追问: {questions}")

    # —— disambiguation ——
    def test_disambiguate_known_concept(self):
        """消歧已知概念"""
        meanings = self.clarifier.disambiguate("自由", "在讨论政治时常常提到自由")
        self.assertIsInstance(meanings, list)
        self.assertGreater(len(meanings), 0)
        for m in meanings:
            self.assertIsInstance(m, Meaning)
            self.assertGreater(len(m.meaning), 0)

    def test_disambiguate_unknown_concept(self):
        """消歧未知概念返回空列表"""
        meanings = self.clarifier.disambiguate("一个不存在的概念", "无上下文")
        self.assertEqual(len(meanings), 0)

    # —— Concept dataclass ——
    def test_concept_dataclass_fields(self):
        """Concept 数据类字段完整性"""
        c = Concept(name="自由", positions=[(0, 2)], is_abstract=True, ambiguity_score=0.5)
        self.assertEqual(c.name, "自由")
        self.assertEqual(c.ambiguity_score, 0.5)
        self.assertTrue(c.is_abstract)

    # —— Assumption dataclass ——
    def test_assumption_dataclass_fields(self):
        """Assumption 数据类字段完整性"""
        a = Assumption(content="人天生自由", assumption_type="value", challengeability=0.7)
        self.assertEqual(a.content, "人天生自由")
        self.assertEqual(a.assumption_type, "value")


class TestConceptClarifierEdgeCases(unittest.TestCase):
    """边界测试"""

    def setUp(self):
        self.clarifier = ConceptClarifier()

    def test_duplicate_concept_not_double_counted(self):
        """重复概念不重复计数"""
        concepts = self.clarifier.identify_concepts("自由是自由的前提")
        names = [c.name for c in concepts]
        self.assertEqual(names.count("自由"), 1)

    def test_long_text_multiple_concepts(self):
        """长文本多概念"""
        long_text = (
            "自由是人的本质属性，平等是社会的基石。"
            "正义需要法律保障，幸福是人生的终极目标。"
            "爱和恨交织在一起，构成了复杂的人生。"
        )
        concepts = self.clarifier.identify_concepts(long_text)
        self.assertGreater(len(concepts), 3)


if __name__ == "__main__":
    unittest.main()
