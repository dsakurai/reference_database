import sys
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QFrame, QPushButton, QMainWindow
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import QMimeDatabase, QMimeType, QSize
from PyQt6.QtPdf import QPdfDocument
from pathlib import Path
import database

def is_pdf(file_path: Path):
    mime_database = QMimeDatabase()
    # Guess the filetype possibly looking into the file contents
    mime_type = mime_database.mimeTypeForFile(str(file_path))
    return mime_type.name() == 'application/pdf'

class DropArea(QFrame):

    def __init__(self, parent):
        super().__init__(parent)

        # You could set some style to distinguish the DropArea visually.
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setLineWidth(1)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setFixedSize(QSize(100, 100))

        self.setAcceptDrops(True)

        self.image = None

    def set_image(self, image): # image is QImage or None
        self.image = image

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():   # if file(s) have been dragged
            event.acceptProposedAction() # Allow drop

    def dropEvent(self, event):
        file_path = Path(
            event.mimeData().urls()[0].toLocalFile()  # get the path of the first file
        )

        if is_pdf(file_path):
            # Keep the document
            self.parent().set_document(file_path)

            # and set the thumbnail iamge
            self.set_image(
                self.render_pdf(file_path)
            )

    # Paint the PDF thumbnail
    def paintEvent(self, event):

        if self.image is not None:
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

            scaled_image = self.image.scaled(self.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)

            # Calculating the center of the widget
            x = (self.width() - scaled_image.width()) // 2
            y = (self.height() - scaled_image.height()) // 2

            # Draw the image at the center of the widget
            painter.drawImage(QtCore.QPoint(x, y), scaled_image)
        else:
            super().paintEvent(event)

    def render_pdf(self, file_path: Path): # Returns a QImage object

        doc = QPdfDocument(self)

        url = QtCore.QUrl.fromLocalFile(str(file_path))
        doc.load(url.toLocalFile())

        image = doc.render(0, self.size())
        doc.deleteLater()

        return image


class Database_row_widget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setAcceptDrops(True)  # to accept drop events
        self.init_ui()
        self.document_path = None

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_edit = QLineEdit()
        self.authors_edit = QLineEdit()

        layout.addWidget(QLabel("authors", self))
        layout.addWidget(self.authors_edit)

        layout.addWidget(QLabel("title", self))
        layout.addWidget(self.title_edit)

        self.drop_area = DropArea(self)
        layout.addWidget(self.drop_area)

        btn_write = QPushButton("Write to DB")
        btn_write.clicked.connect(self.write_to_db)
        layout.addWidget(btn_write)

        self.setLayout(layout)

    def set_document(self, document_path: Path):
        self.document_path = document_path

    def write_to_db(self):

        document_binary = None

        if self.document_path:
            with open(self.document_path, 'rb') as f:
                document_binary = f.read() # bytes

        database.add_row(database.Publication(
            title=self.title_edit.text(),
            authors=self.authors_edit.text(),
            document=document_binary
        ))

        self.title_edit.setText(None)
        self.authors_edit.setText(None)
        self.document_path = None
        self.drop_area.set_image(None)
        self.update() # Repaint the widget (especially the thumbnail.)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.document_path = None

    def init_ui(self):

        centralWidget = QFrame(self)
        self.setCentralWidget(centralWidget)

        layout = QHBoxLayout()
        centralWidget.setLayout(layout)

        from WebView import WebView
        layout.addWidget(WebView(self))

        layout.addWidget(Database_row_widget(self))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
