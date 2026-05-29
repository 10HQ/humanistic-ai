#!/usr/bin/env python3
"""
人文AI Web Demo — Gradio界面

运行: python app.py
访问: http://localhost:7860
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import gradio as gr
except ImportError:
    print("Gradio not installed. Run: pip install gradio")
    sys.exit(1)

from humanistic_ai import HumanisticAI
from socratic_engine import SocraticEngine

ai = HumanisticAI()
engines = {}  # session_id -> SocraticEngine


def analyze_text(text, context):
    """分析文本"""
    if not text.strip():
        return "请输入文本。"
    analysis = ai.analyze(text, context)
    
    lines = [f"## 分析结果\n"]
    
    if analysis.cognitive_distortions:
        lines.append("### 🧠 认知扭曲")
        for d in analysis.cognitive_distortions:
            lines.append(f"- **{d.distortion_type.value}** (置信度: {d.confidence:.2f}): {d.matched_text}")
        lines.append("")
    
    if analysis.core_concepts:
        lines.append("### 💡 核心概念")
        for c in analysis.core_concepts[:5]:
            lines.append(f"- **{c.name}** (歧义度: {c.ambiguity_score:.2f})")
        lines.append("")
    
    if analysis.assumptions:
        lines.append("### 🔍 隐含假设")
        for a in analysis.assumptions[:3]:
            lines.append(f"- [{a.assumption_type}] {a.content}")
        lines.append("")
    
    if analysis.ethical_risks:
        lines.append("### ⚠️ 伦理风险")
        for r in analysis.ethical_risks:
            lines.append(f"- **{r.risk_type.value}**: {r.description}")
        lines.append("")
    
    if analysis.fallacies:
        lines.append("### 📐 逻辑谬误")
        for f in analysis.fallacies:
            lines.append(f"- **{f.type.value}**: {f.description}")
        lines.append("")
    
    lines.append(f"**论证评分**: {analysis.argument_score:.2f}/1.0")
    
    if analysis.socratic_questions:
        lines.append("\n### 🤔 苏格拉底式追问")
        for i, q in enumerate(analysis.socratic_questions[:5], 1):
            lines.append(f"{i}. {q}")
    
    return "\n".join(lines)


def respond_text(text, context):
    """生成回应"""
    if not text.strip():
        return "请输入文本。"
    return ai.respond(text, context)


def socratic_chat(user_input, chat_history, session_state):
    """苏格拉底式对话"""
    if not user_input.strip():
        return chat_history, session_state
    
    if session_state.get("engine") is None:
        engine = SocraticEngine()
        r = engine.start(user_input)
        session_state["engine"] = engine
    else:
        engine = session_state["engine"]
        r = engine.continue_dialogue(user_input)
    
    chat_history.append((user_input, r.text))
    return chat_history, session_state


def reset_dialogue():
    """重置对话"""
    return [], {"engine": None}


def show_capabilities():
    """显示引擎能力"""
    caps = ai.capabilities()
    lines = [
        f"## 人文AI引擎 v{caps['version']}",
        "",
        "### 模块",
    ]
    for name, desc in caps["modules"].items():
        lines.append(f"- **{name}**: {desc}")
    
    lines.extend([
        "",
        "### 基准测试",
        f"- 测试用例: {caps['benchmark']['cases']}",
        f"- 测试维度: {caps['benchmark']['dimensions']}",
        f"- CBT检测率: {caps['benchmark']['cbt_rate']}",
        f"- 伦理检测率: {caps['benchmark']['ethics_rate']}",
        f"- 论证区分度: {caps['benchmark']['argument_discrimination']}",
        "",
        f"### 单元测试: {caps['unit_tests']}",
    ])
    return "\n".join(lines)


# Build UI
with gr.Blocks(title="人文AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌗 人文AI — 追求智慧的人文科学专家级AI系统")
    gr.Markdown("*\"技术是船，人文是舵。\"*")
    
    with gr.Tabs():
        with gr.TabItem("📊 分析"):
            with gr.Row():
                with gr.Column():
                    analyze_input = gr.Textbox(label="输入文本", lines=5, placeholder="输入要分析的文本...")
                    analyze_context = gr.Textbox(label="上下文（可选）", placeholder="场景描述...")
                    analyze_btn = gr.Button("分析", variant="primary")
                with gr.Column():
                    analyze_output = gr.Markdown(label="分析结果")
            analyze_btn.click(analyze_text, [analyze_input, analyze_context], analyze_output)
        
        with gr.TabItem("💬 回应"):
            with gr.Row():
                with gr.Column():
                    respond_input = gr.Textbox(label="输入文本", lines=5, placeholder="输入文本...")
                    respond_context = gr.Textbox(label="上下文（可选）")
                    respond_btn = gr.Button("生成回应", variant="primary")
                with gr.Column():
                    respond_output = gr.Markdown(label="人文AI回应")
            respond_btn.click(respond_text, [respond_input, respond_context], respond_output)
        
        with gr.TabItem("🗣️ 苏格拉底对话"):
            chatbot = gr.Chatbot(label="对话", height=400)
            chat_input = gr.Textbox(label="输入", placeholder="说点什么...")
            session_state = gr.State(value={"engine": None})
            
            with gr.Row():
                send_btn = gr.Button("发送", variant="primary")
                reset_btn = gr.Button("重置对话")
            
            send_btn.click(socratic_chat, [chat_input, chatbot, session_state], [chatbot, session_state])
            chat_input.submit(socratic_chat, [chat_input, chatbot, session_state], [chatbot, session_state])
            reset_btn.click(reset_dialogue, [], [chatbot, session_state])
        
        with gr.TabItem("ℹ️ 能力"):
            caps_output = gr.Markdown()
            demo.load(show_capabilities, [], caps_output)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
