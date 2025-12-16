#!/usr/bin/env python3
"""
Ken Burns 动画生成脚本

功能：
1. 读取场景参数 JSON 文件
2. 为每个场景生成 ffmpeg zoompan 命令
3. 输出视频片段或拼接脚本

依赖：
    - ffmpeg (系统安装)
    - Python 3.8+

用法：
    # 生成单个场景的 Ken Burns 动画
    python generate-kenburns.py <image> <output.mp4> --duration 30 --type push_in

    # 从参数文件批量生成
    python generate-kenburns.py --params scene-params.json --images-dir images/scenes/ --output-dir clips/

    # 生成 shell 脚本（不执行）
    python generate-kenburns.py --params scene-params.json --images-dir images/scenes/ --output-dir clips/ --dry-run

选项：
    --duration <seconds>    持续时间（单个文件模式）
    --type <type>           动画类型（单个文件模式）
    --fps <fps>             帧率，默认 30
    --resolution <WxH>      分辨率，默认 1920x1080
    --params <json>         场景参数 JSON 文件（批量模式）
    --images-dir <dir>      图片目录（批量模式）
    --output-dir <dir>      输出目录（批量模式）
    --dry-run               只生成脚本不执行
    --parallel <n>          并行处理数量，默认 4

动画类型：
    push_in     - 缓慢推进（放大）
    pull_out    - 缓慢拉远（缩小）
    pan_left    - 向左平移
    pan_right   - 向右平移
    pan_up      - 向上平移
    pan_down    - 向下平移
    diagonal    - 斜向推进
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed


# ==================== Ken Burns 预设 ====================

KENBURNS_PRESETS = {
    "push_in": {
        "description": "缓慢推进（放大）",
        "start": {"scale": 1.0, "x": 0.5, "y": 0.5},
        "end": {"scale": 1.3, "x": 0.5, "y": 0.45}
    },
    "pull_out": {
        "description": "缓慢拉远（缩小）",
        "start": {"scale": 1.3, "x": 0.5, "y": 0.5},
        "end": {"scale": 1.0, "x": 0.5, "y": 0.5}
    },
    "pan_left": {
        "description": "向左平移",
        "start": {"scale": 1.2, "x": 0.7, "y": 0.5},
        "end": {"scale": 1.2, "x": 0.3, "y": 0.5}
    },
    "pan_right": {
        "description": "向右平移",
        "start": {"scale": 1.2, "x": 0.3, "y": 0.5},
        "end": {"scale": 1.2, "x": 0.7, "y": 0.5}
    },
    "pan_up": {
        "description": "向上平移",
        "start": {"scale": 1.2, "x": 0.5, "y": 0.7},
        "end": {"scale": 1.2, "x": 0.5, "y": 0.3}
    },
    "pan_down": {
        "description": "向下平移",
        "start": {"scale": 1.2, "x": 0.5, "y": 0.3},
        "end": {"scale": 1.2, "x": 0.5, "y": 0.7}
    },
    "diagonal": {
        "description": "斜向推进",
        "start": {"scale": 1.0, "x": 0.4, "y": 0.6},
        "end": {"scale": 1.25, "x": 0.6, "y": 0.4}
    }
}


# ==================== ffmpeg 命令生成 ====================

def generate_zoompan_filter(
    duration: float,
    fps: int,
    resolution: Tuple[int, int],
    start_scale: float,
    end_scale: float,
    start_x: float,
    end_x: float,
    start_y: float,
    end_y: float
) -> str:
    """
    生成 ffmpeg zoompan 滤镜字符串

    参数：
        duration: 持续时间（秒）
        fps: 帧率
        resolution: (宽, 高)
        start_scale, end_scale: 起始/结束缩放比例
        start_x, end_x: 起始/结束 X 位置 (0-1)
        start_y, end_y: 起始/结束 Y 位置 (0-1)
    """
    total_frames = int(duration * fps)
    width, height = resolution

    # 计算每帧的缩放变化
    scale_delta = (end_scale - start_scale) / total_frames
    x_delta = (end_x - start_x) / total_frames
    y_delta = (end_y - start_y) / total_frames

    # zoompan 滤镜
    # z: 缩放因子
    # x, y: 裁剪位置
    # d: 总帧数
    # s: 输出分辨率
    # fps: 帧率

    # 使用表达式计算每帧的值
    zoom_expr = f"if(eq(on,1),{start_scale},{start_scale}+{scale_delta}*(on-1))"
    x_expr = f"iw/2-(iw/zoom/2)+({start_x}-0.5+{x_delta}*(on-1))*iw/zoom"
    y_expr = f"ih/2-(ih/zoom/2)+({start_y}-0.5+{y_delta}*(on-1))*ih/zoom"

    # 简化的 zoompan（线性插值）
    filter_str = (
        f"zoompan=z='min(max({start_scale}+{scale_delta}*(on-1),1),10)':"
        f"x='(iw-iw/zoom)*({start_x}+{x_delta}*(on-1))':"
        f"y='(ih-ih/zoom)*({start_y}+{y_delta}*(on-1))':"
        f"d={total_frames}:s={width}x{height}:fps={fps}"
    )

    return filter_str


def generate_ffmpeg_command(
    input_image: str,
    output_video: str,
    duration: float,
    animation_type: str = "push_in",
    custom_params: Optional[Dict] = None,
    fps: int = 30,
    resolution: Tuple[int, int] = (1920, 1080)
) -> List[str]:
    """生成 ffmpeg 命令"""

    # 获取动画参数
    if custom_params:
        start = custom_params.get('start', KENBURNS_PRESETS["push_in"]["start"])
        end = custom_params.get('end', KENBURNS_PRESETS["push_in"]["end"])
    elif animation_type in KENBURNS_PRESETS:
        preset = KENBURNS_PRESETS[animation_type]
        start = preset["start"]
        end = preset["end"]
    else:
        print(f"警告: 未知动画类型 '{animation_type}'，使用默认 push_in")
        preset = KENBURNS_PRESETS["push_in"]
        start = preset["start"]
        end = preset["end"]

    # 生成滤镜
    filter_str = generate_zoompan_filter(
        duration=duration,
        fps=fps,
        resolution=resolution,
        start_scale=start.get('scale', 1.0),
        end_scale=end.get('scale', 1.3),
        start_x=start.get('x', 0.5),
        end_x=end.get('x', 0.5),
        start_y=start.get('y', 0.5),
        end_y=end.get('y', 0.5)
    )

    cmd = [
        'ffmpeg', '-y',
        '-loop', '1',
        '-i', input_image,
        '-vf', filter_str,
        '-t', str(duration),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'medium',
        '-crf', '23',
        output_video
    ]

    return cmd


# ==================== 批量处理 ====================

def process_scene(
    scene: Dict,
    images_dir: Path,
    output_dir: Path,
    fps: int,
    resolution: Tuple[int, int],
    dry_run: bool
) -> Tuple[str, bool, str]:
    """处理单个场景"""
    scene_id = scene.get('scene_id', '0001')
    image_name = scene.get('image', f'scene-{scene_id}.png')
    duration = scene.get('duration_seconds', 30)

    animation = scene.get('animation', {})
    animation_type = animation.get('type', 'push_in')

    input_image = images_dir / image_name
    output_video = output_dir / f'scene-{scene_id}.mp4'

    # 检查输入图片是否存在
    if not input_image.exists():
        return str(scene_id), False, f"图片不存在: {input_image}"

    # 生成命令
    cmd = generate_ffmpeg_command(
        input_image=str(input_image),
        output_video=str(output_video),
        duration=duration,
        animation_type=animation_type,
        custom_params=animation if 'start' in animation else None,
        fps=fps,
        resolution=resolution
    )

    if dry_run:
        return str(scene_id), True, ' '.join(cmd)

    # 执行命令
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return str(scene_id), True, str(output_video)
        else:
            return str(scene_id), False, result.stderr[:200]
    except Exception as e:
        return str(scene_id), False, str(e)


def batch_process(
    params_file: str,
    images_dir: str,
    output_dir: str,
    fps: int,
    resolution: Tuple[int, int],
    dry_run: bool,
    parallel: int
) -> None:
    """批量处理所有场景"""

    # 读取参数文件
    with open(params_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    scenes = data.get('scenes', [])
    if not scenes:
        print("错误: 参数文件中没有场景数据")
        return

    images_path = Path(images_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"共 {len(scenes)} 个场景")
    print(f"图片目录: {images_path}")
    print(f"输出目录: {output_path}")
    print(f"分辨率: {resolution[0]}x{resolution[1]}, FPS: {fps}")
    print()

    if dry_run:
        print("=== 生成的命令（未执行）===")
        for scene in scenes:
            scene_id, success, result = process_scene(
                scene, images_path, output_path, fps, resolution, True
            )
            if success:
                print(f"\n# Scene {scene_id}")
                print(result)
        return

    # 并行处理
    results = []
    with ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = {
            executor.submit(
                process_scene, scene, images_path, output_path, fps, resolution, False
            ): scene.get('scene_id', 'unknown')
            for scene in scenes
        }

        for future in as_completed(futures):
            scene_id, success, result = future.result()
            status = "✅" if success else "❌"
            print(f"{status} Scene {scene_id}: {result[:80]}")
            results.append((scene_id, success, result))

    # 统计
    success_count = sum(1 for _, s, _ in results if s)
    print(f"\n完成: {success_count}/{len(scenes)} 成功")


# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(
        description='Ken Burns 动画生成脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # 单文件模式
    parser.add_argument('input', nargs='?', help='输入图片（单文件模式）')
    parser.add_argument('output', nargs='?', help='输出视频（单文件模式）')
    parser.add_argument('--duration', type=float, default=30,
                        help='持续时间（秒），默认 30')
    parser.add_argument('--type', dest='animation_type', default='push_in',
                        choices=list(KENBURNS_PRESETS.keys()),
                        help='动画类型，默认 push_in')

    # 批量模式
    parser.add_argument('--params', help='场景参数 JSON 文件')
    parser.add_argument('--images-dir', help='图片目录')
    parser.add_argument('--output-dir', help='输出目录')

    # 通用选项
    parser.add_argument('--fps', type=int, default=30, help='帧率，默认 30')
    parser.add_argument('--resolution', default='1920x1080',
                        help='分辨率，默认 1920x1080')
    parser.add_argument('--dry-run', action='store_true',
                        help='只生成命令不执行')
    parser.add_argument('--parallel', type=int, default=4,
                        help='并行处理数量，默认 4')
    parser.add_argument('--list-types', action='store_true',
                        help='列出所有动画类型')

    args = parser.parse_args()

    # 列出动画类型
    if args.list_types:
        print("可用的 Ken Burns 动画类型:")
        for name, preset in KENBURNS_PRESETS.items():
            print(f"  {name:12} - {preset['description']}")
        return

    # 解析分辨率
    try:
        width, height = map(int, args.resolution.split('x'))
        resolution = (width, height)
    except:
        print(f"错误: 无效的分辨率格式: {args.resolution}")
        sys.exit(1)

    # 批量模式
    if args.params:
        if not args.images_dir or not args.output_dir:
            print("错误: 批量模式需要 --images-dir 和 --output-dir")
            sys.exit(1)

        batch_process(
            params_file=args.params,
            images_dir=args.images_dir,
            output_dir=args.output_dir,
            fps=args.fps,
            resolution=resolution,
            dry_run=args.dry_run,
            parallel=args.parallel
        )
        return

    # 单文件模式
    if not args.input or not args.output:
        parser.print_help()
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}")
        sys.exit(1)

    cmd = generate_ffmpeg_command(
        input_image=args.input,
        output_video=args.output,
        duration=args.duration,
        animation_type=args.animation_type,
        fps=args.fps,
        resolution=resolution
    )

    if args.dry_run:
        print(' '.join(cmd))
        return

    print(f"生成 Ken Burns 动画: {args.input} -> {args.output}")
    print(f"  类型: {args.animation_type}")
    print(f"  时长: {args.duration}s")
    print(f"  分辨率: {resolution[0]}x{resolution[1]}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ 完成!")
    else:
        print(f"❌ 失败: {result.stderr[:200]}")
        sys.exit(1)


if __name__ == '__main__':
    main()
