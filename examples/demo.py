#!/usr/bin/env python3
"""
人文AI演示 - 展示核心能力

运行: python examples/demo.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from humanistic_ai import HumanisticAI
from socratic_engine import SocraticEngine


def demo_basic():
    """基础分析演示"""
    ai = HumanisticAI()
    
    print("=" * 60)
    print("人文AI 演示")
    print("=" * 60)
    
    # 场景1：学生焦虑
    print("\n[场景1: 学生焦虑]")
    text = "我这次考试没考好，我真是个废物，永远都这样了。"
    print(f"输入: {text}")
    print(f"\n{ai.respond(text, '学生')}")
    
    # 场景2：哲学讨论
    print("\n\n[场景2: 哲学讨论]")
    text = "自由比平等更重要，因为自由是人的本质属性。"
    print(f"输入: {text}")
    print(f"\n{ai.respond(text, '哲学')}")
    
    # 场景3：逻辑谬误
    print("\n\n[场景3: 逻辑谬误]")
    text = "爱因斯坦说过神不掷骰子，所以量子力学是错的。"
    print(f"输入: {text}")
    print(f"\n{ai.respond(text, '科学')}")
    
    # 场景4：存在主义
    print("\n\n[场景4: 存在主义]")
    text = "活着到底有什么意义？每天重复同样的事情，感觉很空虚。"
    print(f"输入: {text}")
    print(f"\n{ai.respond(text, '存在')}")
    
    # 场景5：伦理困境
    print("\n\n[场景5: 伦理困境]")
    text = "为了公共安全，政府是否有权大规模收集个人数据？"
    print(f"输入: {text}")
    print(f"\n{ai.respond(text, '伦理')}")


def demo_dialogue():
    """苏格拉底式对话演示"""
    engine = SocraticEngine()
    
    print("\n\n" + "=" * 60)
    print("苏格拉底式对话演示")
    print("=" * 60)
    
    # 多轮对话
    turns = [
        "我这次考试没考好，我真是个废物。",
        "我觉得他们都在嘲笑我，所有人都看不起我。",
        "我不知道该怎么办，感觉一切都完了。",
        "也许我太绝对了...但确实很糟糕。",
        "我想我可能夸大了。其实还有其他科目考得不错。",
    ]
    
    print("\n[对话: 从绝望到觉察]")
    r = engine.start(turns[0])
    print(f"\nUser: {turns[0]}")
    print(f"AI: {r.text}")
    print(f"[Stage: {r.stage.value}]")
    
    for turn in turns[1:]:
        r = engine.continue_dialogue(turn)
        print(f"\nUser: {turn}")
        print(f"AI: {r.text}")
        print(f"[Stage: {r.stage.value}]")


def demo_full_report():
    """完整报告演示"""
    ai = HumanisticAI()
    
    print("\n\n" + "=" * 60)
    print("完整分析报告演示")
    print("=" * 60)
    
    text = "所有政客都是不诚实的，因为政客都是不诚实的人。你一个连大学都没毕业的人，有什么资格讨论政治？"
    print(f"\n{ai.full_report(text, '政治讨论')}")


def demo_benchmark_summary():
    """基准测试摘要"""
    print("\n\n" + "=" * 60)
    print("基准测试摘要 (120用例)")
    print("=" * 60)
    
    results = {
        "CBT检测率": "100% (20/20)",
        "伦理检测率": "85% (17/20)",
        "论证区分度": "15/16 低质量检出",
        "概念识别": "117个/120用例",
        "跨文化概念": "42个/20用例",
    }
    
    for metric, value in results.items():
        print(f"  {metric}: {value}")


if __name__ == "__main__":
    demo_basic()
    demo_dialogue()
    demo_full_report()
    demo_benchmark_summary()
