
from PyQt6.QtCore import QUrl, QStandardPaths
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineDownloadRequest, QWebEngineSettings
import os
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-pdf-extension"

class WebView(QWebEngineView):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setUrl(QUrl("http://scholar.google.co.jp"))

        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )

        # Handle downloads
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.downloadRequested.connect(self.handle_download)

        self.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        # self.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        # self.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)

    def handle_download(self, download: QWebEngineDownloadRequest):

        download_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
        # Ensure directory exists
        os.makedirs(download_dir, exist_ok=True)

        print(download_dir)
        download.setDownloadDirectory(download_dir)
        download.accept()

