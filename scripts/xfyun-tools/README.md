# 龙虾人物 TTS 工具说明

## 默认音色
见 `voice_profiles/default.json`。

人物另有 `voice_profiles/science.json` 预设（理科/理性风格），用 `--profile science` 调用。

## 推荐执行方式（避免环境变量丢失）
```
./with_xfyun_env.sh python3 xfyun_super_official_run.py --profile default --text "..." --out out.mp3
```

包装脚本会自动 source 常见 shell 配置（`.bash_profile/.zprofile/.zshrc/.bashrc`）并校验：
- `XFYUN_APPID`
- `XFYUN_API_KEY`
- `XFYUN_API_SECRET`
