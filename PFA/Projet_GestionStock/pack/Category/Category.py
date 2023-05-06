from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pack import menu as me,connection as con
from pack.Client import Client as c,ListeClient as l
from pack.Fournisseur import Fournisseur as f, ListeFournisseur as lf
from pack.Produit import Produit as p,ListeProduit as lp
from pack.Commande import Commande as cmd
# from pack.Category import ListeCategorie as l

def Category(user,s):
        s.destroy()
        cn=con.connection()
        role=user[0][3]
        def isEmpty():
                if name.get()=="" or Desc.get()=="":
                        return True
                return False
        def insert():
                if not isEmpty():
                        nom=name.get()
                        d=Desc.get()
                        mycursor = cn.cursor()
                        sql = ("INSERT INTO category (nom,description) VALUES ('{}','{}')".format(nom,d))
                        mycursor.execute(sql)
                        cn.commit()
                        fillTree("select * from category")
                        empty()
                else :
                        messagebox.showwarning("Attenstion","tous les champs sont obligatoires!!!!!!")

        def edit():
                CategorieExist=hasRows("select * from category where id='{}'".format(num.get()))
                if not isEmpty():
                        if CategorieExist:
                                test=messagebox.askquestion("Modifier categorie","voulez-vous vraiment modifier categorie {} ?".format(name.get()))
                                if test=="yes":
                                        id_=num.get()
                                        nom=name.get()
                                        d=Desc.get()
                                        mycursor = cn.cursor()
                                        sql = ("UPDATE category SET nom=%s,description=%s WHERE id=%s")
                                        val=(nom,d,id_)
                                        mycursor.execute(sql,val)
                                        cn.commit()
                                        fillTree("select * from category")
                        else:
                                messagebox.showinfo("Attention","Categorie que vous rechercher n'existe pas")
                else :
                        messagebox.showwarning("Attenstion","Tous les champs sont obligatoires!!!!!!")




        def delete():
                CategorieExist=hasRows("select * from category where id='{}'".format(num.get()))
                if num.get()!="":
                        if CategorieExist:
                                test=messagebox.askquestion("Modifier cliant","voulez-vous vraiment supprimer le client {} ?".format(name.get()))
                                if test=="yes":
                                        id_=num.get()
                                        mycursor = cn.cursor()
                                        sql = ("DELETE FROM category WHERE id={}".format(id_))
                                        mycursor.execute(sql)
                                        cn.commit()
                                        empty()
                                        fillTree("select * from category")
                        else:
                                messagebox.showinfo("Attention","Categorie que vous rechercher n'existe pas")

                else:
                        messagebox.showwarning("Attenstion","Le champs Numero est obligatoire !!")


        def empty():
                num.delete(0, 'end')
                name.delete(0, 'end')
                Desc.delete(0,'end')
                

        def search(sv):
                var=sv.get()
                fillTree("select * from category where nom like '{0}%' or id='{0}'".format(var))
                
        def selectItem(a):
                try:
                    curItem = tree.focus()
                    Categorie=(tree.item(curItem))['values']
                    empty()
                    num.insert(0,Categorie[0])
                    name.insert(0,Categorie[1])
                    Desc.insert(0,Categorie[2])
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
        win.geometry("800x600+200+100")
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
           file.add_command(label="Commande",command=lambda:cmd.commande(user,win))
           file.add_command(label="Catégorie",state="disabled")
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
        titre=Label(topFrame,text="GESTION CATEGORIE",bg = '#38184c',fg="white",font=('Poppins Bold',25))
        logo=Label(topFrame,text="EMSI STOCK",bg = '#38184c',fg="white",font=('Poppins Bold',25))
        logo.place(x=10,y=2)
        titre.place(x=450,y=0)
        topFrame.grid(row = 0, column = 0, sticky="w")
        #END TITRE

        #Section 1
        section1=Frame(win,bg='#f4e2de',width = 600,relief = 'raised')
        section1.grid(row = 1, column = 0,padx=50,pady=20,sticky="w")

        #ID
        idLbl=Label(section1,bg='#f4e2de', anchor = 'center', text='Numero categorie',font=('Poppins Medium',10))
        idLbl.grid(row = 0, column = 0, sticky = 'w',pady=5)

        num = Entry(section1)
        num.grid(row = 0, column = 0, sticky = 'e',columnspan=2)
        #END ID



        #name
        nameLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Nom categorie',font=('Poppins Medium',10))
        nameLbl.grid(row = 1, column = 0, sticky = 'w',pady=5)

        name = Entry(section1)
        name.grid(row = 1, column = 0, sticky = 'e',columnspan=2)
        #End name

        #Description
        DescLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Description',font=('Poppins Medium',10))
        DescLbl.grid(row = 2, column = 0, sticky = 'w',pady=5)

        Desc= Entry(section1)
        Desc.grid(row = 2, column = 0, sticky = 'e',columnspan=2)

        #search
        emptyy=Label(section1,bg='#f4e2de').grid(row = 3,pady=7)

        searchLbl=Label(section1,bg='#f4e2de', anchor = 'center',text='Rechercher Categorie',font=('Poppins Bold',10))
        searchLbl.grid(row = 4, column = 0, sticky = 'w',pady=5)

        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: search(sv))

        rechercher= Entry(section1,textvariable=sv)
        rechercher.grid(row = 4, column = 0, sticky = 'e',pady=5)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Poppins Meduim',10)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading",font=('Poppins', 10,'bold'))# Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])


        tree = ttk.Treeview(section1, column=("c1", "c2", "c3"), show='headings',height=11,style="mystyle.Treeview")

        tree.column("#1", anchor=CENTER,width=130)

        tree.heading("#1", text="Numero")

        tree.column("#2", anchor=CENTER,width=130)

        tree.heading("#2", text="Nom")

        tree.column("#3", anchor=CENTER,width=130)

        tree.heading("#3", text="Description")

        fillTree("select * from category")

        tree.bind('<ButtonRelease-1>', selectItem)

        tree.grid(row=5,pady=20)

        ajouter=Button(win, text='Ajouter categorie',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=insert)#,command=insert
        ajouter.place(x=600,y=90)

        Modifier=Button(win, text='Modifier categorie',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=edit)#,command=insert
        Modifier.place(x=600,y=150)

        Supprimer=Button(win, text='Supprimer categorie',width=20,bg="#38184c",fg="white", bd=0,font=('Poppins Medium',10),command=delete)#,command=insert
        Supprimer.place(x=600,y=210)

        quitter=Button(win, text='quitter',width=20,bg="#730202",fg="white", bd=0,font=('Poppins Medium',10),command=lambda : me.menu(user,win))#,command=insert
        quitter.place(x=600,y=490)




        footer=Frame(win,bg='#38184c',width = 925,height=40,relief = 'raised')
        footer.grid(row=6,column=0,sticky='s')


        #End Description




        win.mainloop()
        
       
       

        
 



     
       