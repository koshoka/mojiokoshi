"""デモンストレーション用スクリプト."""

import time
from pathlib import Path

from transcription_tool.transcriber import Transcriber
from transcription_tool.utils import save_transcription_as_markdown


def demo_transcription() -> None:
    """文字起こし機能のデモンストレーション."""
    print("🎙️  音声文字起こしツール - デモンストレーション")
    print("=" * 50)

    # テスト用音声ファイルの確認
    test_audio = Path("tests/test_data/test_audio.wav")
    if not test_audio.exists():
        print("❌ テスト用音声ファイルが見つかりません")
        print("   tests/test_data/test_audio.wav を作成してください")
        return

    print(f"✅ 音声ファイル: {test_audio}")
    print(f"   サイズ: {test_audio.stat().st_size / 1024:.1f} KB")

    # モデルの選択
    model_name = "tiny"  # デモ用に軽量モデルを使用
    print(f"\n📦 使用モデル: {model_name}")

    # 文字起こし実行
    print("\n⏳ 文字起こしを開始します...")
    start_time = time.time()

    try:
        # Transcriberのインスタンス化
        print("   - モデルをロード中...")
        transcriber = Transcriber(model_name=model_name)

        # 文字起こし
        print("   - 音声を処理中...")
        result = transcriber.transcribe(test_audio)

        elapsed_time = time.time() - start_time
        print(f"\n✅ 文字起こし完了！（処理時間: {elapsed_time:.1f}秒）")

        # 結果の表示
        print("\n📝 文字起こし結果:")
        print("-" * 50)
        print(result["text"])
        print("-" * 50)

        # 検出された言語
        if "language" in result:
            print(f"\n🌐 検出言語: {result['language']}")

        # Markdownファイルとして保存
        print("\n💾 結果を保存中...")
        output_path = save_transcription_as_markdown(
            result, test_audio.name, include_timestamps=True
        )
        print(f"✅ 保存完了: {output_path}")

        # セグメント情報の表示（タイムスタンプ付き）
        if "segments" in result and result["segments"]:
            print(f"\n🎯 セグメント数: {len(result['segments'])}")
            print("\n最初の3セグメント:")
            for segment in result["segments"][:3]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                print(f"  [{start:.1f}s - {end:.1f}s] {text}")

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    demo_transcription()
