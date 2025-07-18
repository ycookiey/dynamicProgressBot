import json
import os
from typing import Dict, Any

DATA_FILE = "progress.json"

def load_data() -> Dict[str, Any]:
    """
    progress.jsonを読み込む。
    ファイルが存在しない場合は空の辞書を返す。
    """
    if not os.path.exists(DATA_FILE):
        return {}
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_data(data: Dict[str, Any]) -> None:
    """
    辞書データをprogress.jsonに書き込む。
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"データの保存に失敗しました: {e}")

def get_current_progress() -> Dict[str, Any]:
    """
    現在の進捗情報を取得する。
    """
    return load_data()

def update_progress(total: int = None, current: int = None) -> None:
    """
    進捗情報を更新する。
    """
    data = load_data()
    
    if total is not None:
        data['total'] = total
    if current is not None:
        data['current'] = current
    
    save_data(data)

def increment_progress() -> bool:
    """
    進捗を1つ進める。
    成功した場合はTrue、失敗した場合はFalseを返す。
    """
    data = load_data()
    
    if 'total' not in data or 'current' not in data:
        return False
    
    if data['current'] >= data['total']:
        return False
    
    data['current'] += 1
    save_data(data)
    return True