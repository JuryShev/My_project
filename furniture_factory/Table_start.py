# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Yura\PycharmProjects\pythonProject\my_project\furniture_factory\GUI_designer\table.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Table_start(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(1045, 545)
        Form.setWindowOpacity(2.0)
        Form.setStyleSheet("background-color: rgb(74, 80, 106);")
        self.table_conf_criterion = QtWidgets.QTableWidget(Form)
        self.table_conf_criterion.setGeometry(QtCore.QRect(12, 159, 467, 231))
        self.table_conf_criterion.setStyleSheet("\n"
"background-color: rgb(138, 149, 197);")
        self.table_conf_criterion.setRowCount(1)
        self.table_conf_criterion.setObjectName("tableWidget")
        self.table_conf_criterion.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        item.setFont(font)
        item.setBackground(QtGui.QColor(145, 158, 208, 0))
        self.table_conf_criterion.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        item.setFont(font)
        self.table_conf_criterion.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        self.table_conf_criterion.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.table_conf_criterion.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.table_conf_criterion.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.table_conf_criterion.setItem(0, 2, item)
        self.table_conf_criterion.horizontalHeader().setDefaultSectionSize(150)
        self.table_department = QtWidgets.QTableWidget(Form)
        self.table_department.setGeometry(QtCore.QRect(586, 159, 167, 231))
        self.table_department.setStyleSheet("\n"
"background-color: rgb(138, 149, 197);")
        self.table_department.setRowCount(1)
        self.table_department.setObjectName("tableWidget_2")
        self.table_department.setColumnCount(1)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        item.setFont(font)
        item.setBackground(QtGui.QColor(145, 158, 208, 0))
        self.table_department.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.table_department.setItem(0, 0, item)
        self.table_department.horizontalHeader().setDefaultSectionSize(150)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(480, 159, 105, 231))
        self.frame.setStyleSheet("background-color: rgb(138, 149, 197);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(-1, 70, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setGeometry(QtCore.QRect(-1, 111, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(754, 159, 105, 231))
        self.frame_2.setStyleSheet("background-color: rgb(138, 149, 197);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_4.setGeometry(QtCore.QRect(-1, 70, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_5.setEnabled(True)
        self.pushButton_5.setGeometry(QtCore.QRect(-1, 111, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.ButtonNext = QtWidgets.QPushButton(Form)
        self.ButtonNext.setGeometry(QtCore.QRect(910, 500, 101, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.ButtonNext.setFont(font)
        self.ButtonNext.setStyleSheet("background-color: rgb(168, 182, 240);\n"
"color: rgb(0, 0, 0);")
        self.ButtonNext.setObjectName("ButtonNext")
        self.table_bonus_koeficient = QtWidgets.QTableWidget(Form)
        self.table_bonus_koeficient.setGeometry(QtCore.QRect(860, 159, 171, 231))
        self.table_bonus_koeficient.setStyleSheet("\n"
"background-color: rgb(138, 149, 197);")
        self.table_bonus_koeficient.setAutoScroll(True)
        self.table_bonus_koeficient.setDragDropOverwriteMode(True)
        self.table_bonus_koeficient.setWordWrap(True)
        self.table_bonus_koeficient.setRowCount(1)
        self.table_bonus_koeficient.setObjectName("tableWidget_3")
        self.table_bonus_koeficient.setColumnCount(1)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        item.setFont(font)
        item.setBackground(QtGui.QColor(145, 158, 208, 0))
        self.table_bonus_koeficient.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.table_bonus_koeficient.setItem(0, 0, item)
        self.table_bonus_koeficient.horizontalHeader().setDefaultSectionSize(150)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(165, 130, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(589, 130, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(855, 130, 181, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_name_factory = QtWidgets.QLabel(Form)
        self.label_name_factory.setGeometry(QtCore.QRect(0, 40, 1051, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_name_factory.setFont(font)
        self.label_name_factory.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_name_factory.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name_factory.setObjectName("label_name_factory")
        self.label_error = QtWidgets.QLabel(Form)
        self.label_error.setGeometry(QtCore.QRect(20, 410, 471, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_error.setFont(font)
        self.label_error.setStyleSheet("color: rgb(255, 123, 123);")
        self.label_error.setText("")
        self.label_error.setObjectName("label_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.table_conf_criterion.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Название критерия"))
        item = self.table_conf_criterion.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Максимальный балл"))
        item = self.table_conf_criterion.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Весовой коэффициент"))
        __sortingEnabled = self.table_conf_criterion.isSortingEnabled()
        self.table_conf_criterion.setSortingEnabled(False)
        item = self.table_conf_criterion.item(0, 0)
        item.setText(_translate("Form", "критерий 1"))
        item = self.table_conf_criterion.item(0, 1)
        item.setText(_translate("Form", "5"))
        item = self.table_conf_criterion.item(0, 2)
        item.setText(_translate("Form", "0.5"))
        self.table_conf_criterion.setSortingEnabled(__sortingEnabled)
        item = self.table_department.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Название отдела"))
        __sortingEnabled = self.table_department.isSortingEnabled()
        self.table_department.setSortingEnabled(False)
        item = self.table_department.item(0, 0)
        item.setText(_translate("Form", "Отдел 1"))
        self.table_department.setSortingEnabled(__sortingEnabled)
        self.pushButton_3.setText(_translate("Form", "Добавть"))
        self.pushButton_2.setText(_translate("Form", "Удалить"))
        self.pushButton_4.setText(_translate("Form", "Добавить"))
        self.pushButton_5.setText(_translate("Form", "Удалить"))
        self.ButtonNext.setText(_translate("Form", "ДАЛЕЕ"))
        item = self.table_bonus_koeficient.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Коэффициент от дохода"))
        __sortingEnabled = self.table_bonus_koeficient.isSortingEnabled()
        self.table_bonus_koeficient.setSortingEnabled(False)
        item = self.table_bonus_koeficient.item(0, 0)
        item.setText(_translate("Form", "Отдел 1"))
        self.table_bonus_koeficient.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("Form", "таблица критериев"))
        self.label_4.setText(_translate("Form", "таблица отделов"))
        self.label_2.setText(_translate("Form", "коэффициент от дохода"))
        self.label_name_factory.setText(_translate("Form", " MyFactory"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Table_start()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

