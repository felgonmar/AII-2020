#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
from whoosh.support.unicode import uppercase


def extraer_datos():
    f = urllib.request.urlopen("https://www.vinissimus.com/es/vinos/tinto/")
    s = BeautifulSoup(f,"lxml") 
    l = s.find("table", class_= ["table product product-view-2"])
    lf = l.find_all("tr", class_ = ["warning",""])
    return lf

def almacenar_bd():
    conn = sqlite3.connect('vinos.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS VINOS")
    conn.execute('''CREATE TABLE VINOS
       (NOMBRE                    TEXT    NOT NULL,
       PRECIO                     TEXT    NOT NULL,
       DENOMINACION ORIGEN        TEXT    NOT NULL,
       BODEGA                     TEXT    NOT NULL,
       TIPO UVA                   TEXT    NOT NULL);''')
    lf = extraer_datos()
    for i in lf:
        nombre = i.h3.a.string
        precio = list(i.find("span", class_=["price"]).stripped_strings)
        if precio.__len__() == 2:
            precio = precio[1]
        else:
            precio = precio[0]    
        den_orii = i.find("span", class_=["type"]).get_text()
        den_ori=den_orii[den_orii.find(",")+2 : den_orii.find("(")-1]
        bodega = i.find("span", class_=["owner"]).get_text()
        uva  = i.find("span", class_=["grape"]).get_text().replace(" ","").strip()
        uva = ''.join(uva.split())
        
        print( precio)
        conn.execute("""INSERT INTO VINOS VALUES (?,?,?,?,?)""",(nombre,precio,den_ori,bodega,uva))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM VINOS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()

def imprimir_lista(cursor):
    v = Toplevel()
    v.title("VINO ")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    jornada=0
    for row in cursor:
        if row[0] != jornada:
            jornada=row[0]
            lb.insert(END,"\n")
            s = 'VINOS'+ str(jornada)
            lb.insert(END,s)
            lb.insert(END,"-----------------------------------------------------")
        s = "     " + row[1] +' '+ str(row[3]) +'-'+ str(row[4]) +' '+  row[2]
        lb.insert(END,s)
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)

def listar_bd():
    conn = sqlite3.connect('vinos.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT * FROM VINOS ORDER BY NOMBRE")
    imprimir_lista(cursor)
    conn.close()




def ventana_principal():
    top = Tk()
    Datos = Button(top, text="Datos", command = almacenar_bd())
    Datos.pack(side = LEFT)
    Buscar = Button(top, text="Buscar")
    Buscar.pack(side = LEFT)
   
    listar = Button(top, text="Listar vinos", command = listar_bd)
    listar.pack(side = TOP)

    top.mainloop()


if __name__ == "__main__":
    ventana_principal()