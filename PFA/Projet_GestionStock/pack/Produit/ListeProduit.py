from tkinter import *
from tkinter import ttk
from pack import connection as con,menu as me
from pack.Client import Client as c,ListeClient as l
from pack.Category import Category as cat
from pack.Fournisseur import Fournisseur as f,ListeFournisseur as lf
from pack.Produit import Produit as p
from pack.Commande import Commande as cmd

def listeProduit(user,s):
    s.destroy()
    cn=con.connection()
    role=user[0][3]
    def fillTree(req):
        sql_select_Query = req
        cursor = cn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        
        for i in tree.get_children():
            tree.delete(i)
        for row in records:
                tree.insert("",END, values=row)

    def search(sv):
        var=sv.get()
        fillTree("select p.id,p.nom,p.description,p.prix,c.nom,p.quantite from produit p inner join category c on p.id_cat=c.id where p.nom like '{0}%' or p.id='{0}'".format(var))


    win=Tk()
    win['bg']='#f4e2de'
    win.title('Liste produits')
    win.geometry("925x500+200+100")
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
        file.add_command(label="Catégorie",command=lambda:cat.Category(user,win))
    menubar1.add_cascade(label="Gérer", menu=file)  

    afficher = Menu(menubar1, tearoff=0, foreground='black')  
    afficher.add_command(label="Client",command=lambda:l.listeClient(user,win))  
    afficher.add_command(label="Produit",state="disabled")  
    afficher.add_command(label="Fournisseur",command=lambda:lf.listeFournisseur(user,win))  
    afficher.add_command(label="Commande")
    menubar1.add_cascade(label="Affichage", menu=afficher)  
            


    menubar1.add_command(label='Exit',command=quit)

    win.config(menu=menubar1)
    #END MENU BAR



     #TITRE
    topFrame = Frame(win, bg = '#38184c', width = 925, height=60, relief = 'raised') # , padx = 100, pady=100
    titre=Label(topFrame,text="LISTE PRODUITS",bg = '#38184c',fg="white",font=('Poppins Bold',25))
    logo=Label(topFrame,text="EMSI STOCK",bg = '#38184c',fg="white",font=('Poppins Bold',25))
    logo.place(x=10,y=2)
    titre.place(x=650,y=0)
    topFrame.grid(row = 0, column = 0, sticky="w")
    #END TITRE

    #section Tree
    section2 = Frame(win,bg='#f4e2de', width = 625, relief = 'raised') # , padx = 100, pady=100
    section2.grid(row = 1, column = 0,sticky="we",pady=20,padx=50)


    searchLbl=Label(section2,bg='#f4e2de', anchor = 'center',text='Rechercher produit',font=('Poppins Bold',10))
    searchLbl.grid(row = 1, column = 0, sticky="w",columnspan=1,padx=50)

    sv = StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: search(sv))

    rechercher = Entry(section2,width=20,textvariable=sv)
    rechercher.grid(row = 1, column = 2,columnspan=1,sticky="e",padx=50)

    

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Poppins Meduim',10)) # Modify the font of the body
    style.configure("mystyle.Treeview.Heading",font=('Poppins', 10,'bold'))# Modify the font of the headings
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])


    tree = ttk.Treeview(section2, column=("c1", "c2", "c3", "c4", "c5","c6"), show='headings',height=11,style="mystyle.Treeview")

    tree.column("#1", anchor=CENTER,width=120)

    tree.heading("#1", text="Numero")

    tree.column("#2", anchor=CENTER,width=120)

    tree.heading("#2", text="Nom")

    tree.column("#3", anchor=CENTER,width=120)

    tree.heading("#3", text="Drescription")

    tree.column("#4", anchor=CENTER,width=120)

    tree.heading("#4", text="prix")

    tree.column("#5", anchor=CENTER,width=120)

    tree.heading("#5", text="Category")

    tree.column("#6", anchor=CENTER,width=120)

    tree.heading("#6", text="quantite")

    fillTree("select p.id,p.nom,p.description,p.prix,c.nom,p.quantite from produit p inner join category c on p.id_cat=c.id")

    tree.grid(row=2,column = 0,columnspan=3,sticky="we",padx=50,pady=20)

    quitter=Button(win, text='quitter',width=20,bg="#730202",fg="white", bd=0,font=('Poppins Medium',10),command=lambda : me.menu(user,win))#,command=insert
    quitter.grid(row=3,pady=10)

    footer=Frame(win,bg='#38184c',width = 925,height=40,relief = 'raised')
    footer.grid(row=4,column=0,sticky='s')



    win.mainloop()
