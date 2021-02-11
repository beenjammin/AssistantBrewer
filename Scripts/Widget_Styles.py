from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Brewery_Parameters import colourPick, Parameters


def getWidgetStylesheet(self, colour='grey'):
    stylesheet = """ 
                QLabel {color : %s;
                        background: %s}"""%('white',colourPick(colour,'medium'))+"""       
                QDockWidget>QWidget{background:%s}"""%(colourPick(colour,'dark'))+"""
                    QDockWidget>QTabBar::tab:selected {background: %s;color: red}"""%(colourPick(colour,'medium'))+"""
                    QDockWidget::tab {background: %s;color: red}"""%(colourPick(colour,'dark'))+""" 
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
                QLabel {color : %s}"""%('white')+"""
                QPushButton {background-color:  %s; 
                            border: 1px solid black;
                            border-radius: 4px; color : %s}"""%(colourPick(colour,'light'),colourPick(colour,'button_off'))+"""
                QPushButton:checked {background-color: %s; 
                                    border: 1px solid black;
                                    border-radius: 4px;color: %s}"""%(colourPick(colour,'medium'),colourPick(colour,'button_on'))+"""   
                QLineEdit {background-color:  %s;
                            border: 1px solid black; 
                            color: %s}"""%(colourPick(colour,'light'),colourPick(colour,'dark'))+"""
                QComboBox {background-color:  %s;
                            border: 1px solid black; 
                            color: black}"""%(colourPick(colour,'light'))+"""
                QSpinBox {background-color:  %s;
                            border: 1px solid black; 
                            color: %s}"""%(colourPick(colour,'light'),colourPick(colour,'dark'))+"""
                QCheckBox {background-color:  %s; 
                            color: black}"""%(colourPick(colour,'light'))      
    
    return stylesheet                                                            


class dockable(QDockWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.colour = Parameters().colour

        self.sub = QMainWindow()
        self.layout = QVBoxLayout()
        self.sub.setWindowFlags(Qt.Widget)
        # self.sub.setDockOptions(Parameters()._DOCK_OPTS)
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
        super().__init__()

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
        super().__init__(*args, **kwargs)

        #Styling
        self.colour = Parameters().colour
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """ 
                    QLabel {color : %s}"""%('white')                  
        self.setStyleSheet(stylesheet)
        

class bodyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Styling
        self.colour = Parameters().colour
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """ 
                    QPushButton {background-color:  %s; 
                                border: 1px solid %s;
                                border-radius: 4px; color : %s}"""%(colourPick(colour,'medium-dark'),colourPick(colour,'button_off'),colourPick(colour,'button_off'))+"""
                    QPushButton:checked {background-color: %s; 
                                        border: 1px solid %s;
                                        border-radius: 4px;color: %s}"""%(colourPick(colour,'darker'),colourPick(colour,'button_on'),colourPick(self.colour,'button_on'))                
        self.setStyleSheet(stylesheet)


class bodyLineEdit(QLineEdit):
    new_signal = pyqtSignal(str, list)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ls = []
        self.__dict__.update(kwargs)
        self.editingFinished.connect(self.onTextChanged)          
        self.colour = Parameters().colour
        self.applyStyle(self.colour)

    def onTextChanged(self):
        self.new_signal.emit(self.text(), self.ls)

    def applyStyle(self,colour):
        stylesheet = """ 
                    QLineEdit {background-color:  %s;
                                border: 1px solid black; 
                                color: %s}"""%(colourPick(colour,'light'),colourPick(self.colour,'dark'))             
        self.setStyleSheet(stylesheet)


class bodyComboBox(QComboBox):
    new_signal = pyqtSignal(str, str, list)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ls = []
        self.__dict__.update(kwargs)
        self.lastSelected = "None"
        self.activated[str].connect(self.onActivated)        
        #Styling
        self.colour = Parameters().colour
        self.applyStyle(self.colour)

    def onActivated(self, text):
        self.new_signal.emit(self.lastSelected, text, self.ls)
        self.lastSelected = text

    def applyStyle(self,colour):
        stylesheet = """ 
                    QComboBox {background-color:  %s;
                                border: 1px solid black; 
                                color: black}"""%(colourPick(colour,'light'))          
        self.setStyleSheet(stylesheet)


class bodySpinBox(QSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        #Styling
        self.colour = Parameters().colour
        self.setMinimum(0)
        self.setMaximum(86400)
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """ 
                    QSpinBox {background-color:  %s;
                                border: 1px solid black; 
                                color: %s}"""%(colourPick(colour,'light'),colourPick(self.colour,'dark'))             
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