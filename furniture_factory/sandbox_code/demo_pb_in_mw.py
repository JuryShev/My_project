from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QAction
# Импортируем наш шаблон.
from my_project.furniture_factory.start_window import Ui_MainWindow
from my_project.furniture_factory.win_dialog_new_fuctory import Ui_Dialog as creat_dialog
from my_project.furniture_factory.CountCriterion_w import CountCr_2, CountCr
from my_project.furniture_factory.Table_start import Table_start
from my_project.furniture_factory.Table_start_v2 import Table_start_v2
from my_project.furniture_factory.progress_bar import PB_Dialog as PB
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication,\
    QMessageBox,QGraphicsDropShadowEffect,QStyledItemDelegate,QLineEdit
#from progress_bar import PB_Dialog
from PyQt5.QtCore import QThread,pyqtSignal, QObject, pyqtSlot,QRunnable, QThreadPool,QRegExp
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

class NumericDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()
        self.index=2
    def createEditor(self, parent, option, index):
        editor = super(NumericDelegate, self).createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
            validator = QtGui.QRegExpValidator(reg_ex, editor)
            editor.setValidator(validator)
        return editor


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
        self.status_='on'
        self.w_width=784
        self.w_height = 272

    def proc_counter(self, progress_callback, status='on'):  # A slot takes no params
        direct=0
        print("start_PB")
        while self.status_==status:
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
        table_start_.value_criterion = int(self.spinBox_criterion.value())
        table_start_.value_department = int(self.spinBox_departmen.value())
        if table_start_.value_department>0 and table_start_.value_criterion>0:
            stack_window_Height = table_start_.w_height
            stack_window_Width = table_start_.w_width
            table_start_.label_name_factory.setText(_translate("Form", start_w.name_factory_orig))
            table_start_.table_conf_criterion.setRowCount(table_start_.value_criterion)
            table_start_.table_department.setRowCount(table_start_.value_department)
            stack_window.setFixedHeight(stack_window_Height)
            stack_window.setFixedWidth(stack_window_Width)
            stack_window.setCurrentIndex(stack_window.currentIndex() + 1)
            print(f"value_criterion={table_start_.value_criterion}\nvalue_departmen={table_start_.value_department} ")
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

class Table_start_(QWidget, Table_start_v2):
    signal_send_data = pyqtSignal(object)
    signal_receive_data = pyqtSignal(object)

    def __init__(self):
        super( ).__init__()
        self.threadpool = QThreadPool()
        self.setupUi(self)
        self.w_width=1318
        self.w_height = 752
        self.progress_bar = PopUpProgressB()
        self.add_conf_criterion.clicked.connect(self.add_row_criterion)
        self.remove_conf_criterion.clicked.connect(self.drop_row_criterion)
        self.add_department.clicked.connect(self.add_row_department)
        self.remove_department.clicked.connect(self.drop_row_department)
        self.add_post.clicked.connect(self.add_row_post)
        self.remove_post.clicked.connect(self.drop_row_post)
        self.ButtonNext.clicked.connect(self.next)
        self.data_load= {"tables": {}}
        self.data_edit={
                        "tables": {"conf_criterion":[],
                                    "department":   [],
                                    "bonus_koeficient":[],
                                    "posts":[]
                                    }}
        self.data_send={
                        "comand": 5000,
                        "user": "admin",
                        "db_comand": 1,
                        "tables": {"conf_criterion":[],
                                    "department":   [],
                                    "bonus_koeficient":[],
                                    "posts":[]
                                    }}
        self.conf_criterion={"title_criterion":"Порядок_1",
                                        "max_coef": 5,
                                        "w_coef":5.0}
        self.department={"title": "Отдел_1"}
        self.bonus_koeficient={"percentage_of_profits":2.0}
        self.posts={"label_post": "Инженер"}
        self.flag_send_data=0
        self.flag_edit_mode=0
        self.flag_receive_data=0
        self.signal_send_data.connect(self.start_send_data)
        self.signal_receive_data.connect(self.start_work_window)
        # delegate = NumericDelegate(self.tableWidget)
        # self.tableWidget.setItemDelegate(delegate)

        print("ok")
       # self.ButtonNext.clicked.connect(self.next)

    @property
    def check_send_data(self):
        return self.flag_send_data

    @check_send_data.setter
    def check_send_data(self, value):
        self._flag_send_data = value
        self.signal_send_data.emit(value)

    @property
    def check_receive_data(self):
        return self.flag_receive_data

    @check_receive_data.setter
    def check_receive_data(self, value):
        self.flag_receive_data = value
        self.flag_receive_data.emit(value)

    def add_row_criterion(self):
        self.table_conf_criterion.setRowCount(self.table_conf_criterion.rowCount()+1)

    def drop_row_criterion(self):
        self.table_conf_criterion.setRowCount(self.table_conf_criterion.rowCount()-1)

    def add_row_department(self):
        self.table_department.setRowCount(self.table_department.rowCount()+1)

    def drop_row_department(self):
        self.table_department.setRowCount(self.table_department.rowCount()-1)

    def add_row_post(self):
        self.table_posts.setRowCount(self.table_posts.rowCount()+1)

    def drop_row_post(self):
        self.table_posts.setRowCount(self.table_posts.rowCount()-1)

    def all_check(self):
        check_massage = {'conf_criterion': '',
                         'department': '',
                         'bonus_koeficient': '',
                         'posts': ''
                         }
        print("1,0: %s" % self.table_conf_criterion.item(0, 1).text())
        print(self.table_conf_criterion.rowCount())
        check_massage_v = ''
        check_massage['conf_criterion'] = self.chec_type(self.table_conf_criterion, self.conf_criterion)
        check_massage['department'] = self.chec_type(self.table_department, self.department)
        check_massage['bonus_koeficient'] = self.chec_type(self.table_bonus_koeficient, self.bonus_koeficient)
        check_massage['posts'] = self.chec_type(self.table_posts, self.posts)

        for check_massage_k in check_massage:
            check_massage_v = check_massage[check_massage_k]
            if check_massage_v != 'ok':
                break

        if check_massage_v != 'ok':
            # self.label_error.setText(_translate("Form", check_massage_v))
            return check_massage_v

        check_massage['W_coef'] = self.check_procent(self.table_conf_criterion, 2)
        check_massage['percentage_of_profits'] = self.check_procent(self.table_bonus_koeficient, 0)
        check_massage['conf_criterion_duplicate_name'] = self.check_duplicate(self.table_conf_criterion,
                                                                                    self.conf_criterion)
        check_massage['department_duplicate_name'] = self.check_duplicate(self.table_department, self.department)
        check_massage['posts'] = self.check_duplicate(self.table_posts, self.posts)

        for check_massage_k in check_massage:
            check_massage_v = check_massage[check_massage_k]
            if check_massage_v != 'ok':
                break
        return check_massage_v

    def build_data_in_json(self, json_templ):
        self.write_in_data(self.table_conf_criterion, self.conf_criterion, json_templ, 'conf_criterion')
        self.write_in_data(self.table_department, self.department, json_templ, 'department')
        self.write_in_data(self.table_bonus_koeficient, self.bonus_koeficient, json_templ, 'bonus_koeficient')
        self.write_in_data(self.table_posts, self.posts, json_templ,'posts')


    def next(self):

        check_massage_v=self.all_check()
        if check_massage_v!='ok':
            self.label_error.setText(_translate("Form", check_massage_v))
        else:
            self.label_error.setText(_translate("Form", ''))
            print(check_massage_v)
            self.build_data_in_json(self.data_send)
            self.check_send_data = 1

    def refresh(self):
        check_massage_v = self.all_check()
        if check_massage_v != 'ok':
            self.label_error.setText(_translate("Form", check_massage_v))
        else:
            self.label_error.setText(_translate("Form", ''))
            print(check_massage_v)
            self.build_data_in_json(self.data_edit)
            self.check_send_data=2

    def chec_type(self, tablewidget, dir_data):
        list_key = list(dir_data.keys())
        str_type_value=''
        name_column_err=''
        if len(list_key) != tablewidget.columnCount():
            return ('Количество ключей не совпадает с количеством столбцов')
        for row in range(tablewidget.rowCount()):
            for column in range(tablewidget.columnCount()):
                try:
                    value = tablewidget.item(row, column).text()
                except AttributeError :
                        name_column_err = tablewidget.horizontalHeaderItem(column).text()
                        return f"В столбце '{name_column_err}' есть пустые ячейки"
                type_value=type(dir_data[list_key[column]])
                try:
                    value=type_value(value)
                except ValueError:
                    name_column_err= tablewidget.horizontalHeaderItem(column).text()
                    if type_value==int or type_value==float:
                        str_type_value='должно быть число'
                    return f"В столбце '{name_column_err}' {str_type_value}"
                else:
                    if type_value==str:
                        value=value.replace(' ', '')
                        if value.isdecimal():
                            name_column_err = tablewidget.horizontalHeaderItem(column).text()
                            str_type_value = 'должна быть строка'
                            return f"В столбце '{name_column_err}' {str_type_value}"
        return 'ok'

    def check_duplicate(self, tablewidget,  dir_data):
        ind_str_value = []
        set_name=set()

        for ind, val in enumerate(dir_data.values()):
            if type(val) == str:
                ind_str_value.append(ind)

        for column in ind_str_value:
            name_column_err=tablewidget.horizontalHeaderItem(column).text()
            for row in range(tablewidget.rowCount()):
                if tablewidget.item(row, column).text() in set_name:
                    return f"В столбце '{name_column_err}' имя '{tablewidget.item(row, column).text()}' имеет дубликат"
                set_name.add(tablewidget.item(row, column).text())
        return 'ok'

    def check_procent(self, tablewidget, column:int):
        str_check_procent = 'cумма процентов привышает 1'
        full_value=0
        for row in range(tablewidget.rowCount()):
            value = tablewidget.item(row, column).text()
            full_value+=float(value)
        if full_value>1:
            name_column_err = tablewidget.horizontalHeaderItem(column).text()
            return f"В столбце '{name_column_err}' {str_check_procent}"
        return  'ok'

    def write_in_data(self, tablewidget, dir_data, json_templ, name_table):

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

            json_templ["tables"][name_table].append(dir_data.copy())

    def contextMenuEvent(self, event):
        context_menu=QtWidgets.QMenu(self)

        new_action=context_menu.addAction("New")

        action=context_menu.exec_(self.mapToGlobal(event.pos()))

        if action == new_action:
            print("new")

    def start_work_window(self):
        print("start_work_window")

    def start_send_data(self):
        thred_send_data = Worker_2(self.cont_test)
        thred_send_data.signals.finished.connect(self.thread_complete)

        thred_progress_bar = Worker_2(partial(self.progress_bar.proc_counter, status='on')) # Any other args, kwargs are passed to the run function
        thred_progress_bar.kwargs['progress_callback'] = thred_progress_bar.signals.progress
        thred_progress_bar.signals.result.connect(self.progress_bar.print_output)
        thred_progress_bar.signals.finished.connect(self.progress_bar.thread_complete)
        thred_progress_bar.signals.progress.connect(self.progress_bar.on_count_changed)
        self.threadpool.start(thred_send_data)
        self.threadpool.start(thred_progress_bar)

        self.progress_bar.setWindowModality(QtCore.Qt.ApplicationModal)
        self.progress_bar.show()

    def cont_test(self):
        a = 0
        self.progress_bar.status_ = 'on'
        for i in range(5):
            time.sleep(0.5)
            print(i)
        self.progress_bar.status_ = 'ok'
        return a

    def send_data(self):
        self.progress_bar.status_ = 'on'
        if self.check_send_data==1:
            result=client.add_criterion(data_send=self.data_send).content.decode("utf-8")
            self.progress_bar.status_ = result
        elif self.check_send_data==2:
            answer_server = 'none_operation'
            #### del row ##########################################
            # добавили count_del_row строк в конец таблицы
            # отправляем индекс строки на удаления
            # вызвать функцию удаления строк
            for table in self.data_load["tables"]:
                id_dict = {}
                id_list = []
                value_list_copy = self.data_edit["tables"][table]
                value_list = self.data_load["tables"][table]
                count_del_row = len(value_list) - len(value_list_copy)
                if count_del_row > 0:
                    value_list = self.data_load["tables"][table][-count_del_row:]
                    id_key = list(value_list[0].keys())[0]
                    for value_dict in value_list:
                        id_dict[id_key] = value_dict[id_key]
                        id_list.append(id_dict.copy())
                    self.data_send["tables"][table] = id_list
            if len(self.data_send["tables"]) > 0:
                answer_server = client.del_row_table(data_send=self.data_send).content.decode("utf-8")
                self.data_send["tables"].clear()
                print(answer_server)
                if answer_server == 'ok':
                    self.data_load = client.get_struct().content  # загрузка обновленых таблиц
                    self.data_load = json.loads(self.data_load.decode('utf-8'))
            ######################################################################

            ###############add row #####################################################
            if answer_server == 'ok' or answer_server == 'none_operation':
                save_count_add_row = {}
                for table in self.data_load["tables"]:
                    value_add_list = []
                    value_list_copy = self.data_edit["tables"][table]
                    value_list = self.data_load["tables"][table]
                    count_add_row = len(value_list) - len(value_list_copy)
                    save_count_add_row[table] = abs(count_add_row)
                    if count_add_row < 0:
                        value_list_copy = self.data_edit["tables"][table][-abs(count_add_row):]
                        self.data_send["tables"][table] = value_list_copy
                if len(self.data_send["tables"]) > 0:
                    answer_server = client.add_row_table(data_send=self.data_send).content.decode("utf-8")
                    self.data_send["tables"].clear()
                    print(answer_server)
                    if answer_server == 'ok':
                        self.data_load = client.get_struct().content  # загрузка обновленых таблиц
                        self.data_load = json.loads(self.data_load.decode('utf-8'))
                        for table in self.data_load["tables"]:
                            value_list = self.data_load["tables"][table]
                            value_list_copy = self.data_edit["tables"][table].copy()
                            count_add_row = save_count_add_row[table]
                            if count_add_row > 0:
                                value_list_copy[-count_add_row:] = value_list[-count_add_row:]
                                self.data_edit["tables"][table].clear()
                                self.data_edit["tables"][table] = value_list_copy

            #############################################################
            ###############edit row#####################################################
            if answer_server == 'ok' or answer_server == 'none_operation':
                for table in self.data_load["tables"]:
                    value_edit_list = []
                    value_list_copy = self.data_edit["tables"][table]
                    value_list = self.data_load["tables"][table]

                    for v in range(len(value_list)):
                        v_keys = list(value_list[v].keys())
                        equal = value_list[v] == value_list_copy[v]  # проверка на редактирование
                        value_edit_dict = {}
                        if equal == False:
                            value_edit_dict[v_keys[0]] = value_list[v][v_keys[0]]
                            for v_key in v_keys:
                                v_orig = value_list[v][v_key]
                                v_copy = value_list_copy[v][v_key]
                                if v_orig != v_copy:
                                    value_edit_dict[v_key] = v_copy
                        if len(value_edit_dict.keys()) > 0:
                            value_edit_list.append(value_edit_dict)
                    if len(value_edit_list) > 0:
                        self.data_send["tables"][table] = value_edit_list
                client.edit_table(data_send=self.data_send)
            pass

    def thread_complete(self):

        if self.progress_bar.status_ == 'ok':
            print(self.progress_bar.status_)

        else :
            self.label_error.setText(_translate("Form", self.progress_bar.status_))
            print(self.progress_bar.status_)

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
        worker_2 = Worker_2(partial(self.progress_bar.proc_counter, status='on')) # Any other args, kwargs are passed to the run function
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
        client.name_db=self.name_factory_orig
        stack_window.setFixedHeight(stack_window_Height)
        stack_window.setFixedWidth(stack_window_Width)
        stack_window.setCurrentIndex(stack_window.currentIndex()+1)

    def cont_test(self):
        a = 0
        for i in range(5):
            time.sleep(0.5)
            print(i)
        self.progress_bar.status_ = 'ok'
        return a

    def start_creat_factory(self):
        result = client.add_db(comand=1111, db_comand=1).content.decode("utf-8")
        self.progress_bar.status_ = result

    def thread_complete(self):
        print(self.progress_bar.status_)
        if self.progress_bar.status_=='ok':
            self.flag_server=1
            self.progress_bar.status_ = ''

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

    client = client_app.ServerConnector('0', 'localhost', 5000)
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

