---
description: 生成可打印的试卷，格式为 PDF，包含答案
---

## 上下文

- 当前主题：!`ls .learning/`

## 你的任务

生成专业的、可打印的试卷和单独的答案，让用户可以离线打印并完成。

### 步骤 1：收集主题上下文

从上面的上下文识别主题目录（忽略 `scripts`、`references`、`config.json`）。

然后阅读：

- `.learning/<主题-slug>/syllabus.md` - 大纲中有哪些概念
- `.learning/<主题-slug>/metadata.json` - 进度和当前阶段
- `.learning/<主题-slug>/progress.json` - 已完成的概念
- `.learning/<主题-slug>/review_schedule.json` - 学过和复习过的内容

### 步骤 2：合并上下文

创建摘要：

- **主题名称**：[从元数据提取]
- **学习阶段**：[从元数据的当前阶段]
- **涵盖的概念**：[从 progress.json 列表]
- **已掌握的概念**：[从 review_schedule.json - review_count > 2 的概念]
- **近期概念**：[最近学的 5-10 个概念]
- **薄弱领域**：[复习次数少或标记为困难的概念]

### 步骤 3：使用上下文调用试卷生成器

使用 Task 工具调用 exam-generator 智能体与合并的上下文：

**如何调用智能体：**

使用 Task 工具：

- `subagent_type`："exam-generator"
- `prompt`：包含所有合并的上下文和说明
- `description`：简短描述，如"生成可打印试卷"

**示例：**

```
Task 工具调用：
- subagent_type: "exam-generator"
- description: "生成可打印试卷"
- prompt: "生成带答案的可打印试卷。

主题上下文：
- 主题：[主题名称]
- 当前阶段：[阶段名称]
- 涵盖的概念总数：[N]
- 已掌握的概念：[列表]
- 近期概念：[列表]
- 薄弱领域：[列表]

请：
1. 在线搜索该领域的真实试卷示例
2. 询问用户偏好（类型、难度、范围）
3. 生成涵盖这些概念的试卷（重点关注近期和薄弱领域）
4. 生成单独的答案
5. 使用脚本将两者转换为 PDF
6. 提供文件路径和后续步骤"
```

智能体将处理完整的流程并返回结果。
