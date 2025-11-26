import sys
import json
import os
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, 
    QDialog, QFormLayout, QSpinBox, QColorDialog, QDialogButtonBox
)
from PyQt6.QtGui import QColor

# 导入设置
from settings import load_settings, current_settings, save_settings

class SettingsDialog(QDialog):
    """设置对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setup_ui()
        self.load_current_settings()
        
    def setup_ui(self):
        """设置UI"""
        layout = QFormLayout(self)
        
        # 窗口大小设置
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(100, 1000)
        layout.addRow("窗口宽度:", self.width_spinbox)
        
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(100, 1000)
        layout.addRow("窗口高度:", self.height_spinbox)
        
        # 窗口颜色设置
        self.color_button = QPushButton("选择颜色")
        self.color_button.clicked.connect(self.choose_color)
        self.color_label = QLabel()
        layout.addRow("窗口颜色:", self.color_button)
        layout.addRow("当前颜色:", self.color_label)
        
        # 窗口位置设置
        self.x_spinbox = QSpinBox()
        self.x_spinbox.setRange(0, 2000)
        layout.addRow("X位置:", self.x_spinbox)
        
        self.y_spinbox = QSpinBox()
        self.y_spinbox.setRange(0, 2000)
        layout.addRow("Y位置:", self.y_spinbox)
        
        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def load_current_settings(self):
        """加载当前设置"""
        self.width_spinbox.setValue(current_settings["window_size"]["width"])
        self.height_spinbox.setValue(current_settings["window_size"]["height"])
        self.x_spinbox.setValue(current_settings["window_position"]["x"])
        self.y_spinbox.setValue(current_settings["window_position"]["y"])
        self.update_color_label(current_settings["window_color"])
    
    def choose_color(self):
        """选择颜色"""
        color = QColorDialog.getColor(QColor(current_settings["window_color"]), self, "选择窗口颜色")
        if color.isValid():
            color_hex = color.name()
            current_settings["window_color"] = color_hex
            self.update_color_label(color_hex)
    
    def update_color_label(self, color_hex):
        """更新颜色标签"""
        self.color_label.setText(color_hex)
        self.color_label.setStyleSheet(f"background-color: {color_hex}; padding: 5px;")
    
    def accept(self):
        """确认设置"""
        # 更新设置
        current_settings["window_size"]["width"] = self.width_spinbox.value()
        current_settings["window_size"]["height"] = self.height_spinbox.value()
        current_settings["window_position"]["x"] = self.x_spinbox.value()
        current_settings["window_position"]["y"] = self.y_spinbox.value()
        
        # 保存设置
        save_settings()
        
        # 应用设置到主窗口
        if self.parent():
            self.parent().apply_settings()
        
        super().accept()

class DesktopPet(QWidget):
    """桌面宠物主窗口"""
    def __init__(self):
        super().__init__()
        # 加载设置
        load_settings()
        # 初始化UI
        self.initUI()
        # 应用设置
        self.apply_settings()
    
    def initUI(self):
        """初始化UI"""
        # 设置窗口标志
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 添加标题
        self.title_label = QLabel("桌面宠物")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # 添加设置按钮
        self.settings_button = QPushButton("设置")
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)
        
        # 设置布局
        self.setLayout(layout)
    
    def apply_settings(self):
        """应用设置"""
        # 设置窗口大小
        width = current_settings["window_size"]["width"]
        height = current_settings["window_size"]["height"]
        self.resize(width, height)
        
        # 设置窗口颜色
        color = current_settings["window_color"]
        self.setStyleSheet(f"background-color: {color};")
        
        # 设置窗口位置
        x = current_settings["window_position"]["x"]
        y = current_settings["window_position"]["y"]
        self.move(x, y)
    
    def open_settings(self):
        """打开设置对话框"""
        dialog = SettingsDialog(self)
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())