from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, HRFlowable
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "Sunny-Tea-House-Project-Document.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("YaHei", r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("YaHei-Bold", r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))

INK = colors.HexColor("#17211C")
GREEN = colors.HexColor("#244D38")
LIME = colors.HexColor("#DFFF57")
CREAM = colors.HexColor("#F6F3EB")
MUTED = colors.HexColor("#68716C")
LINE = colors.HexColor("#D9DDD8")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CNBody", fontName="YaHei", fontSize=9.5, leading=16, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="CNTitle", fontName="YaHei-Bold", fontSize=28, leading=37, textColor=INK, spaceAfter=12))
styles.add(ParagraphStyle(name="CNH1", fontName="YaHei-Bold", fontSize=19, leading=26, textColor=INK, spaceBefore=3, spaceAfter=12))
styles.add(ParagraphStyle(name="CNH2", fontName="YaHei-Bold", fontSize=12, leading=18, textColor=GREEN, spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name="Small", fontName="YaHei", fontSize=7.8, leading=12, textColor=MUTED))
styles.add(ParagraphStyle(name="Label", fontName="YaHei-Bold", fontSize=7.5, leading=11, textColor=GREEN, spaceAfter=5))
styles.add(ParagraphStyle(name="HeaderWhite", fontName="YaHei-Bold", fontSize=8, leading=12, textColor=colors.white))
styles.add(ParagraphStyle(name="Quote", fontName="YaHei", fontSize=8.5, leading=14, textColor=INK, leftIndent=10, rightIndent=10, borderColor=LINE, borderWidth=.5, borderPadding=9, backColor=colors.white, spaceAfter=8))
styles.add(ParagraphStyle(name="CodeBlock", fontName="YaHei", fontSize=6.8, leading=10, textColor=INK, leftIndent=8, rightIndent=8, borderPadding=8, backColor=colors.HexColor("#EEF0EA"), spaceAfter=8))

def p(text, style="CNBody"):
    return Paragraph(text, styles[style])

def bullet(text):
    return Paragraph("• " + text, ParagraphStyle(name=f"b{hash(text)}", parent=styles["CNBody"], leftIndent=10, firstLineIndent=-8, spaceAfter=4))

def page_header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(LINE)
    canvas.line(18*mm, 15*mm, w-18*mm, 15*mm)
    canvas.setFont("YaHei", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(18*mm, 9*mm, "Sunny Tea House · AI REVIEW ASSISTANT")
    canvas.drawRightString(w-18*mm, 9*mm, f"{doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
    topMargin=18*mm, bottomMargin=21*mm, title="Sunny Tea House AI 评价生成 Demo 项目文档",
    author="Codex"
)

story = []

# Cover
story += [Spacer(1, 20*mm), p("AI REVIEW ASSISTANT", "Label"), p("Sunny Tea House<br/>AI 评价生成 Demo", "CNTitle")]
story.append(HRFlowable(width="28%", thickness=5, color=LIME, spaceBefore=2, spaceAfter=18, hAlign="LEFT"))
story += [p("移动端 H5 · 产品闭环 / Prompt 工程 / 企业微信自动化", "CNH2"), Spacer(1, 8*mm)]
cover_data = [
    [p("交付版本", "Small"), p("v1.0 / 2026-07-11", "CNBody")],
    [p("技术方案", "Small"), p("React + Next-compatible App Router + Server Route", "CNBody")],
    [p("演示模式", "Small"), p("无 Key 也可完整体验；配置后自动切换真实 AI", "CNBody")],
    [p("实际耗时", "Small"), p("约 35 分钟（不含第三方账号配置与对外部署审批）", "CNBody")],
]
t = Table(cover_data, colWidths=[34*mm, 118*mm], rowHeights=[15*mm]*4)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), CREAM), ("BOX", (0,0), (-1,-1), .6, LINE),
    ("INNERGRID", (0,0), (-1,-1), .35, LINE), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
]))
story += [t, Spacer(1, 18*mm), p("设计原则", "Label"), p("真实感受优先、平台语气匹配、用户最终确认、服务端保管密钥、失败时仍可演示。", "Quote"), PageBreak()]

# Product loop
story += [p("01  产品闭环与体验设计", "CNH1"), p("目标不是只生成一段文案，而是让顾客从“有感受”顺畅走到“愿意发布”，同时保留真实、透明和可控。")]
flow = [
    [p("1", "CNH2"), p("感受选择", "CNH2"), p("6 个具体标签，限制 1-2 项，降低决策成本并约束模型不虚构。", "CNBody")],
    [p("2", "CNH2"), p("平台选择", "CNH2"), p("Google / 小红书并列选择；语言、篇幅、语气在后台自动切换。", "CNBody")],
    [p("3", "CNH2"), p("AI 生成", "CNH2"), p("加载态解释正在发生什么；无 Key 时返回稳定 Demo 内容，现场不因网络中断。", "CNBody")],
    [p("4", "CNH2"), p("编辑与发布", "CNH2"), p("生成结果进入可编辑文本框；复制成功后再打开对应平台入口，不做自动代发。", "CNBody")],
    [p("5", "CNH2"), p("商家自动化", "CNH2"), p("同步生成中文摘要与回复草稿，真实或 Mock 推送状态清晰可见。", "CNBody")],
]
t = Table(flow, colWidths=[12*mm, 31*mm, 109*mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), LIME), ("BACKGROUND", (1,0), (-1,-1), colors.white),
    ("BOX", (0,0), (-1,-1), .6, LINE), ("INNERGRID", (0,0), (-1,-1), .35, LINE),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8), ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))
story += [t, Spacer(1, 7*mm), p("移动端细节", "CNH2"), bullet("点击目标不少于约 44px；高对比按钮、清晰禁用态、键盘焦点与 reduced-motion 支持。"), bullet("单列页面避免复杂路由；进度条在平台选择和生成完成时即时反馈。"), bullet("Google 与小红书跳转只打开平台入口；剪贴板失败时自动使用兼容性降级。"), bullet("明确提示“AI 只辅助表达，不代替真实体验”，避免诱导或自动发布。"), PageBreak()]

# Prompt
story += [p("02  跨平台 Prompt 设计", "CNH1"), p("Prompt 采用“共同事实层 + 平台风格层 + 结构化输出层”。共同层锁定店名、城市和用户勾选项；平台层只改变表达；结构层一次返回评论、摘要、回复草稿，避免重复调用。")]
prompt_rows = [
    [p("维度", "HeaderWhite"), p("Google", "HeaderWhite"), p("小红书", "HeaderWhite")],
    [p("语言", "CNBody"), p("英文", "CNBody"), p("简体中文", "CNBody")],
    [p("长度", "CNBody"), p("70-110 words", "CNBody"), p("100-160 字", "CNBody")],
    [p("语气", "CNBody"), p("北美本地顾客；具体、克制、对话感", "CNBody"), p("自然口语；轻种草；分段有呼吸感", "CNBody")],
    [p("格式", "CNBody"), p("无 Emoji、无 hashtag、无星级", "CNBody"), p("2-4 段、2-4 Emoji、3-5 话题", "CNBody")],
    [p("负向约束", "CNBody"), p("不虚构饮品、价格、员工或到店事实", "CNBody"), p("不夸张营销、不用绝对化表达、不虚构品名", "CNBody")],
]
t = Table(prompt_rows, colWidths=[27*mm, 61*mm, 64*mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), GREEN), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("BACKGROUND", (0,1), (-1,-1), colors.white), ("BOX", (0,0), (-1,-1), .6, LINE),
    ("INNERGRID", (0,0), (-1,-1), .35, LINE), ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
]))
story += [t, Spacer(1, 6*mm), p("调优过程", "CNH2"), bullet("第一版只描述“写好评”，结果容易空泛；改为只允许使用已选择感受，并显式禁止虚构细节。"), bullet("Google 版本加入篇幅与禁用项，减少营销腔、Emoji 和泛化赞美。"), bullet("小红书版本限制段落、Emoji 和话题数量，兼顾平台感与可读性，避免符号堆砌。"), bullet("要求 strict JSON，一次生成三部分内容；temperature 0.75 保留变化但不牺牲约束。"), p("核心 Prompt 片段", "CNH2"), p("Help the customer express only the experience they selected; never fabricate visits, products, prices, staff names, or facts. Return strict JSON with exactly three string fields: review, summary, reply.", "CodeBlock"), PageBreak()]

# AI coding
story += [p("03  AI 辅助编程策略与提效", "CNH1"), p("本项目由 Codex 从空目录完成。策略是先锁定可演示闭环，再补安全与自动化，最后通过生产构建和 PDF 渲染验证，而不是先做视觉装饰。")]
story += [p("使用策略", "CNH2"), bullet("需求拆解：把任务书转为状态机 - 感受、平台、生成、编辑、复制跳转、商家通知。"), bullet("一次性实现主交互和视觉系统，减少组件间来回调整；保持一页、少状态、少依赖。"), bullet("Prompt 与 UI 同步设计：UI 限制输入范围，Prompt 再做第二层事实约束。"), bullet("先实现无 Key fallback，再接兼容 OpenAI 协议的服务端调用，使评审现场可控。"), bullet("生成专属社交分享图，并把项目思路自动排版为可提交 PDF。")]
story += [p("提效心得", "CNH2"), p("最明显的提效不是代码生成速度，而是把产品、Prompt、安全、失败降级和交付文档放进同一条验证链。AI 适合快速产出完整第一版，但仍需人为校验三件事：是否虚构事实、是否真的形成发布闭环、是否把敏感配置留在浏览器。", "Quote")]
metrics = [[p("约 35 分钟", "CNH2"), p("实际执行耗时", "Small")], [p("1 个页面", "CNH2"), p("完成全部核心流程", "Small")], [p("0 个前端 Key", "CNH2"), p("密钥只在服务端读取", "Small")]]
t = Table(metrics, colWidths=[51*mm]*3)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CREAM),("BOX",(0,0),(-1,-1),.6,LINE),("INNERGRID",(0,0),(-1,-1),.35,LINE),("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9)]))
story += [t, PageBreak()]

# Webhook and safety
story += [p("04  企业微信自动化与安全", "CNH1"), p("同一次模型调用返回 review / summary / reply。服务端将后两项拼成企业微信 Markdown 消息并调用群机器人 Webhook；失败不阻塞顾客拿到评论。")]
story += [p("Webhook Payload", "CNH2"), p('{<br/>  "msgtype": "markdown",<br/>  "markdown": {<br/>    "content": "**Sunny Tea House 收到新评价**\\n&gt; 摘要：...\\n&gt; 回复草稿：..."<br/>  }<br/>}', "CodeBlock")]
story += [p("处理策略", "CNH2"), bullet("未配置 Webhook：前端展示 Mock 推送卡，便于评审查看数据形态。"), bullet("已配置 Webhook：服务端异步推送；Webhook 错误被隔离，不影响主链路。"), bullet("建议生产化时增加签名代理、错误重试队列、脱敏日志和管理员开关。")]
story += [p("API Key 与成本", "CNHH2") if False else p("API Key 与成本", "CNH2"), bullet("AI_API_KEY 和 WECOM_WEBHOOK_URL 只从服务端环境变量读取，前端 bundle 与仓库均不出现真实值。"), bullet("输入只接受白名单平台和最多两个标签，减少 prompt injection 与异常 token 消耗。"), bullet("单次 max_tokens=600；一次请求同时完成三项生成，减少调用次数。"), bullet("推荐上线时增加按 IP / 设备限流、每日硬预算、供应商配额告警、Key 轮换与来源域校验。"), bullet("保留演示 fallback；额度耗尽或未配置时不产生模型费用，现场体验仍完整。"), PageBreak()]

# Risks and handoff
story += [p("05  验证、边界与下一步", "CNH1"), p("当前版本已完成生产构建验证，覆盖任务书中的核心交互和可选自动化展示。以下边界在 Demo 中被有意保留，便于评审时清晰说明。")]
story += [p("已验证", "CNH2"), bullet("1-2 项选择上限、平台切换、加载态、生成与再生成。"), bullet("生成文本可编辑；剪贴板兼容降级；发布入口新窗口打开。"), bullet("服务端输入校验、无 Key fallback、真实 API 分支和企微 payload 拼装。"), bullet("响应式样式、键盘焦点、reduced-motion 与生产构建。")]
story += [p("Demo 边界", "CNH2"), bullet("Sunny Tea House 地址为虚构信息；Google 跳转使用地点搜索，而非真实商户写评价深链。"), bullet("小红书浏览器入口不保证直接唤起创作页，受平台与设备策略影响。"), bullet("Demo 不做登录、持久化、自动预填或自动代发，避免越权和误发布。"), bullet("真实模型质量仍需用 20-30 组标签组合做离线样本评估后再上线。")]
story += [p("下一步优先级", "CNH2")]
next_rows = [
    [p("P0", "Label"), p("配置托管环境 secrets，并用真实模型完成中文/英文样本验收。", "CNBody")],
    [p("P1", "Label"), p("接入限流与可观测性，记录延迟、失败率、复制率和跳转率，不记录完整用户文案。", "CNBody")],
    [p("P2", "Label"), p("根据真实商户 Place ID 与设备环境优化跳转；为 Prompt 增加可灰度版本号。", "CNBody")],
]
t = Table(next_rows, colWidths=[18*mm, 134*mm])
t.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1),LIME),("BOX",(0,0),(-1,-1),.6,LINE),("INNERGRID",(0,0),(-1,-1),.35,LINE),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story += [t, Spacer(1, 9*mm), p("交付清单", "CNH2"), p("移动端 Demo 源文件 · 服务端生成路由 · 环境变量模板 · 企业微信 Mock / 真实分支 · 项目 README · 本 PDF 文档 · 社交分享图", "Quote")]

doc.build(story, onFirstPage=page_header_footer, onLaterPages=page_header_footer)
print(OUT)
