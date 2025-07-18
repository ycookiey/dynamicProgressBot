import requests
import random
import io
import os
from PIL import Image, ImageDraw, ImageFont
import discord
from dotenv import load_dotenv

load_dotenv()

# 背景用キーワードリスト
KEYWORDS = ["cyberpunk", "futuristic", "neon lights", "dark aesthetic", "sci-fi", "digital art", "synthwave", "blade runner", "matrix", "robot", "artificial intelligence", "cyber", "gaming", "esports", "dark city", "neon cityscape", "tech noir", "hologram", "virtual reality", "metaverse"]

# プログレスバー用キーワードリスト（模様系）
PATTERN_KEYWORDS = ["abstract pattern", "geometric pattern", "circuit pattern", "hexagon pattern", "digital pattern", "neon pattern", "grid pattern", "wave pattern", "stripe pattern", "tech pattern", "mosaic pattern", "fractal pattern", "binary pattern", "code pattern", "matrix pattern"]

# 画像API設定
IMAGE_API_KEY = os.getenv("IMAGE_API_KEY")
IMAGE_API_BASE_URL = os.getenv("IMAGE_API_BASE_URL", "https://api.unsplash.com")

def get_random_image(keywords_list=None, width=1000, height=400) -> bytes:
    """
    外部APIから背景画像を取得する。
    """
    if keywords_list is None:
        keywords_list = KEYWORDS
    
    keyword = random.choice(keywords_list)
    
    try:
        # Unsplash APIを使用した例
        url = f"{IMAGE_API_BASE_URL}/photos/random"
        headers = {
            "Authorization": f"Client-ID {IMAGE_API_KEY}"
        }
        params = {
            "query": keyword,
            "orientation": "landscape",
            "w": width,
            "h": height
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        image_data = response.json()
        image_url = image_data["urls"]["regular"]
        
        # 画像をダウンロード
        image_response = requests.get(image_url, timeout=10)
        image_response.raise_for_status()
        
        return image_response.content
        
    except Exception as e:
        print(f"画像の取得に失敗しました: {e}")
        # フォールバック: 単色の背景画像を生成
        return create_fallback_image(width, height)

def create_fallback_image(width=1000, height=400) -> bytes:
    """
    フォールバック用の単色背景画像を生成する。
    """
    image = Image.new('RGB', (width, height), color=(30, 30, 50))
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.getvalue()

def crop_to_aspect_ratio(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """
    画像を指定されたアスペクト比でクロッピングする
    """
    original_width, original_height = image.size
    target_ratio = target_width / target_height
    original_ratio = original_width / original_height
    
    if original_ratio > target_ratio:
        # 元画像が横長すぎる場合、横を切る
        new_width = int(original_height * target_ratio)
        left = (original_width - new_width) // 2
        image = image.crop((left, 0, left + new_width, original_height))
    elif original_ratio < target_ratio:
        # 元画像が縦長すぎる場合、縦を切る
        new_height = int(original_width / target_ratio)
        top = (original_height - new_height) // 2
        image = image.crop((0, top, original_width, top + new_height))
    
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)

def get_font(size: int = 24) -> ImageFont.FreeTypeFont:
    """
    フォントを取得する。
    """
    font_paths = [
        "assets/fonts/NotoSansJP-Regular.ttf",
        "C:/Windows/Fonts/msgothic.ttc",
        "C:/Windows/Fonts/arial.ttf"
    ]
    
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except:
            continue
    
    # フォールバック: デフォルトフォント
    return ImageFont.load_default()

def create_progress_bar_image(width: int, height: int, progress_ratio: float) -> Image.Image:
    """
    プログレスバー用の画像を生成する（模様系画像を使用）
    """
    # 模様系の背景画像を取得
    bar_image_data = get_random_image(PATTERN_KEYWORDS, width * 2, height * 2)
    bar_image = Image.open(io.BytesIO(bar_image_data))
    
    # アスペクト比を維持してクロッピング
    bar_image = crop_to_aspect_ratio(bar_image, width, height)
    
    # 進捗部分のマスクを作成
    mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    progress_width = int(width * progress_ratio)
    if progress_width > 0:
        mask_draw.rectangle([0, 0, progress_width, height], fill=255)
    
    # 進捗部分だけを切り取り
    progress_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    progress_image.paste(bar_image, mask=mask)
    
    # ネオン効果を追加
    from PIL import ImageFilter
    glow = progress_image.filter(ImageFilter.GaussianBlur(radius=3))
    
    # 最終的な進捗バー画像
    final_bar = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    final_bar = Image.alpha_composite(final_bar, glow)
    final_bar = Image.alpha_composite(final_bar, progress_image)
    
    return final_bar

def generate_image(current: int, total: int) -> discord.File:
    """
    進捗情報を含む画像を生成し、discord.Fileオブジェクトを返す。
    """
    # 新しい画像サイズ（横長）
    image_width = 1000
    image_height = 400
    
    # 背景画像を取得
    image_data = get_random_image(KEYWORDS, image_width, image_height)
    
    # 画像を開く
    image = Image.open(io.BytesIO(image_data))
    
    # アスペクト比を維持してクロッピング
    image = crop_to_aspect_ratio(image, image_width, image_height)
    
    # 描画用のオブジェクトを作成
    draw = ImageDraw.Draw(image)
    
    # 進捗率を計算
    progress_ratio = current / total if total > 0 else 0
    
    # フォントを取得
    large_font = get_font(48)
    
    # 暗いオーバーレイを追加
    overlay = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 160))
    image = Image.alpha_composite(image.convert('RGBA'), overlay)
    draw = ImageDraw.Draw(image)
    
    # 進捗数値を中央に大きく表示
    progress_text = f"{current} / {total}"
    progress_bbox = draw.textbbox((0, 0), progress_text, font=large_font)
    progress_width = progress_bbox[2] - progress_bbox[0]
    progress_x = (image_width - progress_width) // 2
    
    # テキストに縁取り効果
    for adj in range(-2, 3):
        for adj2 in range(-2, 3):
            draw.text((progress_x + adj, 120 + adj2), progress_text, fill=(0, 0, 0), font=large_font)
    draw.text((progress_x, 120), progress_text, fill=(255, 255, 255), font=large_font)
    
    # 画像を使用したプログレスバー
    bar_width = 700
    bar_height = 40
    bar_x = (image_width - bar_width) // 2
    bar_y = 220
    
    # バーの枠（ネオン効果）
    for i in range(3):
        draw.rectangle([bar_x - 3 + i, bar_y - 3 + i, bar_x + bar_width + 3 - i, bar_y + bar_height + 3 - i], 
                       outline=(0, 255, 255, 100 - i * 30), width=2)
    
    # バーの背景
    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], 
                   fill=(20, 20, 20, 180))
    
    # 画像を使用したプログレスバー
    if progress_ratio > 0:
        progress_bar_image = create_progress_bar_image(bar_width, bar_height, progress_ratio)
        # プログレスバーを合成
        image.paste(progress_bar_image, (bar_x, bar_y), progress_bar_image)
    
    # 画像をバイトストリームに保存
    buffer = io.BytesIO()
    image.convert('RGB').save(buffer, format='PNG')
    buffer.seek(0)
    
    # discord.Fileオブジェクトを作成
    return discord.File(buffer, filename=f"progress_{current}_{total}.png")