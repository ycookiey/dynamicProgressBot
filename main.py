import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
import data_manager
import image_generator

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} がログインしました！')
    logger.info(f'Bot ID: {bot.user.id}')
    
    try:
        synced = await bot.tree.sync()
        logger.info(f'{len(synced)} 個のスラッシュコマンドを同期しました')
        for cmd in synced:
            logger.info(f'  - /{cmd.name}: {cmd.description}')
    except Exception as e:
        logger.error(f'スラッシュコマンドの同期に失敗しました: {e}')

@bot.tree.command(name="start", description="新しいタスクを開始します")
async def start_task(interaction: discord.Interaction, total: int):
    logger.info(f"start コマンドが呼び出されました。ユーザー: {interaction.user}, 総数: {total}")
    
    if total <= 0:
        logger.warning(f"無効な総数が指定されました: {total}")
        await interaction.response.send_message("目標値は1以上の整数を入力してください。", ephemeral=True)
        return
    
    data_manager.update_progress(total=total, current=0)
    logger.info(f"新しいタスクを開始しました。目標: {total}")
    
    await interaction.response.send_message(f"新しいタスクを開始しました。目標: {total}")

@bot.tree.command(name="next", description="進捗を1つ進めます")
async def next_progress(interaction: discord.Interaction):
    logger.info(f"next コマンドが呼び出されました。ユーザー: {interaction.user}")
    
    current_data = data_manager.get_current_progress()
    logger.info(f"現在の進捗データ: {current_data}")
    
    if 'total' not in current_data or 'current' not in current_data:
        logger.warning("開始されているタスクがありません")
        await interaction.response.send_message("開始されているタスクがありません。/start で新しいタスクを開始してください。", ephemeral=True)
        return
    
    if current_data['current'] >= current_data['total']:
        logger.warning("タスクは既に完了しています")
        await interaction.response.send_message("タスクは既に完了しています。/start で新しいタスクを開始してください。", ephemeral=True)
        return
    
    success = data_manager.increment_progress()
    if not success:
        logger.error("進捗の更新に失敗しました")
        await interaction.response.send_message("進捗の更新に失敗しました。", ephemeral=True)
        return
    
    updated_data = data_manager.get_current_progress()
    current = updated_data['current']
    total = updated_data['total']
    logger.info(f"更新後の進捗: {current}/{total}")
    
    # Discordは3秒以内の最初の応答を求め、画像の生成は3秒を超えることがあるため、先に応答を保留する
    await interaction.response.defer()
    
    try:
        logger.info("画像生成を開始します")
        image_file = image_generator.generate_image(current, total)
        
        await interaction.followup.send(file=image_file)
        logger.info("画像投稿完了")
        
    except Exception as e:
        logger.error(f"画像生成エラー: {e}")
        await interaction.followup.send("画像生成に失敗しました")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    logger.error(f"コマンドエラーが発生しました: {error}")

@bot.event
async def on_application_command_error(interaction, error):
    logger.error(f"スラッシュコマンドエラー: {error}")
    if not interaction.response.is_done():
        await interaction.response.send_message("コマンドの実行中にエラーが発生しました。", ephemeral=True)

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("DISCORD_BOT_TOKEN が設定されていません。.env ファイルを確認してください。")
        exit(1)
    
    logger.info("Botを起動中...")
    bot.run(token)