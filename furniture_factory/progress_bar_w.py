# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Yura\PycharmProjects\pythonProject\furniture_factory\GUI_designer\progress_bar_w.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
DEFAULT_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: lightblue;
    width: 10px;
    margin: 1px;
}
"""

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(689, 78)
        Form.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        Form.setStyleSheet("background-color: rgb(74, 80, 106);")
        self.progressBar = QtWidgets.QProgressBar(Form)

        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(10, 30, 671, 10))
        self.progressBar.setStyleSheet(DEFAULT_STYLE)
        self.progressBar.setProperty("value", 20)
        self.progressBar.setTextVisible(False)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
