from main_window_des import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
import my_project.furniture_factory.sandbox_code.demo_pb_in_mw as mw
from functools import partial
import time
from my_project.furniture_factory.client_app import ServerConnector
import json
import traceback
from PyQt5.QtCore import QThread,pyqtSignal, QObject, pyqtSlot,QRunnable, QThreadPool,QRegExp



def start_process(progress_bar, self=None):
    thread_funct=mw.Worker_2(self.load_struct)
    thread_funct.signals.finished.connect(self.finish)
    thred_progress_bar = mw.Worker_2(partial(progress_bar.proc_counter, status='on'))  # Any other args, kwargs are passed to the run function
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

        self.struct=mw.Table_start_(cr_ed='edit')
        mw.client=mw.config_connect(user='admin')
        self.server=mw.client
        self.struct.refreshButton.clicked.connect(self.refresh_inside_structure)
        self.struct.ButtonNext.setText(self._translate("Form", "ОТПРАВИТЬ"))
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
        self.progress_bar=mw.PopUpProgressB()
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
        print("load_struct")
        name_db='hellow'
        dir_table_name={"conf_criterion":self.struct.table_conf_criterion,
                        "department":self.struct.table_department,
                        "posts":self.struct.table_posts,
                        "bonus_koeficient":self.struct.table_bonus_koeficient}


        self.server.name_db = name_db
        try:

            get_json = self.server.get_struct().content
            get_json = json.loads(get_json.decode('utf-8'))
            self.struct.data_load["tables"]=get_json["tables"].copy()
            #self.struct.data_load["tables"] = get_json["tables"].copy()
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
        if self.flag_one_load_struct==0:
            start_process(self.progress_bar, self=self)
            self.progress_bar.status_ = 'on'
            self.flag_one_load_struct=1

    def refresh_inside_structure(self):
        start_process(self.progress_bar, self=self)
        self.progress_bar.status_ = 'on'
        self.flag_one_load_struct = 1

        # self.load_data()


class MainWindow_all(object):
    resized = QtCore.pyqtSignal()
    def __init__(self, MW):
        # super(MainWindow_all, self).__init__(parent=parent)
        self.x_start = 0
        self.y_start = 0

        self.MW=MW
        self.MW.resized.connect(self.someFunction)
    def setupUi(self):
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.MW.setObjectName("MainWindow")
        self.MW.resize(1500, 901)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MW.sizePolicy().hasHeightForWidth())
        self.MW.setSizePolicy(sizePolicy)
        self.MW.setStyleSheet("background-color: rgb(74, 80, 106);")
        self.centralwidget = QtWidgets.QWidget(self.MW)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(self.x_start, self.y_start, self.screen.width() - self.x_start,
                                                    self.screen.height() - self.y_start))
        self.stackedWidget.setAutoFillBackground(False)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")

        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(MainWindow())
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.stackedWidget.addWidget(self.page_3)

        self.MW.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MW)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1274, 21))
        # self.menubar.setObjectName("menubar")
        # MW.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MW)
        # self.statusbar.setObjectName("statusbar")
        # MW.setStatusBar(self.statusbar)



        self.stackedWidget.setCurrentIndex(0)
        #MW.setWindowFlags(MW.windowFlags()| QtCore.Qt.MSWindowsFixedSizeDialogHint)
        QtCore.QMetaObject.connectSlotsByName(self.MW)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow_all, self).resizeEvent(event)
    def someFunction(self):
            self.w = self.MW.width()
            self.h = self.MW.height()


class MainWindow_all_2(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow_all_2, self).__init__(parent=parent)
        self.x_start = 0
        self.y_start = 0
        self.resized.connect(self.someFunction)
        self.WorkWindow=MainWindow()




    def setupUi(self):
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setObjectName("MainWindow")
        self.resize(1500, 901)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet("background-color: rgb(74, 80, 106);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(self.x_start, self.y_start, self.screen.width() - self.x_start,
                                                    self.screen.height() - self.y_start))
        self.stackedWidget.setAutoFillBackground(False)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")

        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")

        self.stackedWidget.addWidget(self.WorkWindow)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.stackedWidget.addWidget(self.page_3)

        self.setCentralWidget(self.centralwidget)

        # self.menubar = QtWidgets.QMenuBar(MW)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1274, 21))
        # self.menubar.setObjectName("menubar")
        # MW.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MW)
        # self.statusbar.setObjectName("statusbar")
        # MW.setStatusBar(self.statusbar)

        self.stackedWidget.setCurrentIndex(0)

        # MW.setWindowFlags(MW.windowFlags()| QtCore.Qt.MSWindowsFixedSizeDialogHint)
        QtCore.QMetaObject.connectSlotsByName(self)
    def position(self):
        print("pos")
        self.w = self.width()
        self.h = self.height()
        self.move_ = int(self.w / 2 - self.WorkWindow.x_start)
        self.move_struct = int(self.w / 2 - self.WorkWindow.x_start_struct)
        self.WorkWindow.groupBox.setGeometry(QtCore.QRect(1000, 30, 1011, 741))
        self.WorkWindow.struct.main_frame.setGeometry(QtCore.QRect(self.move_struct - self.WorkWindow.center_struct, 30, 1311, 741))

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow_all_2, self).resizeEvent(event)

    def someFunction(self):
        self.w = self.width()
        self.h = self.height()
        self.move_ = int(self.w / 2 - self.WorkWindow.x_start)
        self.move_struct = int(self.w / 2 - self.WorkWindow.x_start_struct)
        self.WorkWindow.groupBox.setGeometry(QtCore.QRect(self.move_ - self.WorkWindow.center, 30, 1011, 741))
        self.WorkWindow.struct.main_frame.setGeometry(QtCore.QRect(self.move_struct - self.WorkWindow.center_struct, 30, 1311, 741))
        print(f"self.width()={self.width()}\nself.height()={self.height()}\n\n")


class MainWindow_all_3(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self, client, parent=None):
        self._translate = QtCore.QCoreApplication.translate
        super(MainWindow_all_3, self).__init__(parent=parent)
        self.x_start = 0
        self.y_start = 0
        self.resized.connect(self.someFunction)
        self.WorkWindow=Ui_MainWindow()
        self.WorkWindow.setupUi(self)


        self.center = int(1011 / 2)
        self.center_struct=int(1390/2)
        self.x_start_struct=60
        self.struct = mw.Table_start_(cr_ed='edit')
        self.server = client
        self.struct.refreshButton.clicked.connect(self.refresh_inside_structure)
        self.struct.ButtonNext.setText(self._translate("Form", "ОТПРАВИТЬ"))

        self.WorkWindow.stackedWidget.addWidget(self.struct)
        self.WorkWindow.TB_structure.clicked.connect(self.inside_structure)
        self.WorkWindow.TB_search_personal.clicked.connect(self.personal)
        self.progress_bar=mw.PopUpProgressB()
        self.threadpool = QtCore.QThreadPool()
        self.flag_one_load_struct=0

        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setObjectName("MainWindow")
        self.resize(1500, 901)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet("background-color: rgb(74, 80, 106);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.GlobalstackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.GlobalstackedWidget.setGeometry(
            QtCore.QRect(self.x_start, self.y_start, self.screen.width() - self.x_start,
                         self.screen.height() - self.y_start))
        self.GlobalstackedWidget.setAutoFillBackground(False)
        self.GlobalstackedWidget.setStyleSheet("")
        self.GlobalstackedWidget.setObjectName("stackedWidget")


        # self.menubar = QtWidgets.QMenuBar(MW)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1274, 21))
        # self.menubar.setObjectName("menubar")
        # MW.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MW)
        # self.statusbar.setObjectName("statusbar")
        # MW.setStatusBar(self.statusbar)

        # self.GlobalstackedWidget.setCurrentIndex(0)

        # MW.setWindowFlags(MW.windowFlags()| QtCore.Qt.MSWindowsFixedSizeDialogHint)
        QtCore.QMetaObject.connectSlotsByName(self)


    def add_worksapace(self):
        self.GlobalstackedWidget.addWidget(self.WorkWindow.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.GlobalstackedWidget.setCurrentIndex(0)
    # def setupUi_(self):
    #     self.screen = QtWidgets.QDesktopWidget().screenGeometry()
    #     self.setObjectName("MainWindow")
    #     self.resize(1500, 901)
    #     sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
    #     sizePolicy.setHorizontalStretch(0)
    #     sizePolicy.setVerticalStretch(0)
    #     sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
    #     self.setSizePolicy(sizePolicy)
    #     self.setStyleSheet("background-color: rgb(74, 80, 106);")
    #     self.centralwidget = QtWidgets.QWidget(self)
    #     self.centralwidget.setObjectName("centralwidget")
    #     self.GlobalstackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
    #     self.GlobalstackedWidget.setGeometry(QtCore.QRect(self.x_start, self.y_start, self.screen.width() - self.x_start,
    #                                                 self.screen.height() - self.y_start))
    #     self.GlobalstackedWidget.setAutoFillBackground(False)
    #     self.GlobalstackedWidget.setStyleSheet("")
    #     self.GlobalstackedWidget.setObjectName("stackedWidget")
    #    # self.GlobalstackedWidget.addWidget(self.WorkWindow.centralwidget)
    #     self.setCentralWidget(self.centralwidget)
    #
    #     # self.menubar = QtWidgets.QMenuBar(MW)
    #     # self.menubar.setGeometry(QtCore.QRect(0, 0, 1274, 21))
    #     # self.menubar.setObjectName("menubar")
    #     # MW.setMenuBar(self.menubar)
    #     # self.statusbar = QtWidgets.QStatusBar(MW)
    #     # self.statusbar.setObjectName("statusbar")
    #     # MW.setStatusBar(self.statusbar)
    #
    #     #self.GlobalstackedWidget.setCurrentIndex(0)
    #
    #     # MW.setWindowFlags(MW.windowFlags()| QtCore.Qt.MSWindowsFixedSizeDialogHint)
    #     QtCore.QMetaObject.connectSlotsByName(self)

    def load_struct(self):
        print("load_struct")
        name_db = 'hellow'
        dir_table_name = {"conf_criterion": self.struct.table_conf_criterion,
                              "department": self.struct.table_department,
                              "posts": self.struct.table_posts,
                              "bonus_koeficient": self.struct.table_bonus_koeficient}

        #self.server.name_db = name_db
        try:
            self.struct.label_name_factory.setText(self._translate("Form", client.name_db))
            get_json = self.server.get_struct().content
            get_json = json.loads(get_json.decode('utf-8'))
            self.struct.data_load["tables"] = get_json["tables"].copy()
            # self.struct.data_load["tables"] = get_json["tables"].copy()
            for table_server in get_json["tables"]:

                row = 0
                table_vision = dir_table_name[table_server]
                table_vision.setRowCount(len(get_json["tables"][table_server]))
                for row_s in get_json["tables"][table_server]:
                    keys_row_s = list(row_s.keys())
                    column = 0
                    for key_row_s in keys_row_s[1:]:
                        if type(row_s[key_row_s]) == str:
                            table_vision.setItem(row, column, QtWidgets.QTableWidgetItem(row_s[key_row_s]))
                        elif type(row_s[key_row_s]) != str:
                             table_vision.setItem(row, column, QtWidgets.QTableWidgetItem(str(row_s[key_row_s])))
                        column += 1
                    row += 1
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
        self.WorkWindow.stackedWidget.setCurrentIndex(0)
        pass

    def analytics(self):
        print("1")
        self.WorkWindow.stackedWidget.setCurrentIndex(1)
        pass

    def projects(self):
        print("2")
        self.WorkWindow.stackedWidget.setCurrentIndex(2)
        pass

    def inside_structure(self):
        self.WorkWindow.stackedWidget.setCurrentIndex(3)
        if self.flag_one_load_struct == 0:
            start_process(self.progress_bar, self=self)
            self.progress_bar.status_ = 'on'
            self.flag_one_load_struct = 1

    def refresh_inside_structure(self):
        start_process(self.progress_bar, self=self)
        self.progress_bar.status_ = 'on'
        self.flag_one_load_struct = 1



    def position(self):
        print("pos")
        self.w = self.width()
        self.h = self.height()
        self.move_ = int(self.w / 2 - self.x_start)
        self.move_struct = int(self.w / 2 - self.x_start_struct)
        self.groupBox.setGeometry(QtCore.QRect(self.move_ - self.center, 30, 1011, 741))
        self.struct.main_frame.setGeometry(QtCore.QRect(self.move_struct - self.center_struct, 30, 1311, 741))

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow_all_3, self).resizeEvent(event)

    def someFunction(self):
        self.w = self.width()
        self.h = self.height()
        self.move_ = int(self.w / 2 - self.WorkWindow.x_start)
        self.move_struct = int(self.w / 2 - self.x_start_struct)
        self.WorkWindow.groupBox.setGeometry(QtCore.QRect(self.move_ - self.center, 30, 1011, 741))
        self.struct.main_frame.setGeometry(QtCore.QRect(self.move_struct - self.center_struct, 30, 1311, 741))
        print(f"self.width()={self.width()}\nself.height()={self.height()}\n\n")

class RuleForm():

    def __init__(self, ui_):
        ui_.resize(500, 500)
        ui_.setWindowFlags(ui_.windowFlags() | QtCore.Qt.MSWindowsFixedSizeDialogHint)



#################################################################################

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw.client=mw.config_connect(user='admin')
    client=mw.client
    # application = QtWidgets.QMainWindow()
    ui = MainWindow_all_3(client)
    table_start_ = mw.Table_start_(ui)
    count_crit = mw.CountCriterion(ui, table_start_)
    start_w = mw.mywindow(ui, count_crit)
    ui.GlobalstackedWidget.addWidget(start_w)
    ui.GlobalstackedWidget.addWidget(count_crit)
    ui.GlobalstackedWidget.addWidget(table_start_)
    ui.add_worksapace()


    # ui.GlobalstackedWidget.addWidget(ui.WorkWindow.centralwidget)




    # ui.position()
    ui.show()
    start_w.maxres()
    sys.exit(app.exec_())
    # import sys
    # app = QtWidgets.QApplication([])
    # application = MainWindow()
    # application.show()
    # sys.exit(app.exec())


