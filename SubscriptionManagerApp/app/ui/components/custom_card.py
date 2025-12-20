from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class CustomCard(QFrame):
    def __init__(self, title, value, color="#3498db", icon_text=""):
        super().__init__()
        self.setFixedSize(220, 120)

        # Style cho Card
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border-left: 5px solid {color};
            }}
        """)

        # Hiệu ứng đổ bóng (Shadow)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))  # Màu đen mờ
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        # Layout
        layout = QVBoxLayout(self)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #7f8c8d; font-size: 14px;")

        lbl_value = QLabel(str(value))
        lbl_value.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)