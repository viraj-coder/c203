import socket
from threading import Thread
from tkinter import *
nickname=input("chose your nickname:")
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address='127.0.0.1'
port=8000
client.connect((ip_address,port))
print("connect with the server")

class GUI:
    def __init__(self):
        self.Window=Tk()
        self.Window.withdraw()
        self.login=Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=300)
        self.pls=Label(self.login,
                       text="Please login to continue",
                       justify=CENTER,
                       font="Helvetica 14 bold"    
                           )
        self.pls.place(relheight=0.15,relx=0.2,rely=0.07)
        self.labelName=Label(self.login,text="name:",font="Helvetica 12")
        self.labelName.place(relheight=0.2,relx=0.1,rely=0.2)
        self.entryName=Label(self.login,font="Helvetica 14")
        self.entryName.place(relheight=0.12,relx=0.35,rely=0.2,relwidth=0.4)
        self.entryName.focus()
        self.go=Button(self.login,text="Continue",font="Helvetica 14 bold",command=lambda:self.goAhead(self.entryName.get()) )
        self.go.place(relx=0.4,rely=0.55)
        self.Window.mainloop()

    def goAhead(self,name):
        self.login.destroy()
        self.layout(name)
        rcv=Thread(target=self.recieve)
        rcv.start()




    def recieve(self):
        while True:
            try:
                message=client.recv(2048).decode("utf-8")
                if message=="nickname":
                    client.send(nickname.encode("utf-8"))

                else:
                    self.showMessage(message)
            except:
                    print("an error ocurred!")
                    client.close()
                    break




    def layout(self,name):
        self.name=name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,height=False)
        self.Window.configure(width=470,height=550,bg="lightgreen")
        self.labelHead=Label(self.Window,bg="lightgreen",fg="green",text=self.name,font="Helvetica 13 bold",pady=5)
        self.labelhead.place(relwidth=1)
        self.line=Label(self.Window,width=450,bg="blue")
        self.line.place(relwidth=1,rely=0.07,relheight=0.012)
        self.textCons=Text(self.Window,width=20,height=2,bg="lightgreen",fg="darkgreen",font="Helvetica 14 bold",padx=5,pady=5)
        self.textCons.place(relheight=0.745,relwidth=1,rely=0.08)
        self.labelBottom=Label(self.Window,bg="blue",height=80)
        self.labelBottom.place(relwidth=1,rely=0.825)
        self.entryMessage=Entry(self.labelBottom,bg="red",fg="green",font="Helvetica 13 bold")
        self.entryMessage.place(relwidth=0.74,relheight=0.06,relx=0.011,rely=0.008)
        self.entryMessage.focus()
        self.buttonMessage=Button(self.labeButton,text="send",font="Helvetica 10 bold",widht=20,bg="blue",command=lambda:self.sendButton(self.entryMessage.get()))
        self.buttonMessage.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)
        self.textCons.config(cursor="arrow")
        scrollbar=Scrollbar(self.textCons)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.config(command=textCons.yview)
        self.textCons.config(state=DISABLED)


    def sendButton(self,message):
        self.textCons.config(state=DISABLED)
        self.message=message
        self.entryMessage.delete(0,END)
        snd=Thread(target=self.write)
        snd.start()

    def showMessage(self,message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,message+"\n\m")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message=(f"{self.name}:{self.message}")
            client.send(message.encode("utf-8"))   
            self.showMessage(message)
            break

   


g=GUI()
    
#recieveThread=Thread(target=recieve)
#recieveThread.start()
#writeThread=Thread(target=write)
#writeThread.start()
   
            
