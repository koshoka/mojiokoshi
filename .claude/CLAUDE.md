# CLAUDE.md - Transcription Tool プロジェクト

このファイルは文字起こしツールプロジェクト固有の指示を含みます。

## プロジェクト概要

OpenAI Whisperを使用した音声文字起こしツール。GUIでファイルを選択し、自動的にMarkdown形式で文字起こし結果を保存します。

## 技術スタック

- Python 3.9+
- OpenAI Whisper (large-v3モデル)
- Gradio (GUI)
- pytest (テスト)
- ruff (リンター/フォーマッター)
- mypy (型チェック)

## 開発方針

### TDD実践
- 新機能追加時は必ずテストファースト
- t-wadaのTDDサイクルに従う：
  1. 失敗するテストを書く
  2. テストを通す最小限の実装
  3. リファクタリング

### コード品質
- 型ヒントは必須
- docstringは関数・クラスに必須
- ruffとmypyでのチェックをパス

### ディレクトリ構造
- src/transcription_tool/: メインコード
- tests/: テストコード
- transcriptions/: 出力ファイル（gitignore）

## 実装予定機能

1. 基本的な文字起こし機能
   - ファイル選択GUI
   - Whisper処理
   - Markdown出力

2. 拡張機能
   - バッチ処理
   - 進捗表示
   - 複数言語対応
   - タイムスタンプ付き出力

## 注意事項

- 音声ファイルはgitにコミットしない
- 出力ファイルもgitにコミットしない
- APIキーなどの機密情報は環境変数で管理