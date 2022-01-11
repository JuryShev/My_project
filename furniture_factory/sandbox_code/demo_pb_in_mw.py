from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QAction
# Импортируем наш шаблон.
from my_project.furniture_factory.start_window import Ui_MainWindow
from my_project.furniture_factory.win_dialog_new_fuctory import Ui_Dialog as creat_dialog
from my_project.furniture_factory.progress_bar import PB_Dialog as PB
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication,QMessageBox
#from progress_bar import PB_Dialog
from PyQt5.QtCore import QThread,pyqtSignal, QObject, pyqtSlot,QRunnable, QThreadPool
import transliterate
import my_project.furniture_factory.client_app as client_app
import time
from PyQt5 import QtWidgets, QtCore,QtGui
import json
import sys
import traceback
from functools import partial

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



is_killed=False




class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker_2(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''



    def __init__(self, fn, *args, **kwargs):
        super(Worker_2, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.is_final = False



    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class PopUpProgressB(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("Form")
        self.resize(689, 78)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgb(74, 80, 106);")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 691, 39))
        self.frame.setStyleSheet("background-color: rgb(123, 133, 175);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pbar = QProgressBar(self)
        self.pbar.setEnabled(True)
        self.pbar.setGeometry(QtCore.QRect(0, 39, 695, 11))
        self.pbar.setStyleSheet(DEFAULT_STYLE)
        self.pbar.setProperty("value", 20)
        self.pbar.setTextVisible(False)
        self.pbar.setFormat("")
        self.pbar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(290, 10, 201, 20))

        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "связь с сервером..."))
        self.status_=0


        #
        # self.pbar.setGeometry(30, 40, 500, 75)
        # self.layout = QVBoxLayout()
        # self.layout.addWidget(self.pbar)
        # self.setLayout(self.layout)
        # self.setGeometry(300, 300, 550, 100)
        # self.setWindowTitle('Progress Bar')



    def proc_counter(self, progress_callback, status=0):  # A slot takes no params
        while self.status_<status:
            for i in range(1, 100):
                time.sleep(0.01/(i*i))
                progress_callback.emit(i)

        return 'finish_bar'

    def on_count_changed(self, value):
        self.pbar.setValue(value)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        self.hide()




class DialogCreatFactory(QDialog, creat_dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.name_factory = ''
        self.setWindowTitle("Название предприятия")

        self.buttonBox.accepted.connect(self.acept_data)
        self.buttonBox.rejected.connect(self.reject_data)


    def acept_data(self):

        self.close()
        self.name_factory = self.lineEdit.text()
        if u'\u0400' <= self.name_factory <= u'\u04FF' or u'\u0500' <= self.name_factory <= u'\u052F':
            self.name_factory = transliterate.translit(self.name_factory, reversed=True)

    def reject_data(self):
        print('reject')
        self.close()

class mywindow(QtWidgets.QMainWindow):

    valueChanged = pyqtSignal(object)

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool()
        # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton_Creat.clicked.connect(self.btn_Creat)
        self.ui.pushButton_Open.clicked.connect(self.btn_Open)
        self._name_factory=''
        self.finish = QAction("Quit", self)
        self.finish.triggered.connect(self.closeEvent)
        self.valueChanged.connect(self.change_name)
        self.progress_bar=PopUpProgressB()
        self.status=0



    @property
    def name_factory(self):
        return self._name_factory

    @name_factory.setter
    def name_factory(self, value):
        self._name_factory = value
        self.valueChanged.emit(value)

    def btn_Creat(self):
        dlg = DialogCreatFactory(self)
        dlg.exec()
        if len(dlg.name_factory)>0:
            #creat = client_app.ServerConnector('0', 'localhost', 5000)
            dlg.name_factory=dlg.name_factory.replace(' ', '_')
            dlg.name_factory = dlg.name_factory.replace("'", '')
            self.name_factory=dlg.name_factory
            print(dlg.name_factory)

            # self.popup = PopUpProgressB()
            # self.popup.start_progress()


            #result = cont_test()
            #print(result)

    def btn_Open(self):
        print('open')
    def change_name(self):
        worker = Worker_2(self.cont_test)
        worker_2 = Worker_2(partial(self.progress_bar.proc_counter, status=10)) # Any other args, kwargs are passed to the run function
        worker_2.kwargs['progress_callback'] = worker_2.signals.progress
        worker_2.signals.result.connect(self.progress_bar.print_output)
        worker_2.signals.finished.connect(self.progress_bar.thread_complete)
        worker_2.signals.progress.connect(self.progress_bar.on_count_changed)
        self.threadpool.start(worker)
        self.threadpool.start(worker_2)

        self.progress_bar.setWindowModality(QtCore.Qt.ApplicationModal)
        self.progress_bar.show()


    def cont_test(self):
        a = 0
        for i in range(10000):
            time.sleep(0.5)
            self.progress_bar.status_ = i
            print(i)
        return a

    def closeEvent(self, event):
        close = QMessageBox.question(self,
                                     "QUIT",
                                     "Sure?",
                                     QMessageBox.Yes | QMessageBox.No)

        if close == QMessageBox.Yes:
            event.accept()
            self.threadpool.stop()
        else:
            event.ignore()





if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())

