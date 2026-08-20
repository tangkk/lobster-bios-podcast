# 龙虾人物

## Editorial Memory

人物故事播客。每期聚焦一个关键人物的一段代表性阶段或关键事件，而非完整传记；重点寻找人物在困境中的选择、冲突与转折。少煽情、多事实；少神话、多结构；通过一个人的具体故事看懂更大的思想、时代或结构问题。关键历史节点尽量给可核验背景，结尾冷静收束，不喊口号。

## Workflow

**IDEA → WRITE → FREEZE → PREFLIGHT → Draft PR → TTS PREVIEW → ARTIFACT → LISTEN → AUDIO QA → APPROVE ARTIFACT → MERGE → PUBLISH APPROVED ARTIFACT → VERIFY**。

用户确认的定稿就是 TTS-ready canonical 稿，同时用于文字版和 Podcast。每期使用独立 build/episode branch 与 Draft PR 作为 staging boundary：Draft PR 阶段可以反复改稿和生成试听，但 build-only preview 不得上传 R2、修改 RSS 或发布。只有 Audio QA 通过并明确批准该 artifact 后才 merge；正式发布仍是独立、明确的有副作用 gate。

## Canonical / TTS-ready

短句和清晰叙事优先，复杂背景拆开讲，关键转折自然分段。**canonical 从写作阶段就以语音体验为第一排版原则，而不是先按视觉文章排版、再让 TTS 适配。空行 / 自然段只表示真正需要明显长停顿或语义转场的位置；仅用于视觉强调的断行不得进入 canonical。短停顿由正常标点和 TTS 自身 prosody 处理。**

人名、外文名、年份、数字、金额、百分比、年龄、术语与缩写在 FREEZE 前逐项检查，并改成自然、明确、可正确朗读的形式；人名是最高优先级 QA 项。避免为了 TTS 添加奇怪标点或视觉排版 hack。文字版正文与 canonical 逐字一致，因此文字排版本身也服从 spoken rhythm。目标约十二分钟、通常十一到十五分钟，但不机械凑时长。

## Voice & Pause Baseline

使用讯飞，人物保留旧 SOP 已验证的双轨：**文科/感性人物**默认 `x6_lingyuyan_pro`、speed 50、volume 52、pitch 50；**理科/理性人物**使用 `science` profile（`x6_lingfeiyi_pro`、speed 46、volume 52、pitch 48）。

长文正式主路径：**自然段分段合成 + 段间约 350ms 静音**。整体节奏快于《龙虾故事》，但段间要清楚，避免连读。350ms 只用于真实段落 / segment 层级的长停顿；同一语义单元里的视觉强调句、冒号后续句、短对比句不应靠空行制造长停顿。过长段落才按完整句拆，经验约 240–420 字/segment。旧 SOP 已记录文科/感性版本的 segmented + short pause 试听通过，因此 350ms 作为 baseline，而不是重新从零猜参数。

正式长文使用 `xfyun_segmented_run.py`，通过 `--profile default` 或 `--profile science` 选择人物类型。TTS 前检查讯飞环境变量；新稿/新环境先跑第一段最小样本。

## GitHub Build / Artifact Standard

GitHub Actions 是纯 GitHub 路线的执行环境。Preview workflow 长期存在，优先由 Draft PR 自动触发；固定 Python 3.12，并先 `command -v ffmpeg` 检测 runner，存在则复用，不存在才安装，再用 `ffmpeg -version` 验证。Secrets 在真正工作前显式检查，关键步骤失败必须 fail closed，不用 `continue-on-error` 吞错。

Audio QA 批准的是一个具体的 preview artifact，而不是抽象的“这版文字”。**正式发布应优先复用已经试听批准的同一音频 artifact，不应无必要重新 TTS**，避免试听版与上线版产生差异。若技术上暂时必须重新生成，则必须把重新生成的成片视为新的待验证 artifact。

## QA & Publishing Guardrails

Preflight 检查 Editorial / Facts / TTS / Metadata；其中 TTS Preflight 必须做 spoken-form pass：数字 / 年份 / 英文 / 人名归一化、speech paragraphing、pause intent 检查。Audio QA 检查人名、发音、数字、断句、句间/段间停顿、整体节奏。

发布必须 idempotent / fail-closed：发布前检查 guid 未存在、episode number 是 feed 推导的下一期、canonical 与批准 artifact 存在、R2 key / 文件名 / 文章音频链接一致、Secrets 完整。重复 guid 或关键输入不一致时直接停止，禁止静默继续或盲目 rerun。

发布后独立 VERIFY，不能以“音频上传成功”代替发布成功：至少核对 R2 对象、Podcast RSS 最新 item、guid、enclosure URL / length、`itunes:duration`、description 真实换行、文字版 URL / RSS / 页面。时长直接从最终音频用 `ffprobe` 计算；shell 中避免使用 `SECONDS` 等特殊变量名，使用 `AUDIO_SECONDS` 等明确变量。

Preview workflow 可以长期保留；Publish 应使用通用、受控的发布入口，不为每一期长期保留 episode-specific workflow。临时一次性 workflow 用完应清理，避免以后误触发。

README 是当前 source of truth；旧 OpenClaw SOP 只作历史参考，本机绝对路径、旧 rss-hosting/audio、消息平台交付和逐段进度回报等规则淘汰。
