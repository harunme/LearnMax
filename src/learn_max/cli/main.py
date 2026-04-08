#!/usr/bin/env python3
"""
Learn FASTER CLI - One-time installer for Claude Code learning system.

Usage:
    uvx learn-max init
"""

import sys
import shutil
import platform
import inquirer
import json
from pathlib import Path
from typing import Dict, Any


# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"


BANNER = f"""{Colors.CYAN}
██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗    ███████╗ █████╗ ███████╗████████╗███████╗██████╗
██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║    ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██║     █████╗  ███████║██████╔╝██╔██╗ ██║    █████╗  ███████║███████╗   ██║   █████╗  ██████╔╝
██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║    ██╔══╝  ██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
███████╗███████╗██║  ██║██║  ██║██║ ╚████║    ██║     ██║  ██║███████║   ██║   ███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
{Colors.RESET}"""


def print_success(msg: str) -> None:
    """Print success message in green."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def print_info(msg: str) -> None:
    """Print info message in cyan."""
    print(f"{Colors.CYAN}{msg}{Colors.RESET}")


def print_warning(msg: str) -> None:
    """Print warning message in yellow."""
    print(f"{Colors.YELLOW}!{Colors.RESET} {msg}")


def print_header(msg: str) -> None:
    """Print header message in bold magenta."""
    print(f"{Colors.BOLD}{Colors.MAGENTA}{msg}{Colors.RESET}")


def print_dim(msg: str) -> None:
    """Print dimmed message."""
    print(f"{Colors.DIM}{msg}{Colors.RESET}")


def print_error(msg: str) -> None:
    """Print error message in red."""
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")


def get_templates_dir() -> Path:
    """Get the templates directory from the installed package."""
    return Path(__file__).parent.parent / "templates"


def create_or_update_settings(claude_dir: Path) -> None:
    """Create or update .claude/settings.local.json."""
    settings_file = claude_dir / "settings.local.json"

    # Default settings for Learn FASTER
    default_settings = {
        "permissions": {
            "allow": [
                "Bash(python3 .learning/scripts/:*)",
                "Bash(ls:*)",
                "Read(.learning/**)",
                "Write(.learning/**)",
                "Write(**/*.md)",
                "Read(**/*.md)"
            ],
            "deny": [
                "Bash(rm:*)",
                "Bash(curl:*)",
                "Read(.env)",
                "Read(.env.*)",
                "Write(.env)",
                "Write(.env.*)"
            ]
        },
        "companyAnnouncements": [
            "🚀 FASTER 学习系统已启动！输入 /learn \"主题\" 开始学习",
        ]
    }

    if settings_file.exists():
        # Load existing settings
        with open(settings_file, "r") as f:
            settings = json.load(f)

        # Merge with defaults
        if "permissions" not in settings:
            settings["permissions"] = default_settings["permissions"]
        else:
            # Merge permissions allow list
            if "allow" not in settings["permissions"]:
                settings["permissions"]["allow"] = []

            for perm in default_settings["permissions"]["allow"]:
                if perm not in settings["permissions"]["allow"]:
                    settings["permissions"]["allow"].append(perm)

            # Merge permissions deny list
            if "deny" not in settings["permissions"]:
                settings["permissions"]["deny"] = []

            for perm in default_settings["permissions"]["deny"]:
                if perm not in settings["permissions"]["deny"]:
                    settings["permissions"]["deny"].append(perm)

        # Add company announcements if not present
        if "companyAnnouncements" not in settings:
            settings["companyAnnouncements"] = default_settings["companyAnnouncements"]

        print_success(f"已更新 {settings_file}")
    else:
        # Create new settings file
        settings = default_settings
        print_success(f"已创建 {settings_file}")

    # Write settings
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=2)


def check_initialization() -> bool:
    """Check if project has been initialized."""
    config_path = Path.cwd() / ".learning" / "config.json"
    if not config_path.exists():
        return False

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("initialized", False)
    except:
        return False


def init_project() -> None:
    """Initialize Learn FASTER in the current project."""
    

    cwd = Path.cwd()
    templates_dir = get_templates_dir()

    print(BANNER)
    print_header("\n正在当前项目中初始化 FASTER 学习系统...\n")

    # Ask for learning mode selection
    

    learning_mode_question = [
        inquirer.List(
            'mode',
            message="选择你的学习模式",
            choices=[
                ('均衡模式       - 理论、实践与应用相结合', 'balanced'),
                ('备考模式       - 可打印的试卷、练习题与证书备考', 'exam'),
                ('理论模式       - 深度概念理解与心智模型构建', 'theory'),
                ('实践模式       - 立即动手项目，通过实践学习', 'practical'),
                ('编程模式       - 通过构建项目学习编程', 'programming'),
            ],
            default='balanced',
        ),
    ]

    mode_answer = inquirer.prompt(learning_mode_question)
    learning_mode = mode_answer['mode'] if mode_answer else 'balanced'

    mode_names = {
        "exam": "备考模式",
        "theory": "理论模式",
        "practical": "实践模式",
        "balanced": "均衡模式",
        "programming": "编程模式"
    }
    print_success(f"已选择：{mode_names[learning_mode]} 模式\n")

    # Ask about macOS Reminders (only on macOS)
    macos_reminders = False
    if platform.system() == "Darwin":
        response = input(f"{Colors.CYAN}启用 macOS 提醒用于复习通知？(y/n)：{Colors.RESET} ").strip().lower()
        macos_reminders = response in ['y', 'yes']

    # Create .claude directory structure
    claude_dir = cwd / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # Copy mode-specific agents and commands
    mode_templates_dir = templates_dir / "modes" / learning_mode

    # Copy agents for selected mode
    agents_dest = claude_dir / "agents"
    agents_dest.mkdir(exist_ok=True)
    agents_src = mode_templates_dir / "agents"

    if agents_src.exists():
        for file in agents_src.glob("*.md"):
            shutil.copy2(file, agents_dest / file.name)
            print_success(f"已复制智能体：{file.name}")

    # Copy commands for selected mode
    commands_dest = claude_dir / "commands"
    commands_dest.mkdir(exist_ok=True)
    commands_src = mode_templates_dir / "commands"

    if commands_src.exists():
        for file in commands_src.glob("*.md"):
            shutil.copy2(file, commands_dest / file.name)
            print_success(f"已复制命令：{file.name}")

    # Create/update settings.local.json
    create_or_update_settings(claude_dir)

    # Create .learning directory structure
    learning_dir = cwd / ".learning"
    learning_dir.mkdir(exist_ok=True)

    # Create config.json with initialization flag
    config = {
        "initialized": True,
        "learning_mode": learning_mode,
        "macos_reminders_enabled": macos_reminders
    }
    config_path = learning_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print_success(f"已创建 config.json（模式：{mode_names[learning_mode]}，macOS 提醒：{'已启用' if macos_reminders else '已禁用'}）")

    # Copy scripts
    scripts_dest = learning_dir / "scripts"
    scripts_dest.mkdir(exist_ok=True)
    scripts_src = templates_dir / "scripts"
    if scripts_src.exists():
        for file in scripts_src.glob("*.py"):
            shutil.copy2(file, scripts_dest / file.name)
            print_success(f"已复制脚本：{file.name}")

    # Copy references
    references_dest = learning_dir / "references"
    references_dest.mkdir(exist_ok=True)
    references_src = templates_dir / "references"
    if references_src.exists():
        for file in references_src.glob("*.md"):
            shutil.copy2(file, references_dest / file.name)
            print_success(f"已复制参考资料：{file.name}")

    # Copy instructions.md to project root as CLAUDE.md
    instructions_src = templates_dir / "instructions.md"
    claude_md_dest = cwd / "CLAUDE.md"
    if instructions_src.exists() and not claude_md_dest.exists():
        shutil.copy2(instructions_src, claude_md_dest)
        print_success("已将说明复制到项目根目录的 CLAUDE.md")
    elif claude_md_dest.exists():
        print_warning("CLAUDE.md 已存在，跳过复制")

    print(f"\n{Colors.GREEN}{Colors.BOLD}初始化完成！{Colors.RESET}\n")

    print_header("Claude Code 中可用的命令：")
    print(f"  {Colors.CYAN}/learn [主题]{Colors.RESET}  - 开始或继续学习")
    print(f"  {Colors.CYAN}/review{Colors.RESET}          - 间隔重复复习")
    print(f"  {Colors.CYAN}/progress{Colors.RESET}        - 显示详细进度报告")
    print()


def launch_coach(auto_review: bool = False) -> None:
    """Launch Claude Code with learn-max system prompt."""
    import subprocess

    # Get the learning mode from config
    config_path = Path.cwd() / ".learning" / "config.json"
    learning_mode = "balanced"  # default
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                learning_mode = config.get("learning_mode", "balanced")
        except:
            pass

    # Get the path to the system prompt template
    templates_dir = Path(__file__).parent.parent / "templates"
    system_prompt_path = templates_dir / "modes" / learning_mode / "system_prompts" / "learn-max.md"

    if not system_prompt_path.exists():
        print_error(f"错误：找不到 '{learning_mode}' 模式的系统提示")
        print_dim(f"期望路径：{system_prompt_path}")
        sys.exit(1)

    # Read the system prompt content (skip frontmatter)
    with open(system_prompt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip frontmatter (between --- lines)
    in_frontmatter = False
    content_lines = []
    for line in lines:
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                in_frontmatter = False
                continue
        if not in_frontmatter:
            content_lines.append(line)

    system_prompt = "".join(content_lines).strip()

    # Launch Claude Code with the system prompt
    print_info("正在以学习教练模式启动 Claude Code...")
    print_dim("（使用 FASTER 框架系统提示）\n")

    # Build command with optional /review prefix
    cmd = ["claude", "--system-prompt", system_prompt]
    if auto_review:
        cmd.extend(["/review"])

    try:
        subprocess.run(cmd, check=False)
    except FileNotFoundError:
        print_error("错误：找不到 'claude' 命令")
        print_dim("请确保 Claude Code CLI 已安装并在 PATH 中")
        print_dim("安装地址：https://claude.ai/download")
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    # Check for explicit commands
    if len(sys.argv) >= 2:
        command = sys.argv[1]

        if command == "init":
            init_project()
            return
        elif command == "version":
            from learn_max import __version__
            print(f"learn-max version {__version__}")
            return
        elif command in ["help", "--help", "-h"]:
            print("Learn FASTER - 使用 FASTER 框架加速学习\n")
            print("用法：")
            print("  learn-max           自动初始化并以教练模式启动 Claude Code")
            print("  learn-max init      强制重新初始化")
            print("  learn-max version   显示版本")
            print()
            print("更多信息：https://github.com/harunme/LearnMax")
            return
        else:
            print_error(f"未知命令：{command}")
            print_dim("运行 'learn-max --help' 查看用法")
            sys.exit(1)

    # Default behavior: check init, then launch
    if not check_initialization():
        print_info("检测到首次使用，正在初始化...")
        print()
        init_project()
        print()
        print_header("正在使用 FASTER 框架启动 Claude Code...")
        print()
        launch_coach(auto_review=False)
    else:
        print_info("正在以学习教练模式启动 Claude Code...")
        print_dim("（首先检查是否有待复习内容）\n")
        launch_coach(auto_review=True)


if __name__ == "__main__":
    main()
