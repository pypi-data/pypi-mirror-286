"""
__main__ file for obsELN package, used to run the package as a
standalone application.
"""
import sys
from PyQt5.QtWidgets import QApplication
from obsELN.gui.obsidian_import_gui import ObsidianImportGUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ObsidianImportGUI()
    window.show()
    sys.exit(app.exec_())
