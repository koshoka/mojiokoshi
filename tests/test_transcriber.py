"""Transcriberクラスのテスト"""

from pathlib import Path

import pytest
from transcription_tool.transcriber import Transcriber


def test_transcriber_クラスが存在する() -> None:
    """Transcriberクラスがインポートできることを確認"""
    assert Transcriber is not None


def test_transcriber_インスタンスが作成できる() -> None:
    """Transcriberのインスタンスが作成できることを確認"""
    transcriber = Transcriber()
    assert transcriber is not None


def test_transcriber_モデル名を指定して初期化できる() -> None:
    """モデル名を指定してTranscriberを初期化できることを確認"""
    transcriber = Transcriber(model_name="large-v3")
    assert transcriber.model_name == "large-v3"


def test_transcribe_メソッドが存在する() -> None:
    """transcribeメソッドが存在することを確認"""
    transcriber = Transcriber()
    assert hasattr(transcriber, "transcribe")
    assert callable(transcriber.transcribe)


def test_transcribe_存在しないファイルでエラーが発生する() -> None:
    """存在しないファイルを指定した場合、FileNotFoundErrorが発生することを確認"""
    transcriber = Transcriber()
    with pytest.raises(FileNotFoundError):
        transcriber.transcribe("/path/to/nonexistent/file.mp3")


def test_transcribe_音声ファイルのフォーマットをチェックする() -> None:
    """対応していない音声フォーマットの場合、ValueErrorが発生することを確認"""
    transcriber = Transcriber()
    # テスト用の空のテキストファイルを作成
    test_file = Path("tests/test_data/test.txt")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("This is not an audio file")

    try:
        with pytest.raises(ValueError, match="対応していない音声フォーマット"):
            transcriber.transcribe(test_file)
    finally:
        test_file.unlink()  # テストファイルを削除
