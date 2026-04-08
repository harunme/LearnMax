#!/usr/bin/env python3
"""
Generate quick conceptual multiple-choice quizzes based on least-reviewed concepts.
Called after progress logging to reinforce learning.
"""

import json
from pathlib import Path
from datetime import datetime


def get_least_asked_concepts(topic_slug: str, limit: int = 3, base_dir: str = ".learning"):
    """
    Get the least-asked concepts that need reinforcement.

    Args:
        topic_slug: Slug of the topic
        limit: Number of concepts to return (default 3)
        base_dir: Base directory for learning data

    Returns:
        List of concept dictionaries with review data
    """
    topic_dir = Path(base_dir) / topic_slug
    concepts_dir = topic_dir / "concepts"

    if not concepts_dir.exists():
        return []

    concepts = []
    for concept_file in concepts_dir.glob("*.json"):
        with open(concept_file, "r") as f:
            data = json.load(f)
            concepts.append({
                "concept": data["concept"],
                "slug": data["concept_slug"],
                "review_count": data.get("review_count", 0),
                "last_reviewed": data.get("last_reviewed"),
                "learned_date": data.get("learned_date")
            })

    # Sort by review_count (ascending) then by learned_date (oldest first)
    concepts.sort(key=lambda x: (x["review_count"], x["learned_date"]))

    return concepts[:limit]


def generate_quiz_directive(topic_slug: str, base_dir: str = ".learning"):
    """
    Generate LLM directive for creating MC questions about least-asked concepts.

    Args:
        topic_slug: Slug of the topic
        base_dir: Base directory for learning data

    Returns:
        JSON output with quiz directive for LLM
    """
    concepts = get_least_asked_concepts(topic_slug, limit=3, base_dir=base_dir)

    if not concepts:
        output = {
            "status": "no_concepts",
            "quiz_needed": False,
            "llm_directive": "没有可用于测验的概念。继续学习。"
        }
        print(json.dumps(output, indent=2))
        return

    # Build directive for LLM
    concept_names = [c["concept"] for c in concepts]

    directive = f"""
记录进度后，使用 AskUserQuestion 创建快速概念测验。

从这些复习次数最少的概念中选择一个：{', '.join(concept_names)}

创建一个测试理解（而非记忆）的选择题：
- 问题应该测试概念理解
- 4 个似是而非的选项（一个正确，三个干扰项）
- 用户回答后，解释为什么正确答案正确以及为什么其他选项错误
- 保持快速（30 秒内回答）

AskUserQuestion 的示例格式：
{{
  "question": "[概念] 的主要目的是什么？",
  "header": "快速测验",
  "multiSelect": false,
  "options": [
    {{"label": "选项 A", "description": "简要解释"}},
    {{"label": "选项 B", "description": "简要解释"}},
    {{"label": "选项 C", "description": "简要解释"}},
    {{"label": "选项 D", "description": "简要解释"}}
  ]
}}

测验后，更新 .learning/{topic_slug}/concepts/[概念-slug].json 中概念的 quiz_count
"""

    output = {
        "status": "quiz_ready",
        "quiz_needed": True,
        "least_reviewed_concepts": concepts,
        "llm_directive": directive.strip(),
        "suggested_prompt": f"快速测验时间！让我们测试你对其中之一的理解：{', '.join(concept_names)}"
    }

    print(json.dumps(output, indent=2))


def record_quiz_attempt(topic_slug: str, concept: str, correct: bool, base_dir: str = ".learning"):
    """
    Record a quiz attempt for a concept.

    Args:
        topic_slug: Slug of the topic
        concept: Name of the concept
        correct: Whether the answer was correct
        base_dir: Base directory for learning data
    """
    topic_dir = Path(base_dir) / topic_slug
    concepts_dir = topic_dir / "concepts"

    # Find the concept file
    concept_slug = concept.lower().replace(" ", "-").replace("/", "-")
    concept_file = concepts_dir / f"{concept_slug}.json"

    if not concept_file.exists():
        print(f"❌ 找不到概念 '{concept}'")
        return False

    with open(concept_file, "r") as f:
        data = json.load(f)

    # Update quiz history
    if "quiz_history" not in data:
        data["quiz_history"] = []

    data["quiz_history"].append({
        "timestamp": datetime.now().isoformat(),
        "correct": correct
    })

    if "quiz_count" not in data:
        data["quiz_count"] = 0
    data["quiz_count"] += 1

    if "quiz_correct_count" not in data:
        data["quiz_correct_count"] = 0
    if correct:
        data["quiz_correct_count"] += 1

    with open(concept_file, "w") as f:
        json.dump(data, f, indent=2)

    accuracy = (data["quiz_correct_count"] / data["quiz_count"] * 100) if data["quiz_count"] > 0 else 0

    output = {
        "status": "success",
        "concept": concept,
        "correct": correct,
        "quiz_count": data["quiz_count"],
        "accuracy": round(accuracy, 1),
        "llm_directive": f"测验尝试已记录。{'太棒了！' if correct else '继续练习这个概念。'}"
    }

    print(json.dumps(output, indent=2))
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法：")
        print("  生成测验：  python3 concept_quiz.py generate <主题-slug>")
        print("  记录尝试： python3 concept_quiz.py record <主题-slug> <概念> <正确与否>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "generate" and len(sys.argv) >= 3:
        generate_quiz_directive(sys.argv[2])
    elif command == "record" and len(sys.argv) >= 5:
        concept = sys.argv[3]
        correct = sys.argv[4].lower() in ['true', '1', 'yes']
        record_quiz_attempt(sys.argv[2], concept, correct)
    else:
        print("❌ 无效命令或缺少参数")
