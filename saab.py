#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QCoreApplication, QDir, Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtSql import QSqlDatabase, QSqlQueryModel


class Saab(QMainWindow):
    def __init__(self, parent=None):
        super(Saab, self).__init__(parent)
        loader = QUiLoader()
        loader.setWorkingDirectory(QDir.current())
        self.ui = loader.load("saab.ui", self)
        self.ui.show()

        self.ui.action_open.triggered.connect(self.open_database)
        self.ui.button_query.clicked.connect(self.query_database)
        self.ui.action_exit.triggered.connect(self.exit_application)

        self.database = None

    @Slot()
    def open_database(self):
        database_path = QFileDialog.getOpenFileName(self, "Open SQLite database", QDir.homePath(), "SQLite database (*.sqlite)")[0];

        if not database_path:
            return

        self.database = QSqlDatabase.addDatabase("QSQLITE");
        self.database.setDatabaseName(database_path);

        if not self.database.open():
            print(self.database.lastError())
            return

        self.ui.button_query.setEnabled(True)

    @Slot()
    def query_database(self):
        if not self.database or not self.database.isOpen():
            return

        query_model = QSqlQueryModel()
        query_model.setQuery(self.ui.line_edit_query.text())

        self.ui.table_view.setModel(query_model)


    @Slot()
    def exit_application(self):
        QCoreApplication.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Saab()
    window.show()
    sys.exit(app.exec())

