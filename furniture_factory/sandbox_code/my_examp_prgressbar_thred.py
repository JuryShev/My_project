import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication
from PyQt5 import QtWidgets, QtCore
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
class Thread(QThread):
   _signal = pyqtSignal(int)
   def __init__(self):
        super(Thread, self).__init__()

   def __del__(self):
       self.wait()

   def run(self):
       t=0.09
       while True:
           for i in range(100):
               if i>0:
                   time.sleep(t/i)
               else:
                   time.sleep(t)
               self._signal.emit(i)

class Ui_Form(object):
    def setupUi(self, Form):
        super(Ui_Form, self).__init__()
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

        self.btn = QPushButton('Click me')
        self.btn.clicked.connect(self.btnFunc)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.progressBar)
        self.vbox.addWidget(self.btn)
        Form.setLayout(self.vbox)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def btnFunc(self):
        self.thread = Thread()
        self.thread._signal.connect(self.signal_accept)
        self.thread.start()
        self.btn.setEnabled(False)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def signal_accept(self, msg):
        self.progressBar.setValue(int(msg))
        if self.progressBar.value() == 99:
            self.progressBar.setValue(0)
        self.btn.setEnabled(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())





