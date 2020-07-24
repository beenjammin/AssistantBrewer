from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BreweryParameters import Parameters

# QColor.fromHsv(60,50,255).name()
# QColor.fromHsv(60,200,200).name()
# QColor.fromHsv(60,255,100).name()


def colourPick(colour,shade):
    colourDict = {  'green':{'light':'#a9d08e','medium':'#548235','dark':'#375623'},
                    'blue':{'light':'#9bc2e6','medium':'#2f75b5','dark':'#203764'},
                    'orange':{'light':'#f4b084','medium':'#c65911','dark':'#833c0c'},
                    'yellow':{'light':'#ffd966','medium':'#bf8f00','dark':'#806000'},
                    'grey':{'light':'#999999','medium':'#616161','dark':'#383838'}
                    }

    return colourDict[colour][shade]


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
                            background: %s}"""%('white',colourPick(self.colour,'medium'))                  
        label.setStyleSheet(stylesheet)
        self.setTitleBarWidget(label)

        #Styling
        self.applyStyle(self.colour)

    def applyStyle(self,colour):
        stylesheet = """QDockWidget>QWidget{background:%s}"""%(colourPick(colour,'dark'))
                    # QDockWidget {background: %s}"""%(colourPick(colour,'medium'))+"""
                    # QDockWidget::title {text-align: center; 
                    #                     color : white}
               
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

    def applyStyle(self,colours):
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
                                        border-radius: 4px;color: white}"""%(colourPick(colour,'medium'))                
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
                                color: white}"""%(colourPick(colour,'light'))             
        self.setStyleSheet(stylesheet)

