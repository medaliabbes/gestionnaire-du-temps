import sys 
import sqlite3 as sq
from PyQt5.QtCore import Qt,QEvent
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtGui import QGuiApplication,QIcon
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QLabel,QPushButton,QWidget,QAction,QLineEdit
database="files/effectif.db"

class user(QWidget):
    def __init__(self):
        #self.app=QApplication(sys.argv)
        super().__init__()
        QWidget.__init__(self)
        self.window_icon=QIcon("icons/n_user.png")
        self.setGeometry(500,60,300,450)
        self.setWindowIcon(self.window_icon)
        self.setWindowTitle("Nouveau opérateur")
        #style
        #label
        self.image=QImage("icons/man.png")
        #self.image.resize(QSize(100,100))
        self.label_i=QLabel("",self)
        self.label_i.setGeometry(25,30,250,150)
        self.label_i.setPixmap(QPixmap.fromImage(self.image))
        #self.label_i.setStyleSheet("background-color :#6e6e6e")
        self.label_i.setScaledContents(True)
        #creating entry field
        self.name_entry=QLineEdit(self)
        self.name_entry.setGeometry(25,200,250,40)
        self.name_entry.setText("Nom")
        self.code_entry=QLineEdit(self)
        self.code_entry.setGeometry(25,260,250,40)
        self.code_entry.setText("Code")
        self.matricule=QLineEdit(self)
        self.matricule.setGeometry(25,320,250,40)
        self.matricule.setText("Matr")
        #button
        self.btn_add=QPushButton("Ajoute",self)
        self.btn_add.setGeometry(25,380,250,40)
        self.btn_add.clicked.connect(self.add_user_onclick)
        self.code_entry.installEventFilter(self)
        self.btn_add.setObjectName("btn1")
        #self.label_i.setObjectName("lab1")

    def add_user_onclick(self):
        name=self.name_entry.text()
        code=self.code_entry.text()
        matr=self.matricule.text()
        #print(name,code,matr)
        if len(code)!=3:
            self.code_entry.setStyleSheet("color :#E10C0C;")
            self.code_entry.setText("3 chiffre pour le code ")
            #self.code_entry.setStyleSheet("color :#000000;")
            return
        try :
            conn=sq.connect(database)
            c=conn.cursor()
            c.execute("SELECT *FROM users WHERE code='{}'".format(code))
            conn.commit()
            res=c.fetchone()
            if res==None :
                c.execute("INSERT INTO users VALUES('{}','{}','{}','{}')".format(name,code,matr,'O'))
                conn.commit()
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("opérateur ajouté")
                msg.exec()
                self.matricule.setText("matr")
                self.name_entry.setText("Nom")
                self.code_entry.setText("Code")
            else :
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("mot de passe existe ")
                self.code_entry.setText("")
                msg.exec()
        except :
            print("error:",sys.exc_info())
    def eventFilter(self,s ,e):
        if e.type()==QEvent.KeyPress and s is self.code_entry:
            self.code_entry.setStyleSheet("color :#000000;")
        return super(user, self).eventFilter(s,e)