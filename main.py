from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sqlite3

conn = sqlite3.connect('mylist.db')
c = conn.cursor()
c.execute("""CREATE TABLE if not exists todo_list(list_item text)""")
conn.commit()
conn.close()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(512, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mylist = QtWidgets.QListWidget(self.centralwidget)
        self.mylist.setGeometry(QtCore.QRect(30, 120, 461, 381))
        self.mylist.setObjectName("mylist")
        self.addItemButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.add())
        self.addItemButton.setGeometry(QtCore.QRect(30, 70, 101, 41))
        self.addItemButton.setObjectName("addItemButton")
        self.itemsAdd = QtWidgets.QLineEdit(self.centralwidget)
        self.itemsAdd.setGeometry(QtCore.QRect(30, 20, 461, 41))
        self.itemsAdd.setObjectName("itemsAdd")
        self.delete_Button = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.dele())
        self.delete_Button.setGeometry(QtCore.QRect(150, 70, 101, 41))
        self.delete_Button.setObjectName("delete_Button")
        self.clearAll_Button = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.cleart())
        self.clearAll_Button.setGeometry(QtCore.QRect(270, 70, 101, 41))
        self.clearAll_Button.setObjectName("clearAll_Button")
        self.saveDB_Button = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.saveDB())
        self.saveDB_Button.setGeometry(QtCore.QRect(390, 70, 101, 41))
        self.saveDB_Button.setObjectName("saveDB_Button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 512, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.grab_all()

    def grab_all(self):
        conn = sqlite3.connect('mylist.db')
        c = conn.cursor()
        c.execute("SELECT * FROM todo_list")
        records = c.fetchall()
        conn.commit()
        conn.close()
        for record in records:
            self.mylist.addItem(str(record[0]))

    def add(self):
        item = self.itemsAdd.text()
        self.mylist.addItem(item)
        self.itemsAdd.setText("")

    def dele(self):
        clicked = self.mylist.currentRow()
        self.mylist.takeItem(clicked)
    
    def saveDB(self):
        conn = sqlite3.connect('mylist.db')
        c = conn.cursor()
        c.execute("DELETE FROM todo_list;",)
        
        items = []
        for i in range(self.mylist.count()):
            items.append(self.mylist.item(i))
        
        for item in items:
            c.execute("INSERT INTO todo_list VALUES (:item)",
            { 'item': item.text(),})

        conn.commit()
        conn.close()

        msg = QMessageBox()
        msg.setWindowTitle("Saved To Database")
        msg.setText("Your List Has Been Saved.")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

        
    def cleart(self):
        self.mylist.clear()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ToDo List"))
        self.addItemButton.setText(_translate("MainWindow", "Add Item"))
        self.delete_Button.setText(_translate("MainWindow", "Delete Item"))
        self.clearAll_Button.setText(_translate("MainWindow", "Clear List"))
        self.saveDB_Button.setText(_translate("MainWindow", "Save To DB"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
