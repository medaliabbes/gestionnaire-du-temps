import sys
import serial
import serial.tools.list_ports as s
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import QThread,QSize,QMetaType
from PyQt5.QtGui import QGuiApplication,QIcon
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction,QComboBox,QPushButton
 
from table1 import users
from historique import history
from entre_sortie import e_s
import database_func
from new_operateur import user
from _thread import *



class my_mainwindow(QMainWindow):
    def __init__(self):
        self.pyport="COM3"
        super().__init__()
        QMainWindow.__init__(self)
        self.setWindowTitle("WC_GESTIONNAIRE")
        self.setMaximumSize(700,500)
        self.setMinimumSize(700,500)
        self.setGeometry(350,50,700,500)
        
        #serialport
        self.ser=serial.Serial()
        #loading icons
        window_icon=QIcon("icons/main_window.png")
        users_icon=QIcon("icons/users_icon.png")
        historique_icon=QIcon("icons/history.png")
        e_s_icon=QIcon("icons/in_out.png")
        about_icon=QIcon("icons/about.png")
        new_user_icon=QIcon("icons/n_user.png")
        #creating menu bare
        self.setWindowIcon(window_icon)
        self.menubar=self.menuBar()
        self.operateur=self.menubar.addMenu("Opérateur")
        self.historique=self.menubar.addMenu('Historique')
        self.entre_sortie=self.menubar.addMenu("Entrées sorties")
        self.pause=self.menubar.addMenu("Pause")
        self.about=self.menubar.addMenu("About")
        #status bare
        self.statusBar() 
        #creating Actions
        self.new_userAction=QAction("Nouveau opérateur")
        self.usersAction=QAction("Opérateurs")
        self.historiqueAction=QAction("Historique")
        self.aboutAction=QAction("This software is created by Mohamed Ali Ben Abbes for SIDILEC International")
        self.pauseAction=QAction("Pause")
        self.entre_sortieAction=QAction("entrées sorties")
        #shortcut
        self.new_userAction.setShortcut("ctrl+N")
        self.usersAction.setShortcut("ctrl+O")
        self.historiqueAction.setShortcut("ctrl+H")
        self.entre_sortieAction.setShortcut("ctrl+E")
        #adding actions
        self.operateur.addAction(self.usersAction)
        self.operateur.addAction(self.new_userAction)
        self.historique.addAction(self.historiqueAction)
        self.about.addAction(self.aboutAction)
        self.entre_sortie.addAction(self.entre_sortieAction)
        self.pause.addAction(self.pauseAction)
        #setting icons
        self.new_userAction.setIcon(new_user_icon)
        self.usersAction.setIcon(users_icon)
        self.historiqueAction.setIcon(historique_icon)
        self.aboutAction.setIcon(about_icon)
        self.entre_sortieAction.setIcon(e_s_icon)
        #button_label_etat
        self.label=QPushButton(self)
        self.label.setGeometry(630,60,50,30)
        #label data from serial port 
        self.data_label=QtWidgets.QLabel(self)
        self.data_label.setGeometry(500,95,100,30)
        #calling the others classes
    
        
        
        #self.entre_s.setParent(self)
        #connectting the actions
        self.usersAction.triggered.connect(self.users)
        self.historiqueAction.triggered.connect(self.history)
        self.new_userAction.triggered.connect(self.new_u)
        self.entre_sortieAction.triggered.connect(self.in_out)
        ##connecting to port 3
        #buttons
        #labels
        y=60
        self.lab_o=QtWidgets.QLabel("<h3><i>Opérateurs</i></h3>",self)
        self.lab_o.setGeometry(80,165+y,100,20)
        self.lab_es=QtWidgets.QLabel("<h3><i>Entrée sortie</i></h3>",self)
        self.lab_es.setGeometry(240,165+y,120,20)
        self.lab_new_o=QtWidgets.QLabel("<h3><i>Ajouter</i></h3>",self)
        self.lab_new_o.setGeometry(100,305+y,100,20)
        self.lab_his=QtWidgets.QLabel("<h3><i>Historique</i></h3>",self)
        self.lab_his.setGeometry(250,305+y,120,20)
        #creating buttons
        self.btn_operateur=QPushButton("",self)
        self.btn_histo=QPushButton("",self)
        self.btn_e_s=QPushButton("",self)
        self.btn_new_o=QPushButton("",self)
        #button position
        self.h=50
        self.btn_operateur.setGeometry(50,50+y,150,60+self.h)
        self.btn_new_o.setGeometry(50,120+self.h+20+y,150,60+self.h)
        self.btn_e_s.setGeometry(210,50+y,150,60+self.h)
        self.btn_histo.setGeometry(210,120+self.h+20+y,150,60+self.h)
        #buttons icons
        self.btn_operateur.setIcon(users_icon)
        self.btn_e_s.setIcon(e_s_icon)
        self.btn_histo.setIcon(historique_icon)
        self.btn_new_o.setIcon(new_user_icon)
        #icons sizes
        self.size_icon=QSize(100,100)
        self.btn_e_s.setIconSize(self.size_icon)
        self.btn_histo.setIconSize(self.size_icon)
        self.btn_new_o.setIconSize(self.size_icon)
        self.btn_operateur.setIconSize(self.size_icon)
        #connecting buttons
        self.btn_e_s.clicked.connect(self.in_out)
        self.btn_histo.clicked.connect(self.history)
        self.btn_operateur.clicked.connect(self.users)
        self.btn_new_o.clicked.connect(self.new_u)
        self.style="""
        QPushButton#add{
            text-align: center;
            color: white;
            border-radius: 12px ;
            font-size: 20px;
        }
        QPushButton#btn{
            text-align: center;
            color: white;
            border-radius: 12px ;
            border: 2px solid #000000;
            font-size: 20px;
        }
        QPushButton#btn1{
            text-align: center;
            color: black;
            border-radius: 8px ;
            border: 0.5px solid #000000;
            font-size: 12px;
        }
        QLabel#lab1{
            border-radius: 70% ;
            border: 0.5px solid #000000;
        }
        QLineEdit{
            border-radius: 5px ;7
            border: 0.5px solid #000000;
        }
        """
        self.btn_e_s.setObjectName("btn")
        self.btn_histo.setObjectName("btn")
        self.btn_operateur.setObjectName("btn")
        self.btn_new_o.setObjectName("btn")
        self.label.setObjectName("add")
        self.connect_to_port()
    def history(self):
    	self.table_e_s=history()
    	
    	self.table_e_s.show()
    def in_out(self):
    	self.entre_s=e_s()
    	self.entre_s.show()
    def users(self):
    	self.table_operateur=users()
    	self.table_operateur.show()
    def new_u(self):
    	self.add_userClass=user()
    	self.add_userClass.show()
    def connect_to_port(self):
        try :#try to connect fonction
            self.ser.port=self.myport
            self.ser.baudrate=115200
            self.ser.parity=serial.PARITY_NONE
            self.ser.stopbits=serial.STOPBITS_ONE
            self.ser.timout=10
            self.ser.xonxoff=False
            self.ser.rtscts=False
            self.ser.dsrdtr=False
            self.ser.writeTimeout=10
            self.ser.open()
            if self.ser.isOpen()==1:
                print("ser state",self.ser.isOpen())
                self.label.setIcon(QIcon('icons/usb_connected.png'))
                start_new_thread(self.run_until_end,())
                print("ser is open && thread is running")
            else :
                self.label.setIcon(QIcon('icons/usb_disconnected.png'))
        except :
            print("error:",sys.exc_info())
            self.label.setIcon(QIcon('icons/usb_disconnected.png'))
        
    def run_until_end(self):
        #saver=saveData()
        print("thread 1 is on")
        while self.ser.isOpen()==1:
            #print("thread is running")
            data_s=self.ser.readline()#read(4)
            print("data prim:",data_s)
            print("got it")
            data_s=str(data_s)
            data_s=data_s[2:6]
            #self.ser.write(str.encode('o'))
            #print("dataserial",data_s)
            try :
                if len(data_s)==0:
                    self.data_label.setText("pas de données")
                if len(data_s)==4:
                    recu=data_s[1:4]
                    #print(data_s[0])
                    #print("recu",recu)
                    self.data_label.setText(str(data_s))
                    rep=database_func.find_pass_word_in_db(recu)
                    self.ser.write(str.encode(rep))
                    database_func.save_mouvement(data_s[0],recu)
                    #self.entre_s.update_table()
                else :
                    pass 
            except :
                print("error :",sys.exc_info())
            
        

application=QApplication(sys.argv)  
mainW=my_mainwindow()
mainW.show()
application.exec_()