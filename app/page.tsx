"use client";

import { useMemo, useState } from "react";

type Platform = "google" | "xiaohongshu";

const FEELINGS = [
  { id: "service", label: "服务很贴心", icon: "☺" },
  { id: "speed", label: "出餐速度快", icon: "↗" },
  { id: "clean", label: "环境很干净", icon: "✦" },
  { id: "pretty", label: "饮品颜值高", icon: "◉" },
  { id: "taste", label: "味道很惊喜", icon: "♡" },
  { id: "value", label: "性价比不错", icon: "$" },
];

const PLATFORM_META = {
  google: {
    name: "Google",
    hint: "真实口吻 · 中文",
    mark: "G",
    url: "https://www.google.com/maps/search/?api=1&query=Sunny+Tea+House+San+Jose",
  },
  xiaohongshu: {
    name: "小红书",
    hint: "种草感 · 中文",
    mark: "小",
    url: "https://www.xiaohongshu.com/explore",
  },
} as const;

function buildStaticDemo(feelings: string[], platform: Platform) {
  const chinese: Record<string, string> = {
    "服务很贴心": "店员服务很贴心",
    "出餐速度快": "出餐速度很快",
    "环境很干净": "店里干净又舒服",
    "饮品颜值高": "饮品颜值很在线",
    "味道很惊喜": "味道比预期更惊喜",
    "性价比不错": "这个品质和价格很值",
  };
  const zh = feelings.map((item) => chinese[item]).filter(Boolean);
  const review = platform === "google"
    ? `路过 San Jose 时顺道去了 Sunny Tea House，整体体验挺舒服的。${zh.join("，")}。饮品清爽不齁甜，喝起来很顺口，环境也让人放松。下次来附近还会想再喝一杯。`
    : `在 San Jose 挖到一家会想二刷的奶茶店！🧋\n\nSunny Tea House 真的有点超出预期～${zh.join("，")}，整个体验很舒服。点的饮品清爽不齁甜，随手拍也很好看 ✨\n\n如果刚好在附近，适合来一杯给下午充充电。下次想再试试别的口味！\n\n#SanJose探店 #湾区美食 #奶茶控 #SunnyTeaHouse`;
  return {
    review,
    summary: `顾客认可${zh.join("、")}，整体体验积极，并表达了再次到店意愿。`,
    reply: `谢谢你分享这次体验！很开心我们的${zh.join("和")}给你留下了好印象。期待下次再为你做一杯喜欢的饮品！`,
    source: "demo",
  };
}

export default function Home() {
  const [feelings, setFeelings] = useState<string[]>([]);
  const [platform, setPlatform] = useState<Platform | null>(null);
  const [review, setReview] = useState("");
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState("");
  const [details, setDetails] = useState<{ summary: string; reply: string; source: string } | null>(null);

  const selectedLabels = useMemo(
    () => FEELINGS.filter((item) => feelings.includes(item.id)).map((item) => item.label),
    [feelings],
  );

  function toggleFeeling(id: string) {
    if (feelings.includes(id)) {
      setFeelings(feelings.filter((item) => item !== id));
      return;
    }
    if (feelings.length >= 2) {
      showToast("最多选择 2 项感受");
      return;
    }
    setFeelings([...feelings, id]);
  }

  function showToast(message: string) {
    setToast(message);
    window.setTimeout(() => setToast(""), 2200);
  }

  async function generateReview() {
    if (!feelings.length || !platform) return;
    setLoading(true);
    setReview("");
    setDetails(null);

    try {
      if (window.location.hostname.endsWith("github.io")) {
        await new Promise((resolve) => window.setTimeout(resolve, 700));
        const data = buildStaticDemo(selectedLabels, platform);
        setReview(data.review);
        setDetails({ summary: data.summary, reply: data.reply, source: data.source });
        showToast("演示文案已生成");
        return;
      }
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feelings: selectedLabels, platform }),
      });
      if (!response.ok) throw new Error("generation failed");
      const data = await response.json();
      setReview(data.review);
      setDetails({ summary: data.summary, reply: data.reply, source: data.source });
      showToast(data.source === "ai" ? "AI 已生成并同步给店家" : "演示文案已生成");
    } catch {
      const data = buildStaticDemo(selectedLabels, platform);
      setReview(data.review);
      setDetails({ summary: data.summary, reply: data.reply, source: data.source });
      showToast("已切换至演示生成模式");
    } finally {
      setLoading(false);
    }
  }

  async function copyAndOpen() {
    if (!review || !platform) return;
    try {
      await navigator.clipboard.writeText(review);
    } catch {
      const textarea = document.createElement("textarea");
      textarea.value = review;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      textarea.remove();
    }
    showToast("已复制，即将前往发布");
    window.setTimeout(() => window.open(PLATFORM_META[platform].url, "_blank", "noopener,noreferrer"), 450);
  }

  const canGenerate = feelings.length > 0 && platform !== null;

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Sunny Tea House 首页">
          <span className="brand-mark">S</span>
          <span>Sunny Tea House</span>
        </a>
        <div className="location"><span>●</span> San Jose, CA</div>
      </header>

      <section className="hero" id="top">
        <div className="eyebrow"><span className="spark">✦</span> AI REVIEW ASSISTANT</div>
        <h1>喜欢这一杯？<br /><em>帮我们说出来。</em></h1>
        <p>选出此刻最真实的感受，让 AI 帮你写好评价。<br />你始终拥有最终决定权。</p>
        <div className="progress" aria-label="完成进度">
          <span className="active" />
          <span className={platform ? "active" : ""} />
          <span className={review ? "active" : ""} />
        </div>
      </section>

      <section className="step-card">
        <div className="step-heading">
          <span className="step-number">01</span>
          <div><h2>今天哪里让你满意？</h2><p>选择 1–2 项</p></div>
          <span className="selection-count">{feelings.length}/2</span>
        </div>
        <div className="feeling-grid">
          {FEELINGS.map((item) => {
            const selected = feelings.includes(item.id);
            return (
              <button
                key={item.id}
                className={`feeling-chip ${selected ? "selected" : ""}`}
                onClick={() => toggleFeeling(item.id)}
                aria-pressed={selected}
              >
                <span className="chip-icon">{item.icon}</span>
                <span>{item.label}</span>
                <span className="check">{selected ? "✓" : "+"}</span>
              </button>
            );
          })}
        </div>
      </section>

      <section className="step-card">
        <div className="step-heading">
          <span className="step-number">02</span>
          <div><h2>想发布到哪里？</h2><p>AI 会自动匹配语言与语气</p></div>
        </div>
        <div className="platform-grid">
          {(Object.keys(PLATFORM_META) as Platform[]).map((id) => {
            const item = PLATFORM_META[id];
            const selected = platform === id;
            return (
              <button
                key={id}
                className={`platform-card ${selected ? "selected" : ""}`}
                onClick={() => setPlatform(id)}
                aria-pressed={selected}
              >
                <span className={`platform-logo ${id}`}>{item.mark}</span>
                <span><strong>{item.name}</strong><small>{item.hint}</small></span>
                <span className="radio">{selected ? "●" : ""}</span>
              </button>
            );
          })}
        </div>
      </section>

      <section className={`step-card result-card ${review ? "revealed" : ""}`}>
        <div className="step-heading">
          <span className="step-number">03</span>
          <div><h2>你的专属评价</h2><p>{review ? "可以自由修改，满意后再发布" : "选择完成后，让 AI 动笔"}</p></div>
          {details && <span className="ai-badge">{details.source === "ai" ? "AI" : "DEMO"}</span>}
        </div>

        {!review && !loading && (
          <div className="empty-state">
            <div className="wand">✦</div>
            <p>{canGenerate ? "准备好了，一键生成你的评价" : "完成上面两步后即可生成"}</p>
          </div>
        )}

        {loading && (
          <div className="loading-state" aria-live="polite">
            <div className="loader"><span /><span /><span /></div>
            <strong>正在匹配平台语气…</strong>
            <p>把真实感受整理成自然表达</p>
          </div>
        )}

        {review && (
          <>
            <label className="editor-label" htmlFor="review-editor">点击文字即可编辑</label>
            <textarea
              id="review-editor"
              className="review-editor"
              value={review}
              onChange={(event) => setReview(event.target.value)}
              rows={platform === "xiaohongshu" ? 10 : 7}
            />
            <div className="editor-meta"><span>{review.length} 字符</span><span>内容由你确认后发布</span></div>
          </>
        )}

        <button className="primary-button" disabled={!canGenerate || loading} onClick={review ? copyAndOpen : generateReview}>
          <span>{review ? "复制并前往发布" : "生成我的评价"}</span>
          <span className="button-arrow">→</span>
        </button>

        {review && (
          <button className="regenerate" onClick={generateReview} disabled={loading}>↻ 换一个版本</button>
        )}
      </section>

      {details && (
        <section className="merchant-card">
          <div className="merchant-title"><span>企</span><div><strong>商家自动化</strong><small>企业微信机器人 · {details.source === "ai" ? "已推送" : "Mock 演示"}</small></div><b>✓</b></div>
          <details>
            <summary>查看推送内容</summary>
            <div className="message-preview"><label>评论摘要</label><p>{details.summary}</p><label>回复草稿</label><p>{details.reply}</p></div>
          </details>
        </section>
      )}

      <footer>
        <span>Sunny Tea House</span>
        <p>AI 只辅助表达，不代替你的真实体验</p>
        <span>San Jose · 2026</span>
      </footer>

      {toast && <div className="toast" role="status">✓ {toast}</div>}
    </main>
  );
}
