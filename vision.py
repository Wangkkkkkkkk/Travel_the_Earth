# encoding: utf-8

from PyQt6.QtWidgets import (QApplication, QWidget, QFileDialog, QMainWindow,
                             QGraphicsView, QGraphicsItem, QGraphicsRectItem,
                             QGraphicsItemGroup, QGraphicsLineItem, QGraphicsEllipseItem,
                             QGraphicsTextItem, QPushButton)
from PyQt6 import QtGui
import cv2
import sys

from ImageView import *
import res_rc


class ImageWin(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        # 初始化窗口
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.graphicsView.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)

        # 初始化视图
        self.graphicsView = self.ui.graphicsView
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1080, 720)
        self.graphicsView.setScene(self.scene)

        self.ratio_orgin = 0.1
        self.ratio = 0.1  # 缩放初始比例
        self.zoom_step = 0.01  # 缩放步长
        self.zoom_max = 1.00  # 缩放最大值
        self.zoom_min = 0.10  # 缩放最小值
        self.pixmapItem = None

        self.ratio_pop = 0.5  # 图标出现的缩放比例
        self.ratio_up = 0.2   # 省级消失缩放比例
        self.change_x = 0.  # 图像x方向变化量
        self.change_y = 0.  # 图像y方向变化量
        self.size = 10      # 圆形图标的直径
        self.text_offset = 14  # 文字偏置

        # 接管图形场景的鼠标事件
        self.scene.mousePressEvent = self.scene_MousePressEvent
        # self.scene.mouseReleaseEvent = self.scene_mouseReleaseEvent
        self.scene.mouseMoveEvent = self.scene_mouseMoveEvent
        self.scene.wheelEvent = self.scene_wheelEvent

        self.grp_market = QGraphicsItemGroup()  # 市级
        self.grp_province = QGraphicsItemGroup()  # 省级

        self.china_dicts = {
            "湖南省": {
                "info": [5400, 4600, 0],
                "market": {
                    "长沙": [5754, 4683, 0],
                    "张家界": [5383, 4521, 0],
                    "常德": [5572, 4535, 0],
                    "益阳": [5681, 4617, 0],
                    "汨罗": [5782, 4571, 0],
                    "浏阳": [5869, 4682, 0],
                    "娄底": [5617, 4767, 0],
                    "株洲": [5790, 4754, 0],
                    "衡阳": [5724, 4917, 0],
                    "郴州": [5786, 5100, 0],
                    "怀化": [5310, 4803, 0]
                }
            },
        }

        self.buttons_market = {}
        self.buttons_province = {}
        self.lineedit_finding = {}

        for key_province in self.china_dicts.keys():
            self.buttons_province[key_province] = QPushButton(key_province)
            self.buttons_province[key_province].setStyleSheet(
                "QPushButton{\n"
                "    font-family:'宋体';font-size:24px;\n"
                "    background-color: rgba(0, 0, 0, 0);\n"
                "    border:none;\n"
                "}\n")
            self.lineedit_finding[key_province] = QtWidgets.QLineEdit(
                "探索度: " + str(self.china_dicts[key_province]["info"][2]) + " %")
            self.lineedit_finding[key_province].setStyleSheet(
                "border:none;\n"
                "font-family:'宋体';font-size:12px;\n"
                "background-color: rgba(0, 0, 0, 0);\n")

            for key_market in self.china_dicts[key_province]["market"].keys():
                self.buttons_market[key_market] = QPushButton(key_market)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/icons/圆形_round.png"),
                               QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.buttons_market[key_market].setIcon(icon)
                self.buttons_market[key_market].setStyleSheet(
                    "QPushButton{\n"
                    "    font-family:'宋体';font-size:18px;"
                    "    background-color: rgba(255, 132, 139, 30);"
                    "    border:none;\n"
                    "}\n")
                self.buttons_market[key_market].clicked.connect(lambda: self.updata_finding())

        self.show()

    # 载入地图
    def addScenes(self, img):
        self.org = img
        if self.pixmapItem != None:
            originX = self.pixmapItem.x()
            originY = self.pixmapItem.y()
        else:
            originX, originY = 0., 0.  # 坐标基点

        self.scene.clear()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        self.pixmap = QtGui.QPixmap(
            QtGui.QImage(img[:], img.shape[1], img.shape[0], img.shape[1] * 3,
                         QtGui.QImage.Format.Format_RGB888))  # 转化为qlbel格式

        self.pixmapItem = self.scene.addPixmap(self.pixmap)
        self.pixmapItem.setScale(self.ratio)  # 缩放
        self.pixmapItem.setPos(originX, originY)

    #  显示市级标志
    def add_market(self):
        gitup = self.ratio / self.ratio_orgin * self.ratio_orgin
        for key_province in self.china_dicts.keys():
            for key_market in self.china_dicts[key_province]["market"].keys():
                self.buttons_market[key_market].show()
                self.buttons_market[key_market].move(
                    int(self.china_dicts[key_province]["market"][key_market][0] * gitup + self.change_x - self.size / 2),
                    int(self.china_dicts[key_province]["market"][key_market][1] * gitup + self.change_y - self.size / 2))
                self.scene.addWidget(self.buttons_market[key_market])

    # 显示省级标志
    def add_province(self):
        gitup = self.ratio / self.ratio_orgin * self.ratio_orgin
        for key_province in self.china_dicts.keys():
            self.buttons_province[key_province].show()
            self.buttons_province[key_province].move(
                int(self.china_dicts[key_province]["info"][0] * gitup + self.change_x + (self.ratio - self.ratio_up) * 120),
                int(self.china_dicts[key_province]["info"][1] * gitup + self.change_y + (self.ratio - self.ratio_up) * 120))
            self.scene.addWidget(self.buttons_province[key_province])

            self.lineedit_finding[key_province].show()
            self.lineedit_finding[key_province].setText(
                "探索度: " + str(self.china_dicts[key_province]["info"][2]) + " %")
            self.lineedit_finding[key_province].move(
                int(self.china_dicts[key_province]["info"][0] * gitup + self.change_x + (self.ratio - self.ratio_up) * 120),
                int(self.china_dicts[key_province]["info"][1] * gitup + self.change_y + (self.ratio - self.ratio_up) * 120 + 25))
            self.scene.addWidget(self.lineedit_finding[key_province])

    #  隐藏按钮
    def hide_pushbutton(self, buttons, lineedit=None):
        for key in buttons.keys():
            buttons[key].hide()
            self.scene.addWidget(buttons[key])
        if lineedit != None:
            for key in lineedit.keys():
                lineedit[key].hide()
                self.scene.addWidget(lineedit[key])

    # 判断按钮是否显示，更新按钮位置
    def updata_button(self):
        if self.ratio > self.ratio_pop:  # 缩放比例是否大于 ratio_pop
            self.add_market()  # 实现市级标志
        else:
            self.hide_pushbutton(self.buttons_market)  # 隐藏市级标志

        if self.ratio_up < self.ratio < self.ratio_pop - 0.02:  # 缩放比例是否处于省级范围
            self.add_province()  # 显示省级标志
        else:
            self.hide_pushbutton(self.buttons_province, self.lineedit_finding)  # 隐藏省级标志

    def updata_finding(self):
        sender = self.sender()  # 获得哪个按钮触发的信息

        for key_province in self.china_dicts.keys():
            num = 0
            for key_market in self.china_dicts[key_province]["market"].keys():
                if key_market == sender.text():
                    self.china_dicts[key_province]["market"][key_market][2] += 1
                if self.china_dicts[key_province]["market"][key_market][2] > 0:
                    num += 1
            self.china_dicts[key_province]["info"][2] = \
                int(float(num) / float(len(self.china_dicts[key_province]["market"])) * 100)

    def scene_MousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:  # 左键按下
            self.preMousePosition = event.scenePos()  # 获取鼠标当前位置

    def scene_mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.MouseMove = event.scenePos() - self.preMousePosition  # 鼠标当前位置-先前位置=单次偏移量
            self.preMousePosition = event.scenePos()  # 更新当前鼠标在窗口上的位置，下次移动用
            self.pixmapItem.setPos(self.pixmapItem.pos() + self.MouseMove)  # 更新图元位置

            self.change_x += self.MouseMove.x()
            self.change_y += self.MouseMove.y()

            self.updata_button()

    # 定义滚轮方法。当鼠标在图元范围之外，以图元中心为缩放原点；当鼠标在图元之中，以鼠标悬停位置为缩放中心
    def scene_wheelEvent(self, event):
        angle = event.delta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        if angle > 0:
            # print("滚轮上滚")
            self.ratio += self.zoom_step  # 缩放比例自加
            if self.ratio - self.zoom_max > 0.01:
                self.ratio = self.zoom_max
            else:
                w = self.pixmap.size().width() * (self.ratio - self.zoom_step)
                h = self.pixmap.size().height() * (self.ratio - self.zoom_step)
                x1 = self.pixmapItem.pos().x()  # 图元左位置
                x2 = self.pixmapItem.pos().x() + w  # 图元右位置
                y1 = self.pixmapItem.pos().y()  # 图元上位置
                y2 = self.pixmapItem.pos().y() + h  # 图元下位置
                if x1 < event.scenePos().x() < x2 and y1 < event.scenePos().y() < y2:  # 判断鼠标悬停位置是否在图元中
                    # print('在内部')
                    self.pixmapItem.setScale(self.ratio)  # 缩放
                    a1 = event.scenePos() - self.pixmapItem.pos()  # 鼠标与图元左上角的差值
                    a2 = self.ratio/(self.ratio - self.zoom_step) - 1    # 对应比例
                    delta = a1 * a2
                    self.pixmapItem.setPos(self.pixmapItem.pos() - delta)

                    self.change_x -= delta.x()
                    self.change_y -= delta.y()

                else:
                    # print('在外部')  # 以图元中心缩放
                    self.pixmapItem.setScale(self.ratio)  # 缩放
                    delta_x = (self.pixmap.size().width() * self.zoom_step) / 2  # 图元偏移量
                    delta_y = (self.pixmap.size().height() * self.zoom_step) / 2
                    self.pixmapItem.setPos(self.pixmapItem.pos().x() - delta_x,
                                           self.pixmapItem.pos().y() - delta_y)  # 图元偏移

                    self.change_x -= delta_x
                    self.change_y -= delta_y
        else:
            # print("滚轮下滚")
            self.ratio -= self.zoom_step
            if self.ratio - self.zoom_min < 0.01:
                self.ratio = self.zoom_min
            else:
                w = self.pixmap.size().width() * (self.ratio + self.zoom_step)
                h = self.pixmap.size().height() * (self.ratio + self.zoom_step)
                x1 = self.pixmapItem.pos().x()
                x2 = self.pixmapItem.pos().x() + w
                y1 = self.pixmapItem.pos().y()
                y2 = self.pixmapItem.pos().y() + h
                if x1 < event.scenePos().x() < x2 and y1 < event.scenePos().y() < y2:
                    # print('在内部')
                    self.pixmapItem.setScale(self.ratio)  # 缩放
                    a1 = event.scenePos() - self.pixmapItem.pos()  # 鼠标与图元左上角的差值
                    a2 = self.ratio/(self.ratio + self.zoom_step) - 1    # 对应比例
                    delta = a1 * a2
                    self.pixmapItem.setPos(self.pixmapItem.pos() - delta)

                    self.change_x -= delta.x()
                    self.change_y -= delta.y()
                else:
                    # print('在外部')
                    self.pixmapItem.setScale(self.ratio)
                    delta_x = (self.pixmap.size().width() * self.zoom_step) / 2
                    delta_y = (self.pixmap.size().height() * self.zoom_step) / 2
                    self.pixmapItem.setPos(self.pixmapItem.pos().x() + delta_x, self.pixmapItem.pos().y() + delta_y)

                    self.change_x += delta_x
                    self.change_y += delta_y

        self.updata_button()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ImageWin()

    img = cv2.imread("images/China_2.JPG")
    win.addScenes(img)

    sys.exit(app.exec())
