# import sys
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QColor, QPalette
# from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QVBoxLayout
#
#
# class HLine(QFrame):
#     def __init__(self, parent=None, color=QColor("black")):
#         super(HLine, self).__init__(parent)
#         self.setFrameShape(QFrame.HLine)
#         # self.setFrameShadow(QFrame.Plain)
#         # self.setLineWidth(0)
#         # self.setMidLineWidth(3)
#         # self.setContentsMargins(0, 0, 0, 0)
#         # self.setColor(color)
#
#     def setColor(self, color):
#         pal = self.palette()
#         pal.setColor(QPalette.WindowText, color)
#         self.setPalette(pal)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = QWidget()
#     w.resize(400, 400)
#     lay = QVBoxLayout(w)
#     lay.addWidget(HLine())
#
#     for color in [QColor("red"), QColor(0, 255, 0), QColor(Qt.blue)]:
#         h = HLine()
#         h.setColor(color)
#         lay.addWidget(h)
#
#     w.show()
#     sys.exit(app.exec_())

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# class ButtonName(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Example - Validator")
#         self.setGeometry(800, 200, 200, 200)
#         self.UI()
#         self.layouts()
#         self.show()
#
#     def UI(self):
#         self.lbl_integer = QLabel("Integer Validator")
#         self.textbox_integervalidator = QLineEdit()
#         self.textbox_integervalidator.setPlaceholderText("upto 3 digit value only accept")
#         self.textbox_integervalidator.setValidator(QIntValidator(1, 999, self))
#
#         self.lbl_double = QLabel("Double Validator")
#         self.textbox_doublevalidator = QLineEdit()
#         self.textbox_doublevalidator.setValidator(QDoubleValidator(0.99, 99.99, 2))
#
#         self.lbl_regexp = QLabel("RexExp Validator")
#         self.textbox_regexpvalidator = QLineEdit()
#         reg_ex_1 = QRegExp("[0-9]+.?[0-9]{,2}") # double^[+0-9]{1,3})*([0-9]{10,11}$
#         reg_ex_1 = QRegExp("[+0-9]{1,3})*([0-9]{10,11}")
#
#         # reg_ex_2 = QRegExp("[0-9]{1,5}")  # minimum 1 integer number to maxiumu 5 integer number
#         # reg_ex_3 = QRegExp("-?\\d{1,3}")  # accept negative number also
#         # reg_ex_4 = QRegExp("")
#         self.textbox_regexpvalidator.setValidator(QRegExpValidator(reg_ex_1))
#
#     def layouts(self):
#         mainlayout = QVBoxLayout()
#         mainlayout.addWidget(self.lbl_integer)
#         mainlayout.addWidget(self.textbox_integervalidator)
#         mainlayout.addWidget(self.lbl_double)
#         mainlayout.addWidget(self.textbox_doublevalidator)
#         mainlayout.addWidget(self.lbl_regexp)
#         mainlayout.addWidget(self.textbox_regexpvalidator)
#         self.setLayout(mainlayout)
#
# def main():
#     app = QApplication(sys.argv)
#     mainwindow = ButtonName()
#     sys.exit(app.exec_())
#
# if __name__ == "__main__":
#     main()


from PyQt5.QtCore import QEvent, Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel
)


# class Widget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         completer = QCompleter()
#         self.i=0
#         self.lay = QVBoxLayout(self)
#         self.label_head_depart = QLabel()
#         self.l=QLineEdit()
#         self.l2=QLineEdit()
#         self.rx = QtCore.QRegExp("[0-9]{3}")
#         self.val = QtGui.QRegExpValidator(self.rx)
#         self.l.setValidator(self.val)
#         self.l.inputRejected.connect(self.next_)
#         self.l2.inputRejected.connect(self.next_)
#         self.lay.addWidget(self.l)
#         self.lay.addWidget(self.label_head_depart)
#         self.lay.addWidget(self.l2)
#        lay.addWidget(QPushButton())
#        lay.addWidget(QComboBox())
        #completer.activated.connect(self.next_)



    # def event(self, event):
    #     if event.type() == QEvent.KeyPress and event.key() in (
    #         Qt.Key_Enter,
    #         Qt.Key_Return,
    #     ):
    #         self.focusNextPrevChild(True)
    #     return super().event(event)
#     def next_(self):
#
#         self.focusNextPrevChild(True)
#         print("stop")
#         return None
#
# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#     w = Widget()
#     w.show()
#     sys.exit(app.exec())

# from PyQt5 import QtGui
# from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QLabel
# import sys
#
#
# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.title = "PyQt5 Window"
#         self.top = 200
#         self.left = 500
#         self.width = 400
#         self.height = 300
#         self.setWindowIcon(QtGui.QIcon("icon.png"))
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         hbox = QHBoxLayout()
#         self.lineedit = QLineEdit(self)
#         self.lineedit.setFont(QtGui.QFont("Sanserif", 15))
#         self.lineedit.returnPressed.connect(self.onPressed)
#         self.label = QLabel(self)
#         self.label.setFont(QtGui.QFont("Sanserif", 15))
#         hbox.addWidget(self.label)
#         hbox.addWidget(self.lineedit)
#         self.setLayout(hbox)
#         self.show()
#
#
#     def onPressed(self):
#         self.label.setText(self.lineedit.text())
#
#
# if __name__ == "__main__":
#     App = QApplication(sys.argv)
#     window = Window()
#     sys.exit(App.exec())

# from PyQt5.QtWidgets import QApplication,QLineEdit,QWidget,QFormLayout
# from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
# from PyQt5.QtCore import Qt
# import sys
#
# class lineEditDemo(QWidget):
#         def __init__(self,parent=None):
#                 super().__init__(parent)
#                 e1 = QLineEdit()
#                 e1.setValidator(QIntValidator())
#                 e1.setMaxLength(4)
#                 e1.setAlignment(Qt.AlignRight)
#                 e1.setFont(QFont("Arial",20))
#
#                 e2 = QLineEdit()
#                 e2.setValidator(QDoubleValidator(0.99,99.99,2))
#                 e3 = QLineEdit()
#                 e3.setPlaceholderText("+7")
#                 e3.setInputMask("+9 (999) 999 99-99")
#
#                 e4 = QLineEdit()
#                 e4.textChanged.connect(self.textchanged)
#
#                 e5 = QLineEdit()
#                 e5.setEchoMode(QLineEdit.Password)
#
#                 e6 = QLineEdit("Hello PyQt5")
#                 e6.setReadOnly(True)
#                 e5.editingFinished.connect(self.enterPress)
#
#                 flo = QFormLayout()
#                 flo.addRow("integer validator",e1)
#                 flo.addRow("Double validator",e2)
#                 flo.addRow("Input Mask",e3)
#                 flo.addRow("Text changed",e4)
#                 flo.addRow("Password",e5)
#                 flo.addRow("Read Only",e6)
#
#                 self.setLayout(flo)
#                 self.setWindowTitle("QLineEdit Example")
#
#         def textchanged(self,text):
#                 print("Changed: " + text)
#
#         def enterPress(self):
#                 print("Enter pressed")
#
# if __name__ == "__main__":
#         app = QApplication(sys.argv)
#         win = lineEditDemo()
#         win.show()
#         sys.exit(app.exec_())

# from PyQt5.Qt import QApplication
# from PyQt5.QtCore import QRegExp
# from PyQt5.QtGui import QRegExpValidator
# from PyQt5.QtWidgets import QWidget, QLineEdit
# import sys
#
# class MyWidget(QWidget):
#     def __init__(self, parent=None):
#         super(QWidget, self).__init__(parent)
#         self.le_input = QLineEdit(self)
#         reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
#         input_validator = QRegExpValidator(reg_ex, self.le_input)
#         self.le_input.setValidator(input_validator)
# if __name__ == '__main__':
#     a = QApplication(sys.argv)
#     w = MyWidget()
#     w.show()
#     a.exec()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, qApp, QMessageBox

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 300, 200)
        button = QPushButton('Click me', self)
        qApp.setStyleSheet("QMessageBox QPushButton {color: rgb(255, 255, 255); background-color: rgb(145, 158, 208);}"
                           "QMessageBox QLabel {color: rgb(255, 255, 255);}")
        button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        QMessageBox.information(self, 'Notification', 'Text', QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = App()
    widget.show()
    sys.exit(app.exec_())