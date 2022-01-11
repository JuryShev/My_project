from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time

class Worker(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

    def process(self):
        # dummy worker process
        for n in range(0, 10):
            print ('process {}'.format(n))
            time.sleep(0.5)
        self.finished.emit()

    finished = QtCore.pyqtSignal()

class Dialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.init_ui()

    def init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.btn_run = QtWidgets.QPushButton('Run', self)
        self.layout.addWidget(self.btn_run)
        self.btn_cancel = QtWidgets.QPushButton('Cancel', self)
        self.layout.addWidget(self.btn_cancel)

        self.btn_run.clicked.connect(self.run)
        self.btn_cancel.clicked.connect(self.reject)

        self.show()
        self.raise_()

    def run(self):
        # start the worker thread
        self.thread = QtCore.QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.connect(self.worker.process)
        self.worker.connect( self.thread.quit)
        self.thread.connect( self.worker.deleteLater)
        self.worker.connect(self.thread.deleteLater)
        self.thread.start()

def main():
    app = QtWidgets.QApplication(sys.argv)
    dlg = Dialog()
    ret = dlg.exec_()

if __name__ == '__main__':
    main()