import sys
import os
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, 
    QDialog, QFormLayout, QSpinBox, QDialogButtonBox
)
from PyQt6.QtGui import QPixmap, QResizeEvent

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
        # 保存原始图片
        self.original_pixmap = None
        # 拖动位置
        self.drag_position = QPoint()
        # 应用设置
        self.apply_settings()
    
    def initUI(self):
        """初始化UI"""
        # 设置窗口标志为无框
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 添加图片标签
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 允许图片缩放
        self.image_label.setScaledContents(True)
        self.main_layout.addWidget(self.image_label)
        
        # 添加设置按钮
        self.settings_button = QPushButton("设置")
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 150);
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 3px 8px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 200);
            }
        """)
        self.settings_button.clicked.connect(self.open_settings)
        self.main_layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        # 加载图片
        self.load_image()
        
        # 设置布局
        self.setLayout(self.main_layout)
    
    def load_image(self):
        """加载图片"""
        # 检查图片文件是否存在
        image_path = os.path.join("Material", "cat_pixel.png")
        if os.path.exists(image_path):
            # 保存原始图片
            self.original_pixmap = QPixmap(image_path)
            # 设置图片到标签
            self.image_label.setPixmap(self.original_pixmap)
            # 初始调整图片大小
            self.resize_image()
        else:
            # 如果图片不存在，显示提示信息
            self.image_label.setText("图片文件不存在")
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def resize_image(self):
        """调整图片大小以适应窗口"""
        if self.original_pixmap and self.isVisible():
            # 获取当前窗口大小
            current_size = self.size()
            
            # 计算可用空间（考虑按钮高度）
            available_width = current_size.width()
            available_height = current_size.height() - 30  # 减去按钮的大致高度
            
            # 确保可用空间为正
            if available_width > 0 and available_height > 0:
                # 设置图片标签的大小为可用空间
                self.image_label.setFixedSize(available_width, available_height)
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        # 调整图片大小
        self.resize_image()
    
    def apply_settings(self):
        """应用设置"""
        # 获取设置的窗口大小
        width = current_settings["window_size"].get("width", 200)
        height = current_settings["window_size"].get("height", 250)
        
        # 清除窗口大小限制
        self.setMinimumSize(50, 50)
        self.setMaximumSize(2000, 2000)
        
        # 调整窗口大小
        self.resize(width, height)
        
        # 设置窗口位置
        x = current_settings["window_position"]["x"]
        y = current_settings["window_position"]["y"]
        self.move(x, y)
        
        # 强制重新调整图片
        self.resize_image()
    
    def showEvent(self, event):
        """窗口显示事件"""
        super().showEvent(event)
        # 窗口显示后重新调整图片
        self.resize_image()
    
    def open_settings(self):
        """打开设置对话框"""
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def mousePressEvent(self, event):
        """鼠标按下事件，用于拖动窗口"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件，用于拖动窗口"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())