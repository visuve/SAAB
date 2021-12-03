#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtCore import QCoreApplication, QDir
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel


class Saab(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(QDir.currentPath() + "/saab.ui", self)

        self.action_open.triggered.connect(self.open_database)
        self.button_query.clicked.connect(self.query_database)
        self.action_exit.triggered.connect(QCoreApplication.exit)

        self.database = None

    def open_database(self):
        database_path = QFileDialog.getOpenFileName(
            self,
            "Open SQLite database",
            QDir.homePath(),
            "SQLite database (*.sqlite)")[0]

        if not database_path:
            return

        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName(database_path)

        if not self.database.open():
            print(self.database.lastError())

        self.button_query.setEnabled(self.database.isOpen())

    def query_database(self):
        query_model = QSqlQueryModel()
        query_model.setQuery(self.line_edit_query.text())

        self.table_view.setModel(query_model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Saab()
    window.show()
    sys.exit(app.exec())
