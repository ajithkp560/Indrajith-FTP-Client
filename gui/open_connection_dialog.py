from PyQt6.QtWidgets import QVBoxLayout, QDialog, QHBoxLayout, QLineEdit, QLabel, \
  QPushButton, QApplication

class OpenNewConnectionDialog(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Open New FTP Connection")
    self.setGeometry(100, 100, 300, 150)

    # Layouts
    main_layout = QVBoxLayout()
    form_layout = QVBoxLayout()
    button_layout = QHBoxLayout()

    # Hostname Field
    self.hostname_label = QLabel("Hostname:")
    self.hostname_input = QLineEdit()
    form_layout.addWidget(self.hostname_label)
    form_layout.addWidget(self.hostname_input)

    # Username Field
    self.username_label = QLabel("Username:")
    self.username_input = QLineEdit()
    form_layout.addWidget(self.username_label)
    form_layout.addWidget(self.username_input)

    # Password Field
    self.password_label = QLabel("Password:")
    self.password_input = QLineEdit()
    self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
    form_layout.addWidget(self.password_label)
    form_layout.addWidget(self.password_input)

    # Buttons
    self.ok_button = QPushButton("OK")
    self.cancel_button = QPushButton("Cancel")
    button_layout.addWidget(self.ok_button)
    button_layout.addWidget(self.cancel_button)

    # Connect buttons
    self.ok_button.clicked.connect(self.accept)
    self.cancel_button.clicked.connect(self.reject)

    # Combine layouts
    main_layout.addLayout(form_layout)
    main_layout.addLayout(button_layout)
    self.setLayout(main_layout)

  def get_inputs(self):
    return {
      "hostname": self.hostname_input.text(),
      "username": self.username_input.text(),
      "password": self.password_input.text()
    }

  def center_on_screen(self):
    screen = QApplication.primaryScreen().geometry()
    dialog_geometry = self.geometry()
    x = (screen.width() - dialog_geometry.width()) // 2
    y = (screen.height() - dialog_geometry.height()) // 2
    self.move(x, y)