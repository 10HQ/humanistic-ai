"""
semantic_analyzer.py - 人文AI语义分析层 v1.0

集成DeepSeek API做语义级分析，作为规则引擎的补充。
规则引擎捕获模式匹配能发现的问题，语义分析捕获需要理解的问题。

作者：灵台未央
日期：2026-05-29
"""

import os
import json
import requests
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class SemanticFallacy:
    """语义级谬误"""
    type: str
    description: str
    evidence: str
    severity: float


@dataclass
class ConceptMeaning:
    """概念含义"""
    meaning: str
    domain: str
    confidence: float


@dataclass
class SemanticResult:
    """语义分析结果"""
    fallacies: List[SemanticFallacy] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    score: float = 0.0
    summary: str = ""


class SemanticAnalyzer:
    """
    语义分析器 — DeepSeek API集成
    
    用法：
        analyzer = SemanticAnalyzer()  # 从环境变量读取API key
        result = analyzer.analyze_argument("自由比平等更重要")
    """
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.xiaomimimo.com/v1"):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        self.base_url = base_url
        self.enabled = bool(self.api_key)
        
        if not self.enabled:
            print("[SemanticAnalyzer] WARNING: DEEPSEEK_API_KEY not set. Semantic analysis disabled.")
    
    def _call_api(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """调用DeepSeek API"""
        if not self.enabled:
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.3
            }
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[SemanticAnalyzer] API error: {e}")
            return None
    
    def analyze_argument(self, text: str) -> SemanticResult:
        """语义级论证分析"""
        prompt = f"""分析以下论证的逻辑质量。用JSON格式返回：

论证：{text}

返回格式（只返回JSON，不要其他文字）：
{{
  "fallacies": [
    {{"type": "谬误类型", "description": "具体描述", "evidence": "文本证据", "severity": 0.0-1.0}}
  ],
  "strengths": ["论证的优点"],
  "score": 0.0-1.0,
  "summary": "一句话总结"
}}"""
        
        response = self._call_api(prompt)
        if not response:
            return SemanticResult(summary="API不可用")
        
        try:
            data = json.loads(response)
            fallacies = [SemanticFallacy(**f) for f in data.get("fallacies", [])]
            return SemanticResult(
                fallacies=fallacies,
                strengths=data.get("strengths", []),
                score=data.get("score", 0.5),
                summary=data.get("summary", "")
            )
        except (json.JSONDecodeError, KeyError) as e:
            return SemanticResult(summary=f"解析失败: {e}")
    
    def clarify_concept(self, concept: str, context: str = "") -> Dict[str, Any]:
        """深度概念澄清"""
        prompt = f"""澄清以下概念的含义，考虑不同语境和文化背景。

概念：{concept}
上下文：{context or '无'}

用JSON格式返回（只返回JSON）：
{{
  "meanings": [
    {{"meaning": "含义描述", "domain": "所属领域", "confidence": 0.0-1.0}}
  ],
  "key_distinctions": ["需要区分的关键点"],
  "common_misunderstandings": ["常见误解"],
  "suggested_clarification": "建议的澄清问题"
}}"""
        
        response = self._call_api(prompt)
        if not response:
            return {"error": "API不可用"}
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "解析失败", "raw": response}
    
    def cross_cultural_analysis(self, text: str) -> Dict[str, Any]:
        """跨文化价值分析"""
        prompt = f"""分析以下文本中的文化假设和偏见。

文本：{text}

用JSON格式返回（只返回JSON）：
{{
  "cultural_assumptions": ["文本隐含的文化假设"],
  "biases": ["可能的文化偏见"],
  "western_perspective": "西方视角下的解读",
  "eastern_perspective": "东方视角下的解读",
  "balanced_view": "更平衡的视角"
}}"""
        
        response = self._call_api(prompt)
        if not response:
            return {"error": "API不可用"}
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "解析失败", "raw": response}
    
    def ethical_analysis(self, text: str) -> Dict[str, Any]:
        """语义级伦理分析"""
        prompt = f"""从伦理角度分析以下行为或陈述，考虑功利主义、义务论和德性伦理三个维度。

内容：{text}

用JSON格式返回（只返回JSON）：
{{
  "consequentialist": "功利主义分析",
  "deontological": "义务论分析",
  "virtue_ethics": "德性伦理分析",
  "risk_level": "low/medium/high/critical",
  "concerns": ["伦理关切"],
  "suggestions": ["伦理建议"]
}}"""
        
        response = self._call_api(prompt)
        if not response:
            return {"error": "API不可用"}
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "解析失败", "raw": response}


def main():
    analyzer = SemanticAnalyzer()
    
    if not analyzer.enabled:
        print("API key not set. Set DEEPSEEK_API_KEY to enable semantic analysis.")
        print("Running in disabled mode - showing interface only.")
        return
    
    print("=" * 50)
    print("人文AI · 语义分析层 v1.0")
    print("=" * 50)
    
    # Test 1: Argument analysis
    print("\n[Test 1: Argument Analysis]")
    r = analyzer.analyze_argument("爱因斯坦说过神不掷骰子，所以量子力学是错的")
    print(f"Score: {r.score}")
    print(f"Fallacies: {len(r.fallacies)}")
    for f in r.fallacies:
        print(f"  - {f.type}: {f.description}")
    print(f"Strengths: {r.strengths}")
    print(f"Summary: {r.summary}")
    
    # Test 2: Concept clarification
    print("\n[Test 2: Concept Clarification]")
    r = analyzer.clarify_concept("自由", "自由比平等更重要")
    print(json.dumps(r, ensure_ascii=False, indent=2))
    
    # Test 3: Cross-cultural
    print("\n[Test 3: Cross-Cultural Analysis]")
    r = analyzer.cross_cultural_analysis("个人追求自我实现比履行社会责任更重要")
    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
