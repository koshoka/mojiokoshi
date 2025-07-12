"""Gradioアプリケーションのテスト"""

from unittest.mock import Mock, patch

from transcription_tool.app import create_app, transcribe_audio


def test_create_app_関数が存在する() -> None:
    """create_app関数が存在することを確認"""
    assert create_app is not None
    assert callable(create_app)


def test_transcribe_audio_関数が存在する() -> None:
    """transcribe_audio関数が存在することを確認"""
    assert transcribe_audio is not None
    assert callable(transcribe_audio)


def test_create_app_が正しいインターフェースを返す() -> None:
    """create_appがGradioインターフェースを返すことを確認"""
    app = create_app()
    assert app is not None
    # Gradio Interfaceまたはgr.Blocksのインスタンスであることを確認
    assert hasattr(app, "launch")


@patch("transcription_tool.app.Transcriber")
@patch("transcription_tool.app.save_transcription_as_markdown")
def test_transcribe_audio_正常な処理(
    mock_save: Mock, mock_transcriber_class: Mock
) -> None:
    """transcribe_audioが正常に音声ファイルを処理することを確認"""
    # モックの設定
    mock_transcriber = Mock()
    mock_transcriber.transcribe.return_value = {
        "text": "テストの文字起こし結果",
        "language": "ja",
    }
    mock_transcriber_class.return_value = mock_transcriber
    mock_save.return_value = "/path/to/output.md"

    # テスト実行
    audio_path = "/test/audio.wav"
    model_name = "tiny"
    include_timestamps = False

    result = transcribe_audio(audio_path, model_name, include_timestamps)

    # 結果の確認
    assert "テストの文字起こし結果" in result
    assert "保存しました" in result
    mock_transcriber.transcribe.assert_called_once_with(audio_path)


def test_transcribe_audio_エラー処理() -> None:
    """transcribe_audioがエラーを適切に処理することを確認"""
    # 存在しないファイルでテスト
    result = transcribe_audio(None, "tiny", False)
    assert "エラー" in result or "選択" in result
