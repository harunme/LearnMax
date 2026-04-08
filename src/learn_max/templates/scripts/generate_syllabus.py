#!/usr/bin/env python3
"""
Generate a structured learning syllabus for a topic.
This is a helper that Claude will use to create comprehensive learning paths.
"""

import json
from pathlib import Path
from datetime import datetime


def update_syllabus(topic_slug: str, syllabus_content: str, base_dir: str = ".learning"):
    """
    Update the syllabus file with generated content.

    Args:
        topic_slug: Slug of the topic
        syllabus_content: Markdown content for the syllabus
        base_dir: Base directory for learning data
    """
    topic_dir = Path(base_dir) / topic_slug
    syllabus_path = topic_dir / "syllabus.md"

    if not topic_dir.exists():
        print(f"❌ 主题 '{topic_slug}' 未找到。")
        return False

    with open(syllabus_path, "w") as f:
        f.write(syllabus_content)

    # Update metadata
    metadata_path = topic_dir / "metadata.json"
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    metadata["syllabus_generated"] = True
    metadata["syllabus_updated_at"] = datetime.now().isoformat()

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ 大纲已更新：'{topic_slug}'")
    print(f"📄 {syllabus_path}")

    return True


def get_topic_info(topic_slug: str, base_dir: str = ".learning"):
    """
    Get information about a learning topic.

    Args:
        topic_slug: Slug of the topic
        base_dir: Base directory for learning data

    Returns:
        Dictionary with topic information
    """
    topic_dir = Path(base_dir) / topic_slug

    if not topic_dir.exists():
        return None

    metadata_path = topic_dir / "metadata.json"
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    return {
        "topic": metadata["topic"],
        "status": metadata["status"],
        "sessions": metadata["total_sessions"],
        "syllabus_exists": metadata.get("syllabus_generated", False),
        "directory": str(topic_dir)
    }


def list_topics(base_dir: str = ".learning"):
    """
    List all learning topics.

    Args:
        base_dir: Base directory for learning data

    Returns:
        List of topic information dictionaries
    """
    learning_dir = Path(base_dir)

    if not learning_dir.exists():
        return []

    topics = []
    for topic_dir in learning_dir.iterdir():
        if topic_dir.is_dir() and (topic_dir / "metadata.json").exists():
            info = get_topic_info(topic_dir.name, base_dir)
            if info:
                topics.append(info)

    return topics


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法：")
        print("  列出主题：  python3 generate_syllabus.py list")
        print("  主题信息：   python3 generate_syllabus.py info <topic_slug>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        topics = list_topics()
        if not topics:
            output = {
                "status": "no_topics",
                "topics": [],
                "llm_directive": "No learning topics found. Ask user what they'd like to learn and initialize a new topic.",
                "suggested_response": "No learning topics found yet. What would you like to learn?"
            }
            print(json.dumps(output, indent=2))
        else:
            output = {
                "status": "success",
                "topic_count": len(topics),
                "topics": topics,
                "llm_directive": "向用户展示主题列表。询问他们想处理哪个主题，或者是否要开始一个新主题。",
                "suggested_response": f"你有 {len(topics)} 个学习主题：\n\n" + "\n".join([
                    f"{'✅' if t['status'] == 'completed' else '📖'} {t['topic']} - {t['sessions']} 次学习"
                    for t in topics
                ]) + "\n\n你想学习哪个主题？"
            }
            print(json.dumps(output, indent=2))

    elif command == "info" and len(sys.argv) >= 3:
        info = get_topic_info(sys.argv[2])
        if info:
            output = {
                "status": "success",
                "topic_info": info,
                "llm_directive": "向用户显示主题信息。检查此主题是否有待复习内容。",
                "suggested_response": f"主题：{info['topic']}\n学习次数：{info['sessions']}\n状态：{info['status']}"
            }
            print(json.dumps(output, indent=2))
        else:
            output = {
                "status": "error",
                "error": f"主题 '{sys.argv[2]}' 未找到",
                "llm_directive": "告知用户未找到主题。建议列出所有主题或创建新主题。"
            }
            print(json.dumps(output, indent=2))
