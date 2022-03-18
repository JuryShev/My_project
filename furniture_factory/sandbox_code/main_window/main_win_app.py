from main_window_des import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from my_project.furniture_factory.sandbox_code.demo_pb_in_mw import Table_start_, Worker_2, PopUpProgressB
from functools import partial
import time
from my_project.furniture_factory.client_app import ServerConnector
import json
import traceback
from PyQt5.QtCore import QThread,pyqtSignal, QObject, pyqtSlot,QRunnable, QThreadPool,QRegExp



def start_process(progress_bar, self=None):
    thread_funct=Worker_2(self.load_struct)
    thread_funct.signals.finished.connect(self.finish)
    thred_progress_bar = Worker_2(partial(progress_bar.proc_counter, status='on'))  # Any other args, kwargs are passed to the run function
    thred_progress_bar.kwargs['progress_callback'] = thred_progress_bar.signals.progress
    thred_progress_bar.signals.result.connect(progress_bar.print_output)
    thred_progress_bar.signals.finished.connect(progress_bar.thread_complete)
    thred_progress_bar.signals.progress.connect(progress_bar.on_count_changed)
    self.threadpool.start(thread_funct)
    self.threadpool.start(thred_progress_bar)

    progress_bar.setWindowModality(QtCore.Qt.ApplicationModal)
    progress_bar.show()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        self._translate = QtCore.QCoreApplication.translate
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.resized.connect(self.someFunction)
        self.center = int(1011 / 2)
        self.center_struct=int(1390/2)
        self.x_start_struct=60
        self.struct=Table_start_()
        self.struct.ButtonNext.setText(self._translate("Form", "ОБНОВИТЬ"))
        #####################################################################
        # self.lay_load_struct = QtWidgets.QWidget()
        # self.lay_load_struct.setObjectName("load_struct")
        # self.frame = QtWidgets.QFrame(self.lay_load_struct)
        # self.frame.setGeometry(QtCore.QRect(30, 40, 1331, 711))
        # self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame.setObjectName("frame")
        # self.struct.setupUi(self.frame)
        # self.struct.label_error.setText(self._translate("Form", "Ошибка"))
        #####################################################################
        self.stackedWidget.addWidget(self.struct)
        self.TB_structure.clicked.connect(self.inside_structure)
        self.TB_search_personal.clicked.connect(self.personal)
        self.progress_bar=PopUpProgressB()
        self.threadpool = QtCore.QThreadPool()
        self.flag_one_load_struct=0

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    def someFunction(self):
            self.w = self.width()
            self.h = self.height()
            self.move_ = int(self.w / 2 - self.x_start)
            self.move_struct = int(self.w / 2 - self.x_start_struct)
            self.groupBox.setGeometry(QtCore.QRect(self.move_-self.center, 30, 1011, 741))
            self.struct.main_frame.setGeometry(QtCore.QRect(self.move_struct-self.center_struct, 30, 1311, 741))

    def load_struct(self):
        row=0
        column=0
        print("load_struct  ")
        name_db='novaja_mebel'
        dir_table_name={"conf_criterion":self.struct.table_conf_criterion,
                        "department":self.struct.table_department,
                        "posts":self.struct.table_posts,
                        "bonus_koeficient":self.struct.table_bonus_koeficient}

        server = ServerConnector("admin", "127.0.0.1", 5000)
        server.name_db = name_db
        try:

            get_json = server.get_struct().content
            get_json = json.loads(get_json.decode('utf-8'))
            for table_server in get_json["tables"]:

                row=0
                table_vision=dir_table_name[table_server]
                table_vision.setRowCount(len(get_json["tables"][table_server]))
                for row_s in get_json["tables"][table_server]:
                    keys_row_s = list(row_s.keys())
                    column=0
                    for key_row_s in keys_row_s[1:]:
                            if type(row_s[key_row_s])==str:
                                table_vision.setItem(row, column, QtWidgets.QTableWidgetItem(row_s[key_row_s]))
                            elif type(row_s[key_row_s])!=str :
                                table_vision.setItem(row, column, QtWidgets.QTableWidgetItem(str(row_s[key_row_s])))
                            column+=1
                    row+=1
        except:
            print("load_struct  2")
            self.struct.label_error.setText(self._translate("Form", "Ошибка подключения к серверу"))
        finally:
             self.progress_bar.status_ = 'ok'


    def cont_test(self):
        a = 0
        for i in range(5):
            time.sleep(0.5)
            print(i)
        self.progress_bar.status_ = 'ok'
        return a

    def finish(self):
        print("finish")
        return None

###############function_button##################################################

    def personal(self):
        print("0")
        self.stackedWidget.setCurrentIndex(0)
        pass

    def analytics(self):
        print("1")
        self.stackedWidget.setCurrentIndex(1)
        pass

    def projects (self):
        print("2")
        self.stackedWidget.setCurrentIndex(2)
        pass

    def inside_structure(self):
        self.stackedWidget.setCurrentIndex(3)
        #self.load_struct()
        if self.flag_one_load_struct==0:
            start_process(self.progress_bar, self=self)
            self.progress_bar.status_ = 'on'
            self.flag_one_load_struct=1

        # self.load_data()



#################################################################################

if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()
    sys.exit(app.exec())


