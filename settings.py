# 设置文件

# 默认窗口设置
DEFAULT_SETTINGS = {
    "window_size": {
        "width": 400,
        "height": 300
    },
    "window_color": "#FFFFFF",  # 默认白色
    "window_position": {
        "x": 100,
        "y": 100
    }
}

# 当前设置
current_settings = DEFAULT_SETTINGS.copy()

# 保存设置到文件
import json
import os

def save_settings():
    """保存设置到文件"""
    with open("settings.json", "w") as f:
        json.dump(current_settings, f)

# 加载设置

def load_settings():
    """从文件加载设置"""
    global current_settings
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            current_settings = json.load(f)
    else:
        current_settings = DEFAULT_SETTINGS.copy()