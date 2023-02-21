import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.setWindowTitle("My Browser")
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(0, 0, 1024, 768)

        # create the web view
        self.web_view = QWebEngineView(self)
        self.web_view.setUrl(QUrl('https://www.google.com'))

        # set up JavaScript support
        self.web_channel = QWebChannel()
        self.web_page = QWebEnginePage(self.web_view)
        self.web_page.setWebChannel(self.web_channel)
        self.web_page.settings().setAttribute(
            QWebEngineSettings.JavascriptEnabled, True)
        self.web_page.loadFinished.connect(self.on_load_finished)

        # add the web view to the main window
        self.setCentralWidget(self.web_view)

    def on_load_finished(self):
        self.web_channel.registerObject('browser', self)

        # execute some JavaScript
        self.web_view.page().runJavaScript('console.log("Hello from Python!")')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
