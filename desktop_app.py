from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
import sys

# Define the main window of the application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Desktop App')
        self.setGeometry(100, 100, 300, 200)

        # Create a line edit widget for message input
        self.message_input = QLineEdit(self)
        self.message_input.setGeometry(50, 30, 200, 30)

        # Create a button
        self.button = QPushButton('Send Notification', self)
        self.button.setGeometry(100, 80, 100, 30)
        self.button.clicked.connect(self.send_notification)

        # Create a system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('./Safetybug white.png'))  # Set your desired icon path here
        self.tray_icon.setToolTip('Desktop App')
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # Create a context menu for the tray icon
        self.tray_menu = QMenu(self)
        self.show_action = QAction('Show', self)
        self.show_action.triggered.connect(self.show_application)
        self.quit_action = QAction('Quit', self)
        self.quit_action.triggered.connect(self.quit_application)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)

    def send_notification(self):
        # Get the message from the input field
        message = self.message_input.text()

        # Show tray notification
        self.tray_icon.showMessage('New Message', message, QSystemTrayIcon.Information, 10000)

    def tray_icon_activated(self, reason):
        # Show the application window when the tray icon is clicked
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_application()

    def show_application(self):
        # Show the application window
        self.show()

    def quit_application(self):
        # Clean up and quit the application
        self.tray_icon.hide()
        QApplication.quit()

# Create the application instance and run the event loop
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the application icon
    app_icon = QIcon('./Safetybug white.png')  # Set your desired icon path here
    app.setWindowIcon(app_icon)

    window = MainWindow()

    # Show the main window initially
    window.show()

    # Show the tray icon
    window.tray_icon.show()

    sys.exit(app.exec_())
