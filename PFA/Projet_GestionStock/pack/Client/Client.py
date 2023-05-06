from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from unicodedata import name
from pack import menu as me,connection as con
from pack.Client import ListeClient as l
from pack.Category import Category as cat
from pack.Fournisseur import Fournisseur as f , ListeFournisseur as lf
from pack.Produit import Produit as p,ListeProduit as lp
from pack.Commande import Commande as cmd

def client(user,s):
        s.destroy()
        cn=con.connection()
        role=user[0][3]
        def isEmpty():
                if name.get()=="" or adress.get()=="" or email.get()=="" or selectedValue.get()=="":
                        return True
                return False
        def insert():
                if not isEmpty():
                        nom=name.get()
                        adresse=adress.get()
                        tel=tele.get()
                        em=email.get()
                        sexe=selectedValue.get()
                        mycursor = cn.cursor()
                        sql = ("INSERT INTO CLIENT (nom,adress,tele,email,sexe) VALUES (%s,%s,%s,%s,%s)")
                        val=(nom,adresse,tel,em,sexe)
                        mycursor.execute(sql,val)
                        cn.commit()
                        fillTree("select * from client")
                        empty()
                else:
                        messagebox.showwarning("Attenstion","tous les champs sont obligatoires!!!!!!")

        def edit():
                ClientExist=hasRows("select * from client where id='{}'".format(num.get()))
                if not isEmpty():
                        if ClientExist:
                                test=messagebox.askquestion("Modifier client","voulez-vous vraiment modifier le client {} ?".format(name.get()))
                                if test=="yes":
                                        id_=num.get()
                                        nom=name.get()
                                        adresse=adress.get()
                                        em=email.get()
                                        tel=tele.get()
                                        mycursor = cn.cursor()
                                        sexe=selectedValue.get()
                                        sql = ("UPDATE CLIENT SET nom=%s,adress=%s,sexe=%s,email=%s,tele=%s WHERE id=%s")
                                        val=(nom,adresse,sexe,em,tel,id_)
                                        mycursor.execute(sql,val)
                                        cn.commit()
                                        fillTree("select * from client")
                        else:
                                messagebox.showinfo("Attention","Ce client que vous rechercher n'existe pas")
                else :
                        messagebox.showwarning("Attenstion","tous les champs sont obligatoires!!!!!!")



        def delete():
                ClientExist=hasRows("select * from client where id='{}'".format(num.get()))
                if num.get()!="":
                        if ClientExist:
                                test=messagebox.askquestion("Supprimer client","voulez-vous vraiment supprimer le client {} ?".format(name.get()))
                                if test=="yes":
                                        id_=num.get()
                                        mycursor = cn.cursor()
                                        sql = ("DELETE FROM CLIENT WHERE id={}".format(id_))
                                        mycursor.execute(sql)
                                        cn.commit()
                                        empty()
                                        fillTree("select * from client")
                        else:
                                messagebox.showinfo("Attention","Ce client que vous rechercher n'existe pas")

                else:
                        messagebox.showwarning("Attenstion","Le champs Numero est obligatoire !!")


        def empty():
                num.delete(0, 'end')
                name.delete(0, 'end')
                adress.delete(0, 'end')
                email.delete(0, 'end')
                tele.delete(0, 'end')
                selectedValue.set(0)

        def search(sv):
                var=sv.get()
                fillTree("select * from client where nom like '{0}%' or id='{0}'".format(var))
                
        def selectItem(a):
                try:
                    curItem = tree.focus()
                    client=(tree.item(curItem))['values']
                    empty()
                    num.config(state="normal")
                    num.insert(0,client[0])
                    num.config(state="readonly")
                    name.insert(0,client[1])
                    adress.insert(0,client[2])
                    tele.insert(0,client[3])
                    email.insert(0,client[4])
                    sexe=client[5]
                    if sexe == "M":
                            selectedValue.set("M")
                    else:
                            selectedValue.set("F")
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
        win.title('Gérer client')
        win.geometry("925x600+200+50")
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
           file.add_command(label="Client",state="disabled")  
           file.add_command(label="Produit",command=lambda:p.produit(user,win))
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
        titre=Label(topFrame,text="GESTION CLIENTS",bg = '#38184c',fg="white",font=('Poppins Bold',25))
        logo=Label(topFrame,text="EMSI STOCK",bg = '#38184c',fg="white",font=('Poppins Bold',25))
        logo.place(x=10,y=2)
        titre.place(x=615,y=0)
        topFrame.grid(row = 0, column = 0, sticky="w")
        #END TITRE
        #Section 1
        section1=Frame(win,bg='#f4e2de',width = 600,relief = 'raised')
        section1.grid(row = 1, column = 0,padx=50,pady=20,sticky="w")

        #ID
        idLbl=Label(section1,bg='#f4e2de', anchor = 'center', text='Numero client',font=('Poppins Medium',10))
        idLbl.grid(row = 0, column = 0, sticky = 'w',padx=30,pady=5)

        num = Entry(section1)
        num.grid(row = 0, column = 1, sticky = 'e',columnspan=2)
        num.config(state="readonly")
        #END ID
        #name
        nameLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Nom client',font=('Poppins Medium',10))
        nameLbl.grid(row = 1, column = 0, sticky = 'w',padx=30,pady=5)

        name = Entry(section1)
        name.grid(row = 1, column = 1, sticky = 'e',columnspan=2)
        #End name

        #adress
        adressLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Adresse client',font=('Poppins Medium',10))
        adressLbl.grid(row = 2, column = 0, sticky = 'w',padx=30,pady=5)

        adress = Entry(section1)
        adress.grid(row = 2, column = 1, sticky = 'e',columnspan=2)
        #End adress

        #tele
        teleLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Telephone client',font=('Poppins Medium',10))
        teleLbl.grid(row = 0, column = 3, sticky = 'w',padx=30,pady=5)

        tele = Entry(section1)
        tele.grid(row = 0, column = 4, sticky = 'e',columnspan=2)
        #End tele

        #email
        emailLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Email client',font=('Poppins Medium',10))
        emailLbl.grid(row = 1, column = 3, sticky = 'w',padx=30,pady=5)

        email = Entry(section1)
        email.grid(row = 1, column = 4, sticky = 'e',columnspan=2)
        #End email

        #sexe
        sexeLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Sexe',font=('Poppins Medium',10))
        sexeLbl.grid(row = 2, column = 3, sticky = 'w',padx=30,pady=5)


        selectedValue=StringVar()

        sexeH=Radiobutton(section1,bg='#f4e2de', text='M',variable=selectedValue, value="M",font=('Poppins Medium',10))
        sexeF=Radiobutton(section1,bg='#f4e2de', text='F',variable=selectedValue, value="F",font=('Poppins Medium',10))

        selectedValue.set(0)

        sexeH.grid(row =2, column = 4, sticky = 'e')
        sexeF.grid(row = 2, column = 5, sticky = 'e')

        #End Section 1

        #Section 2
        section2=Frame(win,bg='#f4e2de',width = 600,relief = 'raised')
        section2.grid(row = 2, column = 0,padx=50,pady=20,sticky="w")

        searchLbl=Label(section2,bg='#f4e2de', anchor = 'center',text='Rechercher client',font=('Poppins Bold',10))
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

        tree.heading("#3", text="Adress")

        tree.column("#4", anchor=CENTER,width=90)

        tree.heading("#4", text="Telephone")

        tree.column("#5", anchor=CENTER,width=90)

        tree.heading("#5", text="Email")

        tree.column("#6", anchor=CENTER,width=90)

        tree.heading("#6", text="Sexe")

        fillTree("select * from client")

        tree.bind('<ButtonRelease-1>', selectItem)

        tree.grid(row=1,padx=30,pady=20)

        footer=Frame(win,bg='#38184c',width = 925,height=40,relief = 'raised')
        footer.grid(row=3,column=0,sticky='s')

        #End Section 25

        ajouter=Button(win, text='Ajouter Client',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=insert)#,command=insert
        ajouter.place(x=700,y=90)

        Modifier=Button(win, text='Modifier Client',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=edit)#,command=insert
        Modifier.place(x=700,y=150)

        Supprimer=Button(win, text='Supprimer Client',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=delete)#,command=insert
        Supprimer.place(x=700,y=210)





        quitter=Button(win, text='quitter',width=20,bg="#730202",fg="white", bd=0,font=('Poppins Medium',10),command=lambda : me.menu(user,win))#,command=insert
        quitter.place(x=700,y=490)

        win.mainloop()
