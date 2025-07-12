"""ユーティリティ関数を提供するモジュール."""

from datetime import datetime
from pathlib import Path
from typing import Any, Optional


def save_transcription_as_markdown(
    transcription_result: dict[str, Any],
    audio_filename: str,
    output_dir: Optional[Path] = None,
    include_timestamps: bool = False,
) -> Path:
    """文字起こし結果をMarkdown形式で保存する.

    Args:
    ----
        transcription_result: Whisperの文字起こし結果
        audio_filename: 元の音声ファイル名
        output_dir: 出力ディレクトリ（Noneの場合はtranscriptionsディレクトリ）
        include_timestamps: タイムスタンプを含めるかどうか

    Returns:
    -------
        保存したファイルのパス
    """
    # 出力ディレクトリの設定
    if output_dir is None:
        output_dir = Path("transcriptions")
    output_dir.mkdir(parents=True, exist_ok=True)

    # ファイル名の生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = Path(audio_filename).stem
    output_filename = f"{timestamp}_{base_name}.md"
    output_path = output_dir / output_filename

    # Markdownコンテンツの生成
    content_lines = [
        "# 文字起こし結果",
        "",
        f"**ファイル名**: {audio_filename}",
        f"**作成日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
        "",
        "## 文字起こし内容",
        "",
    ]

    if include_timestamps and "segments" in transcription_result:
        # タイムスタンプ付きで出力
        for segment in transcription_result["segments"]:
            start_time = _format_timestamp(segment["start"])
            end_time = _format_timestamp(segment["end"])
            text = segment["text"].strip()
            content_lines.append(f"[{start_time} - {end_time}] {text}")
            content_lines.append("")
    else:
        # 通常のテキスト出力
        content_lines.append(transcription_result["text"])

    # ファイルに保存
    output_path.write_text("\n".join(content_lines), encoding="utf-8")

    return output_path


def _format_timestamp(seconds: float) -> str:
    """秒数を MM:SS 形式のタイムスタンプに変換する."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
