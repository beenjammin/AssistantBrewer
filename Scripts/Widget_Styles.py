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
    # if colour == 'grey':
    #     shadeDict = {   'light': [0,255],
    #                         'medium' : [0,200],
    #                         'dark' : [0,100]}
    # else:
    #     shadeDict = {   'light': [50,255],
    #                     'medium' : [200,200],
    #                     'dark' : [255,100]}
    # colourDict = {'yellow':60,'red':0,'purple':300,'blue':240,'green':60,'grey':60}

    # return QColor.fromHsv(colourDict[colour],shadeDict[shade][0],shadeDict[shade][1]).name()


class dockable(QDockWidget):
    def __init__(self, *args, **kwargs):
        QDockWidget.__init__(self, *args, **kwargs)
        self.sub = QMainWindow()
        self.sub.setWindowFlags(Qt.Widget)
        self.sub.setDockOptions(Parameters()._DOCK_OPTS)
        self.setWidget(self.sub)   

        #Styling
        self.colour = Parameters().colour
        stylesheet = """ 
                    QDockWidget {background: %s}"""%(colourPick(self.colour,'medium'))+"""
                    QDockWidget::title {text-align: center; 
                                        color : white}
                    QDockWidget>QWidget{background:%s}"""%(colourPick(self.colour,'dark'))
        self.setStyleSheet(stylesheet)

    def setThisWidget(self,widget):
        self.sub.setCentralWidget(widget)

    # def addDockWidget(self,dock,window)

    #     window.addDockWidget(Qt.RightDockWidgetArea,dock)


class groupBox(QGroupBox):
    def __init__(self, *args, **kwargs):
        QGroupBox.__init__(self, *args, **kwargs)

        #Styling
        self.colour = Parameters().colour
        stylesheet = """ 
                    QGroupBox {border: 1px solid black;
                                border-radius: 9px;
                                margin-top: 0.5em;
                                margin: 3px}
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
        stylesheet = """ 
                    QLabel {color : %s}"""%('white')                  
        self.setStyleSheet(stylesheet)
        

class bodyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)

        #Styling
        self.colour = Parameters().colour
        stylesheet = """ 
                    QPushButton {background-color:  %s; 
                                border: 1px solid black;
                                border-radius: 4px; color : %s}"""%(colourPick(self.colour,'light'),'black')+"""
                    QPushButton:checked {background-color: %s; 
                                        border: 1px solid black;
                                        border-radius: 4px;color: white}"""%(colourPick(self.colour,'medium'))                
        self.setStyleSheet(stylesheet)


class bodyLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        QLineEdit.__init__(self, *args, **kwargs)
        
        #Styling
        self.colour = Parameters().colour
        stylesheet = """ 
                    QLineEdit {background-color:  %s;
                                border: 1px solid black; 
                                color: white}"""%(colourPick(self.colour,'light'))             
        self.setStyleSheet(stylesheet)

