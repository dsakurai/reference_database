import sys
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame, QPushButton
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import QMimeDatabase, QMimeType, QSize
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

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():   # if file(s) have been dragged
            event.acceptProposedAction() # Allow drop

    def dropEvent(self, event):
        file_path = Path(
            event.mimeData().urls()[0].toLocalFile()  # get the path of the first file
        )

        if is_pdf(file_path):
            self.parent().set_document(file_path)

class DbApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)  # to accept drop events
        self.init_ui()
        self.document_path = None

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_edit = QLineEdit()
        self.authors_edit = QLineEdit()

        from WebView import WebView
        layout.addWidget(WebView(self))

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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = DbApp()
    window.show()

    sys.exit(app.exec())
