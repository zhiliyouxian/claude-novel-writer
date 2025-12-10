#!/usr/bin/env python3
"""
TTS 文本预处理脚本

功能：
1. 去除 YAML frontmatter
2. 去除 Markdown 格式
3. 合并段落（去掉多余换行）
4. 输出适合 TTS 朗读的纯文本

用法：
    python prepare-tts.py <chapters_dir> <output_file>
    python prepare-tts.py productions/zongheng/chapters/ releases/zongheng/audio/novel-tts.txt

选项：
    --single <chapter>  只处理单个章节
    --range <start-end> 处理指定范围，如 1-10
"""

import os
import re
import sys
import argparse
from pathlib import Path


def remove_yaml_frontmatter(content: str) -> str:
    """移除 YAML frontmatter"""
    # 匹配 --- 开头和结尾的 YAML 块
    pattern = r'^---\s*\n.*?\n---\s*\n'
    return re.sub(pattern, '', content, flags=re.DOTALL)


def remove_markdown_formatting(content: str) -> str:
    """移除 Markdown 格式标记"""
    # 移除标题标记 # ## ### 等，但保留标题文字
    content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)

    # 移除粗体 **text** 或 __text__
    content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
    content = re.sub(r'__(.+?)__', r'\1', content)

    # 移除斜体 *text* 或 _text_
    content = re.sub(r'\*(.+?)\*', r'\1', content)
    content = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\1', content)

    # 移除行内代码 `code`
    content = re.sub(r'`(.+?)`', r'\1', content)

    # 移除链接 [text](url)
    content = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', content)

    # 移除图片 ![alt](url)
    content = re.sub(r'!\[.*?\]\(.+?\)', '', content)

    # 移除水平分隔线
    content = re.sub(r'^[-*_]{3,}\s*$', '', content, flags=re.MULTILINE)

    # 移除引用标记 >
    content = re.sub(r'^>\s*', '', content, flags=re.MULTILINE)

    # 移除列表标记 - * 1.
    content = re.sub(r'^[\-\*]\s+', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\d+\.\s+', '', content, flags=re.MULTILINE)

    return content


def normalize_whitespace(content: str) -> str:
    """规范化空白字符"""
    # 将多个连续空行合并为单个空行
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 去除行首行尾空白
    lines = [line.strip() for line in content.split('\n')]
    content = '\n'.join(lines)

    # 去除文件开头和结尾的空白
    content = content.strip()

    return content


def extract_chapter_title(content: str) -> str:
    """提取章节标题"""
    # 匹配 # 第X章 标题 格式
    match = re.search(r'^#\s*(第.+?章.*)$', content, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def process_chapter(filepath: Path) -> str:
    """处理单个章节文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取标题（在移除格式之前）
    title = extract_chapter_title(content)

    # 处理流程
    content = remove_yaml_frontmatter(content)
    content = remove_markdown_formatting(content)
    content = normalize_whitespace(content)

    return content


def get_chapter_number(filepath: Path) -> int:
    """从文件名提取章节号"""
    match = re.search(r'chapter-(\d+)', filepath.name)
    if match:
        return int(match.group(1))
    return 0


def process_chapters(chapters_dir: Path, output_file: Path,
                     chapter_range: tuple = None, single_chapter: int = None):
    """处理多个章节文件"""

    # 获取所有章节文件
    chapter_files = sorted(chapters_dir.glob('chapter-*.md'),
                          key=lambda f: get_chapter_number(f))

    if not chapter_files:
        print(f"错误: 在 {chapters_dir} 中未找到章节文件")
        sys.exit(1)

    # 筛选章节范围
    if single_chapter:
        chapter_files = [f for f in chapter_files
                        if get_chapter_number(f) == single_chapter]
    elif chapter_range:
        start, end = chapter_range
        chapter_files = [f for f in chapter_files
                        if start <= get_chapter_number(f) <= end]

    if not chapter_files:
        print("错误: 指定范围内没有找到章节文件")
        sys.exit(1)

    print(f"处理 {len(chapter_files)} 个章节文件...")

    # 处理每个章节
    all_content = []
    for filepath in chapter_files:
        chapter_num = get_chapter_number(filepath)
        print(f"  处理: chapter-{chapter_num:03d}.md")

        content = process_chapter(filepath)
        all_content.append(content)

    # 合并所有章节，用双空行分隔
    final_content = '\n\n\n'.join(all_content)

    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

    # 统计信息
    total_chars = len(final_content)
    total_words = len(re.findall(r'[\u4e00-\u9fff]', final_content))  # 中文字符数

    print(f"\n✅ TTS 文本准备完成!")
    print(f"   输出文件: {output_file}")
    print(f"   章节数量: {len(chapter_files)}")
    print(f"   总字符数: {total_chars:,}")
    print(f"   中文字数: {total_words:,}")
    print(f"   预计朗读: {total_words // 300} 分钟 (按 300字/分钟)")


def parse_range(range_str: str) -> tuple:
    """解析范围字符串，如 '1-10' -> (1, 10)"""
    if '-' in range_str:
        parts = range_str.split('-')
        return (int(parts[0]), int(parts[1]))
    else:
        num = int(range_str)
        return (num, num)


def main():
    parser = argparse.ArgumentParser(
        description='TTS 文本预处理：去除 YAML、Markdown 格式，生成纯文本'
    )
    parser.add_argument('chapters_dir', help='章节目录路径')
    parser.add_argument('output_file', help='输出文件路径')
    parser.add_argument('--single', type=int, help='只处理单个章节')
    parser.add_argument('--range', dest='chapter_range', help='处理指定范围，如 1-10')

    args = parser.parse_args()

    chapters_dir = Path(args.chapters_dir)
    output_file = Path(args.output_file)

    if not chapters_dir.exists():
        print(f"错误: 目录不存在 {chapters_dir}")
        sys.exit(1)

    chapter_range = None
    if args.chapter_range:
        chapter_range = parse_range(args.chapter_range)

    process_chapters(
        chapters_dir=chapters_dir,
        output_file=output_file,
        chapter_range=chapter_range,
        single_chapter=args.single
    )


if __name__ == '__main__':
    main()
