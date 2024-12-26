from ftplib import FTP

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QStandardItemModel


class FTP_Functions(QObject):
  finished = pyqtSignal()
  dataReady = pyqtSignal(list)

  def __init__(self, hostname, username, password):
    super().__init__()
    self.hostname = hostname
    self.username = username
    self.password = password

    self.ftp = FTP(self.hostname)
    self.ftp.login(self.username, self.password)

  @pyqtSlot()
  def list_files(self, path):
    try:
      if self.is_directory(path):
        # print(path)
        items = []
        self.ftp.cwd(path)
        files = []
        self.ftp.retrlines("LIST", files.append)
        for line in files:
          # print(line)
          parts = line.split()
          name = parts[-1]
          is_dir = line[0] == 'd'
          size = int(parts[4]) if not is_dir else 0
          items.append((name, size, is_dir))
        self.dataReady.emit(items)
    except Exception as e:
      print(f"Error listing directory {path}: {e}")
      self.dataReady.emit([])
    finally:
      self.finished.emit()

  def is_directory(self, path):
    current = self.ftp.pwd()
    try:
      self.ftp.cwd(path)
      self.ftp.cwd(current)  # Restore the current directory
      return True
    except Exception:
      return False