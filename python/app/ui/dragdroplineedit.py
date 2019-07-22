import sys
from sgtk.platform.qt import QtCore, QtGui


class DragDropLineEdit(QtGui.QLineEdit):
    def __init__(self, parent):
        super(DragDropLineEdit, self).__init__(parent)

        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            # for some reason, this doubles up the intro slash
            filepath = str(urls[0].path())[1:]  # Windows/OSX returns a "/" at start of file path ie: "/X:/temp"

            if sys.platform == 'linux2':    # Linux doesn't return "/" at start of file path
                filepath = str(urls[0].path())

            self.setText(filepath)
