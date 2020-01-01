import os
import subprocess
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        self.check = QPushButton(central_widget)
        self.check.setText("Check for update")
        self.check.clicked.connect(self.openAutoUpdater)
        main_layout.addWidget(self.check)
        self.setCentralWidget(central_widget)

    def findAutoUpdaterLocation(self):
        executable = sys.executable
        (all_last_dir, folder) = os.path.split(executable)
        (all_before_last_dir, last_dir) = os.path.split(all_last_dir)
        (all_before_before_last_dir, before_last_dir) = os.path.split(all_before_last_dir)
        if last_dir == 'MacOS' and before_last_dir == 'Contents':
            # For MacOS, the updater app should be located in Resources folder
            folder = os.path.join(all_before_last_dir, "Resources")
        else:
            folder = all_last_dir
        return folder

    def openAutoUpdater(self):
        folder = self.findAutoUpdaterLocation()
        script = os.path.join(folder, 'AutoUpdater.exe' if sys.platform.startswith('win') else 'AutoUpdater')
        try:
            process = subprocess.run([script])
            process.check_returncode()

            # Restart app
            os.execlp(sys.executable, *sys.argv)
        except subprocess.CalledProcessError as e:
            print('Exception occurred, e: ', e)


def run():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
