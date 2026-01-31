from PyQt5 import QtCore, QtWidgets

class PlainTextEdit(QtWidgets.QPlainTextEdit):
    def focusInEvent(self, event):
        print('event-focus-in:', self.objectName())
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        print('event-focus-out:', self.objectName())
        super().focusOutEvent(event)

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.textEdit = PlainTextEdit(objectName='textEdit')
        self.dateEdit = QtWidgets.QDateEdit(objectName='dateEdit')
        self.button = QtWidgets.QPushButton('Test', objectName='button')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.dateEdit)
        layout.addWidget(self.button)
        self.dateEdit.installEventFilter(self)
        QtWidgets.QApplication.instance().focusObjectChanged.connect(
            self.handleFocusChange)

    def handleFocusChange(self, source):
        print(f'signal-focus-in:', source.objectName())

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.FocusIn:
            print('filter-focus-in:', source.objectName())
        elif event.type() == QtCore.QEvent.FocusOut:
            print('filter-focus-out:', source.objectName())
        return super().eventFilter(source, event)

if __name__ == '__main__':

    # Enable High DPI display with PyQt5
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    
    app = QtWidgets.QApplication(['Test'])
    window = Window()
    window.setGeometry(600, 100, 300, 200)
    window.show()
    app.exec_()