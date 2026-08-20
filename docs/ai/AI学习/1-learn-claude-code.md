GitHub上一个以Claude code为例子的agent/harness原理[教程](https://github.com/shareAI-lab/learn-claude-code)

## 前言
agent = model + harness
### Agency
agency是感知、推理、行动的能力，llm的agency是训练出来的，不是编写出来的。
**提示词水管工式 "Agent" 是不做模型的程序员的意淫。**
### 从开发agent到开发harness
开发agent一方面是开发model，另一方面是开发harness
### harness工程师在做什么
实现工具、策划知识、管理上下文、控制权限、收集执行过程数据
### Claude code的构成
```
Claude Code = 一个 agent loop
            + 工具 (bash, read, write, edit, glob, grep, browser...)
            + 按需 skill 加载
            + 上下文压缩
            + 子 agent 派生
            + 带依赖图的任务系统
            + 异步邮箱的团队协调
            + 任务绑定的 worktree 并行执行
            + 权限治理
```

### 一个agent loop
```python
def agent_loop(messages):
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM,
            messages=messages, tools=TOOLS,
        )
        messages.append({"role": "assistant",
                         "content": response.content})

        tool_calls = [
            block for block in response.content if block.type == "tool_use"
        ]
        if not tool_calls:
            return

        results = []
        for block in tool_calls:
            output = TOOL_HANDLERS[block.name](**block.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": output,
            })
        messages.append({"role": "user", "content": results})
```

```
                    THE AGENT PATTERN
                    =================

    User --> messages[] --> LLM --> response
                                      |
                              包含 tool_use block?
                           /                          \
                         yes                           no
                          |                             |
                    execute tools                    return text
                    append results
                    loop back -----------------> messages[]


    这是最小循环。每个 AI Agent 都需要这个循环。
    模型决定何时调用工具、何时停止。
    代码只是执行模型的要求。
    本仓库教你构建围绕这个循环的一切 --
    让 agent 在特定领域高效工作的 harness。
```

### 学习路线
能动手、能做复杂任务、能记住和恢复、能长期运行、能协作、能扩展并合体

```mermaid
flowchart TD
    %% 统一定义卡片样式：加入 text-align:left 保证列表不会居中乱飘
    classDef stage1 fill:#E3F2FD,stroke:#1976D2,stroke-width:2px,color:#0D47A1,rx:12,ry:12,text-align:left
    classDef stage2 fill:#E8F5E9,stroke:#388E3C,stroke-width:2px,color:#1B5E20,rx:12,ry:12,text-align:left
    classDef stage3 fill:#FFF3E0,stroke:#F57C00,stroke-width:2px,color:#E65100,rx:12,ry:12,text-align:left
    classDef stage4 fill:#FCE4EC,stroke:#C2185b,stroke-width:2px,color:#880E4F,rx:12,ry:12,text-align:left
    classDef stage5 fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px,color:#4A148C,rx:12,ry:12,text-align:left
    classDef stage6 fill:#E0F7FA,stroke:#0097A7,stroke-width:2px,color:#006064,rx:12,ry:12,text-align:left
    
    %% 背景框样式
    classDef groupBox fill:#F8F9FA,stroke:#CED4DA,stroke-width:2px,stroke-dasharray: 5 5,rx:15,ry:15,color:#495057
    
    %% 第一层：1-3阶段
    subgraph Phase1 ["🌱 阶段 1-3：基础能力构建（从简单到复杂）"]
        direction LR
        S1["<b>第一阶段：让 Agent 能动手</b><br/>━━━━━━━━━━━━━<br/><b>s01 Agent Loop</b><br/>└─ 一个循环 + bash<br/><br/><b>s02 Tool Use</b><br/>└─ 单个到多个工具<br/><br/><b>s03 Permission</b><br/>└─ 判断能不能做<br/><br/><b>s04 Hooks</b><br/>└─ 工具前后留扩展插口"]:::stage1

        S2["<b>第二阶段：做复杂任务</b><br/>━━━━━━━━━━━━━<br/><b>s05 TodoWrite</b><br/>└─ 先列计划，再执行<br/><br/><b>s06 Subagent</b><br/>└─ 全新消息，返回最终文本<br/><br/><b>s08 Context Compact</b><br/>└─ 长下文腾空间"]:::stage2

        S3["<b>第三阶段：跨会话记忆</b><br/>━━━━━━━━━━━━━<br/><b>s09 Memory</b><br/>└─ 保存并召回可复用知识"]:::stage3

        S1 ==> S2 ==> S3
    end

    %% 第二层：4-6阶段
    subgraph Phase2 ["🚀 阶段 4-6：高阶能力进化（长期、协作与融合）"]
        direction LR
        S4["<b>第四阶段：让任务长期运行</b><br/>━━━━━━━━━━━━━<br/><b>s10 Task System</b><br/>└─ 任务落盘记依赖<br/><br/><b>s11 Background Tasks</b><br/>└─ 慢操作丢后台<br/><br/><b>s12 Cron Scheduler</b><br/>└─ 按时自动触发"]:::stage4

        S5["<b>第五阶段：让多个 Agent 协作</b><br/>━━━━━━━━━━━━━<br/><b>s13 Agent Teams</b><br/>└─ 队友 + 消息投递 + 协作协议<br/>└─ 原子认领就绪任务<br/>└─ 任务绑定的 Worktree"]:::stage5

        S6["<b>第六阶段：接外部能力合体</b><br/>━━━━━━━━━━━━━<br/><b>s07 Skill Loading</b><br/>└─ 技能按需展开<br/><br/><b>s14 MCP Plugin</b><br/>└─ 外部接进工具池<br/><br/><b>s15 Agent Harness 集成</b><br/>└─ 课程机制回到同一循环"]:::stage6

        S4 ==> S5 ==> S6
    end

    %% 第三层：编排与目标闭环
    subgraph Phase3 ["🎯 第七阶段：编排与目标闭环"]
        direction LR
        S7["<b>第七阶段：编排并完成</b><br/>━━━━━━━━━━━━━<br/><b>s16 Workflow Runtime</b><br/>└─ 脚本拥有固定编排<br/><br/><b>s17 Goal Loop</b><br/>└─ 独立判断决定何时停止"]:::stage1
        S6 ==> S7
    end

    %% 将三个模块连接起来，形成 Z 字形阅读流
    Phase1 ===> Phase2 ===> Phase3

    %% 应用背景样式
    class Phase1,Phase2,Phase3 groupBox

```

## S01-Agent loop

> One loop & bash is all you need

传统chat的问题：大模型输出完了就结束了，不会自己调试。
解决方案：引入agent loop，harness内核本质是一个循环

![[1-learn-claude-code-1787210447380.webp]]

## s02-Tool Use

![[1-learn-claude-code-1787210921245.webp]]

## s03-Permissiong

![[1-learn-claude-code-1787211237210.webp]]

## s04-Hooks

想扩展agent的行为，又不改变循环本身，把扩展挂在外面

![[1-learn-claude-code-1787211830207.webp]]

## s05-TodoWrite
