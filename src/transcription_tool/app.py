"""Gradioを使用した文字起こしツールのWebインターフェース."""

import time
from pathlib import Path
from typing import Optional

import gradio as gr

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
        if progress:
            progress(0.1, desc="モデルをロード中...")
        transcriber = Transcriber(model_name=model_name)

        # 文字起こし実行
        if progress:
            progress(0.3, desc="音声を処理中...")
        start_time = time.time()
        result = transcriber.transcribe(audio_file)
        elapsed_time = time.time() - start_time

        # 結果を保存
        if progress:
            progress(0.8, desc="結果を保存中...")
        audio_filename = Path(audio_file).name
        output_path = save_transcription_as_markdown(
            result, audio_filename, include_timestamps=include_timestamps
        )

        # 結果の整形
        if progress:
            progress(1.0, desc="完了!")
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

    except Exception as e:
        return f"❌ エラーが発生しました: {str(e)}"


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
                        choices=[
                            "tiny",
                            "base",
                            "small",
                            "medium",
                            "large",
                            "large-v2",
                            "large-v3",
                        ],
                        value="large-v3",
                        label="Whisperモデル",
                        info="大きいモデルほど精度が高いですが、処理時間も長くなります",
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

            💡 **ヒント**: 日本語音声には`large-v3`モデルがおすすめです
            """
        )

        # イベントハンドラの設定
        transcribe_button.click(
            fn=transcribe_audio,
            inputs=[audio_input, model_dropdown, timestamp_checkbox],
            outputs=result_output,
            show_progress="full",
        )

    return app


def main() -> None:
    """メインエントリーポイント."""
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )


if __name__ == "__main__":
    main()
