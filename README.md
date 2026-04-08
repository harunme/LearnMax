# Learn FASTER

[![Python 版本](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![许可证：MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv](https://img.shields.io/badge/uv-包管理器-green.svg)](https://github.com/astral-sh/uv)

> 由 AI 驱动的学习教练，通过间隔重复、个性化大纲和主动练习加速掌握。

**专为 [Claude Code](https://claude.com/claude-code) 构建** - 将 AI 教练直接集成到你的开发环境中。

## 为什么使用 FASTER？

使用科学支持的学习原则掌握任何技术技能：

- **个性化大纲** - 根据你的技能水平和学习目标生成
- **间隔重复** - 系统以最佳间隔安排复习
- **四种学习模式** - 选择均衡、考试准备、理论专注或实践模式
- **主动练习** - 自动生成的练习和项目
- **进度追踪** - 可视化你的学习旅程

## FASTER 框架

- **F**orget（遗忘）：初学者心态 - 以新鲜的视角对待主题
- **A**ct（行动）：做中学 - 动手练习优于被动阅读
- **S**tate（状态）：优化专注 - 创造理想的学习条件
- **T**each（教授）：讲解保持 - 教学强化理解
- **E**nter（进入）：持续会话 - 定期练习建立动力
- **R**eview（复习）：间隔重复 - 以间隔复习以获得长期保持

## 安装

**前置要求：** [uv](https://docs.astral.sh/uv/) 包管理器

```bash
# 如果还没有安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 选项 1：持久安装（推荐）

安装一次，在所有项目中使用：

```bash
uv tool install learn-max --from git+https://github.com/harunme/LearnMax.git
```

然后在任何项目目录中，简单运行：

```bash
learn-max
```

这将在首次运行时自动初始化，并启动带有 FASTER 教练模式的 Claude Code。

### 选项 2：一次性使用

无需安装直接运行：

```bash
uvx --from git+https://github.com/harunme/LearnMax.git learn-max
```

### 安装内容

首次运行时，learn-max 会创建：

```
your-project/
├── .claude/
│   ├── agents/practice-creator.md
│   ├── commands/
│   │   ├── learn.md
│   │   ├── review.md
│   │   └── progress.md
│   └── settings.local.json
├── .learning/
│   ├── config.json (追踪初始化)
│   ├── scripts/
│   │   ├── init_learning.py
│   │   ├── log_progress.py
│   │   ├── review_scheduler.py
│   │   └── generate_syllabus.py
│   └── references/faster_framework.md
└── CLAUDE.md
```

## 快速开始

1. **安装工具**

   ```bash
   uv tool install learn-max --from git+https://github.com/harunme/LearnMax.git
   ```

2. **在任何项目目录中启动**

   ```bash
   cd your-learning-project
   learn-max
   ```

   首次运行将：
   - 提示你选择学习模式
   - 初始化项目结构
   - 启动带有 FASTER 教练功能的 Claude Code

3. **开始学习**

   ```bash
   /learn "Go 语言基础"
   ```

   AI 教练将生成个性化大纲并引导你的学习会话。

## 演示：讲解实践

FASTER 中的"T"——教学保持——是关键差异化因素。以下是它的工作方式：

```bash
mkdir learn-go && cd learn-go
learn-max                    # 选择"均衡模式"
/learn "Go 错误处理"          # 在 Claude Code 中
```

```
教练：你刚学了错误包装。准备好讲解回去吗？
       ┌ 讲解
       │ ● 好的，我来讲解
       │ ○ 需要先复习
       │ ○ 还不确定
       └

你：   所以当你用 fmt.Errorf 和 %w 包装错误时，你添加了
       像"打开配置失败"这样的上下文，同时保留了
       原始错误。然后 errors.Is 仍然可以匹配根本原因。

教练：✅ 解释得太好了！你抓住了关键——包装的错误
       保留了链以便检查。将"错误包装"添加到
       你的复习计划。第一次复习明天。
```

**为什么有效：** 用你自己的话解释概念会强制主动回忆——被证明比被动阅读提高 2-3 倍保持率。教练不会只告诉你答案；它会引导你自己构建理解。

## 使用方法

### CLI 命令

- `learn-max` - 启动带有 FASTER 教练的 Claude Code（首次运行时自动初始化）
- `learn-max init` - 强制重新初始化或切换学习模式
- `learn-max version` - 显示当前版本

### Claude Code 斜杠命令

一旦 Claude Code 运行，使用这些命令：

- `/learn [主题]` - 开始或继续学习带有个性化大纲的主题
- `/review` - 对你学过的主题进行间隔重复复习
- `/progress` - 查看详细进度报告和学习统计

## 学习模式

选择适合你学习风格的模式：

- **均衡模式** - 理论、实践和真实应用相结合（推荐给大多数学习者）
- **备考模式** - 专注于回忆、练习测试和证书备考
- **理论模式** - 深度概念理解，包括心智模型和第一性原理
- **实践模式** - 基于项目的学习，立即应用

每种模式都提供量身定制的教练体验，包含模式特定的大纲和练习。

## 开发

### 设置

```bash
# 克隆仓库
git clone https://github.com/harunme/LearnMax.git
cd LearnMax

# 如需要安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
uv sync
```

## 使用场景

Learn FASTER 非常适合：

- 学习新的编程语言（Go、Rust、Python、TypeScript 等）
- 准备技术认证和考试
- 掌握框架和库（React、Next.js、Django 等）
- 建立结构化的自学计划
- 入门新的代码库或技术

## 要求

- Python 3.12+
- [Claude Code](https://claude.com/claude-code)
- [uv](https://docs.astral.sh/uv/) 包管理器

## 贡献

欢迎贡献！随意打开 issues 或提交 pull requests。

## 许可证

MIT 许可证 - 参见 LICENSE 文件了解详情
