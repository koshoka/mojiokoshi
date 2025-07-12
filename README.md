# Transcription Tool

OpenAI Whisperを使用した音声文字起こしツール

## 機能

- GUIでファイル選択
- Whisper large-v3モデルによる高精度な文字起こし
- 日本語対応
- 自動的にMarkdown形式で保存
- 複数の音声フォーマットに対応（WAV, MP3, MP4, M4A, FLAC, OGG, OPUS）

## インストール

### 開発環境のセットアップ

```bash
# 依存関係のインストール
make install-dev

# または直接pip使用
pip install -e ".[dev]"
```

### 本番環境のインストール

```bash
make install

# または直接pip使用
pip install -e .
```

## 使用方法

```bash
# アプリケーションの起動
make run

# または直接実行
python -m transcription_tool
```

## 開発

### コード品質チェック

```bash
# リンターの実行
make lint

# コードフォーマット
make format

# 型チェック
make type-check

# テストの実行
make test
```

### プロジェクト構造

```
transcription-tool/
├── src/
│   └── transcription_tool/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py           # Gradioアプリケーション
│       ├── transcriber.py   # Whisper処理
│       └── utils.py         # ユーティリティ関数
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_transcriber.py
│   └── test_utils.py
├── docs/
├── scripts/
├── pyproject.toml
├── Makefile
├── .gitignore
└── README.md
```

## ライセンス

MIT License