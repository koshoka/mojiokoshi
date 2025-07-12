"""文字起こし処理を行うモジュール."""

from pathlib import Path
from typing import Any, Union


class Transcriber:
    """音声ファイルから文字起こしを行うクラス."""

    def __init__(self, model_name: str = "large-v3") -> None:
        """Transcriberを初期化する.

        Args:
        ----
            model_name: 使用するWhisperモデルの名前（デフォルト: large-v3）
        """
        self.model_name = model_name

    def transcribe(self, audio_path: Union[str, Path]) -> dict[str, Any]:
        """音声ファイルを文字起こしする.

        Args:
        ----
            audio_path: 音声ファイルのパス

        Returns:
        -------
            文字起こし結果を含む辞書

        Raises:
        ------
            FileNotFoundError: 指定されたファイルが存在しない場合
            ValueError: 対応していない音声フォーマットの場合
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"音声ファイルが見つかりません: {audio_path}")

        # 対応している音声フォーマットをチェック
        supported_formats = {".wav", ".mp3", ".mp4", ".m4a", ".flac", ".ogg", ".opus"}
        if audio_path.suffix.lower() not in supported_formats:
            raise ValueError(f"対応していない音声フォーマット: {audio_path.suffix}")

        # TODO: Whisperモデルのロードと文字起こし処理
        return {"text": ""}
