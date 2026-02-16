# Pokemon Agent (GBA Emerald, macOS, mGBA)

目标：构建一个能自动启动 mGBA、基于视觉感知与 LLM 决策的宝可梦 Agent。支持自适应采集、遇阻联网检索与经验总结。

## 快速开始
1. 准备合法 ROM 并记录路径。
2. 安装并验证 mGBA 可正常打开 ROM。
3. 安装依赖（PDM）：
   - `pdm install`
4. 配置 `config/config.json` 中的 `rom_path` 与 `mgba_path`。
5. 运行 `pdm run python3 src/main.py` 进入采集循环（会自动尝试启动游戏菜单）。

## 目录说明
- `PLAN.md` 项目总体计划
- `ROADMAP.md` 里程碑与版本节奏
- `DECISIONS.md` 关键技术决策记录
- `EVAL.md` 评估指标与实验记录
- `NOTES_TEMPLATE.md` 会话总结模板
- `config/` 配置目录
- `src/` 代码目录
- `scripts/` 脚本目录
- `agent/ARCHITECTURE.md` Agent 架构与数据流
- `agent/RUNBOOK.md` Agent 运行与排障指南
- `agent/skills/` Agent 技能模板

## 重要约定
- 不存放 ROM 到仓库。
- 只在必要时联网检索，检索结果必须摘要化。
