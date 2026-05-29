#!/usr/bin/env python3
"""
人文AI全模块单元测试
运行: python tests/test_all.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cognitive_distortion_detector import CognitiveDistortionDetector
from concept_clarifier import ConceptClarifier
from ethics_checker import EthicsChecker
from argument_analyzer import ArgumentAnalyzer
from humanistic_ai import HumanisticAI


passed = 0
failed = 0

def check(name, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name}")


def test_cbt():
    print("\n[CBT Detector]")
    d = CognitiveDistortionDetector()
    
    check("catastrophizing", "灾难化" in [x.distortion_type.value for x in d.detect("我就彻底完蛋了这辈子都没希望了")])
    check("black_and_white", "非黑即白" in [x.distortion_type.value for x in d.detect("要么成功要么失败没有中间道路")])
    check("overgeneralization", "过度概括" in [x.distortion_type.value for x in d.detect("我每次都失败从来都没有成功过")])
    check("personalization", "个人化" in [x.distortion_type.value for x in d.detect("都怪我如果不是我项目就不会失败")])
    check("mind_reading", "读心术" in [x.distortion_type.value for x in d.detect("他肯定觉得我很差劲一定在背后嘲笑我")])
    check("labeling", "贴标签" in [x.distortion_type.value for x in d.detect("我就是个废物什么都做不好")])
    check("should", "应该思维" in [x.distortion_type.value for x in d.detect("我应该做得更好我必须成功怎么能失败呢")])
    check("emotional", "情绪推理" in [x.distortion_type.value for x in d.detect("我感觉这件事一定会搞砸心里觉得肯定不行")])
    check("magnification", "放大/缩小" in [x.distortion_type.value for x in d.detect("这点成绩不值一提谁都能做到")])
    check("no_distortion", len(d.detect("今天天气不错我打算去公园散步")) == 0)
    check("response_gen", len(d.generate_response(d.detect("我真是个废物")[0])) > 10)
    
    conv = d.analyze_conversation(["我真是个废物", "他们都在嘲笑我", "永远都这样了"])
    check("conversation", conv.total_messages == 3 and len(conv.distortions_found) > 0)


def test_concepts():
    print("\n[Concept Clarifier]")
    c = ConceptClarifier()
    
    r = c.identify_concepts("自由比平等更重要因为自由是人的本质属性")
    names = [x.name for x in r]
    check("identify_freedom", "自由" in names)
    check("identify_equality", "平等" in names)
    
    r = c.identify_concepts("今天天气不错")
    check("no_concepts", len(r) == 0)
    
    m = c.disambiguate("自由", "政治哲学讨论")
    check("disambiguate", len(m) >= 3)
    
    q = c.generate_clarifying_questions("自由比平等更重要")
    check("questions", len(q) >= 2)
    
    a = c.extract_assumptions("因为自由是人的本质属性所以自由更重要")
    check("assumptions", len(a) >= 1)


def test_ethics():
    print("\n[Ethics Checker]")
    e = EthicsChecker()
    
    r = e.full_check("隐瞒产品真实成本误导消费者购买", "电商")
    check("deception_fail", not r.passed)
    
    r = e.full_check("部署大规模监控系统记录所有用户行为", "公共")
    check("surveillance_fail", not r.passed)
    
    r = e.full_check("基于性别筛选求职者区别对待不同群体", "招聘")
    check("discrimination_fail", not r.passed)
    
    r = e.full_check("强迫用户接受条款否则无法使用", "软件")
    check("coercion_fail", not r.passed)
    
    r = e.full_check("为视障人士提供语音辅助功能", "公共")
    check("accessibility_pass", r.passed)
    
    r = e.full_check("帮助用户提高学习效率", "教育")
    check("education_pass", r.passed)
    
    r = e.check_character("谨慎评估各方利益公平分配资源")
    check("virtues", len(r.virtues) >= 1)


def test_arguments():
    print("\n[Argument Analyzer]")
    a = ArgumentAnalyzer()
    
    r = a.analyze("所有政客都是不诚实的因为政客都是不诚实的人")
    check("circular", any(f.type.value == "以偏概全" for f in r.fallacies))
    
    r = a.analyze("要么支持我们的政策要么就是反对进步没有其他选择")
    check("false_dilemma", any(f.type.value == "虚假二分" for f in r.fallacies))
    
    r = a.analyze("对方认为应该增加教育投入这无非是想让政府多花钱你一个连孩子都没有的人有什么资格讨论教育政策")
    check("strawman_adhominem", any(f.type.value in ["稻草人", "人身攻击"] for f in r.fallacies))
    
    r = a.analyze("根据2023年统计数据城市通勤时间过长影响生活质量因此建议优化公共交通")
    check("high_quality", r.overall_score >= 0.8)
    
    r = a.analyze("爱因斯坦说过神不掷骰子所以量子力学是错的")
    check("authority", any(f.type.value == "诉诸权威" for f in r.fallacies))
    
    r = a.analyze("想想那些因为贫困失学的孩子你们怎么能不通过这个法案")
    check("emotion", any(f.type.value == "诉诸情感" for f in r.fallacies))


def test_integration():
    print("\n[Integration]")
    ai = HumanisticAI()
    
    a = ai.analyze("我这次考试没考好我真是个废物永远都这样了")
    check("analyze_cbt", len(a.cognitive_distortions) > 0)
    check("analyze_questions", len(a.socratic_questions) > 0)
    
    r = ai.respond("自由比平等更重要")
    check("respond", len(r) > 50)
    
    report = ai.full_report("隐瞒产品真实成本误导消费者")
    check("report_ethics", "FAIL" in report or "!" in report)
    
    d = ai.dialogue_start("我这次考试没考好我真是个废物")
    check("dialogue_start", d.stage is not None)
    
    d2 = ai.dialogue_continue("我觉得他们都在嘲笑我")
    check("dialogue_continue", d2.stage is not None)


if __name__ == "__main__":
    print("=" * 50)
    print("人文AI 全模块单元测试")
    print("=" * 50)
    
    test_cbt()
    test_concepts()
    test_ethics()
    test_arguments()
    test_integration()
    
    print(f"\n{'=' * 50}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    print(f"Pass rate: {passed / (passed + failed) * 100:.0f}%")
    print("=" * 50)
