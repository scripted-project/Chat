import sys
import socket
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QVBoxLayout, QLineEdit, QGridLayout, QGroupBox, QCalendarWidget, QListWidget, QPlainTextEdit
from PyQt6.QtWidgets import QCalendarWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chat")
        widget = QWidget()
        mainBox = QGroupBox()

        baseLayout = QGridLayout()
        baseLayout.addWidget(mainBox, 0, 0)
        
        mainLayout = QGridLayout()
        mainBox.setLayout(mainLayout)
        
        
        widget.setLayout(baseLayout)
        self.setCentralWidget(widget)
        self.setFixedSize(QSize(1000, 500))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()