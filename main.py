# coding=UTF-8
from LoginUi import *
from InterfaceUi import *
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QMimeData
from PyQt6.QtGui import QDrag
import sys


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.pushButton.clicked.connect(self.go_to_inter)
        self.show()

    def go_to_inter(self):
        account = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if account == "WK" and password == "123456":
            InterfaceWindow()
            self.close()
        else:
            pass

    # 拖动
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton and not self.isMaximized():
            self.m_flag = True
            self.m_Position = event.position().toPoint() - self.pos()

            event.accept()
            # self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.MouseButton.LeftButton and self.m_flag:
            self.move(mouse_event.position().toPoint() - self.m_Position)  # 更改窗口位置
            # mouse_event.setDropAction(QtCore.Qt.DropAction.MoveAction)
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        # self.setCursor(QtGui.QCursor(QtCore.Qt.MouseButton.ArrowCursor))


class InterfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_inter()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.pushButton_CH.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))  # 绑定槽0
        self.ui.pushButton_HN.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))  # 绑定槽0
        self.ui.pushButton_XJ.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))  # 绑定槽0
        self.ui.pushButton_max.clicked.connect(self.resize_win)
        self.show()

    def resize_win(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.pushButton_max.setIcon(QtGui.QIcon(u":/icons/icons/展开文本域_expand-text-input.png"))
        else:
            self.showMaximized()
            self.ui.pushButton_max.setIcon(QtGui.QIcon(u":/icons/icons/收起文本域_collapse-text-input.png"))

    # 拖动
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton and not self.isMaximized():
            self.m_flag = True
            self.m_Position = event.position().toPoint() - self.pos()

            event.accept()
            # self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.MouseButton.LeftButton and self.m_flag:
            self.move(mouse_event.position().toPoint() - self.m_Position)  # 更改窗口位置
            # mouse_event.setDropAction(QtCore.Qt.DropAction.MoveAction)
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        # self.setCursor(QtGui.QCursor(QtCore.Qt.MouseButton.ArrowCursor))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    sys.exit(app.exec())



