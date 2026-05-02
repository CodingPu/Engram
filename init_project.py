#!/usr/bin/env python3
"""
Engram 项目初始化脚本

功能：
1. 验证项目结构
2. 初始化配置文件
3. 创建必要的目录
4. 生成示例活动数据
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
import uuid


def create_sample_activities() -> List[Dict]:
    """生成示例学习活动"""
    
    return [
        {
            "id": str(uuid.uuid4()),
            "type": "fact",
            "question": "什么是间隔重复？",
            "expected_length": "50-100 words",
            "difficulty": 2,
            "source_wiki_id": "concepts/spaced_repetition.md",
            "created_at": datetime.now().isoformat(),
            "fsrs": {
                "difficulty": 5.0,
                "stability": 1.0,
                "retrievability": 0.9,
                "last_review": datetime.now().isoformat(),
                "next_review": (datetime.now() + timedelta(days=1)).isoformat(),
                "reps": 0,
                "lapses": 0
            },
            "user_response": None,
            "feedback": None
        },
        {
            "id": str(uuid.uuid4()),
            "type": "feynman",
            "question": "用自己的话解释 Ebbinghaus 遗忘曲线。",
            "expected_length": "100-200 words",
            "difficulty": 3,
            "source_wiki_id": "concepts/spaced_repetition.md",
            "created_at": datetime.now().isoformat(),
            "fsrs": {
                "difficulty": 5.0,
                "stability": 1.0,
                "retrievability": 0.9,
                "last_review": None,
                "next_review": (datetime.now() + timedelta(days=1)).isoformat(),
                "reps": 0,
                "lapses": 0
            },
            "user_response": None,
            "feedback": None
        },
        {
            "id": str(uuid.uuid4()),
            "type": "connection",
            "question": "间隔重复和 FSRS 算法有什么关系？",
            "expected_length": "80-150 words",
            "difficulty": 4,
            "source_wiki_id": "concepts/spaced_repetition.md",
            "created_at": datetime.now().isoformat(),
            "fsrs": {
                "difficulty": 5.0,
                "stability": 1.0,
                "retrievability": 0.9,
                "last_review": None,
                "next_review": (datetime.now() + timedelta(days=2)).isoformat(),
                "reps": 0,
                "lapses": 0
            },
            "user_response": None,
            "feedback": None
        }
    ]


def init_project():
    """初始化项目"""
    
    project_root = Path(__file__).parent
    
    print("🚀 Engram 项目初始化\n")
    
    # 1. 验证项目结构
    print("1️⃣  验证项目结构...")
    required_dirs = [
        "ingest/agents",
        "ingest/processors",
        "ingest/prompts",
        "bot/channels",
        "wiki/concepts",
        "wiki/entities",
        "wiki/sources",
        "wiki/synthesis",
        "raw/articles",
        "raw/papers",
        "raw/books",
        "activities/templates",
        "tools",
        "tests",
        "docs",
        "shell",
        "logs"
    ]
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
    
    print("   ✓ 所有目录已创建\n")
    
    # 2. 检查关键文件
    print("2️⃣  检查关键配置文件...")
    required_files = {
        "CONVENTIONS.md": "Wiki 规范",
        "SCHEMA.md": "LLM Schema",
        "requirements.txt": "项目依赖",
        ".env.example": "环境变量模板",
        "docker-compose.yml": "Docker 配置"
    }
    
    for file_name, description in required_files.items():
        file_path = project_root / file_name
        status = "✓" if file_path.exists() else "✗"
        print(f"   {status} {file_name:30} {description}")
    
    print()
    
    # 3. 初始化 .env
    print("3️⃣  初始化环境变量...")
    env_file = project_root / ".env"
    if not env_file.exists():
        env_example = project_root / ".env.example"
        if env_example.exists():
            env_file.write_text(env_example.read_text())
            print("   ✓ 从 .env.example 创建 .env")
        else:
            print("   ⚠️  .env.example 不存在，跳过")
    else:
        print("   ℹ️  .env 已存在，跳过")
    
    print()
    
    # 4. 初始化活动数据
    print("4️⃣  初始化示例活动...")
    activities_file = project_root / "activities" / "deck.json"
    
    activities_data = {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "activities": create_sample_activities()
    }
    
    activities_file.write_text(json.dumps(activities_data, indent=2, ensure_ascii=False))
    print(f"   ✓ 创建了 {len(activities_data['activities'])} 个示例活动")
    
    print()
    
    # 5. 创建 __init__.py 文件（Python 包）
    print("5️⃣  初始化 Python 包...")
    packages = [
        "ingest",
        "ingest/agents",
        "ingest/processors",
        "bot",
        "bot/channels",
        "tools"
    ]
    
    for pkg in packages:
        init_file = project_root / pkg / "__init__.py"
        if not init_file.exists():
            init_file.touch()
    
    print(f"   ✓ 创建了 {len(packages)} 个 Python 包")
    
    print()
    
    # 6. 总结
    print("=" * 60)
    print("✅ 项目初始化完成！\n")
    print("📚 后续步骤：\n")
    print("1. 编辑 .env，填入 Claude API Key 和 QQ Bot 信息")
    print("   cp .env.example .env")
    print("   # 编辑 .env\n")
    print("2. 安装依赖")
    print("   pip install -r requirements.txt\n")
    print("3. 查看 Wiki 规范")
    print("   cat CONVENTIONS.md\n")
    print("4. 查看开发计划")
    print("   cat DEVELOPMENT_PLAN.md\n")
    print("=" * 60)


if __name__ == "__main__":
    init_project()
