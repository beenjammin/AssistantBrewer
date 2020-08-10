from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random


class UI_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1300, 800)
        self.btnA = QtWidgets.QPushButton(Dialog)
        self.btnA.setGeometry(QtCore.QRect(10, 80, 101, 131))
        self.btnA.setObjectName("btn1")

        self.formLayout = QtWidgets.QFormLayout()
        self.groupBox = QtWidgets.QGroupBox("Results")
        self.groupBox.setLayout(self.formLayout)
        self.resultScrollArea = QtWidgets.QScrollArea(Dialog)
        self.resultScrollArea.setWidget(self.groupBox)
        self.resultScrollArea.setGeometry(QtCore.QRect(20, 220, 1011, 531))
        self.resultScrollArea.setWidgetResizable(True)
        self.resultScrollArea.setObjectName("resultScrollArea")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Example Program"))
        self.btnA.setText(_translate("Dialog", "Push Button"))


class Dialog(QtWidgets.QDialog, UI_Dialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.btnA.clicked.connect(self.pushed)

    @QtCore.pyqtSlot()
    def pushed(self):
        unkownLength = random.randint(1, 5)
        self.addButtons(unkownLength)

    def addButtons(self, looping):
        for button in self.groupBox.findChildren(QtWidgets.QPushButton):
            button.deleteLater()
        placement = -100
        pos = QtCore.QPoint(20, 40)
        HLayout = QtWidgets.QHBoxLayout()
        for i in range(looping):
            currentName = "btn" + str(i)
            self.btnB = QtWidgets.QPushButton(currentName)
#            self.btnB.setGeometry(QtCore.QRect(pos, QtCore.QSize(100, 100)))
#            pos += QtCore.QPoint(110, 110)
            HLayout.addWidget(self.btnB)
        self.groupBox.setLayout(HLayout)
        self.groupBox.show()
        print('success')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())