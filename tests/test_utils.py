"""utilsモジュールのテスト"""

from pathlib import Path

from transcription_tool.utils import save_transcription_as_markdown


def test_save_transcription_as_markdown_関数が存在する() -> None:
    """save_transcription_as_markdown関数が存在することを確認"""
    assert save_transcription_as_markdown is not None
    assert callable(save_transcription_as_markdown)


def test_save_transcription_基本的な保存ができる(tmp_path: Path) -> None:
    """基本的な文字起こし結果をMarkdownとして保存できることを確認"""
    # テストデータ
    transcription_result = {
        "text": "これはテストの文字起こし結果です。",
        "language": "ja",
    }
    audio_filename = "test_audio.wav"

    # 保存実行
    output_path = save_transcription_as_markdown(
        transcription_result, audio_filename, output_dir=tmp_path
    )

    # ファイルが作成されたことを確認
    assert output_path.exists()
    assert output_path.suffix == ".md"

    # ファイル内容の確認
    content = output_path.read_text(encoding="utf-8")
    assert "# 文字起こし結果" in content
    assert "test_audio.wav" in content
    assert "これはテストの文字起こし結果です。" in content


def test_save_transcription_タイムスタンプ付き保存ができる(tmp_path: Path) -> None:
    """タイムスタンプ付きの文字起こし結果を保存できることを確認"""
    # テストデータ（セグメント付き）
    transcription_result = {
        "text": "これはテストです。",
        "segments": [{"start": 0.0, "end": 2.5, "text": "これはテストです。"}],
    }
    audio_filename = "test_audio.wav"

    # 保存実行
    output_path = save_transcription_as_markdown(
        transcription_result,
        audio_filename,
        output_dir=tmp_path,
        include_timestamps=True,
    )

    # ファイル内容の確認
    content = output_path.read_text(encoding="utf-8")
    assert "[00:00 - 00:02]" in content or "[0:00 - 0:02]" in content
