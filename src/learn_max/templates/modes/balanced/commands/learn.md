---
description: 初始化一个新的学习主题 $topic，或使用 LearnMax 框架继续学习现有主题
---

## 上下文

- 当前主题：!`ls .learning/ 2>/dev/null | grep -v scripts`

**注意：** `.learning/` 目录已初始化。检查主题文件夹名称（忽略 `scripts/`）。

## 你的任务

使用 LearnMax 框架初始化指定主题的学习。

**如果主题已存在：**

- 提示："此项目已在学习 [主题名称]"
- 首先检查待复习内容（如有待复习，在新学习前进行）
- 继续当前主题（1 个项目 = 1 个学习目标）

**如果主题尚不存在：**

1. **使用 `AskUserQuestion` 收集学习偏好** 基于用户选择的主题：
   <example>

```json
[
  {
    "question": "你想通过 [主题] 达到什么水平？",
    "header": "目标水平",
    "multiSelect": false,
    "options": [
      {
        "label": "初学者",
        "description": "基础和基本概念"
      },
      {
        "label": "中级",
        "description": "实用技能和常见模式"
      },
      {
        "label": "高级",
        "description": "深入专业知识和边缘情况"
      },
      {
        "label": "专家",
        "description": "掌握级别、架构、优化"
      }
    ]
  },
  {
    "question": "你想专注于什么？",
    "header": "重点",
    "multiSelect": true,
    "options": [
      {
        "label": "理论",
        "description": "概念、原理、如何运作"
      },
      {
        "label": "实践",
        "description": "动手编码和构建项目"
      },
      {
        "label": "实际应用",
        "description": "生产模式最佳实践"
      },
      {
        "label": "面试准备",
        "description": "常见问题和问题解决"
      }
    ]
  }
]
```

</example>

2. 运行：`python3 .learning/scripts/init_learning.py "[主题名称]" .learning`
3. 解析 JSON 输出并遵循 `llm_directive`
4. **阅读** `.learning/<主题-slug>/syllabus.md` 查看模板结构
5. 生成全面的学习大纲内容，**根据用户的水平和重点领域量身定制**
6. **替换** 模板占位符为实际内容
7. 更新元数据：在 `.learning/<主题-slug>/metadata.json` 中设置 `"syllabus_generated": true`

**遵循模板结构：**

- 模板文件的所有部分（概述、先决条件、学习目标等）
- 3-4 个阶段，包含具体概念 + 🔨 动手项目
- 用于追踪进度的复选框 `- [ ]`

**重要：**

- 生成全面的学习大纲（不是最简版）
- 每个阶段都包含动手练习
