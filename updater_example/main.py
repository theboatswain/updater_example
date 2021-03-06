#  This file is part of Boatswain.
#
#      Boatswain <https://github.com/theboatswain> is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Boatswain is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#

import json
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

        # Automatic check for update when we start the main application
        # You can do this in background every specified period of time
        print("Starting to check the update status in background...")
        if self.checkForUpdate():
            self.openAutoUpdater()

        # Or we can have a button for user to click check-for-update
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
        script = os.path.join(folder, 'AutoUpdater.exe' if sys.platform.startswith('win') else 'AutoUpdater')
        return script

    def checkForUpdate(self):
        script = self.findAutoUpdaterLocation()
        try:
            process = subprocess.run([script, '--checking-mode=True'], stdout=subprocess.PIPE)
            res = process.stdout.decode('utf-8')
            update = json.loads(res)
            return update['has_release']
        except subprocess.CalledProcessError as e:
            print('Exception occurred, e: ', e)

    def openAutoUpdater(self):
        script = self.findAutoUpdaterLocation()
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
