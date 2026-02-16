# Architecture

## 模块
- Game Runner: 启动 mGBA、聚焦窗口、分辨率固定。
- Observation: 自适应采集，输出帧与时间戳。
- State Tracker: UI 识别与 OCR，输出结构化状态。
- Policy: LLM 决策，输出动作序列。
- Action Executor: 键盘输入执行。
- Retrieval: 触发检索，摘要化输出。
- Memory: 会话总结与策略沉淀。
- Skills: 技能化行为模板与白名单。

## 数据流
1. Runner 启动并固定窗口。
2. Observation 采集画面。
3. State Tracker 解析画面为状态。
4. Policy 基于状态与目标输出动作。
5. Executor 执行动作。
6. Memory 记录关键事件与总结。
7. Retrieval 在卡关时加入外部知识。
8. Skills 通过白名单约束可用能力。

## 自适应采集
- 探索与对话低帧率。
- 战斗与菜单高帧率。
- 变化检测驱动动态调节。
