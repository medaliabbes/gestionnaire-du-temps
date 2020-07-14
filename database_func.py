import sqlite3
import time
from time import strftime,strptime

data_base = "files/effectif.db"

def find_pass_word_in_db(pass_word):
    conn= sqlite3.connect(data_base)
    c=conn.cursor()
    c.execute("SELECT * FROM users WHERE code='{}'".format(pass_word))
    conn.commit()
    exist=c.fetchone()
    c.close()
    conn.close()
    if exist is None :
        return 'N'
    else :
        print("exist")
        return 'O'


def time_cal(d):
    h=int(d/60)
    m=d%60
    hour=str(h)
    mint=str(m)
    if len(hour)==1:
        hour='0'+hour
    if len(mint)==1:
        mint='0'+mint
    else:
        hour=hour
        mint=mint
    return hour+':'+mint

def save_mouvement(a,code):
    #entre_sortie(name TEXT,matricule TEXT ,code TEXT,_date TEXT ,uveme TEXT ,temps TEXT)"
    t=time.localtime()
    #print(t)
    conn=sqlite3.connect(data_base)
    c=conn.cursor()
    c.execute("SELECT * FROM users WHERE code='{}'".format(code))
    conn.commit()
    data=c.fetchone()
    if data is None:
        conn.close()
        #print("not found")
        return
    else :
        date=strftime("%d/%m/%Y",t)
        tnow=strftime("%H:%M",t)
        name=data[0]
        matr=data[2]
        #print('fouded')
        if a=='U':
            #print("fff U")
            c.execute("INSERT INTO entre_sortie VALUES('{}','{}','{}','{}','{}','{}')".format(name,matr,code,date,a,tnow))
            conn.commit()
        if a=='V':
            c.execute("SELECT max(temps) from (select * from entre_sortie where code='{}' and _date='{}' and uveme='U')".format(code,date))
            conn.commit()
            data=c.fetchone()
            st=data[0]
            #print(st)
            if st is None:#maybe_changed_to_data
                c.execute("INSERT INTO entre_sortie VALUES('{}','{}','{}','{}','{}','{}')".format(name,matr,code,date,a,tnow))
                conn.commit()
            else :
                # historiqueES (nom TEXT,code TEXT ,matricule TEXT,_date TEXT,sortie TEXT,retour TEXT,dure TEXT) ")
                temp_sortie=strptime(st,"%H:%M")
                #print("t hour",type(temp_sortie.tm_hour))
                duration=(t.tm_hour*60+t.tm_min)-(temp_sortie.tm_hour*60+temp_sortie.tm_min)
                dur=time_cal(duration)
                print(dur)
                c.execute("INSERT INTO historiqueES VALUES('{}','{}','{}','{}','{}','{}','{}')".format(name,code,matr,date,st,tnow,dur))
                conn.commit()
                c.execute("DELETE FROM entre_sortie WHERE temps='{}' AND code='{}' AND _date='{}' and uveme='U'".format(st,code,date,))
                conn.commit()

    conn.close()