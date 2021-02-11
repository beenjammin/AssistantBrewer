from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createStatusBar()
        self.createDockWindows()

        self.setWindowTitle("Dock Widgets")

        self.newLetter()
        self.setUnifiedTitleAndToolBarOnMac(True)

    def newLetter(self):
        self.textEdit.clear()
        cursor = QTextCursor(self.textEdit.textCursor())
        cursor.movePosition(QTextCursor.Start)
        topFrame = cursor.currentFrame()
        topFrameFormat = topFrame.frameFormat()
        topFrameFormat.setPadding(16)
        topFrame.setFrameFormat(topFrameFormat)

        textFormat = QTextCharFormat()
        boldFormat = QTextCharFormat()
        boldFormat.setFontWeight(QFont.Bold)
        italicFormat = QTextCharFormat()
        italicFormat.setFontItalic(True)

        tableFormat = QTextTableFormat()
        tableFormat.setBorder(1)
        tableFormat.setCellPadding(16)
        tableFormat.setAlignment(QtCore.Qt.AlignRight)
        cursor.insertTable(1, 1, tableFormat)
        cursor.insertText("The Firm", boldFormat)
        cursor.insertBlock()
        cursor.insertText("321 City Street", textFormat)
        cursor.insertBlock()
        cursor.insertText("Industry Park")
        cursor.insertBlock()
        cursor.insertText("Some Country")
        cursor.setPosition(topFrame.lastPosition())
        cursor.insertText(QtCore.QDate.currentDate().toString("d MMMM yyyy"), textFormat)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText("Dear ", textFormat)
        cursor.insertText("NAME", italicFormat)
        cursor.insertText(",", textFormat)

        for i in range(3): 
            cursor.insertBlock()

        cursor.insertText("Yours sincerely,", textFormat)

        for i in range(3):  
            cursor.insertBlock()

        cursor.insertText("The Boss", textFormat)
        cursor.insertBlock()
        cursor.insertText("ADDRESS", italicFormat)

    def print_(self):
        document = self.textEdit.document()
        printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        if dlg.exec() != QDialog.Accepted: 
            return

        document.print_(printer)
        self.statusBar().showMessage("Ready", 2000)

    def save(self):
        fileName = QFileDialog.getSaveFileName(self,
                        "Choose a file name", ".", "HTML document (*.html *.htm)")

        if not fileName:
            return

        file = QtCore.QFile(fileName)

        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QMessageBox.warning(self, "Dock Widgets",
                             "Cannot write file {}:\n{}."
                             .format(QtCore.QDir.toNativeSeparators(fileName), file.errorString()))
            return

        out = QTextStream(file)
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        out << textEdit.toHtml()
        QApplication.restoreOverrideCursor()
        self.statusBar().showMessage("Saved '{}'".format(fileName), 2000)

    def undo(self):
        document = self.textEdit.document()
        document.undo()

    def insertCustomer(self, customer):
        if not customer:
            return
        customerList = customer.split(", ")
        document = self.textEdit.document()
        cursor = document.find("NAME")

        if not cursor.isNull():
            cursor.beginEditBlock()
            cursor.insertText(customerList[0])
            oldcursor = cursor
            cursor = document.find("ADDRESS")
            if not cursor.isNull():
                for c in customerList:
                    cursor.insertBlock()
                    cursor.insertText(c)

                cursor.endEditBlock()
            else:
                oldcursor.endEditBlock()

    def addParagraph(self, paragraph):
        if not paragraph:
            return
        document = self.textEdit.document()
        cursor = document.find("Yours sincerely,")

        if cursor.isNull():
            return

        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor, 2)
        cursor.insertBlock()
        cursor.insertText(paragraph)
        cursor.insertBlock()
        cursor.endEditBlock()

    def about(self):
        QMessageBox.about(self, "About Dock Widgets",
               "The <b>Dock Widgets</b> example demonstrates how to "
               "use Qt's dock widgets. You can enter your own text, "
               "click a customer to add a customer name and "
               "address, and click standard paragraphs to add them.")

    def createActions(self):
        fileMenu = self.menuBar().addMenu("&File")
        fileToolBar = self.addToolBar("File")

        newIcon = QIcon.fromTheme("document-new", QIcon(":/images/new.png"))
        newLetterAct = QAction(newIcon, "&New Letter", self)
        newLetterAct.setShortcuts(QKeySequence.New)
        newLetterAct.setStatusTip("Create a new form letter")
        newLetterAct.triggered.connect(self.newLetter)
        fileMenu.addAction(newLetterAct)
        fileToolBar.addAction(newLetterAct)

        saveIcon = QIcon.fromTheme("document-save", QIcon(":/images/save.png"))
        saveAct = QAction(saveIcon, "&Save...", self)
        saveAct.setShortcuts(QKeySequence.Save)
        saveAct.setStatusTip("Save the current form letter")
        saveAct.triggered.connect(self.save)
        fileMenu.addAction(saveAct)
        fileToolBar.addAction(saveAct)

        printIcon = QIcon.fromTheme("document-print", QIcon(":/images/print.png"))
        printAct = QAction(printIcon,"&Print...", self)
        printAct.setShortcuts(QKeySequence.Print)
        printAct.setStatusTip("Print the current form letter")
        printAct.triggered.connect(self.print_)
        fileMenu.addAction(printAct)
        fileToolBar.addAction(printAct)

        fileMenu.addSeparator()

        quitAct = fileMenu.addAction("&Quit", self.close)
        quitAct.setShortcuts(QKeySequence.Quit)
        quitAct.setStatusTip("Quit the application")

        editMenu = self.menuBar().addMenu("&Edit")
        editToolBar = self.addToolBar("Edit")
        undoIcon = QIcon.fromTheme("edit-undo", QIcon(":/images/undo.png"))
        undoAct = QAction(undoIcon, "&Undo", self)
        undoAct.setShortcuts(QKeySequence.Undo)
        undoAct.setStatusTip("Undo the last editing action")
        undoAct.triggered.connect(self.undo)
        editMenu.addAction(undoAct)
        editToolBar.addAction(undoAct)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        helpMenu = self.menuBar().addMenu("&Help")

        aboutAct = helpMenu.addAction("&About", self.about)
        aboutAct.setStatusTip("Show the application's About box")

        aboutQtAct = helpMenu.addAction("About &Qt", qApp.aboutQt)
        aboutQtAct.setStatusTip("Show the Qt library's About box")

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        dock = QDockWidget("Customers", self)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.customerList = QListWidget(dock)
        self.customerList.addItems([
            "John Doe, Harmony Enterprises, 12 Lakeside, Ambleton",
            "Jane Doe, Memorabilia, 23 Watersedge, Beaton",
            "Tammy Shea, Tiblanka, 38 Sea Views, Carlton",
            "Tim Sheen, Caraba Gifts, 48 Ocean Way, Deal",
            "Sol Harvey, Chicos Coffee, 53 New Springs, Eccleston",
            "Sally Hobart, Tiroli Tea, 67 Long River, Fedula"])
        dock.setWidget(self.customerList)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())


        dock = QDockWidget("Paragraphs", self)
        self.paragraphsList = QListWidget(dock)
        self.paragraphsList.addItems([
            """Thank you for your payment which we have received today.""",
            """Your order has been dispatched and should be with you \
within 28 days.""",
            """We have dispatched those items that were in stock. The \
rest of your order will be dispatched once all the \
remaining items have arrived at our warehouse. No \
additional shipping charges will be made.""",
            """You made a small overpayment (less than $5) which we \
will keep on account for you, or return at your request.""",
            """You made a small underpayment (less than $1), but we have \
sent your order anyway. We'll add this underpayment to \
your next bill.""",
            """Unfortunately you did not send enough money. Please remit \
an additional $. Your order will be dispatched as soon as \
the complete amount has been received.""",
            """You made an overpayment (more than $5). Do you wish to \
buy more items, or should we return the excess to you?"""])

        dock.setWidget(self.paragraphsList);
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        self.customerList.currentTextChanged.connect(self.insertCustomer)
        self.paragraphsList.currentTextChanged.connect(self.addParagraph)

# import dockwidgets_rc

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())