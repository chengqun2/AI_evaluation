import { NextResponse } from "next/server";

type Platform = "google" | "xiaohongshu";

const feelingMap: Record<string, { en: string; zh: string }> = {
  "服务很贴心": { en: "the thoughtful, friendly service", zh: "店员服务很贴心" },
  "出餐速度快": { en: "the surprisingly quick service", zh: "出餐速度很快" },
  "环境很干净": { en: "the clean, comfortable space", zh: "店里干净又舒服" },
  "饮品颜值高": { en: "the beautiful presentation", zh: "饮品颜值很在线" },
  "味道很惊喜": { en: "the balanced, genuinely good flavor", zh: "味道比预期更惊喜" },
  "性价比不错": { en: "the fair price for the quality", zh: "这个品质和价格很值" },
};

function mockContent(feelings: string[], platform: Platform) {
  const items = feelings.map((item) => feelingMap[item]).filter(Boolean);
  const en = items.map((item) => item.en);
  const zh = items.map((item) => item.zh);
  const review = platform === "google"
    ? `Stopped by Sunny Tea House while I was in San Jose and had a really pleasant experience. I especially appreciated ${en.join(" and ")}. The drink tasted fresh without being overly sweet, and the whole visit felt easy and welcoming. I’d happily come back when I’m in the area.`
    : `在 San Jose 挖到一家会想二刷的奶茶店！🧋\n\nSunny Tea House 真的有点超出预期～${zh.join("，")}，整个体验很舒服。点的饮品清爽不齁甜，随手拍也很好看 ✨\n\n如果刚好在附近，适合来一杯给下午充充电。下次想再试试别的口味！\n\n#SanJose探店 #湾区美食 #奶茶控 #SunnyTeaHouse`;
  return {
    review,
    summary: `顾客认可${zh.join("、")}，整体体验积极，并表达了再次到店意愿。`,
    reply: `谢谢你分享这次体验！很开心我们的${zh.join("和")}给你留下了好印象。期待下次再为你做一杯喜欢的饮品！`,
  };
}

function buildPrompt(feelings: string[], platform: Platform) {
  const style = platform === "google"
    ? "用简体中文写 70–110 字的评价，像一位真实的本地顾客。具体、客观、口语化。不使用 Emoji、话题标签、夸张营销、星级或虚构品名。"
    : "用简体中文写 100–160 字的小红书种草笔记。自然口语，2–4 个短段落，2–4 个恰当 Emoji，结尾 3–5 个相关话题。避免夸张营销、虚构品名和绝对化表达。";

  return `You are a review-writing assistant. Help the customer express only the experience they selected; never fabricate visits, products, prices, staff names, or facts. Store: Sunny Tea House, San Jose. Selected feelings: ${feelings.join(", ")}. Platform rules: ${style}\n\nReturn strict JSON with exactly three string fields: review, summary, reply. summary must be a one-sentence Chinese summary for the merchant. reply must be a warm, concise Chinese merchant reply draft. Do not wrap JSON in markdown.`;
}

export async function POST(request: Request) {
  try {
    const body = await request.json() as { feelings?: string[]; platform?: Platform };
    const feelings = Array.isArray(body.feelings) ? body.feelings.slice(0, 2) : [];
    const platform = body.platform;
    if (!feelings.length || !platform || !["google", "xiaohongshu"].includes(platform)) {
      return NextResponse.json({ error: "invalid input" }, { status: 400 });
    }

    const apiUrl = process.env.AI_API_URL;
    const apiKey = process.env.AI_API_KEY;
    const model = process.env.AI_MODEL;

    if (!apiUrl || !apiKey || !model) {
      await new Promise((resolve) => setTimeout(resolve, 850));
      return NextResponse.json({ ...mockContent(feelings, platform), source: "demo" });
    }

    const aiResponse = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
      body: JSON.stringify({
        model,
        temperature: 0.75,
        max_tokens: 600,
        messages: [
          { role: "system", content: "Follow platform style precisely. Output valid JSON only." },
          { role: "user", content: buildPrompt(feelings, platform) },
        ],
      }),
    });

    if (!aiResponse.ok) throw new Error(`AI provider returned ${aiResponse.status}`);
    const payload = await aiResponse.json();
    const raw = payload.choices?.[0]?.message?.content;
    if (typeof raw !== "string") throw new Error("invalid AI response");
    const parsed = JSON.parse(raw.replace(/^```json\s*|\s*```$/g, ""));

    const webhook = process.env.WECOM_WEBHOOK_URL;
    if (webhook) {
      await fetch(webhook, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          msgtype: "markdown",
          markdown: { content: `**Sunny Tea House 收到新评价**\n> 摘要：${parsed.summary}\n> 回复草稿：${parsed.reply}` },
        }),
      }).catch(() => undefined);
    }

    return NextResponse.json({ review: parsed.review, summary: parsed.summary, reply: parsed.reply, source: "ai" });
  } catch {
    return NextResponse.json({ error: "generation failed" }, { status: 502 });
  }
}
