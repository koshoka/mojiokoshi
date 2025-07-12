# Transcription Tool

OpenAI Whisperを使用した音声文字起こしツール

## 機能

- 📱 使いやすいWebベースのGUI（Gradio使用）
- 🎯 Whisper large-v3モデルによる高精度な文字起こし
- 🇯🇵 日本語音声に最適化
- 📝 自動的にMarkdown形式で保存
- ⏱️ タイムスタンプ付き出力オプション
- 🎵 複数の音声フォーマットに対応（WAV, MP3, MP4, M4A, FLAC, OGG, OPUS）
- 📊 処理進捗のリアルタイム表示

## インストール

### 開発環境のセットアップ

```bash
# リポジトリのクローン
git clone https://github.com/koshoka/mojiokoshi.git
cd mojiokoshi

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

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

### GUIアプリケーションの起動

```bash
# アプリケーションの起動
make run

# または直接実行
python -m transcription_tool
```

ブラウザで `http://localhost:7860` を開いてアクセスします。

### 使い方

1. **音声ファイルをアップロード**
   - ドラッグ&ドロップまたはクリックしてファイルを選択

2. **設定を選択**
   - Whisperモデル：精度と速度のバランスを選択
     - `tiny`/`base`：高速だが精度は低め
     - `small`/`medium`：バランス型
     - `large-v3`：最高精度（日本語推奨）
   - タイムスタンプ：必要に応じてチェック

3. **文字起こし開始**
   - 「🚀 文字起こしを開始」ボタンをクリック
   - 処理の進捗がリアルタイムで表示されます

4. **結果の確認**
   - 文字起こし結果が画面に表示
   - 自動的に`transcriptions`フォルダにMarkdownファイルとして保存

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
