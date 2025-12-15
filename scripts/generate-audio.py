#!/usr/bin/env python3
"""
TTS 音频生成脚本（使用 edge-tts）

功能：
1. 读取 TTS 文本文件
2. 使用 edge-tts 生成音频
3. 支持多种中文音色
4. 支持分章节并行生成（默认10并发，最高20）

依赖安装：
    pip install edge-tts

用法：
    # 生成单个音频文件
    python generate-audio.py <input_txt> <output_mp3>
    python generate-audio.py releases/zongheng/audio/novel-tts.txt releases/zongheng/audio/novel.mp3

    # 分章节并行生成（每章单独文件）
    python generate-audio.py <input_txt> <output_dir> --split-chapters

    # 指定并发数（默认10，最高20）
    python generate-audio.py <input_txt> <output_dir> --split-chapters --concurrency 15

选项：
    --voice <voice_name>  指定音色（默认：zh-CN-XiaoxiaoNeural）
    --rate <rate>         语速，如 +10% 或 -10%（默认：+0%）
    --volume <volume>     音量，如 +10% 或 -10%（默认：+0%）
    --split-chapters      分章节生成单独音频文件
    --concurrency <n>     并行生成数量（默认：10，范围：1-20）
    --list-voices         列出所有可用的中文音色

常用音色：
    女声：
    - zh-CN-XiaoxiaoNeural   （晓晓，温柔女声，推荐）
    - zh-CN-XiaoyanNeural    （晓颜，甜美女声）
    - zh-CN-XiaochenNeural   （晓辰，成熟女声）

    男声：
    - zh-CN-YunxiNeural      （云希，年轻男声，推荐）
    - zh-CN-YunjianNeural    （云健，成熟男声）
    - zh-CN-YunyangNeural    （云扬，新闻播报风格）
"""

import os
import re
import sys
import asyncio
import argparse
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("错误: 请先安装 edge-tts")
    print("运行: pip install edge-tts")
    sys.exit(1)


# 推荐的中文音色
CHINESE_VOICES = {
    # 女声
    'xiaoxiao': 'zh-CN-XiaoxiaoNeural',
    'xiaoyan': 'zh-CN-XiaoyanNeural',
    'xiaochen': 'zh-CN-XiaochenNeural',
    'xiaomo': 'zh-CN-XiaomoNeural',
    'xiaoxuan': 'zh-CN-XiaoxuanNeural',
    'xiaoyi': 'zh-CN-XiaoyiNeural',
    'xiaozhen': 'zh-CN-XiaozhenNeural',
    # 男声
    'yunxi': 'zh-CN-YunxiNeural',
    'yunjian': 'zh-CN-YunjianNeural',
    'yunyang': 'zh-CN-YunyangNeural',
    'yunhao': 'zh-CN-YunhaoNeural',
    'yunfeng': 'zh-CN-YunfengNeural',
    'yunxia': 'zh-CN-YunxiaNeural',
}


async def list_voices():
    """列出所有可用的中文音色"""
    voices = await edge_tts.list_voices()
    chinese_voices = [v for v in voices if v['Locale'].startswith('zh-')]

    print("可用的中文音色：\n")
    for voice in sorted(chinese_voices, key=lambda x: x['ShortName']):
        gender = "女" if voice['Gender'] == 'Female' else "男"
        print(f"  {voice['ShortName']:30} ({gender}声) - {voice['Locale']}")

    print("\n快捷名称：")
    for short, full in CHINESE_VOICES.items():
        print(f"  {short:12} -> {full}")


def resolve_voice(voice_name: str) -> str:
    """解析音色名称"""
    # 如果是快捷名称，转换为完整名称
    if voice_name.lower() in CHINESE_VOICES:
        return CHINESE_VOICES[voice_name.lower()]
    return voice_name


def split_into_chapters(content: str) -> list:
    """将文本按章节分割"""
    # 按 "第X章" 分割
    pattern = r'(第[一二三四五六七八九十百千\d]+章)'
    parts = re.split(pattern, content)

    chapters = []
    current_chapter = ""
    chapter_num = 0

    for i, part in enumerate(parts):
        if re.match(pattern, part):
            # 这是章节标题
            if current_chapter.strip():
                chapters.append((chapter_num, current_chapter.strip()))
            chapter_num += 1
            current_chapter = part
        else:
            current_chapter += part

    # 添加最后一章
    if current_chapter.strip():
        chapters.append((chapter_num, current_chapter.strip()))

    return chapters


async def generate_audio(text: str, output_path: Path,
                        voice: str, rate: str, volume: str):
    """生成单个音频文件"""
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
    await communicate.save(str(output_path))


async def generate_single_file(input_file: Path, output_file: Path,
                               voice: str, rate: str, volume: str):
    """生成单个合并的音频文件"""
    print(f"读取文本: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    total_chars = len(content)
    print(f"文本长度: {total_chars:,} 字符")
    print(f"使用音色: {voice}")
    print(f"生成中...")

    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)

    await generate_audio(content, output_file, voice, rate, volume)

    file_size = output_file.stat().st_size / (1024 * 1024)  # MB
    print(f"\n✅ 音频生成完成!")
    print(f"   输出文件: {output_file}")
    print(f"   文件大小: {file_size:.1f} MB")


async def generate_chapter(chapter_num: int, chapter_text: str, output_dir: Path,
                           voice: str, rate: str, volume: str, semaphore: asyncio.Semaphore):
    """生成单个章节音频（带并发控制）"""
    async with semaphore:
        output_file = output_dir / f"chapter-{chapter_num:03d}.mp3"
        print(f"  开始: chapter-{chapter_num:03d}.mp3 ({len(chapter_text):,} 字符)")

        await generate_audio(chapter_text, output_file, voice, rate, volume)

        file_size = output_file.stat().st_size / 1024  # KB
        print(f"  完成: chapter-{chapter_num:03d}.mp3 ({file_size:.0f} KB)")
        return output_file.stat().st_size


async def generate_split_files(input_file: Path, output_dir: Path,
                               voice: str, rate: str, volume: str,
                               concurrency: int = 10):
    """分章节并行生成多个音频文件"""
    print(f"读取文本: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    chapters = split_into_chapters(content)

    if not chapters:
        print("错误: 未能识别出章节")
        sys.exit(1)

    print(f"识别到 {len(chapters)} 个章节")
    print(f"使用音色: {voice}")
    print(f"并发数: {concurrency}")
    print()

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 使用信号量控制并发数
    semaphore = asyncio.Semaphore(concurrency)

    # 创建所有任务
    tasks = [
        generate_chapter(chapter_num, chapter_text, output_dir,
                        voice, rate, volume, semaphore)
        for chapter_num, chapter_text in chapters
    ]

    # 并行执行所有任务
    results = await asyncio.gather(*tasks)

    total_size = sum(results)
    total_size_mb = total_size / (1024 * 1024)
    print(f"\n✅ 音频生成完成!")
    print(f"   输出目录: {output_dir}")
    print(f"   章节数量: {len(chapters)}")
    print(f"   总大小: {total_size_mb:.1f} MB")


def main():
    parser = argparse.ArgumentParser(
        description='使用 edge-tts 生成 TTS 音频'
    )
    parser.add_argument('input', nargs='?', help='输入文本文件路径')
    parser.add_argument('output', nargs='?', help='输出音频文件/目录路径')
    parser.add_argument('--voice', default='zh-CN-XiaoxiaoNeural',
                       help='音色名称（默认：zh-CN-XiaoxiaoNeural）')
    parser.add_argument('--rate', default='+0%',
                       help='语速调整（默认：+0%%）')
    parser.add_argument('--volume', default='+0%',
                       help='音量调整（默认：+0%%）')
    parser.add_argument('--split-chapters', action='store_true',
                       help='分章节生成单独音频文件')
    parser.add_argument('--concurrency', type=int, default=10,
                       help='并行生成的章节数（默认：10，范围：1-20）')
    parser.add_argument('--list-voices', action='store_true',
                       help='列出所有可用的中文音色')

    args = parser.parse_args()

    # 列出音色
    if args.list_voices:
        asyncio.run(list_voices())
        return

    # 检查必需参数
    if not args.input or not args.output:
        parser.print_help()
        sys.exit(1)

    input_file = Path(args.input)
    output_path = Path(args.output)

    if not input_file.exists():
        print(f"错误: 输入文件不存在 {input_file}")
        sys.exit(1)

    # 解析音色
    voice = resolve_voice(args.voice)

    # 限制并发数范围
    concurrency = max(1, min(20, args.concurrency))

    # 生成音频
    if args.split_chapters:
        asyncio.run(generate_split_files(
            input_file, output_path, voice, args.rate, args.volume, concurrency
        ))
    else:
        if not output_path.suffix:
            output_path = output_path.with_suffix('.mp3')
        asyncio.run(generate_single_file(
            input_file, output_path, voice, args.rate, args.volume
        ))


if __name__ == '__main__':
    main()
