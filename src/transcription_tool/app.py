"""Gradioを使用した文字起こしツールのWebインターフェース."""

import time
from pathlib import Path
from typing import Optional

import gradio as gr

from transcription_tool.file_manager import (
    get_file_full_path,
    list_transcription_files,
    read_transcription_file,
)
from transcription_tool.model_utils import MODEL_SIZES, is_model_downloaded
from transcription_tool.transcriber import Transcriber
from transcription_tool.utils import save_transcription_as_markdown


def transcribe_audio(
    audio_file: Optional[str],
    model_name: str,
    include_timestamps: bool,
    progress: Optional[gr.Progress] = None,
) -> str:
    """音声ファイルを文字起こしして結果を返す.

    Args:
    ----
        audio_file: アップロードされた音声ファイルのパス
        model_name: 使用するWhisperモデル名
        include_timestamps: タイムスタンプを含めるかどうか
        progress: Gradioのプログレストラッカー

    Returns:
    -------
        処理結果のメッセージ
    """
    if audio_file is None:
        return "❌ 音声ファイルを選択してください。"

    try:
        # プログレス表示
        audio_path = Path(audio_file)
        file_size_mb = audio_path.stat().st_size / (1024 * 1024)

        if progress:
            progress(0.05, desc=f"音声ファイルを確認中... ({file_size_mb:.1f} MB)")

        # モデルのダウンロード状況をチェック
        if not is_model_downloaded(model_name):
            model_size_mb = MODEL_SIZES.get(model_name, 0)
            if progress:
                progress(
                    0.1,
                    desc=(
                        f"{model_name}モデル ({model_size_mb}MB) "
                        "のダウンロードが必要です..."
                    ),
                )

        # Transcriberインスタンスを作成
        transcriber = Transcriber(model_name=model_name)

        # 進捗表示を更新する変数
        current_progress = 0.1

        # 進捗コールバック関数（ダウンロード進捗も含む）
        def model_progress(message: str) -> None:
            nonlocal current_progress
            if progress:
                # ダウンロード進捗の場合
                if "ダウンロード中:" in message:
                    # パーセンテージを抽出
                    try:
                        percent_str = message.split("(")[1].split("%")[0]
                        percent = float(percent_str) / 100.0
                        # 0.1から0.4の範囲でマッピング
                        current_progress = 0.1 + (percent * 0.3)
                    except Exception:
                        current_progress = min(current_progress + 0.05, 0.4)
                elif "メモリにロード中" in message:
                    current_progress = 0.45
                elif "ロード完了" in message:
                    current_progress = 0.5
                else:
                    current_progress = min(current_progress + 0.05, 0.5)

                progress(current_progress, desc=message)

        # 文字起こし実行
        start_time = time.time()

        # 音声処理の進捗コールバック
        def transcription_progress(message: str) -> None:
            nonlocal current_progress
            if progress:
                if "音声ファイルを解析中" in message:
                    current_progress = 0.6
                else:
                    current_progress = min(current_progress + 0.05, 0.8)
                progress(current_progress, desc=message)

        # モデルの準備と文字起こし実行
        # model_progressコールバックでモデルのダウンロード/ロード進捗を表示
        result = transcriber.transcribe(
            audio_file,
            progress_callback=lambda msg: model_progress(msg)
            if current_progress < 0.5
            else transcription_progress(msg),
        )
        elapsed_time = time.time() - start_time

        # 結果を保存
        if progress:
            progress(0.8, desc="文字起こし完了！結果を保存中...")
        audio_filename = Path(audio_file).name
        output_path = save_transcription_as_markdown(
            result, audio_filename, include_timestamps=include_timestamps
        )

        # 結果の整形
        if progress:
            progress(1.0, desc="すべての処理が完了しました！")
        return f"""✅ 文字起こしが完了しました！

**処理時間**: {elapsed_time:.1f}秒
**検出言語**: {result.get('language', '不明')}
**保存場所**: {output_path}

---

**文字起こし結果**:
{result['text']}

---

📝 Markdownファイルを`{output_path}`に保存しました。
"""

    except FileNotFoundError as e:
        return f"❌ ファイルエラー: {str(e)}"
    except ValueError as e:
        return f"❌ フォーマットエラー: {str(e)}"
    except Exception as e:
        import traceback

        error_details = traceback.format_exc()
        return f"""❌ エラーが発生しました: {str(e)}

詳細情報:
```
{error_details}
```

ヒント:
- 初回実行時はモデルのダウンロードに時間がかかります（数分〜10分程度）
- メモリ不足の場合は、より小さいモデル（tiny, base）を試してください
- 音声ファイルが破損していないか確認してください
"""


def get_model_choices() -> list[tuple[str, str]]:
    """モデル選択肢を生成（ダウンロード状況付き）."""
    choices = []
    for name, label in [
        ("tiny", "最速・低精度"),
        ("base", "高速・やや低精度"),
        ("small", "バランス型"),
        ("medium", "高精度"),
        ("large", "最高精度"),
        ("large-v2", "最高精度v2"),
        ("large-v3", "最高精度v3・日本語推奨"),
    ]:
        size = MODEL_SIZES.get(name, 0)
        status = "✓" if is_model_downloaded(name) else "↓"
        choices.append((f"{name} ({size}MB) - {label} {status}", name))
    return choices


def create_app() -> gr.Blocks:
    """Gradioアプリケーションを作成する."""
    # カスタムCSS（UIデザインの法則を適用）
    custom_css = """
    .container {
        max-width: 800px;
        margin: auto;
    }
    /* 8ポイントグリッドでスペーシング */
    .gr-button {
        min-height: 48px !important;
        font-size: 16px !important;
        margin: 8px 0 !important;
    }
    /* プライマリボタンの強調 */
    .gr-button-primary {
        background-color: #2563eb !important;
        color: white !important;
        font-weight: 600 !important;
    }
    /* 高コントラスト比の確保 */
    .gr-box {
        border: 1px solid #d1d5db !important;
        padding: 16px !important;
        margin: 8px 0 !important;
    }
    /* ドロップダウンのカーソル修正 */
    .gr-dropdown {
        cursor: pointer !important;
    }
    .gr-dropdown svg {
        cursor: pointer !important;
    }
    /* ドロップダウン全体をクリッカブルに */
    select, .gr-input-dropdown {
        cursor: pointer !important;
    }
    """

    with gr.Blocks(
        title="音声文字起こしツール",
        theme=gr.themes.Soft(),
        css=custom_css,
    ) as app:
        # ヘッダー
        gr.Markdown(
            """
            # 🎙️ 音声文字起こしツール

            OpenAI Whisperを使用して、音声ファイルを高精度で文字起こしします。
            対応フォーマット: WAV, MP3, MP4, M4A, FLAC, OGG, OPUS
            """
        )

        # タブで機能を分ける
        with gr.Tabs():
            # 文字起こしタブ
            with gr.Tab("文字起こし"):
                with gr.Row():
                    with gr.Column(scale=1):
                        # ファイルアップロード部（大きなターゲットエリア）
                        audio_input = gr.Audio(
                            label="音声ファイルをドラッグ&ドロップまたはクリックして選択",
                            type="filepath",
                            elem_classes=["gr-box"],
                        )

                        # オプション設定（常に表示）
                        with gr.Group():
                            gr.Markdown("### ⚙️ 設定")
                            model_dropdown = gr.Dropdown(
                                choices=get_model_choices(),
                                value="large-v3",
                                label="Whisperモデル",
                                info="✓=ダウンロード済み ↓=ダウンロード必要",
                            )

                            timestamp_checkbox = gr.Checkbox(
                                label="タイムスタンプを含める",
                                value=False,
                                info="文字起こし結果に時間情報を追加します",
                            )

                        # プライマリボタン（単一で目立つ）
                        transcribe_button = gr.Button(
                            "🚀 文字起こしを開始",
                            variant="primary",
                            elem_classes=["gr-button-primary"],
                        )

                    with gr.Column(scale=2):
                        # 結果表示エリア
                        result_output = gr.Textbox(
                            label="処理結果",
                            lines=20,
                            max_lines=30,
                            show_copy_button=True,
                            elem_classes=["gr-box"],
                        )

                # 使い方の説明（下部に配置）
                gr.Markdown(
                    """
                    ---
                    ### 📖 使い方
                    1. 音声ファイルを選択またはドラッグ&ドロップ
                    2. 必要に応じてモデルとオプションを選択
                    3. 「文字起こしを開始」ボタンをクリック
                    4. 結果は自動的にMarkdownファイルとして保存されます

                    💡 **ヒント**:
                    - 日本語音声には`large-v3`モデルがおすすめです
                    - モデル選択欄の ✓ はダウンロード済み、
                      ↓ はダウンロードが必要なモデルです
                    - 初回実行時は選択したモデルのダウンロードが必要です
                      （サイズ: tiny=39MB〜large-v3=1.5GB）
                    - ダウンロード進捗は画面上部のプログレスバーに表示されます

                    ⚠️ **注意事項**:
                    - 大きなファイルの処理には時間がかかります
                    - メモリ不足の場合は、より小さいモデルをお試しください
                    """
                )

                # 文字起こし実行と同時にドロップダウンを更新
                def transcribe_and_update(
                    audio_file: Optional[str],
                    model_name: str,
                    include_timestamps: bool,
                ) -> tuple[str, dict]:
                    result = transcribe_audio(
                        audio_file, model_name, include_timestamps
                    )
                    # モデルリストを更新
                    # （ダウンロード済みステータスが変わる可能性があるため）
                    updated_choices = gr.update(
                        choices=get_model_choices(), value=model_name
                    )
                    return result, updated_choices

                # イベントハンドラの設定
                transcribe_button.click(
                    fn=transcribe_and_update,
                    inputs=[audio_input, model_dropdown, timestamp_checkbox],
                    outputs=[result_output, model_dropdown],
                    show_progress="full",
                )

            # 過去の結果タブ
            with gr.Tab("過去の結果"):
                gr.Markdown(
                    """
                    ### 📁 文字起こし結果一覧

                    過去に文字起こしした結果ファイルを確認できます。
                    """
                )

                with gr.Row():
                    # 更新ボタン
                    refresh_button = gr.Button("🔄 一覧を更新", scale=1)

                # ファイル一覧表示
                file_list = gr.DataFrame(
                    headers=["ファイル名", "作成日時", "サイズ"],
                    interactive=False,
                    wrap=True,
                )

                with gr.Row():
                    with gr.Column(scale=1):
                        # ファイル選択
                        selected_file = gr.Dropdown(
                            label="ファイルを選択",
                            choices=[],
                            interactive=True,
                        )

                        # ファイルパス表示
                        file_path_display = gr.Textbox(
                            label="ファイルパス",
                            interactive=False,
                            show_copy_button=True,
                        )

                    with gr.Column(scale=2):
                        # ファイル内容プレビュー
                        file_preview = gr.Textbox(
                            label="ファイル内容",
                            lines=20,
                            max_lines=30,
                            interactive=False,
                            show_copy_button=True,
                        )

                # 初期表示とイベントハンドラ
                def update_file_list() -> tuple[list[list[str]], dict, str, str]:
                    """ファイル一覧を更新."""
                    files = list_transcription_files()
                    # DataFrameに表示するデータ（タイムスタンプを除く）
                    display_data = [[f[0], f[1], f[2]] for f in files]
                    # ドロップダウンの選択肢
                    file_choices = [f[0] for f in files]
                    return (
                        display_data,
                        gr.update(choices=file_choices, value=None),
                        "",
                        "",
                    )

                def on_file_selected(filename: Optional[str]) -> tuple[str, str]:
                    """ファイル選択時の処理"""
                    if not filename:
                        return "", ""

                    # ファイルパスを取得
                    file_path = get_file_full_path(filename)

                    # ファイル内容を読み込む
                    content = read_transcription_file(filename)
                    if content is None:
                        content = "ファイルが見つかりません。"

                    return file_path, content

                # 初期表示
                app.load(
                    fn=update_file_list,
                    outputs=[file_list, selected_file, file_path_display, file_preview],
                )

                # イベントハンドラの設定
                refresh_button.click(
                    fn=update_file_list,
                    outputs=[file_list, selected_file, file_path_display, file_preview],
                )

                selected_file.change(
                    fn=on_file_selected,
                    inputs=[selected_file],
                    outputs=[file_path_display, file_preview],
                )

    return app


def main() -> None:
    """メインエントリーポイント."""
    app = create_app()
    # queueを有効にして非同期処理を可能にする
    app.queue(max_size=10, api_open=False).launch(
        server_name="0.0.0.0",
        server_port=7862,  # ポート変更
        share=False,
        show_error=True,
        inbrowser=False,  # 自動的にブラウザを開かない
    )


if __name__ == "__main__":
    main()
