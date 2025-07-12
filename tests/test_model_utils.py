"""model_utilsモジュールのテスト."""

from typing import Callable, Optional
from unittest.mock import Mock, patch

from transcription_tool.model_utils import (
    ensure_model_downloaded,
    get_model_path,
    is_model_downloaded,
)


def test_get_model_path() -> None:
    """モデルパスが正しく生成されることを確認."""
    path = get_model_path("tiny")
    assert path.name == "tiny.pt"
    assert ".cache/whisper" in str(path)

    # large-v2の特殊ケース
    path = get_model_path("large")
    assert path.name == "large-v2.pt"

    path = get_model_path("large-v2")
    assert path.name == "large-v2.pt"


@patch("transcription_tool.model_utils.Path.exists")
def test_is_model_downloaded(mock_exists: Mock) -> None:
    """モデルのダウンロード状態が正しくチェックされることを確認."""
    mock_exists.return_value = True
    assert is_model_downloaded("tiny") is True

    mock_exists.return_value = False
    assert is_model_downloaded("tiny") is False


@patch("transcription_tool.model_utils.urllib.request.urlretrieve")
@patch("transcription_tool.model_utils.is_model_downloaded")
def test_ensure_model_downloaded_already_exists(
    mock_is_downloaded: Mock, mock_urlretrieve: Mock
) -> None:
    """既存のモデルはダウンロードされないことを確認."""
    mock_is_downloaded.return_value = True

    progress_calls = []

    def progress_callback(ratio: float, message: str) -> None:
        progress_calls.append((ratio, message))

    result = ensure_model_downloaded("tiny", progress_callback)

    assert result is False  # 新規ダウンロードではない
    assert len(progress_calls) == 1
    assert "既にダウンロード済み" in progress_calls[0][1]
    mock_urlretrieve.assert_not_called()


@patch("transcription_tool.model_utils.urllib.request.urlretrieve")
@patch("transcription_tool.model_utils.is_model_downloaded")
@patch("transcription_tool.model_utils.Path.rename")
def test_ensure_model_downloaded_new_download(
    mock_rename: Mock, mock_is_downloaded: Mock, mock_urlretrieve: Mock
) -> None:
    """新しいモデルがダウンロードされることを確認."""
    mock_is_downloaded.return_value = False

    progress_calls = []

    def progress_callback(ratio: float, message: str) -> None:
        progress_calls.append((ratio, message))

    # urlretrieveのコールバックをシミュレート
    def simulate_download(
        url: str, path: str, reporthook: Optional[Callable] = None
    ) -> None:
        if reporthook:
            # ダウンロード進捗をシミュレート
            reporthook(0, 1024, 10240)  # 10%
            reporthook(5, 1024, 10240)  # 50%
            reporthook(10, 1024, 10240)  # 100%

    mock_urlretrieve.side_effect = simulate_download

    result = ensure_model_downloaded("tiny", progress_callback)

    assert result is True  # 新規ダウンロード
    assert len(progress_calls) >= 3  # 開始、進捗、完了
    assert any("ダウンロード中" in call[1] for call in progress_calls)
    assert any("完了" in call[1] for call in progress_calls)
    mock_urlretrieve.assert_called_once()
