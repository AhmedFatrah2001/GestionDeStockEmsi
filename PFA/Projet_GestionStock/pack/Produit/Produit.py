from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from unicodedata import name
from pack import menu as me,connection as con
from pack.Client import ListeClient as l,Client as c
from pack.Category import Category as cat
from pack.Fournisseur import Fournisseur as f , ListeFournisseur as lf
from pack.Produit import ListeProduit as lp
from pack.Commande import Commande as cmd
def produit(user,s):
        s.destroy()
        cn=con.connection()
        role=user[0][3]
        def isEmpty():
                if name.get()=="" or quantite.get()=="" or prix.get()=="" or desc.get()=="" or catDropDown.current()==-1:
                        return True
                return False
        def insert():
                if not isEmpty():
                        nom=name.get()
                        qte=quantite.get()
                        price=prix.get()
                        de=desc.get()
                        cat=idsCategory[catDropDown.current()]
                        mycursor = cn.cursor()
                        sql = ("INSERT INTO Produit (nom,description,prix,id_cat,quantite) VALUES (%s,%s,%s,%s,%s)")
                        val=(nom,de,price,cat,qte)
                        mycursor.execute(sql,val)
                        cn.commit()
                        fillTree("select p.id,p.nom,p.description,prix,c.nom,p.quantite from produit p inner join category c on p.id_cat=c.id")
                        empty()
                else:
                        messagebox.showwarning("Attenstion","tous les champs sont obligatoires!!!!!!")

        def edit():
                produitExist=hasRows("select * from produit where id='{}'".format(num.get()))
                if not isEmpty():
                        if produitExist:
                                test=messagebox.askquestion("Modifier produit","voulez-vous vraiment modifier le produit {} ?".format(name.get()))
                                if test=="yes":
                                        id_=num.get()
                                        nom=name.get()
                                        qte=quantite.get()
                                        price=prix.get()
                                        de=desc.get()
                                        mycursor = cn.cursor()
                                        cat=idsCategory[catDropDown.current()]
                                        print(cat)
                                        sql = ("UPDATE produit SET nom=%s,quantite=%s,prix=%s,description=%s,id_cat=%s WHERE id=%s")
                                        val=(nom,qte,price,de,cat,id_)
                                        mycursor.execute(sql,val)
                                        cn.commit()
                                        fillTree("select p.id,p.nom,p.description,prix,c.nom,p.quantite from produit p inner join category c on p.id_cat=c.id")
                        else:
                                messagebox.showinfo("Attention","Ce produit que vous rechercher n'existe pas")
                else :
                        messagebox.showwarning("Attenstion","tous les champs sont obligatoires!!!!!!")

        


        def delete():
                produitExist=hasRows("select * from produit where id='{}'".format(num.get()))
                if num.get()!="":
                        if produitExist:
                                test=messagebox.askquestion("Supprimer produit","voulez-vous vraiment supprimer le produit {} ?".format(name.get()))
                                if test=="yes":
                                        id_=num.get()
                                        mycursor = cn.cursor()
                                        sql = ("DELETE FROM produit WHERE id={}".format(id_))
                                        mycursor.execute(sql)
                                        cn.commit()
                                        empty()
                                        fillTree("select p.id,p.nom,p.description,prix,c.nom,p.quantite from produit p inner join category c on p.id_cat=c.id")
                        else:
                                messagebox.showinfo("Attention","Ce produit que vous rechercher n'existe pas")

                else:
                        messagebox.showwarning("Attenstion","Le champs Numero est obligatoire !!")


        def empty():
                num.delete(0, 'end')
                name.delete(0, 'end')
                quantite.delete(0, 'end')
                desc.delete(0, 'end')
                prix.delete(0, 'end')



        def search(sv):
                var=sv.get()
                fillTree("select p.id,p.nom,p.description,prix,c.nom,p.quantite from produit p inner join category c on p.id_cat=c.id where p.nom like '{0}%' or p.id='{0}'".format(var))
                
        def selectItem(a):
                try:
                    curItem = tree.focus()
                    produit=(tree.item(curItem))['values']
                    empty()
                    num.config(state="normal")
                    num.insert(0,produit[0])
                    num.config(state="readonly")
                    name.insert(0,produit[1])
                    quantite.insert(0,produit[5])
                    desc.insert(0,produit[2])
                    prix.insert(0,produit[3])
                    n.set(produit[4])
                except:
                    print(0)
        def hasRows(req):
                sql_select_Query = req
                cursor = cn.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
                if len(records)==0:
                        return False
                return True
        
        def getCategories():
    
                cursor = cn.cursor()

                cursor.execute("select id,nom from category")

                records = cursor.fetchall()

                return records

        def fillTree(req):
                sql_select_Query = req
                cursor = cn.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
                
                for i in tree.get_children():
                    tree.delete(i)
                for row in records:
                        tree.insert("",END, values=row)
                    
        win=Tk()
        win['bg']='#f4e2de'
        win.title('Gérer produit')
        win.geometry("925x600+200+100")
        win.resizable(False,False)


        #MENU BAR
        menubar1 = Menu(win, foreground='black', activebackground='white', activeforeground='black')  
        file = Menu(menubar1, tearoff=0, foreground='black')
        if(role!=1):
           file.add_command(label="produit", state="disabled")  
           file.add_command(label="Produit", state="disabled")  
           file.add_command(label="Fournisseur", state="disabled")  
           file.add_command(label="Commande", state="disabled")
           file.add_command(label="Catégorie", state="disabled")
        else:
           file.add_command(label="Client",command=lambda:c.client(user,win)) 
           file.add_command(label="Produit",state="disabled")
           file.add_command(label="Fournisseur",command=lambda:f.Fournisseur(user,win))  
           file.add_command(label="Commande",command=lambda:cmd.commande(user,win))
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
        topFrame = Frame(win, bg = '#38184c', width = 925, height=60, relief = 'raised') # , padx = 100, pady=100
        titre=Label(topFrame,text="GESTION PRODUITS",bg = '#38184c',fg="white",font=('Poppins Bold',25))
        logo=Label(topFrame,text="EMSI STOCK",bg = '#38184c',fg="white",font=('Poppins Bold',25))
        logo.place(x=10,y=2)
        titre.place(x=595,y=0)
        topFrame.grid(row = 0, column = 0, sticky="w")
        #END TITRE
        #Section 1
        section1=Frame(win,bg='#f4e2de',width = 600,relief = 'raised')
        section1.grid(row = 1, column = 0,padx=50,pady=20,sticky="w")

        #ID
        idLbl=Label(section1,bg='#f4e2de', anchor = 'center', text='Numero produit',font=('Poppins Medium',10))
        idLbl.grid(row = 0, column = 0, sticky = 'w',padx=30,pady=5)

        num = Entry(section1)
        num.grid(row = 0, column = 1, sticky = 'e',columnspan=2)
        num.config(state="readonly")
        #END ID
        #name
        nameLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Nom produit',font=('Poppins Medium',10))
        nameLbl.grid(row = 1, column = 0, sticky = 'w',padx=30,pady=5)

        name = Entry(section1)
        name.grid(row = 1, column = 1, sticky = 'e',columnspan=2)
        #End name

        #adress
        quantiteLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Quantité produit',font=('Poppins Medium',10))
        quantiteLbl.grid(row = 2, column = 0, sticky = 'w',padx=30,pady=5)

        quantite = Entry(section1)
        quantite.grid(row = 2, column = 1, sticky = 'e',columnspan=2)
        #End adress

        #tele
        descLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Description produit',font=('Poppins Medium',10))
        descLbl.grid(row = 0, column = 3, sticky = 'w',padx=30,pady=5)

        desc = Entry(section1)
        desc.grid(row = 0, column = 4, sticky = 'e',columnspan=2)
        #End tele

        #email
        prixLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Prix produit',font=('Poppins Medium',10))
        prixLbl.grid(row = 1, column = 3, sticky = 'w',padx=30,pady=5)

        prix = Entry(section1)
        prix.grid(row = 1, column = 4, sticky = 'e',columnspan=2)
        #End email

        namesCategory =[]

        idsCategory =[]

        for i in getCategories():

                idsCategory.append(i[0])

                namesCategory.append(i[1])



        n = StringVar()

        catLbl=Label(section1, bg='#f4e2de',anchor = 'center',text='Categorie Produit',font=('Poppins Medium',10))

        catLbl.grid(row = 2, column = 3, sticky = 'w',padx=30,pady=5)

        catDropDown = ttk.Combobox(section1,width=17, textvariable = n)

        # print(n.get())

        # print(catDropDown.current())

        # Adding combobox drop down list

        catDropDown['values'] = namesCategory

        catDropDown.grid(row = 2, column = 4, sticky = 'e',columnspan=2)
        #End Section 1

        #Section 2
        section2=Frame(win,bg='#f4e2de',width = 600,relief = 'raised')
        section2.grid(row = 2, column = 0,padx=50,pady=20,sticky="w")

        searchLbl=Label(section2,bg='#f4e2de', anchor = 'center',text='Rechercher produit',font=('Poppins Bold',10))
        searchLbl.grid(row=0,column = 0,padx=30,sticky="w")

        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: search(sv))

        rechercher=Entry(section2,width=20,bd=0,font=('Poppins Medium',10),textvariable=sv)
        rechercher.grid(row=0,column = 0,padx=30,sticky="e")

        tree = ttk.Treeview(section2, column=("c1", "c2", "c3", "c4", "c5","c6"), show='headings',height=11)

        tree.column("#1", anchor=CENTER,width=90)

        tree.heading("#1", text="Numero")

        tree.column("#2", anchor=CENTER,width=90)

        tree.heading("#2", text="Nom")

        tree.column("#3", anchor=CENTER,width=90)

        tree.heading("#3", text="Description")

        tree.column("#4", anchor=CENTER,width=90)

        tree.heading("#4", text="Prix")

        tree.column("#5", anchor=CENTER,width=90)

        tree.heading("#5", text="Categorie")

        tree.column("#6", anchor=CENTER,width=90)

        tree.heading("#6", text="Quantite")

        fillTree("select p.id,p.nom,p.description,prix,c.nom,p.quantite from produit p inner join category c on p.id_cat=c.id")

        tree.bind('<ButtonRelease-1>', selectItem)

        tree.grid(row=1,padx=30,pady=20)

        footer=Frame(win,bg='#38184c',width = 925,height=40,relief = 'raised')
        footer.grid(row=3,column=0,sticky='s')

        #End Section 25

        ajouter=Button(win, text='Ajouter produit',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=insert)#,command=insert
        ajouter.place(x=700,y=90)

        Modifier=Button(win, text='Modifier produit',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=edit)#,command=insert
        Modifier.place(x=700,y=150)

        Supprimer=Button(win, text='Supprimer produit',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=delete)#,command=insert
        Supprimer.place(x=700,y=210)





        quitter=Button(win, text='quitter',width=20,bg="#730202",fg="white", bd=0,font=('Poppins Medium',10),command=lambda : me.menu(user,win))#,command=insert
        quitter.place(x=700,y=490)

        win.mainloop()
