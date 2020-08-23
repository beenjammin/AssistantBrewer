from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt5.QtGui import QPalette, QColor

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.flag = False

        self.button = QPushButton('change the colors of the buttons', self)
        self.button.clicked.connect(self.click)
        lay = QVBoxLayout(self)
        lay.addWidget(self.button)

        stylesheet = """
                    QPushButton {background-color:  %s;
                                border: 5px solid black;
                                border-radius: 4px; color : %s}"""%('red','white')
        self.button.setStyleSheet(stylesheet)


    def click(self):
        print("click")
        if not self.flag:
            stylesheet = """
                    QPushButton {background-color:  %s;
                                border: 1px solid black;
                                border-radius: 4px; color : %s}"""%('red','white')
            self.button.setStyleSheet(stylesheet)

        else:
            stylesheet = """
                        QPushButton {background-color:  %s;
                                    border: 1px solid black;
                                    border-radius: 4px; color : %s}"""%('green','red')
            self.button.setStyleSheet(stylesheet)

        self.flag = not self.flag


if __name__ == '__main__':
    import sys
    app = QApplication([])

    app.setStyle('Fusion')                              # <-----

    w = Window()
    w.show()
    sys.exit(app.exec_())