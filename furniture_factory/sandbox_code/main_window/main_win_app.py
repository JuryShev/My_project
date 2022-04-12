from main_window_des import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QFileDialog
import my_project.furniture_factory.sandbox_code.demo_pb_in_mw as mw
from my_project.furniture_factory.DialofAddPersonal import DialogAddPersonal
from functools import partial
import time
import cv2
from io import BytesIO
import base64
from PIL import Image
import numpy as np
import pickle
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


class ImpDialofAddPersonal(QDialog, DialogAddPersonal):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.rejected.connect(self.reject_)
        self.TB_AddPhoto.clicked.connect(self.AddPhoto)
        self.PersonalData={
        "comand": 2000,
        "user": "admin",
        "db_comand": 1,
        "tables": {"personal":[{"name":"Петров Иван Иванович",
                                        "education": "ГМИ",
                                        "number":"+7(988)-834-15-41",
										"certification": 5,
										"id_posts": 1,
										"id_department":2,
										"salaryl":50000,
										"bonus":0,
                                        "dir_avatar":'q'}
                                       ]}}
        self.PhotoPersonal=''

        ################asteric########################
        self.Asterisk_FamalyName = QtWidgets.QLabel(self)
        self.Asterisk_FamalyName.setEnabled(True)
        self.Asterisk_FamalyName.hide()
        self.Asterisk_FamalyName.setGeometry(QtCore.QRect(297, 52, 17, 17))
        self.Asterisk_FamalyName.setStyleSheet("border-image: url(./icon/asterisk.png);")
        self.Asterisk_FamalyName.setText("")
        self.Asterisk_FamalyName.setObjectName("Asterisk_FamalyName")
        self.Asterisk_Name = QtWidgets.QLabel(self)
        self.Asterisk_Name.hide()
        self.Asterisk_Name.setEnabled(True)
        self.Asterisk_Name.setGeometry(QtCore.QRect(297, 82, 17, 17))
        self.Asterisk_Name.setStyleSheet("border-image: url(./icon/asterisk.png);")
        self.Asterisk_Name.setText("")
        self.Asterisk_Name.setObjectName("Asterisk_Name")
        self.Asterisk_BaseRate = QtWidgets.QLabel(self)
        self.Asterisk_BaseRate.hide()
        self.Asterisk_BaseRate.setEnabled(True)
        self.Asterisk_BaseRate.setGeometry(QtCore.QRect(158, 377, 17, 17))
        self.Asterisk_BaseRate.setStyleSheet("border-image: url(./icon/asterisk.png);")
        self.Asterisk_BaseRate.setText("")
        self.Asterisk_BaseRate.setObjectName("Asterisk_BaseRate")
        self.Asterisk_Attestation = QtWidgets.QLabel(self)
        self.Asterisk_Attestation.setEnabled(True)
        self.Asterisk_Attestation.hide()
        self.Asterisk_Attestation.setGeometry(QtCore.QRect(297, 377, 17, 17))
        self.Asterisk_Attestation.setStyleSheet("border-image: url(./icon/asterisk.png);")
        self.Asterisk_Attestation.setText("")
        self.Asterisk_Attestation.setObjectName("Asterisk_Attestation")
        self.Asterisk_FatherName = QtWidgets.QLabel(self)
        self.Asterisk_FatherName.setEnabled(True)
        self.Asterisk_FatherName.hide()
        self.Asterisk_FatherName.setGeometry(QtCore.QRect(297, 112, 17, 17))
        self.Asterisk_FatherName.setStyleSheet("border-image: url(./icon/asterisk.png);")
        self.Asterisk_FatherName.setText("")
        self.Asterisk_FatherName.setObjectName("Asterisk_FatherName")
        self.Asterisk_Day = QtWidgets.QLabel(self)
        self.Asterisk_Day.setEnabled(True)
        self.Asterisk_Day.hide()
        self.Asterisk_Day.setGeometry(QtCore.QRect(297, 180, 17, 17))
        self.Asterisk_Day.setStyleSheet("border-image: url(./icon/asterisk.png);")
        self.Asterisk_Day.setText("")
        self.Asterisk_Day.setObjectName("Asterisk_Day")
        self.Asterisk_NumberPhone = QtWidgets.QLabel(self)
        self.Asterisk_NumberPhone.setEnabled(True)
        self.Asterisk_NumberPhone.hide()
        self.Asterisk_NumberPhone.setGeometry(QtCore.QRect(297, 240, 17, 17))
        self.Asterisk_NumberPhone.setStyleSheet("border-image: url(./icon/asterisk.png);")
        self.Asterisk_NumberPhone.setText("")
        self.Asterisk_NumberPhone.setObjectName("Asterisk_NumberPhone")
        self.flag_filling=1
        self._translate = QtCore.QCoreApplication.translate
        ################################################
    def accept(self) -> None:

        LE_list=[self.LE_Name,
                 self.LE_FatherName,
                 self.LE_FamilyName,
                 self.LE_NuberPhone,
                 self.LE_Day,
                 self.LE_BaseRate,
                 self.LE_Attestation]

        Asteric_list=[self.Asterisk_Name,
                      self.Asterisk_FatherName,
                      self.Asterisk_FamalyName,
                      self.Asterisk_NumberPhone,
                      self.Asterisk_Day,
                      self.Asterisk_BaseRate,
                      self.Asterisk_Attestation]
        self.Asterisk_NumberPhone.show()
        for id,LE in enumerate(LE_list):
            text=LE.text()
            Asteric_list[id].hide()
            if len(text)==0 or (text.find('+')!=-1 and len(text.replace(' ', ''))<15):
                Asteric_list[id].show()
                self.flag_filling=0

        if self.flag_filling==0:
            print("Не все заполнено")
        if self.flag_filling==1:
            print("все отлично")
            self.close()
            self.flag_filling = 1
            print(f"self.flag_filling={self.flag_filling}")


    def reject_(self) -> None:
        self.close()
        self.flag_filling = 0


    def find_face(self, path):
        img=cv2.imread(path,0)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.1, 4)
        if len(faces)>0:
            x, y, w, h=faces[0]
            percent=0.08
            percent_w=0
            percent_h=0
            max_h, max_w = img.shape
            if max_h<max_w:
                dev=max_w/max_h
                percent_h=percent*dev
                percent_w=percent
            elif max_h>max_w:
                dev=max_h/max_w
                percent_h=percent
                percent_w=percent*dev
            else:
                percent_h=percent
                percent_w=percent

            x_p=0
            w_p=0
            y_p=0
            h_p=0
            if x-max_w*percent_w>0:
                x_p = int(max_w * percent_w)
            if x+w+max_w*percent_w<max_w:
                w_p=int(max_w*percent_w)

            if y-max_h*percent_h>0:
                y_p = int(max_h * percent_h)
            if y+h+max_h*percent_h<max_h:
                h_p=int(max_h*percent_h)
            img = cv2.imread(path)
            face_save=img[y-y_p:y+h+h_p, x-x_p:x+w+w_p , :]
            scale_percent=int(13500/max(face_save.shape))
            width_res = int(face_save.shape[1] * scale_percent / 100)
            height_res = int(face_save.shape[0] * scale_percent / 100)
            dim = (width_res, height_res)
            face_save = cv2.resize(face_save, dim, interpolation=cv2.INTER_AREA)
        else:
            face_save=-1
        return face_save

    def AddPhoto(self):

        face=None
        buffered = BytesIO()
        image_name=QFileDialog.getOpenFileName(self, "Openfile", "./image/", "All Files (*);;PNG files (*.png);; Jpg Files (*.jpg)")
        if len(image_name[0])>0:
            face=self.find_face(image_name[0])


        if type(face)==np.ndarray:
            face_to_json = Image.fromarray(face)
            face_to_json.save(buffered, format="JPEG")
            img_byte = buffered.getvalue()
            img_base64 = base64.b64encode(img_byte)
            self.PhotoPersonal = img_base64.decode('utf-8')
            # ####################pikle img###################
            # with open("img.pickle", "wb") as outfile:
            #     # "wb" argument opens the file in binary mode
            #     pickle.dump(img_base64, outfile)
            # ##########bin to image##########################
            # img = base64.b64decode(img_base64)  # Convert image data converted to base64 to original binary data# bytes
            # img = BytesIO(img)  # _io.Converted to be handled by BytesIO pillow
            # img = Image.open(img)
            # img_shape = img.size
            # face_=np.asarray(img)
            # ################################################

            height, width, channel = face.shape
            bytesPerLine = 3 * width
            qFace = QtGui.QImage(face.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
            self.pixmap = QtGui.QPixmap(qFace)
            self.Label_SpaceImage.setPixmap(self.pixmap)
        elif face==-1:
            self.Label_SpaceImage.setText(self._translate("Dialog", "Загрузите изображения\n с лицом"))





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
        self.WorkWindow.PB_serch_personal.clicked.connect(self.get_personal)

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
        self.WorkWindow.TB_AddPersonal.clicked.connect(self.add_personal)
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
        self.Personal = {
            "comand": 2001,
            "user": "admin",
            "db_comand": 1,
            "tables": {"personal": [{"name": ''
                                     }
                                    ]}}


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

    def add_personal(self):
        print("addpersonal")
        dict_post_id={}
        dict_department_id={}

        dlg = ImpDialofAddPersonal(self)
        self.struct.label_name_factory.setText(self._translate("Form", client.name_db))
        get_json = self.server.get_struct().content
        get_json = json.loads(get_json.decode('utf-8'))
        for  post in get_json["tables"]["posts"]:
            dlg.comboBox_2.addItem(self._translate("Dialog", post['label_post']))
            dict_post_id[post['label_post']]=post['id_posts']
        for department in get_json["tables"]["department"]:
            dlg.comboBox.addItem(self._translate("Dialog", department['title']))
            dict_department_id[department['title']] = department['id_department']
        dlg.exec()
        if dlg.flag_filling==1:
            dlg.PersonalData["tables"]["personal"][0]["name"]=dlg.LE_FamilyName.text()+" "+dlg.LE_Name.text()+" "+dlg.LE_FatherName.text()
            dlg.PersonalData["tables"]["personal"][0]["education"]="-"
            dlg.PersonalData["tables"]["personal"][0]["number"]=dlg.LE_NuberPhone.text()
            dlg.PersonalData["tables"]["personal"][0]["certification"]=int(dlg.LE_Attestation.text())
            dlg.PersonalData["tables"]["personal"][0]["id_posts"]=dict_post_id[dlg.comboBox_2.currentText()]
            dlg.PersonalData["tables"]["personal"][0]["id_department"]=dict_department_id[dlg.comboBox.currentText()]
            dlg.PersonalData["tables"]["personal"][0]["salaryl"]=int(dlg.LE_BaseRate.text())
            dlg.PersonalData["tables"]["personal"][0]["dir_avatar"]=dlg.PhotoPersonal
            result=client.add_personal(dlg.PersonalData).content.decode("utf-8")


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

    def get_personal(self):
        import itertools
        name_personal=self.WorkWindow.LE_serch_personal.text()
        print(name_personal)
        self.Personal["tables"]["personal"][0]["name"]=name_personal
        person=client.get_personal(data_send=self.Personal).content
        person=json.loads(person.decode('utf-8'))
        if len(person)==1:
            person=person[0]

        FamilyName, Name, FatherName=person['name'].split(" ")
        self.WorkWindow.label_surname.setText(self._translate("MainWindow", FamilyName))
        self.WorkWindow.label_name.setText(self._translate("MainWindow", Name +' '+FatherName))
        self.WorkWindow.label_number.setText(self._translate("MainWindow", person['number']))
        self.WorkWindow.label_name_depart.setText(self._translate("MainWindow", person["label_department"]))
        self.WorkWindow.label_name_post.setText(self._translate("MainWindow", person["label_post"]))
        self.WorkWindow.label_salaryl.setText(self._translate("MainWindow", str(person["salaryl"])))
        self.WorkWindow.label_asses_certification.setText(self._translate("MainWindow", str(person["certification"])))
        self.WorkWindow.label_asses_bonus.setText(self._translate("MainWindow", str(person["bonus"])))
        avatar=person["dir_avatar"]
        img = base64.b64decode(avatar)  # Convert image data converted to base64 to original binary data# bytes
        img = BytesIO(img)  # _io.Converted to be handled by BytesIO pillow
        img = Image.open(img)
        face=np.asarray(img)
        height, width, channel = face.shape
        bytesPerLine = 3 * width
        qFace = QtGui.QImage(face.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(qFace)
        self.WorkWindow.label_avatar.setPixmap(pixmap)



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


