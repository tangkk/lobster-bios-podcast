# 龙虾人物

## Editorial Memory

人物故事播客。每期聚焦一个关键人物的一段代表性阶段或关键事件，而非完整传记；重点寻找人物在困境中的选择、冲突与转折。少煽情、多事实；少神话、多结构；通过一个人的具体故事看懂更大的思想、时代或结构问题。关键历史节点尽量给可核验背景，结尾冷静收束，不喊口号。

## Workflow

**IDEA → WRITE → FREEZE → PREFLIGHT → BUILD → LISTEN → PUBLISH → VERIFY**。用户确认的定稿就是 TTS-ready canonical 稿，同时用于文字版和 Podcast；定稿前不进入 GitHub 发布流程，正式发布前再次确认。

## Canonical / TTS-ready

短句和清晰叙事优先，复杂背景拆开讲，关键转折自然分段。人名、外文名、年份、数字、术语在定稿前逐项检查实际朗读效果；人名是最高优先级 QA 项。文字版正文与 canonical 逐字一致。目标约十二分钟、通常十一到十五分钟，但不机械凑时长。

## Voice & Pause Baseline

使用讯飞，人物保留旧 SOP 已验证的双轨：**文科/感性人物**默认 `x6_lingyuyan_pro`、speed 50、volume 52、pitch 50；**理科/理性人物**使用 `science` profile（`x6_lingfeiyi_pro`、speed 46、volume 52、pitch 48）。

长文正式主路径：**自然段分段合成 + 段间约 350ms 静音**。整体节奏快于《龙虾故事》，但段间要清楚，避免连读。过长段落才按完整句拆，经验约 240–420 字/segment。旧 SOP 已记录文科/感性版本的 segmented + short pause 试听通过，因此 350ms 作为 baseline，而不是重新从零猜参数。

正式长文使用 `xfyun_segmented_run.py`，通过 `--profile default` 或 `--profile science` 选择人物类型。TTS 前检查讯飞环境变量；新稿/新环境先跑第一段最小样本。

## QA & Publishing Guardrails

Preflight 检查 Editorial / Facts / TTS / Metadata；Audio QA 检查人名、发音、数字、断句、句间/段间停顿、整体节奏。episode number 从 feed 推导，guid、音频文件名、文章音频链接一致；RSS description 使用真实换行。发布后验证 R2、Podcast RSS、文字 RSS 和文章。

README 是当前 source of truth；旧 OpenClaw SOP 只作历史参考，本机绝对路径、旧 rss-hosting/audio、消息平台交付和逐段进度回报等规则淘汰。
