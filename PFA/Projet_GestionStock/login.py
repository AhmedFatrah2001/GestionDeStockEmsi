from tkinter import *
from tkinter import messagebox
from pack import menu as m,connection as c

cn=c.connection()

def isUser():
    u=user.get()
    c=code.get()
    sql_select_Query = "select * from utilisateur where login ='{}' and password='{}'".format(u,c)
    cursor = cn.cursor()
    cursor.execute(sql_select_Query)
    user_ = cursor.fetchall()
    if(len(user_)!=0):  
        m.menu(user_,root)
    else:
        messagebox.showwarning(title='Connection failed', message='Invalid login or password')

def on_enter(e):
    user.delete(0,'end')
    
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')




# code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('',11))
# code.place(x=30,y=150)



# ''' BUTTON '''
# Button(frame,width=39,pady=7,text="Connectez vous",bg='#01E0BF',fg='white',border=0,command=isUser).place(x=35,y=250)


root=Tk()
root.title('login')
root.geometry('925x500+200+100')
root.configure(bg="#f4e2de")
root.resizable(False,False)

leftFrame=Frame(root,bg="#38184c",width=460,height=925)
leftFrame.grid(row = 0, column = 0, sticky="w")

bienvenue=Label(leftFrame,text="BIENVENUE",bg="#38184c",fg="white",font=('Poppins Bold',40))
bienvenue.place(x=80,y=180)
b=Label(leftFrame,text="Bonjour,cette application permert la gestion de stock de l'entreprise Emsi",bg="#38184c",fg="#A4A4A4",font=('Poppins Bold',8))
b.place(x=30,y=250)

seconn=Label(root,text="SE CONNECTER",bg="#f4e2de",fg="#190033",font=('Poppins Bold',25))
seconn.place(x=560,y=100)


user=Entry(root,width=24,fg='black',border=0,bg='#F6F6F6',font=('Poppins Medium',11))
user.place(x=570,y=170,height=30)

user.insert(0,'Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)

def on_enter(e):
    code.delete(0,'end')
    
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')


code=Entry(root,width=24,fg='black',border=0,bg='#F6F6F6',font=('Poppins Medium',11),show="*")
code.place(x=570,y=230,height=30)

code.insert(0,'Password')
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)



Button(root,width=29,pady=7,text="Connectez vous",bg='#38184c',fg='white',font=('Poppins Bold',9),border=0,command=isUser).place(x=572,y=300)#,command=isUser


root.mainloop()
