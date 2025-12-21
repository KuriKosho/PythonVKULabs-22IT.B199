from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout,
    QLabel, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont


class CustomCard(QFrame):
    def __init__(self, title, value, color="#3498db", icon="📊"):
        super().__init__()

        self.setMinimumSize(240, 120)
        self.setMaximumHeight(130)

        # ================= CARD STYLE =================
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border-radius: 12px;
            }}
        """)

        # ================= SHADOW =================
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 35))
        self.setGraphicsEffect(shadow)

        # ================= LAYOUT =================
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # ================= ICON =================
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedSize(48, 48)
        icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color}20;
                color: {color};
                border-radius: 24px;
                font-size: 22px;
            }}
        """)

        # ================= TEXT =================
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        lbl_title = QLabel(title.upper())
        lbl_title.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 11px;
                letter-spacing: 1px;
            }
        """)

        lbl_value = QLabel(str(value))
        lbl_value.setStyleSheet(f"""
            QLabel {{
                color: #2c3e50;
                font-size: 26px;
                font-weight: bold;
            }}
        """)

        text_layout.addWidget(lbl_title)
        text_layout.addWidget(lbl_value)
        text_layout.addStretch()

        # ================= COMPOSE =================
        main_layout.addWidget(icon_label)
        main_layout.addLayout(text_layout)
