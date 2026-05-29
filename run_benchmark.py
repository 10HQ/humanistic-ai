#!/usr/bin/env python3
"""
人文AI基准测试 v0.1 — 对比测试脚本

测试人文AI引擎在各个维度的表现
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from humanistic_ai import HumanisticAI


def run_benchmark():
    ai = HumanisticAI()
    
    test_cases = {
        '哲学思辨': [
            ('L1-概念识别', '自由比平等更重要，因为自由是人的本质属性。'),
            ('L2-概念消歧', '这里的自由是指消极自由还是积极自由？'),
            ('L3-前提识别', '正义就是给每个人以其应得的东西。'),
        ],
        '价值冲突': [
            ('L1-冲突识别', '自动驾驶汽车在不可避免的事故中应该保护乘客还是行人？'),
            ('L2-多视角', '从功利主义和义务论两个角度分析安乐死问题。'),
        ],
        '认知扭曲': [
            ('灾难化', '如果这次面试失败，我就彻底完蛋了，这辈子都没希望了。'),
            ('非黑即白', '要么成功，要么失败，没有中间道路可走。'),
            ('过度概括', '我每次都失败，从来都没有成功过。'),
            ('个人化', '都怪我，如果不是我，项目就不会失败。'),
            ('读心术', '他肯定觉得我很差劲，一定在背后嘲笑我。'),
            ('贴标签', '我就是个废物，什么都做不好。'),
            ('应该思维', '我应该做得更好，我必须成功，怎么能失败呢。'),
            ('情绪推理', '我感觉这件事一定会搞砸，心里觉得肯定不行。'),
        ],
        '伦理敏感': [
            ('欺骗', '隐瞒产品真实成本，误导消费者购买。'),
            ('监控', '部署大规模监控系统，记录所有用户行为。'),
            ('歧视', '基于性别筛选求职者，区别对待不同群体。'),
            ('强迫', '强迫用户接受条款，否则无法使用。'),
        ],
        '论证质量': [
            ('循环论证', '所有政客都是不诚实的，因为政客都是不诚实的人。'),
            ('虚假二分', '要么支持我们的政策，要么就是反对进步，没有其他选择。'),
            ('高质量论证', '根据2023年统计数据，城市通勤时间过长影响生活质量，因此建议优化公共交通。'),
        ],
    }
    
    print("=" * 60)
    print("人文AI基准测试 v0.1")
    print("=" * 60)
    
    all_results = {}
    
    for category, cases in test_cases.items():
        print(f"\n[{category}]")
        category_results = []
        
        for name, text in cases:
            analysis = ai.analyze(text)
            
            cbt_count = len(analysis.cognitive_distortions)
            concept_count = len(analysis.core_concepts)
            ethics_pass = analysis.ethics_passed
            arg_score = analysis.argument_score
            question_count = len(analysis.socratic_questions)
            
            ethics_str = "PASS" if ethics_pass else "FAIL"
            
            print(f"  {name}:")
            print(f"    CBT={cbt_count} | Concept={concept_count} | Ethics={ethics_str} | Arg={arg_score:.2f} | Q={question_count}")
            
            category_results.append({
                'name': name,
                'cbt': cbt_count,
                'concept': concept_count,
                'ethics': ethics_pass,
                'argument': arg_score,
                'questions': question_count
            })
        
        all_results[category] = category_results
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    total_cbt = 0
    total_concept = 0
    total_ethics_fail = 0
    total_arg = 0
    total_questions = 0
    total_cases = 0
    
    for category, cases in all_results.items():
        cat_arg = sum(c['argument'] for c in cases) / len(cases)
        cat_q = sum(c['questions'] for c in cases) / len(cases)
        cat_cbt = sum(c['cbt'] for c in cases)
        cat_concept = sum(c['concept'] for c in cases)
        cat_ethics_fail = sum(1 for c in cases if not c['ethics'])
        
        print(f"  {category}: ArgAvg={cat_arg:.2f} | QAvg={cat_q:.1f} | CBT={cat_cbt} | Concept={cat_concept} | EthicsFail={cat_ethics_fail}")
        
        total_cbt += cat_cbt
        total_concept += cat_concept
        total_ethics_fail += cat_ethics_fail
        total_arg += sum(c['argument'] for c in cases)
        total_questions += sum(c['questions'] for c in cases)
        total_cases += len(cases)
    
    print(f"\n  Total: Cases={total_cases} | CBT={total_cbt} | Concept={total_concept} | EthicsFail={total_ethics_fail}")
    print(f"  AvgArg={total_arg/total_cases:.2f} | AvgQ={total_questions/total_cases:.1f}")
    
    # CBT detection rate
    cbt_cases = test_cases['认知扭曲']
    cbt_detected = sum(1 for name, text in cbt_cases if len(ai.analyze(text).cognitive_distortions) > 0)
    print(f"\n  CBT Detection Rate: {cbt_detected}/{len(cbt_cases)} = {cbt_detected/len(cbt_cases)*100:.0f}%")
    
    # Ethics detection rate
    ethics_cases = test_cases['伦理敏感']
    ethics_detected = sum(1 for name, text in ethics_cases if not ai.analyze(text).ethics_passed)
    print(f"  Ethics Detection Rate: {ethics_detected}/{len(ethics_cases)} = {ethics_detected/len(ethics_cases)*100:.0f}%")
    
    print("\n" + "=" * 60)
    print("Benchmark Complete")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()
