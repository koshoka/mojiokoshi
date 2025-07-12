"""文字起こし処理を行うモジュール."""

from pathlib import Path
from typing import Any, Callable, Optional, Union

import whisper

from .model_utils import ensure_model_downloaded


class Transcriber:
    """音声ファイルから文字起こしを行うクラス."""

    def __init__(self, model_name: str = "large-v3") -> None:
        """Transcriberを初期化する.

        Args:
        ----
            model_name: 使用するWhisperモデルの名前（デフォルト: large-v3）
        """
        self.model_name = model_name
        self._model: Optional[Any] = None  # 遅延ロード用

    def transcribe(
        self,
        audio_path: Union[str, Path],
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> dict[str, Any]:
        """音声ファイルを文字起こしする.

        Args:
        ----
            audio_path: 音声ファイルのパス
            progress_callback: 進捗状況を通知するコールバック関数

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

        # モデルの遅延ロード
        if self._model is None:
            # まずモデルのダウンロードを確認
            def download_progress(ratio: float, message: str) -> None:
                if progress_callback:
                    progress_callback(message)

            ensure_model_downloaded(self.model_name, download_progress)

            # モデルをロード
            if progress_callback:
                progress_callback(f"{self.model_name}モデルをメモリにロード中...")
            self._model = whisper.load_model(self.model_name)
            if progress_callback:
                progress_callback("モデルのロード完了！")

        # 音声ファイルを文字起こし
        assert self._model is not None
        if progress_callback:
            progress_callback("音声ファイルを解析中...")

        # verbose=Trueにすることで進捗をコンソールに表示（将来的にキャプチャ可能）
        result: dict[str, Any] = self._model.transcribe(
            str(audio_path),
            verbose=False,  # Falseにしてコンソール出力を抑制
            language="ja"
            if "large" in self.model_name
            else None,  # largeモデルの場合は日本語を指定
        )
        return result
