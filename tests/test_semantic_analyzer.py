"""
test_semantic_analyzer.py — 语义分析器单元测试
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic_analyzer import (
    SemanticAnalyzer,
    SemanticFallacy,
    SemanticResult,
    ConceptMeaning,
)


class TestSemanticAnalyzer(unittest.TestCase):
    """语义分析器核心测试"""

    def test_init_without_api_key_disabled(self):
        """无 API key 时禁用"""
        with patch.dict(os.environ, {}, clear=True):
            analyzer = SemanticAnalyzer(api_key=None)
            self.assertFalse(analyzer.enabled)

    def test_init_with_api_key_enabled(self):
        """有 API key 时启用"""
        analyzer = SemanticAnalyzer(api_key="test-key-12345")
        self.assertTrue(analyzer.enabled)

    @patch("semantic_analyzer.requests.post")
    def test_analyze_argument_with_mock(self, mock_post):
        """模拟 API 调用测试 analyze_argument"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": """{
                        "fallacies": [
                            {"type": "false_dilemma", "description": "仅呈现两种选择", "evidence": "要么...要么...", "severity": 0.6}
                        ],
                        "strengths": ["观点明确"],
                        "score": 0.55,
                        "summary": "该论证存在虚假二分问题"
                    }"""
                }
            }]
        }
        mock_post.return_value = mock_response

        analyzer = SemanticAnalyzer(api_key="test-key-12345")
        result = analyzer.analyze_argument("要么自由要么平等")

        self.assertIsInstance(result, SemanticResult)
        self.assertGreater(len(result.fallacies), 0)
        self.assertEqual(result.fallacies[0].type, "false_dilemma")
        self.assertTrue(0.0 <= result.score <= 1.0)
        self.assertGreater(len(result.summary), 0)

    @patch("semantic_analyzer.requests.post")
    def test_analyze_argument_empty_response(self, mock_post):
        """API 返回空响应"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "{}"
                }
            }]
        }
        mock_post.return_value = mock_response

        analyzer = SemanticAnalyzer(api_key="test-key-12345")
        result = analyzer.analyze_argument("测试")

        self.assertIsInstance(result, SemanticResult)
        self.assertEqual(len(result.fallacies), 0)

    @patch("semantic_analyzer.requests.post")
    def test_analyze_argument_api_error(self, mock_post):
        """API 调用失败降级"""
        mock_post.side_effect = Exception("Connection error")

        analyzer = SemanticAnalyzer(api_key="test-key-12345")
        result = analyzer.analyze_argument("测试")

        self.assertIsInstance(result, SemanticResult)
        self.assertEqual(len(result.fallacies), 0)

    def test_disabled_analyzer_returns_none(self):
        """禁用状态下调用 API 返回空结果"""
        analyzer = SemanticAnalyzer(api_key=None)
        result = analyzer.analyze_argument("自由比平等更重要")
        self.assertIsInstance(result, SemanticResult)
        self.assertEqual(len(result.fallacies), 0)
        self.assertEqual(result.score, 0.0)

    def test_base_url_default(self):
        """默认 base_url"""
        analyzer = SemanticAnalyzer(api_key=None)
        self.assertEqual(analyzer.base_url, "https://api.xiaomimimo.com/v1")

    def test_custom_base_url(self):
        """自定义 base_url"""
        analyzer = SemanticAnalyzer(api_key="test", base_url="https://custom.api.com/v1")
        self.assertEqual(analyzer.base_url, "https://custom.api.com/v1")


class TestSemanticFallacy(unittest.TestCase):
    """SemanticFallacy 数据类测试"""

    def test_fields(self):
        sf = SemanticFallacy(
            type="false_dilemma",
            description="仅呈现两种选择",
            evidence="要么...要么...",
            severity=0.6,
        )
        self.assertEqual(sf.type, "false_dilemma")
        self.assertEqual(sf.severity, 0.6)
        self.assertGreater(len(sf.description), 0)
        self.assertGreater(len(sf.evidence), 0)


class TestSemanticResult(unittest.TestCase):
    """SemanticResult 数据类测试"""

    def test_default_values(self):
        result = SemanticResult()
        self.assertEqual(len(result.fallacies), 0)
        self.assertEqual(len(result.strengths), 0)
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.summary, "")


class TestConceptMeaning(unittest.TestCase):
    """ConceptMeaning 数据类测试"""

    def test_fields(self):
        cm = ConceptMeaning(
            meaning="与事实相符",
            domain="认识论",
            confidence=0.8,
        )
        self.assertEqual(cm.meaning, "与事实相符")
        self.assertEqual(cm.domain, "认识论")
        self.assertEqual(cm.confidence, 0.8)


if __name__ == "__main__":
    unittest.main()
