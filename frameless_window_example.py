import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

class FramelessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.drag_position = QPoint()

    def initUI(self):
        # 设置窗口标志为无框
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 设置窗口大小和位置
        self.resize(400, 300)
        self.move(300, 300)
        
        # 创建主容器
        main_widget = QWidget(self)
        main_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #4CAF50;
            }
        """)
        
        # 创建垂直布局
        layout = QVBoxLayout(main_widget)
        
        # 创建标题栏（可拖动区域）
        title_bar = QWidget()
        title_bar.setFixedHeight(30)
        title_bar.setStyleSheet("background-color: #4CAF50;")
        title_bar_layout = QVBoxLayout(title_bar)
        title_label = QLabel("无框窗口示例")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white; font-weight: bold;")
        title_bar_layout.addWidget(title_label)
        layout.addWidget(title_bar)
        
        # 创建内容区域
        content_label = QLabel("这是一个使用 PyQt6 实现的无框窗口！")
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_label.setStyleSheet("font-size: 16px; margin: 20px;")
        layout.addWidget(content_label)
        
        # 创建关闭按钮
        close_btn = QPushButton("关闭窗口")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        # 设置主容器布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_widget)
        
        # 连接标题栏的鼠标事件
        title_bar.mousePressEvent = self.mousePressEvent
        title_bar.mouseMoveEvent = self.mouseMoveEvent

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FramelessWindow()
    window.show()
    sys.exit(app.exec())