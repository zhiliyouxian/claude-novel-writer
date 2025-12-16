#!/usr/bin/env python3
"""
视频拼接脚本

功能：
1. 将 Ken Burns 视频片段拼接成完整视频
2. 添加音频轨道
3. 添加字幕（可选：烧录或作为字幕轨道）

依赖：
    - ffmpeg (系统安装)
    - Python 3.8+

用法：
    # 拼接视频片段
    python assemble-video.py <clips_dir> <output.mp4>

    # 添加音频
    python assemble-video.py <clips_dir> <output.mp4> --audio audio.mp3

    # 添加字幕（烧录）
    python assemble-video.py <clips_dir> <output.mp4> --audio audio.mp3 --subtitles subtitles.srt --burn-subtitles

    # 添加字幕（作为轨道）
    python assemble-video.py <clips_dir> <output.mp4> --audio audio.mp3 --subtitles subtitles.srt

    # 指定字幕样式
    python assemble-video.py <clips_dir> <output.mp4> --subtitles subtitles.srt --burn-subtitles --subtitle-style "FontSize=28,PrimaryColour=&HFFFFFF"

选项：
    --audio <file>          音频文件
    --subtitles <file>      SRT 字幕文件
    --burn-subtitles        将字幕烧录到视频中
    --subtitle-style <str>  ASS 字幕样式
    --chapter <n>           章节号（用于输出文件命名）
    --temp-dir <dir>        临时文件目录
"""

import os
import sys
import glob
import argparse
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional


def get_video_duration(video_path: str) -> float:
    """获取视频时长"""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return float(result.stdout.strip())
    return 0.0


def create_concat_file(clips: List[str], output_path: str) -> str:
    """创建 ffmpeg concat 文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for clip in clips:
            # ffmpeg concat 需要绝对路径
            abs_path = os.path.abspath(clip)
            f.write(f"file '{abs_path}'\n")
    return output_path


def concat_videos(clips: List[str], output: str, temp_dir: str) -> bool:
    """拼接视频片段"""
    # 创建 concat 文件
    concat_file = os.path.join(temp_dir, 'concat.txt')
    create_concat_file(clips, concat_file)

    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_file,
        '-c', 'copy',
        output
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def add_audio(video: str, audio: str, output: str) -> bool:
    """添加音频轨道"""
    # 获取视频和音频时长
    video_duration = get_video_duration(video)
    audio_duration = get_video_duration(audio)

    cmd = [
        'ffmpeg', '-y',
        '-i', video,
        '-i', audio,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
    ]

    # 如果音频比视频长，截断音频
    if audio_duration > video_duration:
        cmd.extend(['-t', str(video_duration)])

    # 如果视频比音频长，循环音频或静音填充（这里选择截断视频）
    if video_duration > audio_duration:
        cmd.extend(['-shortest'])

    cmd.extend(['-map', '0:v:0', '-map', '1:a:0', output])

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def burn_subtitles(video: str, subtitles: str, output: str, style: str = "") -> bool:
    """将字幕烧录到视频中"""
    # 处理字幕文件路径（ffmpeg 需要转义）
    subs_path = subtitles.replace('\\', '/').replace(':', '\\:')

    filter_str = f"subtitles='{subs_path}'"
    if style:
        filter_str += f":force_style='{style}'"

    cmd = [
        'ffmpeg', '-y',
        '-i', video,
        '-vf', filter_str,
        '-c:a', 'copy',
        output
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"字幕烧录错误: {result.stderr[:200]}")
    return result.returncode == 0


def add_subtitle_track(video: str, subtitles: str, output: str) -> bool:
    """添加字幕轨道（不烧录）"""
    cmd = [
        'ffmpeg', '-y',
        '-i', video,
        '-i', subtitles,
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-c:s', 'mov_text',  # MP4 字幕格式
        '-metadata:s:s:0', 'language=chi',
        output
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def assemble_chapter(
    clips_dir: str,
    output: str,
    audio: Optional[str] = None,
    subtitles: Optional[str] = None,
    burn_subs: bool = False,
    subtitle_style: str = "",
    temp_dir: Optional[str] = None
) -> bool:
    """组装完整章节视频"""

    # 查找视频片段
    clips_path = Path(clips_dir)
    patterns = ['scene-*.mp4', 'clip-*.mp4', '*.mp4']

    clips = []
    for pattern in patterns:
        found = sorted(clips_path.glob(pattern))
        if found:
            clips = [str(f) for f in found]
            break

    if not clips:
        print(f"错误: 在 {clips_dir} 中未找到视频片段")
        return False

    print(f"找到 {len(clips)} 个视频片段")

    # 创建临时目录
    if temp_dir:
        os.makedirs(temp_dir, exist_ok=True)
        tmp = temp_dir
    else:
        tmp = tempfile.mkdtemp()

    try:
        # Step 1: 拼接视频片段
        concat_output = os.path.join(tmp, 'concat.mp4')
        print("拼接视频片段...")
        if not concat_videos(clips, concat_output, tmp):
            print("❌ 拼接失败")
            return False
        print(f"  ✅ 拼接完成: {get_video_duration(concat_output):.1f}s")

        current_video = concat_output

        # Step 2: 添加音频
        if audio and os.path.exists(audio):
            audio_output = os.path.join(tmp, 'with_audio.mp4')
            print("添加音频...")
            if not add_audio(current_video, audio, audio_output):
                print("❌ 添加音频失败")
                return False
            print("  ✅ 音频添加完成")
            current_video = audio_output

        # Step 3: 处理字幕
        if subtitles and os.path.exists(subtitles):
            if burn_subs:
                print("烧录字幕...")
                subs_output = os.path.join(tmp, 'with_subs.mp4')
                if not burn_subtitles(current_video, subtitles, subs_output, subtitle_style):
                    print("⚠️ 字幕烧录失败，尝试不带字幕输出")
                else:
                    print("  ✅ 字幕烧录完成")
                    current_video = subs_output
            else:
                print("添加字幕轨道...")
                subs_output = os.path.join(tmp, 'with_subs.mp4')
                if not add_subtitle_track(current_video, subtitles, subs_output):
                    print("⚠️ 添加字幕轨道失败")
                else:
                    print("  ✅ 字幕轨道添加完成")
                    current_video = subs_output

        # Step 4: 复制到最终输出
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        import shutil
        shutil.copy2(current_video, output)
        print(f"\n✅ 输出: {output}")
        print(f"   时长: {get_video_duration(output):.1f}s")

        return True

    finally:
        # 清理临时文件（如果不是用户指定的）
        if not temp_dir:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(
        description='视频拼接脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('clips_dir', help='视频片段目录')
    parser.add_argument('output', help='输出视频路径')
    parser.add_argument('--audio', help='音频文件')
    parser.add_argument('--subtitles', help='SRT 字幕文件')
    parser.add_argument('--burn-subtitles', action='store_true',
                        help='将字幕烧录到视频中')
    parser.add_argument('--subtitle-style', default='',
                        help='ASS 字幕样式，如 "FontSize=28,PrimaryColour=&HFFFFFF"')
    parser.add_argument('--chapter', type=int, help='章节号')
    parser.add_argument('--temp-dir', help='临时文件目录')

    args = parser.parse_args()

    # 检查输入目录
    if not os.path.isdir(args.clips_dir):
        print(f"错误: 目录不存在: {args.clips_dir}")
        sys.exit(1)

    # 检查 ffmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
    except FileNotFoundError:
        print("错误: 未找到 ffmpeg，请先安装")
        sys.exit(1)

    # 执行组装
    success = assemble_chapter(
        clips_dir=args.clips_dir,
        output=args.output,
        audio=args.audio,
        subtitles=args.subtitles,
        burn_subs=args.burn_subtitles,
        subtitle_style=args.subtitle_style,
        temp_dir=args.temp_dir
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
