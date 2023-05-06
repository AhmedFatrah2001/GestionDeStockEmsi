from codecs import namereplace_errors
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from unicodedata import name
from pack import menu as me,connection as con
from pack.Client import ListeClient as l,Client as c
from pack.Category import Category as cat
from pack.Fournisseur import Fournisseur as f , ListeFournisseur as lf
from pack.Produit import Produit as p,ListeProduit as lp


def commande(user,s):
    s.destroy()
    cn=con.connection()
    role=user[0][3]
    def empty():
            quantite.delete(0, 'end')
            qteL.delete(0, 'end')
            rechercher.delete(0, 'end')
            rechercher3.delete(0, 'end')
            prodL.set("")
            prodN.set("")
    def isEmpty():
            if  quantite.get()=="" or produitDropDown.current()==-1 or clientDropDown.current==-1 :
                    return True
            return False
    def isEmpty1():
            if  qteL.get()=="" or produitDropDownL.current()==-1 :
                    return True
            return False
    def hasRows(req):
                sql_select_Query = req
                cursor = cn.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
                return len(records)!=0
    def insert():
            if not isEmpty():
                    qte=quantite.get()
                    prod=idsProduit[produitDropDown.current()]
                    clt=idsClient[clientDropDown.current()]
                    mycursor = cn.cursor()
                    produit=getData("select quantite from produit where id={}".format(prod))
                    if int(qte) > produit[0][0]:
                            messagebox.showwarning("Attention","Stock inssufisant")
                    else:
                        execQry("UPDATE PRODUIT SET QUANTITE=QUANTITE-{} where id={}".format(qte,prod))
                        sql = ("INSERT INTO commande (id_client,date) VALUES ({},CURRENT_DATE())".format(clt))
                        mycursor.execute(sql)
                        cn.commit()
                        idCmd=getData("select max(id) from commande")[0][0]
                        sql=("INSERT INTO ligneCommande (id_commande,id_produit,quantite) values (%s,%s,%s)")
                        val=(idCmd,prod,qte)
                        mycursor = cn.cursor()
                        mycursor.execute(sql,val)
                        cn.commit()
                        fillTree("select co.id,c.nom,date from commande co inner join client c on (co.id_client=c.id)")
                        fillTree1("select l.id_commande,p.nom,l.quantite,p.prix from lignecommande l on produit p on p.id=l.id_produit where id_commande={}".format(idCmd))
                        afficherTotal()
            else:
                    messagebox.showwarning("Attenstion","tous les champs sont obligatoires!!!!!!")
    def insertProd():
            if not isEmpty1() and rechercher.get()!="":
                    qte=qteL.get()
                    prod=idsProduit[produitDropDownL.current()]
                    idCmd=rechercher.get()
                    mycursor = cn.cursor()
                    produit=getData("select quantite from produit where id={}".format(prod))
                    produit1=getData("select quantite from lignecommande where id_produit={} and id_commande={}".format(prod,idCmd))
                    if not hasRows("select * from lignecommande where id_produit={} and id_commande={}".format(prod,idCmd)):
                            if int(qte) > produit[0][0]:
                                        messagebox.showwarning("Attention","Stock inssufisant")
                            else:
                                        sql = ("INSERT INTO lignecommande (id_commande,id_produit,quantite) VALUES ({},{},{})".format(idCmd,prod,qte))
                                        execQry("UPDATE PRODUIT SET QUANTITE=QUANTITE-{} where id={}".format(qte,prod))
                    else:
                        if int(qte) > produit[0][0]:
                                messagebox.showwarning("Attention","Stock inssufisant")
                        else:
                                sql = ("UPDATE lignecommande SET quantite=quantite+{} where id_commande={} and id_produit={}".format(qte,idCmd,prod))
                                execQry("UPDATE PRODUIT SET QUANTITE=QUANTITE-{} where id={}".format(qte,prod))
                    mycursor.execute(sql)
                    cn.commit()
                    fillTree1("select l.id_commande,p.nom,l.quantite,p.prix from lignecommande l inner join produit p on (p.id=l.id_produit) where id_commande={}".format(idCmd))
                    afficherTotal()
            else:
                    messagebox.showwarning("Attenstion","tous les champs sont obligatoires!!!!!!")
    def edit():
                prod=idsProduit[produitDropDownL.current()]
                prodExist=hasRows("select * from lignecommande where id_produit='{}' and id_commande={}".format(prod,rechercher.get()))
                if not isEmpty1():
                        if prodExist:
                                test=messagebox.askquestion("Modifier produit","voulez-vous vraiment modifier le produit {} ?".format(prodL.get()))
                                if test=="yes":
                                         qte=qteL.get()
                                         prod=idsProduit[produitDropDownL.current()]
                                         idCmd=rechercher.get()
                                         mycursor = cn.cursor()
                                         
                                         produit=getData("select quantite from produit where id={}".format(prod))
                                         produit1=getData("select quantite from lignecommande where id_produit={} and id_commande={}".format(prod,idCmd))
                                         if int(qte) > produit[0][0]+produit1[0][0]:
                                                 messagebox.showwarning("Attention","Stock inssufisant")
                                         else:
                                                 execQry("UPDATE PRODUIT SET QUANTITE=QUANTITE+{}-{} where id={}".format(produit1[0][0],qte,prod))
                                                 sql=("UPDATE lignecommande SET quantite={} where id_produit={}".format(qte,prod))
                                                 mycursor.execute(sql)
                                                 cn.commit()
                                                 empty()
                                                 for i in tree3.get_children():
                                                        tree3.delete(i)
                                                 fillTree1("select l.id_commande,p.nom,l.quantite,p.prix from lignecommande l inner join produit p on (p.id=l.id_produit) where id_commande={}".format(idCmd))
                                                 afficherTotal()


                        else:
                                messagebox.showinfo("Attention","Ce produit que vous rechercher n'existe pas")
                else :
                        messagebox.showwarning("Attention","tous les champs sont obligatoires!!!!!!")

    def delete():
                commandeExist=hasRows("select * from commande where id='{}'".format(rechercher.get()))
                if rechercher.get()!="":
                        if commandeExist:
                                test=messagebox.askquestion("Supprimer commande","voulez-vous vraiment supprimer la commande {} ?".format(rechercher.get()))
                                if test=="yes":
                                        idCmd=rechercher.get()
                                        mycursor = cn.cursor()
                                        sql = ("DELETE FROM ligneCommande WHERE id_commande={}".format(idCmd))
                                        mycursor.execute(sql)
                                        cn.commit()
                                        sql = ("DELETE FROM commande WHERE id={}".format(idCmd))
                                        mycursor.execute(sql)
                                        cn.commit()
                                        empty()
                                        fillTree("select co.id,c.nom,date from commande co inner join client c on (co.id_client=c.id)")
                                        afficherTotal()

                        else:
                                messagebox.showinfo("Attention","Ce produit que vous rechercher n'existe pas")

                else:
                        messagebox.showwarning("Attenstion","Le champs Numero est obligatoire !!")
    def deleteProd():
                prod=idsProduit[produitDropDownL.current()]
                prodExist=hasRows("select * from lignecommande where id_produit='{}' and id_commande={}".format(prod,rechercher.get()))
                if produitDropDownL.current()!=-1:
                        if prodExist:
                                test=messagebox.askquestion("Supprimer commande","voulez-vous vraiment supprimer le produit {} ?".format(prodL.get()))
                                if test=="yes":
                                        idCmd=rechercher.get()
                                        mycursor = cn.cursor()
                                        qte=qteL.get()
                                        sql = ("DELETE FROM ligneCommande WHERE id_commande={} and id_produit={}".format(idCmd,prod))
                                        execQry("UPDATE PRODUIT SET QUANTITE=QUANTITE+{} where id={}".format(qte,prod))
                                        mycursor.execute(sql)
                                        cn.commit()
                                        empty()
                                        fillTree1("select l.id_commande,p.nom,l.quantite,p.prix from lignecommande l inner join produit p on (p.id=l.id_produit) where l.id_commande={}".format(idCmd))
                                        afficherTotal()

                        else:
                                messagebox.showinfo("Attention","Ce produit que vous rechercher n'existe pas")

                else:
                        messagebox.showwarning("Attenstion","Le champs Numero est obligatoire !!")
    def search(sv):
                var=sv.get()
                print(var)
                fillTree("select d.id,c.nom,date from commande d inner join client c on (c.id=d.id_client) where c.nom like '{0}%' or d.id='{0}'".format(var))
                
    def search1(sv1):
                var=sv1.get()
                fillTree1("select l.id_commande,p.nom,l.quantite,p.prix from lignecommande l inner join produit p on (l.id_produit=p.id) where p.nom like '{}%' and l.id_commande='{}'".format(var,rechercher.get()))
    def execQry(req):
                mycursor = cn.cursor()
                mycursor.execute(req)
                cn.commit()


    def getData(req):  
        cursor = cn.cursor()
        cursor.execute(req)
        records = cursor.fetchall()
        return records
    def selectItem(a):
                curItem = tree.focus()
                commande=(tree.item(curItem))['values']
                rechercher.delete(0, 'end')
                rechercher.insert(0,commande[0])
                fillTree1("select l.id_commande,p.nom,l.quantite,p.prix from lignecommande l INNER JOIN produit p on (p.id=l.id_produit) where id_commande={}".format(commande[0]))   
                afficherTotal()
    def selectItem1(a):
                curItem = tree3.focus()
                commande=(tree3.item(curItem))['values']
                rechercher3.delete(0, 'end')
                qteL.delete(0, 'end')
                qteL.insert(0,commande[2])
                prodL.set(commande[1])
    def fillTree(req):
                sql_select_Query = req
                cursor = cn.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
                
                for i in tree.get_children():
                    tree.delete(i)
                for row in records:
                        tree.insert("",END, values=row)
    def afficherTotal():
            totals=getData("select sum(l.quantite*p.prix) from lignecommande l inner join produit p on (l.id_produit=p.id) where l.id_commande={}".format(rechercher.get()))
            total1=totals[0][0]
            Total.config(text=total1)
    def fillTree1(req):
                sql_select_Query = req
                cursor = cn.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
                
                for i in tree3.get_children():
                    tree3.delete(i)
                for row in records:
                        tree3.insert("",END, values=row)
                    
    win=Tk()
    win['bg']='#f4e2de'
    win.title('Gérer client')
    win.geometry("1100x660+100+10")
    win.resizable(False,False)


   #MENU BAR
    menubar1 = Menu(win, foreground='black', activebackground='white', activeforeground='black')  
    file = Menu(menubar1, tearoff=0, foreground='black')
    if(role!=1):
        file.add_command(label="Client", state="disabled")  
        file.add_command(label="Produit", state="disabled")  
        file.add_command(label="Fournisseur", state="disabled")  
        file.add_command(label="Commande", state="disabled")
        file.add_command(label="Catégorie", state="disabled")
    else:
        file.add_command(label="Client",command=lambda:c.client(user,win))  
        file.add_command(label="Produit",command=lambda:p.produit(user,win))
        file.add_command(label="Fournisseur",command=lambda:f.Fournisseur(user,win))  
        file.add_command(label="Commande",state="disabled")
        file.add_command(label="Catégorie",command=lambda:cat.Category(user,win))
    menubar1.add_cascade(label="Gérer", menu=file)  

    afficher = Menu(menubar1, tearoff=0, foreground='black')  
    afficher.add_command(label="Client",command=lambda:l.listeClient(user,win))  
    afficher.add_command(label="Produit",command=lambda:lp.listeProduit(user,win))  
    afficher.add_command(label="Fournisseur",command=lambda:lf.listeFournisseur(user,win))  
    menubar1.add_cascade(label="Affichage", menu=afficher)  
            
    


    menubar1.add_command(label='Exit',command=quit)

    win.config(menu=menubar1)
    #END MENU BAR
    

    #TITRE
    topFrame = Frame(win, bg = '#38184c', width = 1100, height=60, relief = 'raised') # , padx = 100, pady=100
    titre=Label(topFrame,text="GESTION COMMANDES",bg = '#38184c',fg="white",font=('Poppins Bold',25))
    logo=Label(topFrame,text="EMSI STOCK",bg = '#38184c',fg="white",font=('Poppins Bold',25))
    logo.place(x=10,y=2)
    titre.place(x=710,y=0)
    topFrame.grid(row = 0, column = 0, sticky="w")
    #END TITRE

    #Section 1
    section1=Frame(win,bg='#f4e2de',width = 925,relief = 'raised')
    section1.grid(row = 1, column = 0,padx=50,pady=20,sticky="w")

    #ID
    idLbl=Label(section1,bg='#f4e2de', anchor = 'center', text='Produit',font=('Poppins Medium',10))
    idLbl.grid(row = 0, column = 0, sticky = 'w',padx=30,pady=5)

    namesProduit =[]

    idsProduit =[]

    for i in getData("select id,nom from produit"):

            idsProduit.append(i[0])
            namesProduit.append(i[1])

    prodN = StringVar()
    produitDropDown=ttk.Combobox(section1,width=17, textvariable = prodN )
    produitDropDown.grid(row = 0, column = 1, sticky = 'e',columnspan=2)

    produitDropDown["values"]=namesProduit
    #END ID



    #name
    nameLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Client',font=('Poppins Medium',10))
    nameLbl.grid(row = 0, column = 3, sticky = 'w',padx=30,pady=5)

    namesClient =[]

    idsClient =[]

    for i in getData("select id,nom from client"):

            idsClient.append(i[0])
            namesClient.append(i[1])

    cltN = StringVar()
    clientDropDown=ttk.Combobox(section1,width=17, textvariable = cltN )
    clientDropDown.grid(row = 0, column = 4, sticky = 'e',columnspan=2)

    clientDropDown["values"]=namesClient
    #adress
    qteLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Quantite',font=('Poppins Medium',10))
    qteLbl.grid(row = 0, column = 6, sticky = 'w',padx=30,pady=5)

    quantite = Entry(section1)
    quantite.grid(row = 0, column = 7, sticky = 'e',columnspan=2)
    #End adress

    #Section 2
    section2=Frame(win,bg='#f4e2de',relief = 'raised')
    section2.grid(row = 2, column = 0,padx=50,pady=20,sticky="w")

    searchLbl=Label(section2,bg='#f4e2de', anchor = 'center',text='Rechercher',font=('Poppins Bold',10))
    searchLbl.grid(row=0,column = 0,padx=30,sticky="w")

    sv = StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: search(sv))

    rechercher=Entry(section2,width=13,bd=0,font=('Poppins Medium',10),textvariable=sv)
    rechercher.grid(row=0,column = 0,padx=30,sticky="e")


    tree = ttk.Treeview(section2, column=("c1", "c2","c3"),show='headings',height=11)

    tree.column("#1", anchor=CENTER,width=90)

    tree.heading("#1", text="Commande")

    tree.column("#2", anchor=CENTER,width=90)

    tree.heading("#2", text="Client")

    tree.column("#3", anchor=CENTER,width=90)

    tree.heading("#3", text="date")


    fillTree("select co.id,c.nom,date from commande co inner join client c on co.id_client=c.id")

    tree.bind('<ButtonRelease-1>', selectItem)

    tree.grid(row=1,column=0,padx=30,pady=20)


    #Section 2
    section3=Frame(win,bg='#f4e2de',relief = 'raised')
    section3.place(x=370,y=160)

    searchLbl3=Label(section3,bg='#f4e2de', anchor = 'center',text='Rechercher',font=('Poppins Bold',10))
    searchLbl3.grid(row=0,column = 0,padx=30,sticky="w")
    
    
    sv1 = StringVar()
    sv1.trace("w", lambda name, index, mode, sv1=sv1: search1(sv1))
    rechercher3=Entry(section3,width=13,bd=0,font=('Poppins Medium',10),textvariable=sv1)
    rechercher3.grid(row=0,column = 0,padx=30,sticky="e")


    tree3 = ttk.Treeview(section3, column=("c1", "c2","c3","c4"), show='headings',height=11)

    tree3.column("#1", anchor=CENTER,width=120)

    tree3.heading("#1", text="Commande")

    tree3.column("#2", anchor=CENTER,width=120)

    tree3.heading("#2", text="Produit")

    tree3.column("#3", anchor=CENTER,width=120)

    tree3.heading("#3", text="Quantite")

    tree3.column("#4", anchor=CENTER,width=120)

    tree3.heading("#4", text="Prix")

    # fillTree("select * from client")

    tree3.bind('<ButtonRelease-1>', selectItem1)

    tree3.grid(row=1,column=0,padx=30,pady=20)



    ajouter=Button(win, text='Ajouter Commande',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=insert)#,command=insert
    ajouter.place(x=910,y=90)


    Supprimer=Button(win, text='Supprimer Commande',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=delete)#,command=insert
    Supprimer.place(x=910,y=150)
    
    #LigneCommade Inputs
    prdLbl=Label(win,bg='#f4e2de', anchor = 'center', text='Produit',font=('Poppins Medium',10))
    prdLbl.place(x=465,y=460)
    prodL = StringVar()
    produitDropDownL=ttk.Combobox(win,width=24, textvariable = prodL )
    produitDropDownL.place(x=465,y=490)

    produitDropDownL["values"]=namesProduit

    LqteLbl=Label(win,bg='#f4e2de', anchor = 'center',text='Quantite',font=('Poppins Medium',10))
    LqteLbl.place(x=645,y=460)

    qteL = Entry(win,width=27)
    qteL.place(x=645,y=490)


    ajouterLigne=Button(win, text='Ajouter produit',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=insertProd)#,command=insert
    ajouterLigne.place(x=465,y=520)

    modifierLigne=Button(win, text='Modifier Quantite',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=edit)#,command=insert
    modifierLigne.place(x=645,y=520)

    supprimerLigne=Button(win, text='Supprimer produit',width=43,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=deleteProd)#,command=insert
    supprimerLigne.place(x=465,y=570)
    #Montant a payer :

    Totalbl=Label(win,bg='#f4e2de', anchor = 'center',text='Montant à payer :',font=('Poppins Bold',10))
    Totalbl.place(x=70,y=500)

    Total=Label(win,bg='#f4e2de', anchor = 'center',text='0',font=('Poppins Bold',10))
    Total.place(x=230,y=500)

    quitter=Button(win, text='quitter',width=20,bg="#730202",fg="white", bd=0,font=('Poppins Medium',10),command=lambda : me.menu(user,win))#,command=insert
    quitter.place(x=910,y=570)


    footer=Frame(win,bg='#38184c',width = 1100,height=40,relief = 'raised')
    footer.place(y=630)

    win.mainloop()


