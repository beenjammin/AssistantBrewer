import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Widget_Styles import getWidgetStylesheet, dockable


class SettingsGUI(QMainWindow):
    def __init__(self,parameters):
        print('initiating settings GUI')
        super().__init__()
        self.parameters = parameters

        self.parameters.settingsGUI['styleCB'] = 'None'
        self.layout = QVBoxLayout()
        gb = QGroupBox('Styling')
        layout = QHBoxLayout()
        lbl = QLabel('Select a style for the GUI')
        cb = QComboBox()
        cb.addItems(list(self.parameters.colours))
        cb.activated.connect(lambda: self.__updateStylesheet())
        cb.setCurrentIndex(4)
        ql = QLineEdit()
        sb = QSpinBox()
        layout.addWidget(lbl)
        layout.addWidget(cb)
        layout.addWidget(ql)
        layout.addWidget(sb)
        self.parameters.settingsGUI['styleCB'] = cb
        self.layout.addLayout(layout)
        gb.setLayout(self.layout)
        self.dock = dockable('Settings')            
        self.dock.addThisWidget(gb)
        self.dock.setCentralWidget()
        self.addDockWidget(Qt.RightDockWidgetArea,self.dock)
        print('added cb')

    def __updateStylesheet(self):
        colour = self.parameters.settingsGUI['styleCB'].currentText()
        styleSheet = getWidgetStylesheet(self, colour=colour)

        print(styleSheet)
        # self.setStyleSheet(styleSheet)
        self.dock.setStyleSheet(styleSheet)
        for widget in self.parameters.mainWindows['BreweryGUI'].children():
            print ('{}'.format(widget))
            if isinstance(widget, dockable):
                widget.setStyleSheet(styleSheet)
