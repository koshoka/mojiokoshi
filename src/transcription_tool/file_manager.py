"""文字起こし結果ファイルの管理機能."""

from datetime import datetime
from pathlib import Path
from typing import Optional


def get_transcriptions_dir() -> Path:
    """文字起こし結果の保存ディレクトリを取得.

    Returns
    -------
        Path: transcriptionsディレクトリのパス
    """
    # プロジェクトルートからの相対パス
    transcriptions_dir = Path.cwd() / "transcriptions"
    transcriptions_dir.mkdir(exist_ok=True)
    return transcriptions_dir


def list_transcription_files() -> list[tuple[str, str, str, float]]:
    """文字起こし結果ファイルの一覧を取得.

    Returns
    -------
        (ファイル名, 作成日時, サイズ, タイムスタンプ)のリスト
    """
    transcriptions_dir = get_transcriptions_dir()
    files = []

    for file_path in transcriptions_dir.glob("*.md"):
        stat = file_path.stat()

        # ファイル名
        filename = file_path.name

        # 作成日時を読みやすい形式に
        created_time = datetime.fromtimestamp(stat.st_mtime)
        created_str = created_time.strftime("%Y年%m月%d日 %H:%M:%S")

        # ファイルサイズを読みやすい形式に
        size_bytes = stat.st_size
        if size_bytes < 1024:
            size_str = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"

        # タイムスタンプ（ソート用）
        timestamp = stat.st_mtime

        files.append((filename, created_str, size_str, timestamp))

    # 作成日時の新しい順にソート
    files.sort(key=lambda x: x[3], reverse=True)

    return files


def read_transcription_file(filename: str) -> Optional[str]:
    """指定されたファイルの内容を読み込む.

    Args:
    ----
        filename: ファイル名

    Returns:
    -------
        Optional[str]: ファイルの内容、またはNone（エラー時）
    """
    transcriptions_dir = get_transcriptions_dir()
    file_path = transcriptions_dir / filename

    if not file_path.exists() or not file_path.is_file():
        return None

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"ファイルの読み込みエラー: {str(e)}"


def get_file_full_path(filename: str) -> str:
    """ファイルのフルパスを取得.

    Args:
    ----
        filename: ファイル名

    Returns:
    -------
        str: ファイルのフルパス
    """
    transcriptions_dir = get_transcriptions_dir()
    return str(transcriptions_dir / filename)
