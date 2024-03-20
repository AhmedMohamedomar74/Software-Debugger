import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QLabel
import serial

class SerialCommunication(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Serial Communication')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.combo = QComboBox()
        self.combo.addItems(['COM1', 'COM2', 'COM3'])
        layout.addWidget(self.combo)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText('Enter register address (hex)')
        layout.addWidget(self.address_input)

        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText('Enter data to send (hex)')
        layout.addWidget(self.data_input)

        self.send_button = QPushButton('Send Data')
        self.send_button.clicked.connect(self.send_data)
        layout.addWidget(self.send_button)

        self.receive_button = QPushButton('Receive Data')
        self.receive_button.clicked.connect(self.receive_data)
        layout.addWidget(self.receive_button)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.received_data_label = QLabel()
        layout.addWidget(self.received_data_label)

        self.setLayout(layout)

    def send_data(self):
        port = self.combo.currentText()
        address = self.address_input.text()
        data = self.data_input.text()
        self.send_serial_data(port, address, data)

    def receive_data(self):
        port = self.combo.currentText()
        address = self.address_input.text()
        received_data = self.receive_serial_data(port, address)
        if received_data is not None:
            self.received_data_label.setText(f"Received data for register {address}: 0x{received_data:0X}")
        else:
            self.received_data_label.setText("No data received.")

    def send_serial_data(self, port, address, data):
        try:
            address_dec = int(address, 16)
            data_dec = int(data, 16)
        except ValueError:
            self.status_label.setText('Invalid input. Please enter hexadecimal values.')
            return

        try:
            ser = serial.Serial(port, 9600, timeout=1)
            ser.write(b'@')  # Start flag
            ser.write(b'R')  # 'R' for read
            ser.write(address_dec.to_bytes(1, 'big'))
            ser.write(data_dec.to_bytes(1, 'big'))
            ser.write(b';')  # End flag
            ser.close()
            self.status_label.setText(f"Data '{data}' sent successfully to register {address} on {port}")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def receive_serial_data(self, port, address):
        try:
            address_dec = int(address, 16)
        except ValueError:
            self.status_label.setText('Invalid input. Please enter hexadecimal values.')
            return None

        try:
            ser = serial.Serial(port, 9600, timeout=1)
            ser.write(b'@')  # Start flag
            ser.write(b'W')  # 'W' for write
            ser.write(address_dec.to_bytes(1, 'big'))
            received_data = ser.read(1)
            ser.write(b';')  # End flag
            ser.close()
            return int.from_bytes(received_data, 'big')
        except Exception as e:
            self.status_label.setText(f"Error: {e}")
            return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialCommunication()
    window.show()
    sys.exit(app.exec_())
