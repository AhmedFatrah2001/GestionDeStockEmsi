from tkinter import *
from tkinter import messagebox
from pack import connection as con
from pack.Client import Client as c
from pack.Produit import Produit as p,ListeProduit as lp
from pack.Client import ListeClient as l
from pack.Category import Category as cat
from pack.Fournisseur import Fournisseur as f
from pack.Fournisseur import ListeFournisseur as lf
from pack.Commande import Commande as cmd


def menu(user,r):
    r.destroy()
    cn=con.connection()
    ws =Tk()
    ws['bg']='#f4e2de'
    ws.title("Gestion de Stock")
    ws.geometry("925x500+200+100")
    ws.resizable(False,False)
    def about():
        messagebox.showinfo('PythonGuides', 'Python Guides aims at providing best practical tutorials')

    def getCount(req):
        sql_select_Query = req
        cursor = cn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        return records[0][0]
    menubar = Menu(ws, foreground='black', activebackground='white', activeforeground='black')  
    file = Menu(menubar, tearoff=0, foreground='black')
    role=user[0][3]
    if(role!=1):
        file.add_command(label="Client", state="disabled")  
        file.add_command(label="Produit", state="disabled")  
        file.add_command(label="Fournisseur", state="disabled")  
        file.add_command(label="Commande", state="disabled")
        file.add_command(label="Catégorie", state="disabled")
    else:
        file.add_command(label="Client",command=lambda:c.client(user,ws))  
        file.add_command(label="Produit",command=lambda:p.produit(user,ws))
        file.add_command(label="Fournisseur",command=lambda:f.Fournisseur(user,ws))  
        file.add_command(label="Commande",command=lambda:cmd.commande(user,ws))
        file.add_command(label="Catégorie",command=lambda:cat.Category(user,ws))
    menubar.add_cascade(label="Gérer", menu=file)  

    afficher = Menu(menubar, tearoff=0, foreground='black')  
    afficher.add_command(label="Client",command=lambda:l.listeClient(user,ws))  
    afficher.add_command(label="Produit",command=lambda:lp.listeProduit(user,ws))  
    afficher.add_command(label="Fournisseur",command=lambda:lf.listeFournisseur(user,ws))  
    menubar.add_cascade(label="Affichage", menu=afficher)  
     


    menubar.add_command(label='Exit',command=quit)

    ws.config(menu=menubar)

    #TITRE
    topFrame = Frame(ws, bg="#38184c",width = 925, height=70, relief = 'raised') # , padx = 100, pady=100
    titre=Label(topFrame,text="BONJOUR",bg="#38184c",fg="white",font=('Poppins Bold',50))
    titre.place(relx=0.5, rely=0.5, anchor=CENTER)
    topFrame.grid(row = 0, column = 0, columnspan = 3,  sticky="w",ipady=10)
    #END TITRE

    frame1=Frame(ws,bg='#38184c',width=200,height=150)
    LblnbrClient=Label(frame1,bg='#38184c',text="NOMBRE CLIENT",fg="white",font=('Poppins Bold',13))
    LblnbrClient.place(relx=0.5, rely=0.3,anchor=CENTER)
    nbrClient=Label(frame1,bg='#38184c',text="23",fg="white",font=('Poppins Bold',40))
    nbrClient.place(relx=0.5, rely=0.7, anchor=CENTER)
    frame1.place(x=150,y=140)
    nbrClient.config(text=getCount("select count(*) from client"))

    frame2=Frame(ws,bg='#38184c',width=200,height=150)
    LblnbrCmd=Label(frame2,bg='#38184c',text="NOMBRE COMMANDE",fg="white",font=('Poppins Bold',13))
    LblnbrCmd.place( relx=0.5, rely=0.3,anchor=CENTER)
    nbrCmd=Label(frame2,bg='#38184c',text="23",fg="white",font=('Poppins Bold',40))
    nbrCmd.place(relx=0.5, rely=0.7, anchor=CENTER)
    frame2.place(x=570,y=140)
    nbrCmd.config(text=getCount("select count(*) from commande"))


    frame3=Frame(ws,bg='#38184c',width=200,height=150)
    LblnbrForni=Label(frame3,bg='#38184c',text="NOMBRE FOURNISSEUR",fg="white",font=('Poppins Bold',13))
    LblnbrForni.place(relx=0.5, rely=0.3,anchor=CENTER)
    nbrForni=Label(frame3,bg='#38184c',text="210",fg="white",font=('Poppins Bold',40))
    nbrForni.place(relx=0.5, rely=0.7, anchor=CENTER)
    frame3.place(x=150,y=310)
    nbrForni.config(text=getCount("select count(*) from fournisseur"))

    frame4=Frame(ws,bg='#38184c',width=200,height=150)
    LblnbrProd=Label(frame4,bg='#38184c',text="NOMBRE PRODUIT",fg="white",font=('Poppins Bold',13))
    LblnbrProd.place( relx=0.5, rely=0.3,anchor=CENTER)
    nbrProd=Label(frame4,bg='#38184c',text="0",fg="white",font=('Poppins Bold',40))
    nbrProd.place(relx=0.5, rely=0.7, anchor=CENTER)
    frame4.place(x=570,y=310)
    nbrProd.config(text=getCount("select count(*) from produit"))

    ws.mainloop()
    

