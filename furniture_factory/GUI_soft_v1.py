from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
# Импортируем наш шаблон.
from start_window import Ui_MainWindow
from win_dialog_new_fuctory import Ui_Dialog as creat_dialog
import transliterate
import client_app
import json
import sys

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
        self.name_factory=self.lineEdit.text()
        if u'\u0400' <= self.name_factory <= u'\u04FF' or u'\u0500' <= self.name_factory <= u'\u052F':
            self.name_factory=transliterate.translit(self.name_factory,reversed=True)




    def reject_data(self):
        print('reject')
        self.close()






class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton_Creat.clicked.connect(self.btn_Creat)
        self.ui.pushButton_Open.clicked.connect(self.btn_Open)


    def btn_Creat(self):
        dlg = DialogCreatFactory(self)
        dlg.exec()
        print(dlg.name_factory)
        if len(dlg.name_factory)>0:
            creat = client_app.ServerConnector('0', 'localhost', 5000)
            dlg.name_factory=dlg.name_factory.replace(' ', '_')
            dlg.name_factory = dlg.name_factory.replace("'", '')
            result=creat.add_db(name_db=dlg.name_factory, comand=1111, db_comand=0)
            print(result)

        # if dlg.exec():
        #     print("Success!")
        # else:
        #     print("Cancel!")
        # Dialog = QDialog()
        # ui = creat_dialog()
        # ui.setupUi(Dialog)
        # Dialog.exec()
       # print('creat')
        # Если не использовать, то часть текста исчезнет.
    def btn_Open(self):
        print('open')

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())

