#!/usr/bin/env python3
"""
SRT 字幕转分镜脚本

功能：
1. 解析 SRT 字幕文件，提取时间轴和文本
2. 自动检测场景边界（地点、时间、角色变化）
3. 输出 JSON 格式的场景数据

依赖安装：
    pip install pysrt

用法：
    # 基本用法
    python srt-to-storyboard.py <input.srt> <output.json>

    # 指定场景最小时长（秒）
    python srt-to-storyboard.py input.srt output.json --scene-min-duration 5

    # 指定合并阈值（秒，间隔小于此值的相似场景合并）
    python srt-to-storyboard.py input.srt output.json --merge-threshold 3

    # 输出 Markdown 格式
    python srt-to-storyboard.py input.srt output.md --format markdown

    # 同时输出 JSON 和 Markdown
    python srt-to-storyboard.py input.srt output --format both

选项：
    --scene-min-duration <seconds>  场景最小时长（默认：5秒）
    --merge-threshold <seconds>     场景合并阈值（默认：3秒）
    --format <json|markdown|both>   输出格式（默认：json）
    --chapter <number>              章节号（用于输出文件命名）
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import timedelta
from typing import List, Dict, Tuple, Optional

try:
    import pysrt
except ImportError:
    print("请先安装 pysrt: pip install pysrt")
    sys.exit(1)


# ==================== 场景边界检测关键词 ====================

# 地点变化词
LOCATION_CHANGE_WORDS = [
    '来到', '走进', '走出', '进入', '离开', '回到', '抵达', '踏入',
    '前往', '返回', '赶到', '飞向', '落在', '降落', '出现在',
    '走入', '步入', '闯入', '冲进', '跑向', '飞往'
]

# 时间跳跃词
TIME_SKIP_WORDS = [
    '第二天', '第三天', '三天后', '数天后', '一个月后', '数月后',
    '一年后', '数年后', '百年后', '千年后', '万年后',
    '片刻后', '半晌后', '须臾间', '转眼间', '不久',
    '天亮', '天黑', '黄昏', '清晨', '午时', '夜半', '子时',
    '日落', '日出', '月上', '月落', '星光下',
    '随后', '接着', '继而', '旋即', '霎时'
]

# 场景转换词
SCENE_TRANSITION_WORDS = [
    '此时', '另一边', '与此同时', '就在这时', '不远处',
    '话分两头', '且说', '却说', '再说', '话说',
    '另一处', '别处', '彼方', '那边厢'
]

# 情绪关键词映射
EMOTION_KEYWORDS = {
    '愤怒': ['怒喝', '暴怒', '震怒', '大怒', '咆哮', '怒吼', '愤怒'],
    '轻蔑': ['冷笑', '嘲讽', '讥讽', '嗤笑', '不屑', '轻蔑'],
    '恐惧': ['惊恐', '颤抖', '惧意', '害怕', '恐惧', '战栗'],
    '喜悦': ['欣喜', '大笑', '兴奋', '高兴', '欢喜', '喜悦'],
    '悲伤': ['悲伤', '泪流', '哽咽', '痛哭', '悲泣', '伤感'],
    '平静': ['平静', '淡然', '从容', '镇定', '沉着'],
    '紧张': ['紧张', '凝重', '肃然', '严峻', '紧迫'],
    '坚定': ['决然', '坚定', '毅然', '果决', '斩钉截铁'],
    '惊讶': ['惊讶', '震惊', '愕然', '吃惊', '诧异'],
    '得意': ['得意', '自豪', '傲然', '趾高气扬']
}


# ==================== 数据结构 ====================

class SubtitleEntry:
    """字幕条目"""
    def __init__(self, index: int, start: timedelta, end: timedelta, text: str):
        self.index = index
        self.start = start
        self.end = end
        self.text = text

    def duration(self) -> float:
        return (self.end - self.start).total_seconds()


class Scene:
    """场景"""
    def __init__(self, scene_id: int):
        self.scene_id = scene_id
        self.subtitles: List[SubtitleEntry] = []
        self.start_time: Optional[timedelta] = None
        self.end_time: Optional[timedelta] = None
        self.location: str = ""
        self.characters: List[str] = []
        self.emotion: str = "平静"
        self.description: str = ""
        self.boundary_reason: str = ""  # 为什么在这里分场景

    def add_subtitle(self, sub: SubtitleEntry):
        self.subtitles.append(sub)
        if self.start_time is None:
            self.start_time = sub.start
        self.end_time = sub.end

    def duration(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0

    def srt_range(self) -> Tuple[int, int]:
        if self.subtitles:
            return (self.subtitles[0].index, self.subtitles[-1].index)
        return (0, 0)

    def full_text(self) -> str:
        return ' '.join(sub.text for sub in self.subtitles)

    def to_dict(self) -> dict:
        return {
            'scene_id': self.scene_id,
            'start_time': format_timedelta(self.start_time) if self.start_time else "00:00:00",
            'end_time': format_timedelta(self.end_time) if self.end_time else "00:00:00",
            'duration_seconds': round(self.duration(), 1),
            'srt_range': list(self.srt_range()),
            'location': self.location,
            'characters': self.characters,
            'emotion': self.emotion,
            'description': self.description[:200] if self.description else "",
            'boundary_reason': self.boundary_reason,
            'subtitle_count': len(self.subtitles)
        }


# ==================== 工具函数 ====================

def format_timedelta(td: timedelta) -> str:
    """格式化时间为 HH:MM:SS"""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def parse_srt(filepath: str) -> List[SubtitleEntry]:
    """解析 SRT 文件"""
    subs = pysrt.open(filepath, encoding='utf-8')
    entries = []

    for sub in subs:
        start = timedelta(
            hours=sub.start.hours,
            minutes=sub.start.minutes,
            seconds=sub.start.seconds,
            milliseconds=sub.start.milliseconds
        )
        end = timedelta(
            hours=sub.end.hours,
            minutes=sub.end.minutes,
            seconds=sub.end.seconds,
            milliseconds=sub.end.milliseconds
        )
        text = sub.text.replace('\n', ' ').strip()
        entries.append(SubtitleEntry(sub.index, start, end, text))

    return entries


def detect_boundary(text: str, prev_text: str = "") -> Tuple[bool, str]:
    """检测是否是场景边界"""
    # 地点变化
    for word in LOCATION_CHANGE_WORDS:
        if word in text:
            return True, f"地点变化: {word}"

    # 时间跳跃
    for word in TIME_SKIP_WORDS:
        if word in text:
            return True, f"时间跳跃: {word}"

    # 场景转换
    for word in SCENE_TRANSITION_WORDS:
        if word in text:
            return True, f"场景转换: {word}"

    return False, ""


def detect_emotion(text: str) -> str:
    """检测文本中的情绪"""
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return emotion
    return "平静"


def extract_location(text: str) -> str:
    """尝试提取地点"""
    # 简单的地点提取模式
    patterns = [
        r'(?:来到|进入|走进|踏入)(?:了)?(.{2,10}?)[，。]',
        r'(?:在)(.{2,10}?)[，。中里]',
        r'(.{2,6}(?:山|峰|殿|宫|城|门|洞|府|阁|塔|院|场|台|谷|林|海|湖))(?:[，。中里上下内外])',
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            location = match.group(1).strip()
            if len(location) >= 2:
                return location

    return ""


# ==================== 主要逻辑 ====================

def segment_scenes(
    subtitles: List[SubtitleEntry],
    min_duration: float = 5.0,
    merge_threshold: float = 3.0
) -> List[Scene]:
    """将字幕分割成场景"""
    if not subtitles:
        return []

    scenes: List[Scene] = []
    current_scene = Scene(1)
    prev_text = ""

    for sub in subtitles:
        # 检测是否是新场景
        is_boundary, reason = detect_boundary(sub.text, prev_text)

        # 如果当前场景有内容且检测到边界
        if is_boundary and current_scene.subtitles:
            # 检查当前场景时长是否足够
            if current_scene.duration() >= min_duration:
                # 完成当前场景
                current_scene.description = current_scene.full_text()[:200]
                current_scene.emotion = detect_emotion(current_scene.full_text())
                location = extract_location(current_scene.full_text())
                if location:
                    current_scene.location = location
                scenes.append(current_scene)

                # 开始新场景
                current_scene = Scene(len(scenes) + 1)
                current_scene.boundary_reason = reason

        current_scene.add_subtitle(sub)
        prev_text = sub.text

    # 处理最后一个场景
    if current_scene.subtitles:
        current_scene.description = current_scene.full_text()[:200]
        current_scene.emotion = detect_emotion(current_scene.full_text())
        location = extract_location(current_scene.full_text())
        if location:
            current_scene.location = location
        scenes.append(current_scene)

    # 合并过短的场景
    scenes = merge_short_scenes(scenes, min_duration, merge_threshold)

    return scenes


def merge_short_scenes(
    scenes: List[Scene],
    min_duration: float,
    merge_threshold: float
) -> List[Scene]:
    """合并过短的场景"""
    if len(scenes) <= 1:
        return scenes

    merged: List[Scene] = []
    current = scenes[0]

    for next_scene in scenes[1:]:
        # 如果当前场景太短，尝试与下一个合并
        if current.duration() < min_duration:
            # 计算间隔
            if current.end_time and next_scene.start_time:
                gap = (next_scene.start_time - current.end_time).total_seconds()
                if gap <= merge_threshold:
                    # 合并
                    for sub in next_scene.subtitles:
                        current.add_subtitle(sub)
                    current.description = current.full_text()[:200]
                    current.emotion = detect_emotion(current.full_text())
                    continue

        merged.append(current)
        current = next_scene

    merged.append(current)

    # 重新编号
    for i, scene in enumerate(merged, 1):
        scene.scene_id = i

    return merged


def to_json(scenes: List[Scene], chapter: int = 1) -> dict:
    """转换为 JSON 格式"""
    total_duration = sum(s.duration() for s in scenes)

    return {
        'chapter': chapter,
        'total_duration': format_timedelta(timedelta(seconds=total_duration)),
        'total_duration_seconds': round(total_duration, 1),
        'scene_count': len(scenes),
        'scenes': [s.to_dict() for s in scenes]
    }


def to_markdown(scenes: List[Scene], chapter: int = 1, source_srt: str = "") -> str:
    """转换为 Markdown 格式"""
    total_duration = sum(s.duration() for s in scenes)

    lines = [
        "---",
        f"chapter: {chapter}",
        f"source_srt: {source_srt}",
        f"total_duration: \"{format_timedelta(timedelta(seconds=total_duration))}\"",
        f"scene_count: {len(scenes)}",
        f"generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}",
        "---",
        "",
        f"# 第{chapter}章 分镜脚本",
        "",
        "## 场景列表",
        "",
        "| 场景 | 时间码 | 时长 | 地点 | 情绪 | SRT序号 |",
        "|------|--------|------|------|------|---------|",
    ]

    for scene in scenes:
        start = format_timedelta(scene.start_time) if scene.start_time else "00:00:00"
        end = format_timedelta(scene.end_time) if scene.end_time else "00:00:00"
        srt_start, srt_end = scene.srt_range()
        location = scene.location or "-"

        lines.append(
            f"| {scene.scene_id:03d} | {start}-{end} | {round(scene.duration())}s | "
            f"{location} | {scene.emotion} | {srt_start}-{srt_end} |"
        )

    lines.extend(["", "---", "", "## 场景详情", ""])

    for scene in scenes:
        start = format_timedelta(scene.start_time) if scene.start_time else "00:00:00"
        end = format_timedelta(scene.end_time) if scene.end_time else "00:00:00"
        srt_start, srt_end = scene.srt_range()

        lines.extend([
            f"### 场景 {scene.scene_id:03d}",
            "",
            f"**时间码**: {start} - {end}",
            f"**时长**: {round(scene.duration())}秒",
            f"**SRT序号**: #{srt_start}-{srt_end}",
            "",
            f"**地点**: {scene.location or '待定'}",
            f"**情绪**: {scene.emotion}",
            "",
            "**内容摘要**:",
            scene.description or "(无)",
            "",
            "---",
            ""
        ])

    return '\n'.join(lines)


# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(
        description='SRT 字幕转分镜脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('input', help='输入 SRT 文件路径')
    parser.add_argument('output', help='输出文件路径')
    parser.add_argument('--scene-min-duration', type=float, default=5.0,
                        help='场景最小时长（秒），默认 5')
    parser.add_argument('--merge-threshold', type=float, default=3.0,
                        help='场景合并阈值（秒），默认 3')
    parser.add_argument('--format', choices=['json', 'markdown', 'both'],
                        default='json', help='输出格式，默认 json')
    parser.add_argument('--chapter', type=int, default=1,
                        help='章节号，默认 1')

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}")
        sys.exit(1)

    # 解析 SRT
    print(f"解析 SRT 文件: {args.input}")
    subtitles = parse_srt(args.input)
    print(f"  共 {len(subtitles)} 条字幕")

    # 分割场景
    print(f"检测场景边界 (最小时长: {args.scene_min_duration}s, 合并阈值: {args.merge_threshold}s)")
    scenes = segment_scenes(
        subtitles,
        min_duration=args.scene_min_duration,
        merge_threshold=args.merge_threshold
    )
    print(f"  生成 {len(scenes)} 个场景")

    # 输出
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format in ['json', 'both']:
        json_path = output_path.with_suffix('.json') if args.format == 'both' else output_path
        data = to_json(scenes, args.chapter)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"JSON 输出: {json_path}")

    if args.format in ['markdown', 'both']:
        md_path = output_path.with_suffix('.md') if args.format == 'both' else output_path
        md_content = to_markdown(scenes, args.chapter, args.input)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Markdown 输出: {md_path}")

    print("完成!")


if __name__ == '__main__':
    main()
