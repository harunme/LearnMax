# LearnMax 学习系统 - 使用说明

## 系统概述

本项目使用 LearnMax 框架：

- **F**orget（遗忘）：初学者心态
- **A**ct（行动）：动手实践
- **S**tate（状态）：优化专注力
- **T**each（教授）：讲解以保持记忆
- **E**nter（进入）：坚持优于强度
- **R**eview（复习）：间隔重复（1天 → 3天 → 7天 → 14天 → 30天 → 60天 → 90天）

## 目录结构

```
project-root/
├── CLAUDE.md (此文件)
├── .claude/
│   ├── agents/practice-creator.md
│   ├── commands/
│   │   ├── learn.md
│   │   ├── review.md
│   │   └── progress.md
│   └── settings.local.json
└── .learning/
    ├── scripts/
    │   ├── init_learning.py
    │   ├── log_progress.py
    │   ├── review_scheduler.py
    │   └── generate_syllabus.py
    ├── references/
    │   └── LearnMax_framework.md
    └── <主题-slug>/
        ├── metadata.json
        ├── syllabus.md
        ├── progress.md
        ├── review_schedule.json
        └── mastery.md
```

## 学习流程

### 每次学习开始

系统自动执行：

1. 检查待复习内容（通过命令中的上下文收集）
2. 如果有待复习，在学习新内容之前先进行复习
3. 引导你完成学习流程

### 学习流程

```
开始
  ↓
[1] 检查复习 → 如有待复习则进行复习
  ↓
[2] 状态检查："你专注吗？"
  ↓
[3] 展示大纲下一项
  ↓
[4] 用户学习/构建/练习
  ↓
[5] 询问："给我讲讲"
  ↓
[6] 记录进度 → 添加到复习计划
  ↓
[7] 提醒："下次学习：[时间]"
  ↓
结束
```

## 脚本使用

所有脚本位于 `.learning/scripts/`。从项目根目录运行。

### 初始化主题

**用户操作：** `/learn "主题名称"`

**流程：**

```bash
python3 .learning/scripts/init_learning.py "<主题名称>" .learning
```

→ **操作：** 根据用户的水平和重点创建全面的学习大纲

### 记录进度

```bash
python3 .learning/scripts/log_progress.py <主题-slug> "<总结>" [概念1] [概念2]
```

→ **操作：** 将每个概念添加到复习计划

### 复习管理

```bash
# 查看状态
python3 .learning/scripts/review_scheduler.py status <主题-slug>

# 添加概念
python3 .learning/scripts/review_scheduler.py add <主题-slug> "<概念>"

# 标记已复习
python3 .learning/scripts/review_scheduler.py review <主题-slug> "<概念>"
```

### 主题信息

```bash
# 列出所有主题
python3 .learning/scripts/generate_syllabus.py list

# 查看主题详情
python3 .learning/scripts/generate_syllabus.py info <主题-slug>
```

## 执行规则

**✅ 必须做到：**

1. 学习开始时检查复习
2. 解析脚本的 JSON 输出
3. 遵循 `next_action` 和 `llm_directive` 字段
4. 提示用户讲解概念
5. 记录每次学习活动
6. 将所学概念添加到复习计划
7. 生成全面的学习大纲（不是最简版）

**❌ 绝对不要：**

1. 跳过复习检查
2. 让用户被动接受
3. 忘记记录进度
4. 跳过将概念添加到复习
5. 生成最简版大纲

## 工作流程模式

```
[运行脚本] → [执行指令] → [回复用户]
```

## 生成学习大纲

当 `next_action: "generate_syllabus"` 时：

1. **阅读** `.learning/<主题-slug>/syllabus.md`（由初始化脚本创建）
2. **替换** 占位符为根据用户水平和重点定制的全面大纲
3. **包含部分**：概述、先决条件、学习目标、3-4 个阶段（含 🔨 动手项目）、教学里程碑、资源、成功标准
4. **更新元数据**：在 `.learning/<主题-slug>/metadata.json` 中设置 `"syllabus_generated": true`

## 教学提示

学习概念后，使用 `AskUserQuestion` 提示讲解：

```json
{
  "question": "准备好讲解你学到的东西了吗？",
  "header": "讲解",
  "multiSelect": false,
  "options": [
    {
      "label": "好的，我来讲解",
      "description": "我会用自己的话解释这个概念"
    },
    {
      "label": "需要先复习",
      "description": "想再看一下这个概念"
    },
    {
      "label": "还不确定",
      "description": "需要更多练习后再讲解"
    }
  ]
}
```

如果用户选择"好的，我来讲解"：

- "用你自己的话解释 [概念]"
- "你会怎么教给初学者？"
- "你会用什么类比？"

## 进度追踪

**里程碑：**

- 每 5 次学习：显示进度报告
- 每周：全面回顾学习轨迹
- 遇到困难时：回顾已学概念，找出差距

**查看学习次数：**

```bash
cat .learning/<主题-slug>/metadata.json | grep total_sessions
```

**近期进度：**

```bash
tail -30 .learning/<主题-slug>/progress.md
```

## 本系统的关键原则

- 使用 `AskUserQuestion` 收集学习偏好
- 始终提示用户讲解概念

**对用户的建议：**

- 1 个项目 = 1 个学习目标
- 每天 30 分钟 > 每周 3 小时（坚持优于强度）
- 主动学习 > 被动接受
- 教学 = 最佳记忆
- 信任间隔重复系统
