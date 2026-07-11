# Sunny Tea House - AI 评价生成 Demo

在线演示：https://chengqun2.github.io/AI_evaluation/

一个面向手机浏览器的完整 H5 闭环：选择 1-2 个真实感受 -> 选择 Google / 小红书 -> AI 生成平台化文案 -> 用户编辑 -> 复制并跳转发布。生成后同时展示企业微信机器人推送的摘要与商家回复草稿。

## 体验与实现

- 无 Key 可演示：默认使用受控本地文案生成器，所有交互均可跑通，并明确显示 `DEMO`。
- 有 Key 可上线：服务端读取 OpenAI-compatible API 配置，Key 不进入浏览器包。
- Google：英文、70-110 词、北美本地消费者口吻，不使用 Emoji 与话题标签。
- 小红书：中文短段落、适量 Emoji 与 3-5 个话题标签，保留自然呼吸感。
- 用户控制：生成结果必须经过可编辑文本框，页面不会自动代发。
- 企微附加题：配置 Webhook 后推送 Markdown；未配置时展示相同 payload 的 Mock 结果。

## 本地运行

```bash
npm install
npm run dev
```

Windows PowerShell 可使用：

```powershell
$env:WRANGLER_LOG_PATH='.wrangler/wrangler.log'
npx vinext dev
```

复制 `.env.example` 为 `.env.local` 并填写服务端变量即可接入真实模型。不要把 `.env.local` 提交到版本库。

## 环境变量

| 变量 | 用途 | 是否必需 |
|---|---|---|
| `AI_API_URL` | OpenAI-compatible chat completions 完整地址 | 真实 AI 模式必需 |
| `AI_API_KEY` | 模型服务密钥 | 真实 AI 模式必需 |
| `AI_MODEL` | 模型名称 | 真实 AI 模式必需 |
| `WECOM_WEBHOOK_URL` | 企业微信群机器人 Webhook | 可选 |

## 安全与成本

Key 仅在服务端路由读取；仓库只保留占位符。生产环境建议再增加每 IP / 设备限流、请求体白名单、单次 token 上限、每日预算告警、模型供应商侧配额与 Key 定期轮换。演示场景可以始终保留无成本 fallback，避免现场因额度或网络失败中断。


完整设计与调优说明见 `output/pdf/Sunny-Tea-House-Project-Document.pdf`。

## GitHub Pages

仓库包含独立的静态构建入口。推送到 `main` 或 Pages 发布分支后，GitHub Actions 会执行 `npm run build:pages` 并发布 `pages-dist`。由于 GitHub Pages 不运行服务端函数，Pages 版本固定使用无 Key Demo 生成器；服务端真实 AI 与企微 Webhook 分支仍保留在项目源码中，可部署到支持 Serverless 的平台。
