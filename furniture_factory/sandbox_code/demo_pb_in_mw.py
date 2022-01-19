from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QAction
# Импортируем наш шаблон.
from my_project.furniture_factory.start_window import Ui_MainWindow
from my_project.furniture_factory.win_dialog_new_fuctory import Ui_Dialog as creat_dialog
from my_project.furniture_factory.CountCriterion_w import CountCr_2, CountCr
from my_project.furniture_factory.Table_start import Table_start
from my_project.furniture_factory.progress_bar import PB_Dialog as PB
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication,QMessageBox,QGraphicsDropShadowEffect
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
stack_window_Height=0
stack_window_Width=0
name_factory_orig=''
_translate = QtCore.QCoreApplication.translate


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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        shadow = QGraphicsDropShadowEffect(blurRadius=12, xOffset=10, yOffset=4)
        self.setGraphicsEffect(shadow)

       #  self.setWindowFlags(
       #
       #
       #  )
        # QtCore.Qt.Window |
        # QtCore.Qt.CustomizeWindowHint |
        # QtCore.Qt.WindowTitleHint |
        # QtCore.Qt.WindowCloseButtonHint |
        # QtCore.Qt.WindowStaysOnTopHint

        self.setStyleSheet("background-color: rgb(74, 80, 106);")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 691, 81))
        self.frame.setStyleSheet("\n"
                                 "background-color: qlineargradient(spread:pad, x1:0.699227, y1:1, x2:0.641409, y2:0.085, stop:0 rgba(74, 80, 106, 255), stop:1 rgba(123, 133, 175, 255));")
        self.frame.setInputMethodHints(QtCore.Qt.ImhNone)
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
        self.label.setGeometry(QtCore.QRect(250, 2, 441, 37))

        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "background-color: qlineargradient(spread:pad, x1:0.83, y1:1, x2:0.835227, y2:0, stop:0 rgba(109, 118, 156, 255), stop:1 rgba(123, 133, 175, 255));")
        self.label.setObjectName("label")
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "связь с сервером..."))
        self.status_=0
        self.w_width=784
        self.w_height = 272





    def proc_counter(self, progress_callback, status=0):  # A slot takes no params
        direct=0
        while self.status_<status:
            for i in range(1, 98):
                time.sleep(0.01/(i*i))
                progress_callback.emit(i)
            if direct==0:
                direct=1
                self.pbar.setLayoutDirection(QtCore.Qt.RightToLeft)

            else:
                direct = 0
                self.pbar.setLayoutDirection ( QtCore.Qt.LeftToRight )
        return 'finish_bar'

    def on_count_changed(self, value):

        self.pbar.setValue(value)

    def print_output(self, s):

        print(s)

    def thread_complete(self):

        self.hide()


class CountCriterion(QWidget, CountCr):
    def __init__(self):
        super( ).__init__()
        self.setupUi(self)
        self.w_width=784
        self.w_height = 272
        self.value_criterion=0
        self.value_departmen = 0
        self.ButtonNext.clicked.connect(self.next)

    def next(self):
        self.value_criterion = int(self.spinBox_criterion.value())
        self.value_departmen = int(self.spinBox_departmen.value())
        if self.value_departmen>0 and self.value_criterion>0:
            stack_window_Height = table_start_.w_height
            stack_window_Width = table_start_.w_width
            table_start_.label_name_factory.setText(_translate("Form", start_w.name_factory_orig))
            table_start_.tableWidget.setRowCount(self.value_criterion)
            table_start_.tableWidget_2.setRowCount(self.value_departmen)
            stack_window.setFixedHeight(stack_window_Height)
            stack_window.setFixedWidth(stack_window_Width)
            stack_window.setCurrentIndex(stack_window.currentIndex() + 1)
            print(f"value_criterion={self.value_criterion}\nvalue_departmen={self.value_departmen} ")
        else:
            self.label_error.setText(_translate("Form", "Значение должны быть больше нуля"))
            print('критерий равен 0')

    def contextMenuEvent(self, event):
        context_menu=QtWidgets.QMenu(self)

        new_action=context_menu.addAction("New")

        action=context_menu.exec_(self.mapToGlobal(event.pos()))

        if action == new_action:
            print("new")



class DialogCreatFactory(QDialog, creat_dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.name_factory = ''
        self.name_factory_orig = ''
        self.setWindowTitle("Название предприятия")

        self.buttonBox.accepted.connect(self.acept_data)
        self.buttonBox.rejected.connect(self.reject_data)


    def acept_data(self):

        self.close()
        self.name_factory_orig = self.lineEdit.text()
        if u'\u0400' <= self.name_factory_orig <= u'\u04FF' or u'\u0500' <= self.name_factory_orig <= u'\u052F':
            self.name_factory = transliterate.translit(self.name_factory_orig, reversed=True)
        else:
            self.name_factory=self.name_factory_orig


    def reject_data(self):
        print('reject')
        self.close()

class Table_start_(QWidget, Table_start):
    def __init__(self):
        super( ).__init__()
        self.setupUi(self)
        self.w_width=1045
        self.w_height = 545
        self.value_criterion=0
        self.value_departmen = 0
        self.ButtonNext.clicked.connect(self.next)
        self.data_send={
                        "comand": 5000,
                        "user": "admin",
                        "db_comand": 1,
                        "tables": {"conf_criterion":[],
                                    "departmen":   [],
                                    "bonus_koeficient":[]
                                    }}
        self.conf_criterion={"title_criterion":"Порядок_1",
                                        "max_coef": 5,
                                        "w_coef":5.0}
        self.departmen={"title": "Отдел_1"}
        self.bonus_koeficient={"percentage_of_profits":2.0}


        print("ok")
       # self.ButtonNext.clicked.connect(self.next)

    def next(self):

        print("1,0: %s" % self.tableWidget.item(0, 1).text())
        print(self.tableWidget.rowCount())
        self.write_in_data(self.tableWidget, self.conf_criterion, 'conf_criterion')
        self.write_in_data(self.tableWidget_2, self.departmen, 'departmen')
        self.write_in_data(self.tableWidget_3, self.bonus_koeficient, 'bonus_koeficient')



        pass
    def write_in_data(self, tablewidget, dir_data, name_table):

        list_key=list(dir_data.keys())
        if len(list_key)!=tablewidget.columnCount():
            return('Количество ключей не совпадает с количеством столбцов')
        for row in range (tablewidget.rowCount()):
            for column in range (tablewidget.columnCount()):
                value=tablewidget.item(row, column).text()
                if type(dir_data[list_key[column]]) != str :
                    type_value=type(dir_data[list_key[column]])
                    value=type_value(value)
                dir_data[list_key[column]]=value

            self.data_send["tables"][name_table].append(dir_data.copy())






    def contextMenuEvent(self, event):
        context_menu=QtWidgets.QMenu(self)

        new_action=context_menu.addAction("New")

        action=context_menu.exec_(self.mapToGlobal(event.pos()))

        if action == new_action:
            print("new")

class mywindow(QtWidgets.QMainWindow):

    valueChanged = pyqtSignal(object)
    flagServerChange=pyqtSignal(object)

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool()
        # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton_Creat.clicked.connect(self.btn_Creat)
        self.ui.pushButton_Open.clicked.connect(self.btn_Open)
        self._name_factory=''
        self.name_factory_orig=''
        self._flag_server=0
        self.finish = QAction("Quit", self)
        self.finish.triggered.connect(self.closeEvent)
        self.valueChanged.connect(self.change_name)
        self.flagServerChange.connect(self.flag_server_change)
        self.progress_bar=PopUpProgressB()
        self.start_w_width=784
        self.start_w_height = 545





    @property
    def name_factory(self):
        return self._name_factory

    @name_factory.setter
    def name_factory(self, value):
        self._name_factory = value
        self.valueChanged.emit(value)

    @property
    def flag_server(self):
        return self._flag_server

    @flag_server.setter
    def flag_server(self, value):
        self._flag_server=value
        self.flagServerChange.emit(value)

    def btn_Creat(self):
        dlg = DialogCreatFactory(self)
        dlg.exec()
        if len(dlg.name_factory)>0:
            #creat = client_app.ServerConnector('0', 'localhost', 5000)
            dlg.name_factory=dlg.name_factory.replace(' ', '_')
            dlg.name_factory = dlg.name_factory.replace("'", '')
            self.name_factory=dlg.name_factory
            self.name_factory_orig = dlg.name_factory_orig
            print(dlg.name_factory)

            # self.popup = PopUpProgressB()
            # self.popup.start_progress()


            #result = cont_test()
            #print(result)

    def btn_Open(self):
        print('open')
    def change_name(self):
        worker = Worker_2(self.cont_test)
        worker.signals.finished.connect(self.thread_complete)
        worker_2 = Worker_2(partial(self.progress_bar.proc_counter, status=3)) # Any other args, kwargs are passed to the run function
        worker_2.kwargs['progress_callback'] = worker_2.signals.progress
        worker_2.signals.result.connect(self.progress_bar.print_output)
        worker_2.signals.finished.connect(self.progress_bar.thread_complete)
        worker_2.signals.progress.connect(self.progress_bar.on_count_changed)
        self.threadpool.start(worker)
        self.threadpool.start(worker_2)

        self.progress_bar.setWindowModality(QtCore.Qt.ApplicationModal)
        self.progress_bar.show()

    def flag_server_change(self):
        print("new win")
        stack_window_Height = count_crit.w_height
        stack_window_Width = count_crit.w_width
        count_crit.label_name_factory.setText(_translate("Form", self.name_factory_orig))
        stack_window.setFixedHeight(stack_window_Height)
        stack_window.setFixedWidth(stack_window_Width)
        stack_window.setCurrentIndex(stack_window.currentIndex()+1)


    def cont_test(self):
        a = 0
        for i in range(5):
            time.sleep(0.5)
            self.progress_bar.status_ = i
            print(i)
        return a

    def thread_complete(self):
        print("complete")
        self.flag_server=1

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
    start_w = mywindow()
    count_crit=CountCriterion()
    table_start_=Table_start_()
    stack_window_Height=start_w.start_w_height
    stack_window_Width=start_w.start_w_width
    stack_window = QtWidgets.QStackedWidget()
    stack_window.setStyleSheet("background-color: rgb(74, 80, 106);")

    stack_window.addWidget(start_w)
    stack_window.addWidget(count_crit)
    stack_window.addWidget(table_start_)

    stack_window.setFixedHeight(stack_window_Height)
    stack_window.setFixedWidth(stack_window_Width)

    stack_window.show()
    # ########################################
    # application = CountCriterion()
    # application.show()
    ############################################
    # application = mywindow()
    # application.show()
    sys.exit(app.exec())

