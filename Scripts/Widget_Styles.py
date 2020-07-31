from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Brewery_Parameters import *


class dockable(QDockWidget):
    def __init__(self, *args, **kwargs):
        QDockWidget.__init__(self, *args, **kwargs)
        self.colour = Parameters().colour

        self.sub = QMainWindow()
        self.layout = QVBoxLayout()
        self.sub.setWindowFlags(Qt.Widget)
        self.sub.setDockOptions(Parameters()._DOCK_OPTS)
        self.setWidget(self.sub)
        label = QLabel(args[0])
        label.setAlignment(Qt.AlignCenter)
        stylesheet = """ 
                    QLabel {color : %s;
                            font-weight: bold;
                            background: %s}"""%('white',colourPick(self.colour,'medium'))                  
        label.setStyleSheet(stylesheet)
        self.setTitleBarWidget(label)

        #Styling
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """QDockWidget>QWidget{background:%s}"""%(colourPick(colour,'dark'))+"""
                        QDockWidget>QTabBar::tab:selected {background: %s;color: red}"""%(colourPick(colour,'medium'))+"""
                        QDockWidget::tab {background: %s;color: red}"""%(colourPick(colour,'dark'))
                    # wont apply as styling specified for qtab on vertical_tabs.py               color : white}
               
        self.setStyleSheet(stylesheet)

    def addThisWidget(self,widget):
        self.layout.addWidget(widget)

    def setCentralWidget(self):
        # self.sub.addWidget(widget)
        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.sub.setCentralWidget(centralWidget)

    # def addDockWidget(self,dock,window)

    #     window.addDockWidget(Qt.RightDockWidgetArea,dock)


class groupBox(QGroupBox):
    def __init__(self, *args, **kwargs):
        QGroupBox.__init__(self, *args, **kwargs)

        #Styling
        self.colour = Parameters().colour
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """ 
                    QGroupBox {border: 1px solid black;
                                border-radius: 9px;
                                margin-top: .5em;
                                margin-bottom: .0em;
                                margin-left: .25em;
                                margin-right: .25em;
                                padding: 1px 1px 1px 1px}
                    QGroupBox::title {subcontrol-origin: margin;
                                        left: 10px;
                                        color: black;
                                        padding: 0 3px 0 3px;}
                    """
        self.setStyleSheet(stylesheet)
        
        
class bodyLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)

        #Styling
        self.colour = Parameters().colour
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """ 
                    QLabel {color : %s}"""%('white')                  
        self.setStyleSheet(stylesheet)
        

class bodyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)

        #Styling
        self.colour = Parameters().colour
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """ 
                    QPushButton {background-color:  %s; 
                                border: 1px solid black;
                                border-radius: 4px; color : %s}"""%(colourPick(colour,'light'),'black')+"""
                    QPushButton:checked {background-color: %s; 
                                        border: 1px solid black;
                                        border-radius: 4px;color: %s}"""%(colourPick(colour,'medium'),colourPick(self.colour,'light'))                
        self.setStyleSheet(stylesheet)


class bodyLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        QLineEdit.__init__(self, *args, **kwargs)
        
        #Styling
        self.colour = Parameters().colour
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """ 
                    QLineEdit {background-color:  %s;
                                border: 1px solid black; 
                                color: %s}"""%(colourPick(colour,'light'),colourPick(self.colour,'dark'))             
        self.setStyleSheet(stylesheet)


class bodyComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        QComboBox.__init__(self, *args, **kwargs)
        
        #Styling
        self.colour = Parameters().colour
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """ 
                    QComboBox {background-color:  %s;
                                border: 1px solid black; 
                                color: black}"""%(colourPick(colour,'light'))          
        self.setStyleSheet(stylesheet)

class bodyCheckBox(QCheckBox):
    def __init__(self, *args, **kwargs):
        QCheckBox.__init__(self, *args, **kwargs)
        
        #Styling
        self.colour = Parameters().colour
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """ 
                    QCheckBox {background-color:  %s; 
                                color: black}"""%(colourPick(colour,'light'))          
        self.setStyleSheet(stylesheet)