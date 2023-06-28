from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
import sys
from plyer import notification
from onesignal_sdk.client import Client
import sqlite3

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

        # Create a connection to the SQLite database
        self.connection = sqlite3.connect('notifications.db')
        self.cursor = self.connection.cursor()

        # Create the notifications table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT
            )
        ''')

    def send_notification(self):
        # Get the message from the input field
        message = self.message_input.text()

        # Initialize OneSignal client with your OneSignal app ID and REST API key
        client = Client(app_id='dc9e5f19-785f-4106-b38b-39c8a62d96c7', rest_api_key='N2U2OTNjMGItNzkzYy00ODMxLWE1NGEtNmU4NTI5ZWVkYTNk')

        # Create a notification payload
        notification_payload = {
            'contents': {'en': message},  # English message content
            'included_segments': ['All']  # Send to all subscribed segments
        }

        # Send the notification
        response = client.send_notification(notification_payload)

        # Check the status code of the response
        if response.status_code == 200:
            # Insert the notification into the database
            self.cursor.execute('INSERT INTO notifications (message) VALUES (?)', (message,))
            self.connection.commit()

            # Show desktop notification
            notification.notify(
                title='New Message',
                message='You have a new message: {}'.format(message),
                app_icon=None,  # You can specify an icon path if needed
                timeout=10  # The notification will automatically close after 10 seconds
            )

    def closeEvent(self, event):
        # Close the database connection when the application is closed
        self.connection.close()

# Create the application instance and run the event loop
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
