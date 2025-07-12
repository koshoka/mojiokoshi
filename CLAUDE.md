# transcription-tool - Python アプリケーション

## プロジェクト概要
[Pythonアプリケーションの目的と概要]

## 技術スタック
- **言語**: Python 3.10+
- **フレームワーク**: FastAPI / Django / Flask
- **非同期処理**: asyncio / aiohttp
- **データベース**: PostgreSQL + SQLAlchemy / MongoDB + PyMongo
- **タスクキュー**: Celery + Redis
- **テスト**: pytest + pytest-asyncio
- **Linter/Formatter**: Ruff / Black + isort
- **型チェック**: mypy

## 開発環境セットアップ
```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows

# 依存関係のインストール
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 開発用

# 開発サーバーの起動
python main.py
# または
uvicorn app.main:app --reload  # FastAPI

# テスト実行
pytest
pytest --cov=app  # カバレッジ付き

# Lint実行
ruff check .
ruff format .

# 型チェック
mypy .
```

## プロジェクト構造
```
project-name/
├── app/                  # アプリケーションコード
│   ├── __init__.py
│   ├── main.py          # エントリーポイント
│   ├── api/             # APIエンドポイント
│   ├── core/            # 設定、セキュリティ
│   ├── models/          # データモデル
│   ├── schemas/         # Pydanticスキーマ
│   ├── services/        # ビジネスロジック
│   └── utils/           # ユーティリティ
├── tests/               # テストコード
├── scripts/             # スクリプト
├── requirements.txt     # 本番用依存関係
├── requirements-dev.txt # 開発用依存関係
├── .env.example        # 環境変数サンプル
├── pyproject.toml      # プロジェクト設定
└── Dockerfile          # Docker設定
```

## 重要なコマンド

### データベースマイグレーション
- **実行コマンド**: `alembic upgrade head`
- **説明**: データベーススキーマを最新に更新

### 新しいマイグレーション作成
- **実行コマンド**: `alembic revision --autogenerate -m "description"`
- **説明**: モデルの変更から自動的にマイグレーションを生成

### 依存関係の更新
- **実行コマンド**: `pip-compile requirements.in`
- **説明**: requirements.txt を更新（pip-tools使用時）

## コーディング規約

### 基本的なスタイル
```python
# app/services/user_service.py
from typing import Optional, List
from app.models import User
from app.schemas import UserCreate, UserUpdate

class UserService:
    """ユーザー関連のビジネスロジック"""
    
    async def create_user(self, user_data: UserCreate) -> User:
        """新しいユーザーを作成"""
        # 実装
        pass
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """IDでユーザーを取得"""
        # 実装
        pass
```

### 型ヒント
- すべての関数に型ヒントを付ける
- 複雑な型は typing モジュールを使用
- Pydantic モデルで API の入出力を定義

### エラーハンドリング
```python
class UserNotFoundError(Exception):
    """ユーザーが見つからない場合のエラー"""
    pass

try:
    user = await get_user(user_id)
except UserNotFoundError:
    raise HTTPException(status_code=404, detail="User not found")
```

## 環境変数
```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
DEBUG=True
```

## テスト

### テストの実行
```bash
# 全テスト実行
pytest

# 特定のテストファイル
pytest tests/test_users.py

# カバレッジレポート
pytest --cov=app --cov-report=html
```

### テストの書き方
```python
# tests/test_user_service.py
import pytest
from app.services import UserService

@pytest.mark.asyncio
async def test_create_user():
    service = UserService()
    user = await service.create_user(...)
    assert user.email == "test@example.com"
```

## パフォーマンス最適化

### 非同期処理
- I/O バウンドなタスクは async/await を使用
- CPU バウンドなタスクは multiprocessing を検討

### キャッシング
- Redis を使用したキャッシング
- functools.lru_cache でメモリキャッシュ

## デプロイ設定

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## トラブルシューティング

### よくあるエラー
1. **ImportError**
   - 原因: PYTHONPATH が正しく設定されていない
   - 解決: プロジェクトルートから実行

2. **asyncio エラー**
   - 原因: イベントループの競合
   - 解決: pytest-asyncio を使用

## 参考リンク
- [Python Documentation](https://docs.python.org/3/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)