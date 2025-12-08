#!/usr/bin/env python3
"""
检测章节文件中的乱码和编码问题

用法:
    python check-encoding.py <目录路径>                    # 检测目录下所有md文件
    python check-encoding.py <目录路径> --report           # 生成修复报告(便于AI修正)
    python check-encoding.py <目录路径> --json             # 输出JSON格式
    python check-encoding.py <文件路径.md>                 # 检测单个文件

示例:
    python check-encoding.py /path/to/chapters
    python check-encoding.py /path/to/chapters --report
    python check-encoding.py /path/to/chapters --json > errors.json
"""

import sys
import os
import glob
import re
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class EncodingError:
    """单个编码错误"""
    line_num: int
    column: int
    char: str
    context: str  # 错误字符前后的上下文


@dataclass
class FileReport:
    """单个文件的检测报告"""
    filepath: str
    error_count: int
    errors: list[EncodingError]


def get_context(line: str, col: int, context_len: int = 20) -> str:
    """获取错误字符的上下文"""
    start = max(0, col - context_len)
    end = min(len(line), col + context_len + 1)

    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(line) else ""

    # 标记错误位置
    context = line[start:end]
    return f"{prefix}{context}{suffix}"


def check_file_detailed(filepath: str) -> Optional[FileReport]:
    """详细检测单个文件，返回所有错误的精确位置"""
    errors = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            # 检测替换字符
            for col, char in enumerate(line):
                if char == '\ufffd':
                    errors.append(EncodingError(
                        line_num=line_num,
                        column=col + 1,
                        char='\\ufffd',
                        context=get_context(line.rstrip(), col)
                    ))
                # 检测控制字符
                elif ord(char) < 32 and char not in '\n\r\t':
                    errors.append(EncodingError(
                        line_num=line_num,
                        column=col + 1,
                        char=f'\\x{ord(char):02x}',
                        context=get_context(line.rstrip(), col)
                    ))

        if errors:
            return FileReport(
                filepath=filepath,
                error_count=len(errors),
                errors=errors
            )
        return None

    except UnicodeDecodeError as e:
        return FileReport(
            filepath=filepath,
            error_count=1,
            errors=[EncodingError(
                line_num=0,
                column=0,
                char='decode_error',
                context=str(e)
            )]
        )
    except Exception as e:
        return FileReport(
            filepath=filepath,
            error_count=1,
            errors=[EncodingError(
                line_num=0,
                column=0,
                char='error',
                context=str(e)
            )]
        )


def scan_directory(path: str) -> list[str]:
    """扫描目录下所有md文件"""
    path = Path(path)

    if path.is_file():
        return [str(path)]

    if path.is_dir():
        # 递归查找所有 .md 文件
        files = list(path.rglob("*.md"))
        return sorted([str(f) for f in files])

    # 尝试作为 glob 模式
    files = glob.glob(str(path), recursive=True)
    return sorted(files)


def print_summary(reports: list[FileReport], total_files: int):
    """打印简洁汇总"""
    print(f"\n{'='*60}")
    print(f"检测完成: {total_files} 个文件")
    print(f"  ✅ 正常: {total_files - len(reports)}")
    print(f"  ❌ 问题: {len(reports)}")

    if reports:
        total_errors = sum(r.error_count for r in reports)
        print(f"  📍 总错误数: {total_errors}")


def print_report(reports: list[FileReport]):
    """打印详细修复报告（便于AI修正）"""
    if not reports:
        print("\n✅ 未发现编码问题")
        return

    print("\n" + "="*60)
    print("📋 编码错误修复报告")
    print("="*60)

    for report in reports:
        print(f"\n## 文件: {report.filepath}")
        print(f"   错误数: {report.error_count}")
        print()

        for err in report.errors:
            print(f"   - 第 {err.line_num} 行, 第 {err.column} 列")
            print(f"     字符: {err.char}")
            print(f"     上下文: {err.context}")
            print()

    # 生成修复建议
    print("="*60)
    print("📝 修复建议")
    print("="*60)
    print("""
对于每个错误位置:
1. 根据上下文推断原本应该是什么字符
2. 常见情况:
   - "一口���" → "一口气"
   - "���说" → "他说" 或 "她说"
   - 数字/标点乱码 → 根据语境判断

修复命令示例:
  请修复以下文件中的乱码:
  - {filepath}: 第X行 "上下文" 中的乱码
""")


def print_json(reports: list[FileReport], total_files: int):
    """输出JSON格式"""
    output = {
        "summary": {
            "total_files": total_files,
            "clean_files": total_files - len(reports),
            "problem_files": len(reports),
            "total_errors": sum(r.error_count for r in reports)
        },
        "files": [asdict(r) for r in reports]
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def print_simple(reports: list[FileReport]):
    """打印简单列表"""
    for report in reports:
        print(f"\n❌ {report.filepath} ({report.error_count} 个错误)")
        # 同一行只显示一次
        seen_lines = set()
        for err in report.errors:
            if err.line_num not in seen_lines:
                seen_lines.add(err.line_num)
                print(f"   第{err.line_num}行: {err.context}")


def main():
    # 解析参数
    args = sys.argv[1:]

    if not args or '-h' in args or '--help' in args:
        print(__doc__)
        return 0

    # 提取选项
    output_json = '--json' in args
    output_report = '--report' in args
    paths = [a for a in args if not a.startswith('-')]

    if not paths:
        print("错误: 请提供目录或文件路径")
        print("用法: python check-encoding.py <路径> [--report|--json]")
        return 1

    # 收集所有文件
    all_files = []
    for path in paths:
        all_files.extend(scan_directory(path))

    if not all_files:
        print(f"未找到 .md 文件: {paths}")
        return 1

    # 检测所有文件
    reports = []
    for filepath in all_files:
        report = check_file_detailed(filepath)
        if report:
            reports.append(report)

    # 输出结果
    if output_json:
        print_json(reports, len(all_files))
    elif output_report:
        print_simple(reports)
        print_summary(reports, len(all_files))
        print_report(reports)
    else:
        print_simple(reports)
        print_summary(reports, len(all_files))

    # 正常退出，检测到乱码不算错误
    return 0


if __name__ == '__main__':
    sys.exit(main())
