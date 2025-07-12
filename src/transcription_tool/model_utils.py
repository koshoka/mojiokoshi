"""Whisperモデル管理のユーティリティ."""

import urllib.request
from pathlib import Path
from typing import Callable, Optional

# Whisperモデルの情報
MODEL_URLS = {
    "tiny": "https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt",
    "base": "https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt",
    "small": "https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt",
    "medium": "https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt",
    "large": "https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt",
    "large-v2": "https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt",
    "large-v3": "https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt",
}

MODEL_SIZES = {
    "tiny": 39,
    "base": 74,
    "small": 244,
    "medium": 769,
    "large": 1550,
    "large-v2": 1550,
    "large-v3": 1550,
}


def get_model_path(model_name: str) -> Path:
    """Whisperモデルの保存パスを取得.

    Args:
    ----
        model_name: モデル名

    Returns:
    -------
        モデルファイルのパス
    """
    # Whisperのデフォルトキャッシュディレクトリ
    cache_dir = Path.home() / ".cache" / "whisper"
    cache_dir.mkdir(parents=True, exist_ok=True)

    # モデルファイル名の取得
    if model_name in ["large", "large-v2"]:
        filename = "large-v2.pt"
    else:
        filename = f"{model_name}.pt"

    return cache_dir / filename


def is_model_downloaded(model_name: str) -> bool:
    """モデルがダウンロード済みかチェック.

    Args:
    ----
        model_name: モデル名

    Returns:
    -------
        ダウンロード済みの場合True
    """
    model_path = get_model_path(model_name)
    return model_path.exists()


def download_model_with_progress(
    model_name: str, progress_callback: Optional[Callable[[float, str], None]] = None
) -> None:
    """進捗表示付きでモデルをダウンロード.

    Args:
    ----
        model_name: モデル名
        progress_callback: 進捗コールバック (progress_ratio, message)
    """
    if model_name not in MODEL_URLS:
        raise ValueError(f"不明なモデル名: {model_name}")

    model_path = get_model_path(model_name)

    # すでにダウンロード済みの場合はスキップ
    if model_path.exists():
        if progress_callback:
            progress_callback(1.0, f"{model_name}モデルは既にダウンロード済みです")
        return

    url = MODEL_URLS[model_name]
    model_size_mb = MODEL_SIZES[model_name]

    # ダウンロード開始
    if progress_callback:
        progress_callback(
            0.0, f"{model_name}モデル ({model_size_mb}MB) のダウンロードを開始..."
        )

    def download_hook(block_num: int, block_size: int, total_size: int) -> None:
        """ダウンロード進捗フック."""
        downloaded = block_num * block_size
        progress_ratio = min(downloaded / total_size, 1.0)
        downloaded_mb = downloaded / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)

        if progress_callback:
            progress_callback(
                progress_ratio,
                f"ダウンロード中: {downloaded_mb:.1f}MB / {total_mb:.1f}MB "
                f"({progress_ratio*100:.1f}%)",
            )

    # 一時ファイルにダウンロード
    temp_path = model_path.with_suffix(".tmp")
    try:
        urllib.request.urlretrieve(url, str(temp_path), reporthook=download_hook)
        # ダウンロード完了後にリネーム
        temp_path.rename(model_path)

        if progress_callback:
            progress_callback(1.0, f"{model_name}モデルのダウンロードが完了しました")
    except Exception as e:
        # エラー時は一時ファイルを削除
        if temp_path.exists():
            temp_path.unlink()
        raise e


def ensure_model_downloaded(
    model_name: str, progress_callback: Optional[Callable[[float, str], None]] = None
) -> bool:
    """モデルがダウンロード済みであることを確認し、必要ならダウンロード.

    Args:
    ----
        model_name: モデル名
        progress_callback: 進捗コールバック

    Returns:
    -------
        新規ダウンロードした場合True、既存の場合False
    """
    if is_model_downloaded(model_name):
        if progress_callback:
            progress_callback(1.0, f"{model_name}モデルは既にダウンロード済みです")
        return False

    download_model_with_progress(model_name, progress_callback)
    return True
