---
description: 使用基于项目的方法初始化或继续学习编程主题 $topic
---

## Context

- 当前主题: !`ls .learning/ 2>/dev/null | grep -v scripts`

**注意:** `.learning/` 目录已初始化。检查主题文件夹名称（忽略 `scripts/`）。

## Your Task

使用 FASTER 框架和基于项目的方法，为指定的编程主题初始化学习。

**如果主题已存在：**

- 告知用户："此项目已在学习 [主题名称]"
- 首先检查是否有待复习内容（如果有，先进行复习再开始新学习）
- 继续当前主题（1 个项目 = 1 个学习目标）

**如果主题不存在：**

1. **根据用户选择的主题，用 `AskUserQuestion` 收集学习偏好：**
   <example>

```json
[
  {
    "question": "你想通过 [topic] 达到什么水平？",
    "header": "Level",
    "multiSelect": false,
    "options": [
      { "label": "初级", "description": "基础知识和基本语法" },
      {
        "label": "中级",
        "description": "常见模式和项目实践"
      },
      { "label": "高级", "description": "架构和优化" },
      { "label": "专家", "description": "深入原理和最佳实践" }
    ]
  },
  {
    "question": "你的学习目标是什么？",
    "header": "Goal",
    "multiSelect": true,
    "options": [
      {
        "label": "构建项目",
        "description": "通过构建真实应用来学习"
      },
      {
        "label": "深入理解",
        "description": "理解底层原理"
      },
      {
        "label": "最佳实践",
        "description": "生产级代码模式"
      },
      {
        "label": "面试准备",
        "description": "问题解决和算法"
      }
    ]
  }
]
```

</example>

2. 运行: `python3 .learning/scripts/init_learning.py "[主题名称]" .learning`
3. 解析 JSON 输出并遵循 `llm_directive`
4. **阅读** `.learning/<topic-slug>/syllabus.md` 查看模板结构
5. 生成以项目为导向的综合大纲
6. **替换** 模板中的占位符为实际内容
7. 更新元数据：在 `.learning/<topic-slug>/metadata.json` 中设置 `"syllabus_generated": true`

**编程模式大纲指南：**

-围绕构建逐步复杂的项目来组织结构
- 每个阶段应包括 2-3 个概念 + 1-2 个 🔨 实践项目
- 项目应建立在前面的概念基础上
- 在每个阶段包含测试和调试
- 关注"如何工作"而不仅仅是"如何使用"
- 使用复选框 `- [ ]` 追踪进度

**重要：**

- 生成综合性、以项目为中心的教学大纲
- 每个概念都应导向构建某个作品
- 始终强调代码质量和最佳实践
