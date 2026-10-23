# Dynamic Progress Bot

Discordのスラッシュコマンドで進捗を数え、進捗の数とバーを描いた画像を投稿するBot。画像の背景には、Unsplashから無作為に取得した写真を使う。

## 使い方

- `/start total:20`: 目標の数を20にして、進捗を0に戻す
- `/next`: 進捗を1つ進め、`3 / 20`のような進捗の数とバーを描いた画像を投稿する

## 必要なもの

- Python 3.12以上
- Discordのアプリケーション
- UnsplashのAccess Key: 無くても動作する。無い場合、画像の背景は単色になる

## セットアップ

1. 依存のライブラリをインストールする

   ```bash
   pip install -r requirements.txt
   ```

2. [Discord Developer Portal](https://discord.com/developers/applications)でアプリケーションを作成し、BotのTokenを取得する
3. OAuth2のURL GeneratorでScopesの`bot`と`applications.commands`、Bot Permissionsの`Send Messages`と`Attach Files`を選び、生成されたURLからBotをサーバーに招待する
4. Unsplashを使う場合は、[Unsplash Developers](https://unsplash.com/developers)でアプリケーションを作成し、Access Keyを取得する
5. `.env.example`を`.env`にコピーし、値を設定する

   | 変数 | 値 |
   | --- | --- |
   | `DISCORD_BOT_TOKEN` | BotのToken。必須 |
   | `IMAGE_API_KEY` | UnsplashのAccess Key |
   | `IMAGE_API_BASE_URL` | Unsplash APIのURL。既定値は`https://api.unsplash.com` |

6. repoのフォルダで起動する

   ```bash
   python main.py
   ```

   起動したフォルダの中の`progress.json`に進捗を、`bot.log`にログを保存する。

## 既知の制限

- 進捗はBot全体で1つだけ保存する。招待したすべてのサーバー・チャンネル・ユーザーが同じ進捗を共有し、誰でも`/start`で進捗を0に戻せる
- `/next`の1回で、背景とバーの模様の写真を取得するため、Unsplash APIを2回呼ぶ。Unsplashで作ったアプリケーションは、本番用の申請が通るまで、APIを1時間に50回までしか呼べない。写真を背景にできる`/next`は、1時間に25回まで。取得に失敗した写真の代わりには単色を使う
- 画像にUnsplashと撮影者の名前を表示しない。[Unsplash API Guidelines](https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines)は、写真を表示するときにUnsplashと撮影者の名前を示すことを求めている
- 進捗の数を描くフォントは、`assets/fonts/NotoSansJP-Regular.ttf`、Windowsの`msgothic.ttc`、`arial.ttf`の順に探す。どれも無いと、Pillowの既定のフォントで小さく描く。Windows以外では、フォントのファイルを`assets/fonts/NotoSansJP-Regular.ttf`に置く。`assets/`はrepoに含まれない

## ライセンス

[MIT](LICENSE)
