# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 14:23:31 2020

@author: BTHRO
"""
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json, ast

from Brewery_Parameters import Parameters
from Brewery_GUI import BreweryGUI
from Settings_GUI import SettingsGUI


class TabBar(QTabBar):
    def tabSizeHint(self, index):
        return QSize(150, 60)


    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt);
            painter.restore()


class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)
        stylesheet = """ 
                    QTabBar::tab:selected {background: black;color: white}
                    QTabWidget>QWidget>QWidget{background: black}
                    """

        self.setStyleSheet(stylesheet)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QTabWidget.West)

class ProxyStyle(QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QStyle.PM_TabBarIconSize)
            r = QRect(opt.rect)
            w =  0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QProxyStyle.drawControl(self, element, opt, painter, widget)

class Main():
    def __init__(self,parameters):
        self.parameters = parameters
        app = QApplication(sys.argv)
        QApplication.setStyle(ProxyStyle())
        w = TabWidget()
        label = QLabel('hi')
        label2 = QLabel('so')
        vlayout = QVBoxLayout()
        vlayout.addWidget(label) 
        vlayout.addWidget(label2)
        theCrush = QWidget()
        theCrush.setLayout(vlayout)
        
        docks = BreweryGUI(self.parameters)
        vlayout = QVBoxLayout()
        vlayout.addWidget(docks) 
        brewDay = QWidget()
        brewDay.setLayout(vlayout)
        
        setting = SettingsGUI(self.parameters)
        vlayout = QVBoxLayout()
        vlayout.addWidget(setting) 
        settingW = QWidget()
        settingW.setLayout(vlayout)
        
        w.addTab(brewDay,QIcon("beer.png"), "Brew Day")
        w.addTab(theCrush,QIcon("crush.png"), "The Crush")
        w.addTab(QWidget(),QIcon("mash.png"), "The Mash")
        w.addTab(QWidget(),QIcon("hops.png"), "The Boil")
        w.addTab(settingW,QIcon("settings.png"), "Settings")
    #    w.addTab(QWidget(), QIcon("zoom-out.png"), "XYZ")
        w.setWindowTitle("Assistant to the Regional Brewer")
        w.resize(1200, 800)
        w.show()

        sys.exit(app.exec_())   

if __name__ == '__main__':
    import sys
    parameters = Parameters()
    a =Main(parameters)
    
