import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtPdf import QPdfDocument

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)


        self.browser = QPdfView(self)
        doc = QPdfDocument(self)
        url = QtCore.QUrl.fromLocalFile("/Users/daisukesakurai/tmp/1-s2.0-S0034487708800031-main.pdf")
        doc.load(url.toLocalFile())
        self.browser.setDocument(doc)

        self.browser.setPageMode(QPdfView.PageMode.MultiPage)
        self.browser.setZoomFactor(2.0)
        # self.browser = QWebEngineView()
        # self.browser.settings().setAttribute(self.browser.settings().WebAttribute.PluginsEnabled, True)
        # self.browser.settings().setAttribute(self.browser.settings().WebAttribute.PdfViewerEnabled, True)
        # self.browser.load(QtCore.QUrl.fromLocalFile("/Users/daisukesakurai/tmp/1-s2.0-S0034487708800031-main.pdf"))
        # self.browser.load(QtCore.QUrl("file:///Users/daisukesakurai/tmp/1-s2.0-S0034487708800031-main.pdf"))

        self.setCentralWidget(self.browser)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
