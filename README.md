# Dynamic Progress Bot

Discord で進捗を視覚的に管理するための Bot です。ユーザーがコマンドを実行するたびに、進捗状況を表現したユニークな画像を生成・投稿します。

## 機能

-   `/start [総数]` - 新しいタスクを開始
-   `/next` - 進捗を 1 つ進める（画像付き）

## セットアップ

### 1. 必要なライブラリをインストール

```bash
pip install -r requirements.txt
```

### 2. Discord Bot を作成

1. [Discord Developer Portal](https://discord.com/developers/applications)にアクセス
2. 新しいアプリケーションを作成
3. Bot セクションでトークンを取得
4. OAuth2 > URL Generator で以下の権限を設定：
    - Scopes: `bot` と `applications.commands`
    - Bot Permissions: 
      - `Send Messages`
      - `Use Slash Commands`
      - `Attach Files`

### 3. 画像 API の設定（オプション）

Unsplash API を使用する場合：

1. [Unsplash Developers](https://unsplash.com/developers)でアカウント作成
2. 新しいアプリケーションを作成して Access Key を取得

### 4. 環境変数の設定

`.env.example`を`.env`にコピーして、必要な値を設定：

```bash
cp .env.example .env
```

`.env`ファイルを編集：

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
IMAGE_API_KEY=your_unsplash_access_key_here
IMAGE_API_BASE_URL=https://api.unsplash.com
```

### 5. Bot の起動

#### 簡単起動（推奨）
- **start_bot.bat** をダブルクリック

#### コマンドライン起動
```bash
python main.py
```

## ファイル構成

```
dynamicProgressBot/
├── main.py              # Botのメイン処理
├── data_manager.py      # データ管理（progress.json）
├── image_generator.py   # 画像生成ロジック
├── requirements.txt     # 依存ライブラリ
├── .env                 # 環境変数（作成する）
├── .env.example         # 環境変数のテンプレート
├── progress.json        # 進捗データ（自動生成）
└── assets/
    └── fonts/           # フォントファイル（オプション）
```

## 使用方法

1. Bot を Discord サーバーに招待
2. `/start 20` - 20 個のタスクを開始
3. `/next` - 進捗を 1 つ進める（画像が生成される）

## 注意事項

-   画像 API（Unsplash）のキーが設定されていない場合は、単色の背景画像が使用されます
-   進捗データは`progress.json`に保存されます
-   一度に管理できるタスクは 1 つのみです

## トラブルシューティング

### フォントエラーが発生する場合

日本語フォントファイルを`assets/fonts/`に配置してください。
推奨フォント：

-   Noto Sans JP
-   M+ FONTS

### 画像生成エラーが発生する場合

1. Unsplash API のキーが正しく設定されているか確認
2. インターネット接続を確認
3. API の利用制限に達していないか確認
