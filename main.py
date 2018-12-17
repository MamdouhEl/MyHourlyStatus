import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import os
import datetime
import pytz
import pystray
import sys
from pystray import Menu, MenuItem
import subprocess
import time
import urllib3
import traceback

# from subprocess import check_call as run
# from subprocess import Popen

User=""
EmailAd=""
Password=""

def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)



class IsilonStatus(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Isilon Status")



        #Centering the window
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        #print("Width",windowWidth,"Height",windowHeight)

        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/2 - windowHeight/2)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))

        self.image = Image.open(resource_path("./images/main_form6.png"))
        width, height = self.image.size

        self.wm_geometry("%sx%s"%(width, height))


        self.resizable(0,0)

        self.overrideredirect(1)

        self.wm_attributes("-topmost", 1)


        container = tk.Frame(self)

        self.hide_int = 2400

        container.pack()
        container.pack_propagate(0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        frame = Startup(container, self)

        for F in (Startup, login, Frontend, Register, Register2):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

            #frame.configure(background="steel blue")

            frame.grid_propagate(0)

        self.show_frame(Startup)





    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def disable_event(self):
        pass

    def hide(self,cont):

        self.withdraw()
        self.after(1000 * self.hide_int, self.show)

    def hideTom(self,cont):

        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())
        Hour = 24 - (int(Current[0:2]) - 2)
        delay = ((Hour * 60) - int(Current[3:5])) * 60
        self.withdraw()
        self.after(1000 * delay, self.show)

    def show(self):

        self.deiconify()





class Startup(tk.Frame):

    def __init__(self,parent, controller):

        tk.Frame.__init__(self, parent)


        self.image = Image.open(resource_path("./images/main_form6.png"))
        width, height = self.image.size
        self.background_image = ImageTk.PhotoImage(self.image)


        canvas = tk.Canvas(self, width=width, height=height)
        canvas.pack()
        canvas.create_image(width/2, height/2, image=self.background_image)


        b1 = ttk.Button(self, width = 15, text="Login", command=lambda : controller.show_frame(login))
        b1.pack(padx = 10, pady = 10)
        b1.place(relx=0.6, rely=0.5, anchor=CENTER)

        b2 = ttk.Button(self, width = 15, text="Register", command=lambda : controller.show_frame(Register))
        b2.pack(padx = 10, pady = 10)
        b2.place(relx=0.4, rely=0.5, anchor=CENTER)

        link = Label(self, text="Are you out of office today? click here", bg="white", fg="deep sky blue", cursor="hand2")
        link.place(relx=0.25, rely=0.95, anchor=CENTER)
        link.bind("<Button-1>",lambda e : self.callback(controller, parent))

        link1 = Label(self, text="Idea and design by Hossam ElShaboury", fg="white", bg="deep sky blue")
        link1.place(relx=0.22, rely=0.87, anchor=CENTER)

        link2 = Label(self, text="Implementation and coding by Mamdouh Ellamei", fg="white", bg="deep sky blue")
        link2.place(relx=0.72, rely=0.87, anchor=CENTER)


    def callback(self,controller, parent):
        controller.hideTom(parent)



class login(tk.Frame):

    def __init__(self,parent, controller):

        tk.Frame.__init__(self, parent)

        self.image = Image.open(resource_path("./images/main_form7.png"))
        width, height = self.image.size
        self.background_image = ImageTk.PhotoImage(self.image)


        canvas = tk.Canvas(self, width=width, height=height)
        canvas.grid(sticky="nsew")
        canvas.create_image(width/2, height/2, image=self.background_image)



        self.l1 = tk.Label(self, text="Invalid Username or Password", fg="red")
        self.l1.place(relx=0.2, rely=0.82, anchor=CENTER)
        self.l1.place_forget()



        self.User_Name=tk.StringVar()
        self.User_Name.trace('w', self.validate)
        self.e1 = tk.Entry(self, font="Helvetica 15", textvariable=self.User_Name)
        self.e1.place(relx=0.6, rely=0.42, anchor=CENTER)
        #self.e1.insert(0, "Username")
        #self.e1.bind("<Button-1>", self.some_callback)
        self.e1.focus_set()

        self.Password=tk.StringVar()
        self.Password.trace('w', self.validate)
        self.e3 = tk.Entry(self, font="Helvetica 15", textvariable=self.Password, show="*")
        self.e3.place(relx=0.6, rely=0.58, anchor=CENTER)
        #self.e3.insert(0, "Password")
        #self.e3.bind("<Button-1>", self.some_callback)
        self.e3.focus_set()

        self.b1 = tk.Button(self, width = 25, text="Login", bg="grey", fg="white", font="Helvetica 10 bold", state = "disabled", command=lambda : controller.show_frame(Frontend) if self.LoginCheck(self.e1.get(), self.e3.get()) == 1 else self.l1.place(relx=0.2, rely=0.8, anchor=CENTER))
        #self.b1.bind("<Button-1>",lambda e : self.callback(controller, parent))
        self.b1.place(relx=0.6, rely=0.7, anchor=CENTER)

        link = Label(self, text="Still haven't registered? click here", bg="white", fg="deep sky blue", cursor="hand2")
        link.place(relx=0.25, rely=0.95, anchor=CENTER)
        link.bind("<Button-1>",lambda e : self.callback(controller, parent))


    def callback(self,controller, parent):
        controller.show_frame(Register)




    def validate(self, name, index, mode): # or just self, *dummy
        self.b1.config(state=("normal" if self.User_Name.get() and self.Password.get() else "disabled"))



    def LoginCheck(self, Username, Password):
        global User, EmailAd

        if(len(Database.CheckCredentials(Username, Password)) == 0):
            return 0
        else:
            User = self.e1.get()
            EmailAd= Database.Search(Username=User)[0][2]
            print(EmailAd)
            return 1

class Register(tk.Frame):

    def __init__(self,parent, controller):

        tk.Frame.__init__(self, parent)

        self.image = Image.open(resource_path("./images/RegisterForm3.png"))
        width, height = self.image.size
        self.background_image = ImageTk.PhotoImage(self.image)


        canvas = tk.Canvas(self, width=width, height=height)

        canvas.create_image((width/2), (height/2), image=self.background_image)
        canvas.grid(sticky='nsew')


        self.l1 = tk.Label(self, text="Email Already Exists", fg="red")
        self.l1.place(relx=0.2, rely=0.82, anchor=CENTER)
        self.l1.place_forget()

        self.l2 = tk.Label(self, text="Invalid email", fg="red")
        self.l2.place(relx=0.2, rely=0.82, anchor=CENTER)
        self.l2.place_forget()


        self.l3 = tk.Label(self, text="Username Already Exists", fg="red")
        self.l3.place(relx=0.2, rely=0.82, anchor=CENTER)
        self.l3.place_forget()


        self.l4 = tk.Label(self, text="Passwords mismatch", fg="red")
        self.l4.place(relx=0.2, rely=0.82, anchor=CENTER)
        self.l4.place_forget()

        self.User_Name=tk.StringVar()
        self.User_Name.trace('w', self.validate)
        self.e1 = tk.Entry(self, textvariable=self.User_Name)
        self.e1.place(relx=0.6, rely=0.33, anchor=CENTER)
        #self.e1.bind("<Button-1>", self.some_callback)
        self.e1.focus_set()



        self.Password=tk.StringVar()
        self.Password.trace('w', self.validate)
        self.e2 = tk.Entry(self, textvariable=self.Password, show="*")
        self.e2.place(relx=0.6, rely=0.43, anchor=CENTER)
        #self.e2.insert(0, "Password")
        #.e2.bind("<Button-1>", self.some_callback)
        self.e2.focus_set()



        self.cPassword=tk.StringVar()
        self.cPassword.trace('w', self.validate)
        self.e3 = tk.Entry(self, textvariable=self.cPassword, show="*")
        self.e3.place(relx=0.6, rely=0.53, anchor=CENTER)
        #self.e3.insert(0, "Confirm Password")
        #self.e3.bind("<Button-1>", self.some_callback)
        self.e3.focus_set()



        self.Email=tk.StringVar()
        self.Email.trace('w', self.validate)
        self.e4 = tk.Entry(self, textvariable=self.Email)
        self.e4.place(relx=0.6, rely=0.63, anchor=CENTER)
        #self.e4.insert(0, "Corp Email")
        #self.e4.bind("<Button-1>", self.some_callback)
        self.e4.focus_set()


        self.b1 = ttk.Button(self, width = 15, text="Next", state = "disabled", command=lambda : self.l1.place(relx=0.6, rely=0.7, anchor=CENTER) if self.ButtonPress(self.e4.get(),self.e1.get()) == 1  else ( self.l2.place(relx=0.6, rely=0.7, anchor=CENTER) if ("@emc.com" not in self.e4.get().lower() and "@dell.com" not in self.e4.get().lower())else (self.l1.place(relx=0.6, rely=0.7, anchor=CENTER) if self.ButtonPress(self.e4.get(),self.e1.get()) == 2 else (self.l4.place(relx=0.6, rely=0.7, anchor=CENTER) if self.e2.get() != self.e3.get() else self.ButtonSuccess(controller, self.e4.get(), self.e2.get(), self.e1.get())))))
        self.b1.place(relx=0.6, rely=0.8, anchor=CENTER)


        self.b2 = ttk.Button(self, width = 15, text="Back to login", command=lambda : controller.show_frame(login))
        self.b2.place(relx=0.2, rely=0.8, anchor=CENTER)

    def some_callback(self,event): # note that you must include the event as an arg, even if you don't use it.
        self.e1.delete(0, "end")
        self.e2.delete(0, "end")
        self.e3.delete(0, "end")
        self.e4.delete(0, "end")
        return None

    def validate(self, name, index, mode): # or just self, *dummy
        self.b1.config(state=("normal" if self.User_Name.get() and self.Password.get() and self.cPassword.get() and self.Email.get() else "disabled"))


    def ButtonPress(self, EmailRetrieve, UsernameRetrieve):

        if(len(Database.Search(Username="", Password="", Email=EmailRetrieve)) != 0):
            return 1
        elif(len(Database.Search(Username = UsernameRetrieve, Password="",Email="")) != 0):
            return 2
        else:
            return 0

    def ButtonSuccess(self, controller, EmailRetrieve, PasswordRetrieve, UsernameRetrieve):
        global User, Password, EmailAd
        User = UsernameRetrieve
        Password = PasswordRetrieve
        EmailAd = EmailRetrieve
        controller.show_frame(Register2)


class Register2(tk.Frame):


    def __init__(self,parent, controller):

        tk.Frame.__init__(self, parent)

        self.image = Image.open(resource_path("./images/RegisterForm4.png"))
        width, height = self.image.size
        self.background_image = ImageTk.PhotoImage(self.image)


        canvas = tk.Canvas(self, width=width, height=height)

        canvas.create_image((width/2), (height/2), image=self.background_image)
        canvas.grid(sticky='nsew')
        self.Geo=tk.StringVar()
        self.Geo.set("Enter your Geo")
        #self.Geo.trace('w', self.validate)

        # self.e1 = tk.Menubutton(self, text="Select your Geo")
        # self.e1.menu=tk.Menu(self.e1)
        # self.e1["menu"]=self.e1.menu
        # #self.GeoLoc=tk.StringVar()
        # self.e1.menu.add_radiobutton(label="EMEA", value="EMEA", variable=self.Geo)
        # self.e1.menu.add_radiobutton(label="APJK", value="APJK", variable=self.Geo)
        # self.e1.menu.add_radiobutton(label="AMER", value="AMER", variable=self.Geo)
        self.e1 = OptionMenu(self, self.Geo, "EMEA", "APJK", "AMER")
        self.e1.place(relx=0.6, rely=0.33, anchor=CENTER)
        #self.e1.bind("<Button-1>", self.some_callback)
        self.e1.focus_set()

        #self.Loc=tk.StringVar()
        self.Location=tk.StringVar()
        self.Location.set("Enter your location")
        #self.Location.trace('w', self.validate)
        # self.e2 = tk.Menubutton(self, text="Select your Location")
        # self.e2.menu=tk.Menu(self.e2)
        # self.e2["menu"]=self.e2.menu
        #
        # self.e2.menu.add_radiobutton(label="Cairo", value="Cairo", variable=self.Location)
        # self.e2.menu.add_radiobutton(label="Cork", value="Cork", variable=self.Location)
        self.e2=OptionMenu(self, self.Location, "Cairo", "Cork")
        self.e2.place(relx=0.6, rely=0.43, anchor=CENTER)
        #self.e1.bind("<Button-1>", self.some_callback)
        self.e2.focus_set()


        self.Product=tk.StringVar()
        self.Product.trace('w', self.validate)
        self.e3 = tk.Entry(self, textvariable=self.Product)
        self.e3.place(relx=0.6, rely=0.53, anchor=CENTER)
        #self.e3.insert(0, "Confirm Password")
        #self.e3.bind("<Button-1>", self.some_callback)
        self.e3.focus_set()


        self.b1 = ttk.Button(self, width = 15, text="Submit", state = "disabled", command=lambda :  self.ButtonSuccess(controller, self.Geo.get(), self.Location.get(), self.e3.get()))

        self.b1.place(relx=0.6, rely=0.8, anchor=CENTER)

    def validate(self, name, index, mode): # or just self, *dummy
        self.b1.config(state=("normal" if self.Geo.get() and self.Location.get() and self.Product.get() else "disabled"))


    def ButtonSuccess(self, controller, GeoRetrieve, LocationRetrieve, ProductRetrieve):
        global User, Password, EmailAd
        Database.Insert(User, Password, EmailAd, GeoRetrieve, LocationRetrieve, ProductRetrieve)
        controller.show_frame(login)
    # self.b1 = ttk.Button(self, width = 15, text="Submit", state = "disabled", command=lambda : self.l1.place(relx=0.6, rely=0.7, anchor=CENTER) if self.ButtonPress(self.e4.get(),self.e1.get()) == 1  else ( self.l2.place(relx=0.6, rely=0.7, anchor=CENTER) if ("@emc.com" not in self.e4.get().lower() and "@dell.com" not in self.e4.get().lower())else (self.l1.place(relx=0.6, rely=0.7, anchor=CENTER) if self.ButtonPress(self.e4.get(),self.e1.get()) == 2 else (self.l4.place(relx=0.6, rely=0.7, anchor=CENTER) if self.e2.get() != self.e3.get() else self.ButtonSuccess(controller, self.e4.get(), self.e2.get(), self.e1.get())))))
    # self.b1.place(relx=0.6, rely=0.8, anchor=CENTER)


class Frontend(tk.Frame):

    def __init__(self,parent, controller):


        tk.Frame.__init__(self, parent)

        self.image = Image.open(resource_path("./images/StatusForm4.png"))
        width, height = self.image.size
        self.background_image = ImageTk.PhotoImage(self.image)


        canvas = tk.Canvas(self, width=width, height=height)

        canvas.create_image((width/2), (height/2), image=self.background_image)
        canvas.grid(sticky='nsew')

        print(User)
        self.Avail=PhotoImage(file=resource_path("./images/Avail.png"))
        b1 = tk.Button(self, width = 50, height = 50, bg='white', highlightthickness=0, relief='flat', command=lambda : self.ButtonClickAvail(parent, controller, User))
        b1.config(image=self.Avail, compound=TOP)
        #b1.grid(row = 1, column = 1, rowspan=3, columnspan=2, padx = 10, pady =10)
        b1.place(relx=0.1, rely=0.6, anchor="center")

        self.Webex=PhotoImage(file=resource_path("./images/webex.png"))
        #self.Webex=Image.open("images.gif")
        #maxsize = [150,150]
        #self.Webex = self.Resize_Image(self.Webex, maxsize)
        b2 = tk.Button(self, width = 50, height = 50, bg='white', highlightthickness=0, relief='flat', command=lambda : self.ButtonClickWebex(parent, controller, User))
        #b2 = Button(window, width = 15, height = 5, compound=TOP, image=self.photo, text="WebEx")
        b2.config(image=self.Webex, compound=TOP)
        #b2.grid(row = 1, column = 4, rowspan=3, columnspan=2)
        b2.place(relx=0.56, rely=0.6, anchor=CENTER)

        self.logs=PhotoImage(file=resource_path("./images/logs.png"))
        b3 = tk.Button(self, width = 50, height = 50, bg='white', highlightthickness=0, relief='flat', command=lambda : self.ButtonClickLogs(parent, controller, User))
        b3.config(image=self.logs, compound=TOP)
        #b3.grid(row = 1, column = 7, rowspan=3, columnspan=2)
        b3.place(relx=0.72, rely=0.6, anchor=CENTER)

        self.NoBW=PhotoImage(file=resource_path("./images/NoBW.png"))
        b4 = tk.Button(self, width = 50, height = 50, bg='white', highlightthickness=0, relief='flat', command=lambda : self.ButtonClickNoBW(parent, controller, User))
        b4.config(image=self.NoBW, compound=TOP)
        #b4.grid(row = 1, column = 10, rowspan=3, columnspan=2)
        b4.place(relx=0.27, rely=0.6, anchor=CENTER)

        self.Away=PhotoImage(file=resource_path("./images/Away.png"))
        b5 = tk.Button(self, width = 50, height = 50, bg='white' , highlightthickness=0, relief='flat', command=lambda : self.ButtonClickAway(parent, controller, User))
        b5.config(image=self.Away, compound=TOP)
        #b5.grid(row = 1, column = 12, rowspan=3, columnspan=2)
        b5.place(relx=0.88, rely=0.6, anchor=CENTER)


        self.incall=PhotoImage(file=resource_path("./images/incall.png"))
        b6 = tk.Button(self, width = 50, height = 50, bg='white', highlightthickness=0, relief='flat', command=lambda : self.ButtonClickIncall(parent, controller, User))
        b6.config(image=self.incall, compound=TOP)
        #b3.grid(row = 1, column = 7, rowspan=3, columnspan=2)
        b6.place(relx=0.41, rely=0.6, anchor=CENTER)

        link = Label(self, text="Going out of office? click here", bg="white", fg="deep sky blue", cursor="hand2")
        link.place(relx=0.8, rely=0.2, anchor=CENTER)
        link.bind("<Button-1>",lambda e : self.callback(controller, parent, User))

        link2 = Label(self, text="Click here if you are on BT today", bg="white", fg="deep sky blue", cursor="hand2")
        link2.place(relx=0.8, rely=0.3, anchor=CENTER)
        link2.bind("<Button-1>",lambda e : self.callback2(controller, parent, User))



    def callback(self,controller, parent, Username):
        Result = StatusDatabase.Search(Username)
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="Out of office", LastModified=DateTime)
            controller.hideTom(parent)
        elif(Result[0][2] != "Out of office"):
            StatusDatabase.Update(Username=Username, Status="Out of office", LastModified=DateTime)
            controller.hideTom(parent)
        else:
            controller.hideTom(parent)


    def callback2(self,controller, parent, Username):
        Result = StatusDatabase.Search(Username)
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="BT duty", LastModified=DateTime)
            controller.hideTom(parent)
        elif(Result[0][2] != "BT duty"):
            print(Result[0][2])
            StatusDatabase.Update(Username=Username, Status="BT duty", LastModified=DateTime)
            controller.hideTom(parent)
        else:
            controller.hideTom(parent)



    def ButtonClickAvail(self, parent, controller, Username):
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="Available since " + Current, LastModified=DateTime)
            controller.hide(parent)
        elif("Available" not in str(Result[0][2])):
            print(Result[0][2])
            StatusDatabase.Update(Username=Username,Status="Available since " + Current, LastModified=DateTime)
            controller.hide(parent)
        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)
            controller.hide(parent)


    def ButtonClickWebex(self, parent, controller, Username):
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="WebEx since " + Current, LastModified=DateTime)
            controller.hide(parent)
        elif("WebEx" not in str(Result[0][2])):

            StatusDatabase.Update(Username=Username,Status="WebEx since " + Current, LastModified=DateTime)
            controller.hide(parent)
        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)
            controller.hide(parent)


    def ButtonClickLogs(self, parent, controller, Username):
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="Log Analysis / ESRS since " + Current, LastModified=DateTime)
            controller.hide(parent)
        elif("Log Analysis / ESRS" not in str(Result[0][2])):
            print(Result[0][2])
            StatusDatabase.Update(Username=Username, Status="Log Analysis / ESRS since " + Current, LastModified=DateTime)
            controller.hide(parent)
        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)
            controller.hide(parent)


    def ButtonClickNoBW(self, parent, controller, Username):
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="No Bandwidth since " + Current, LastModified=DateTime)
            controller.hide(parent)
        elif("No Bandwidth" not in str(Result[0][2])):
            print(Result[0][2])
            StatusDatabase.Update(Username=Username, Status="No Bandwidth since " + Current, LastModified=DateTime)
            controller.hide(parent)
        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)
            controller.hide(parent)


    def ButtonClickAway(self, parent, controller, Username):
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="Away since " + Current, LastModified=DateTime)
            controller.hide(parent)
        elif("Away" not in str(Result[0][2])):
            print(Result[0][2])
            StatusDatabase.Update(Username=Username, Status="Away since " + Current, LastModified=DateTime)
            controller.hide(parent)
        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)
            controller.hide(parent)



    def ButtonClickIncall(self, parent, controller, Username):
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="In a call since " + Current, LastModified=DateTime)
            controller.hide(parent)
        elif("In a call" not in str(Result[0][2])):
            print(Result[0][2])
            StatusDatabase.Update(Username=Username, Status="In a call since " + Current, LastModified=DateTime)
            controller.hide(parent)
        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)
            controller.hide(parent)


    def exit_action(icon):
        icon.visible = False
        icon.stop()






def ButtonClickAvail(Username):

    if User == "":
        pass
    else:
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="Available since " + Current, LastModified=DateTime)
        elif("Available" not in str(Result[0][2])):
            print(Result[0][2])
            StatusDatabase.Update(Username=Username, Status="Available since " + Current, LastModified=DateTime)
        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)


def ButtonClickWebex(Username):

    if User == "":
        pass
    else:
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="WebEx since " + Current, LastModified=DateTime)
        elif("WebEx" not in str(Result[0][2])):

            StatusDatabase.Update(Username=Username, Status="WebEx since " + Current, LastModified=DateTime)

        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)


def ButtonClickLogs(Username):

    if User == "":
        pass
    else:
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="Log Analysis / ESRS since " + Current, LastModified=DateTime)
        elif("Log Analysis / ESRS" not in str(Result[0][2])):
            print(Result[0][2])
            StatusDatabase.Update(Username=Username, Status="Log Analysis / ESRS since " + Current, LastModified=DateTime)

        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)

def ButtonClickNoBW(Username):
    if User == "":
        pass
    else:
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="No Bandwidth since " + Current, LastModified=DateTime)
        elif("No Bandwidth" not in str(Result[0][2])):
            print(Result[0][2])
            StatusDatabase.Update(Username=Username, Status="No Bandwidth since " + Current, LastModified=DateTime)

        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)


def ButtonClickAway(Username):
    if User == "":
        pass
    else:
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="Away since " + Current, LastModified=DateTime)
        elif("away" not in str(Result[0][2])):
            print(Result[0][2])
            StatusDatabase.Update(Username=Username, Status="Away since " + Current, LastModified=DateTime)

        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)



def ButtonClickIncall(Username):
    if User == "":
        pass
    else:
        Result = StatusDatabase.Search(Username)
        Current = str(datetime.datetime.now().astimezone(pytz.timezone('US/Eastern')).time())[0:8]
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]
        #Current = str(pendulum.now('America/Toronto'))[11:19] + " EST"
        #DateTime = str(pendulum.now('America/Toronto'))[0:19] + " EST"

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="In a call since " + Current, LastModified=DateTime)
        elif("In a call" not in str(Result[0][2])):

            StatusDatabase.Update(Username=Username, Status="In a call since " + Current, LastModified=DateTime)

        else:
            StatusDatabase.Update(Username=Username, Status=str(Result[0][2]), LastModified=DateTime)



def ButtonClickOOO(Username):
    if User == "":
        pass
    else:
        Result = StatusDatabase.Search(Username)
        DateTime = str(datetime.datetime.today().astimezone(pytz.timezone('US/Eastern')))[0:19]

        if(len(Result) == 0):
            StatusDatabase.Insert(Username=Username, Email=EmailAd, Status="Out of office", LastModified=DateTime)
        else:
            print(Result[0][2])
            StatusDatabase.Update(Username=Username, Status="Out of office", LastModified=DateTime)


# def exit_action(icon):
#     icon.visible = False
#     icon.stop()
# def inactive(self, prex, prevy):
#     newflags, newhcursor, (newx,newy) = win32gui.GetCursorInfo()
#     if(prex == newx and prevy == newy):
#         StatusDatabase.Update(User, "Inactive")

def init_icon():
    icon = pystray.Icon('Status')
    icon.menu = Menu(
        MenuItem('Available', lambda : ButtonClickAvail(User)),
        MenuItem('Webex', lambda : ButtonClickWebex(User)),
        MenuItem('Logs/ESRS', lambda : ButtonClickLogs(User)),
        MenuItem('No Bandwidth', lambda : ButtonClickNoBW(User)),
        MenuItem('Away', lambda : ButtonClickAway(User)),
        MenuItem('In Call', lambda : ButtonClickIncall(User)),
        MenuItem('Out of office', lambda : ButtonClickOOO(User)),
    )
    icon.icon = Image.open(resource_path('./images/icon.png'))
    icon.title = 'Status Update'

    def setup(icon):
        icon.visible = True
        app = IsilonStatus()

        app.mainloop()

        # while icon.visible==True:
        #     flags, hcursor, (prevx,prevy) = win32gui.GetCursorInfo()
        #     self.after(1000 * 10, self.inactive(prevx, prevy))

    icon.run(setup)

    return icon


#Subprocess issue fix
##############################################################################################################


# Create a set of arguments which make a ``subprocess.Popen`` (and
# variants) call work with or without Pyinstaller, ``--noconsole`` or
# not, on Windows and Linux. Typical use::
#
#   subprocess.call(['program_to_run', 'arg_1'], **subprocess_args())
#
# When calling ``check_output``::
#
#   subprocess.check_output(['program_to_run', 'arg_1'],
#                           **subprocess_args(False))
def subprocess_args(include_stdout=True):
    # The following is true only on Windows.
    if hasattr(subprocess, 'STARTUPINFO'):
        # On Windows, subprocess calls will pop up a command window by default
        # when run from Pyinstaller with the ``--noconsole`` option. Avoid this
        # distraction.
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # Windows doesn't search the path by default. Pass it an environment so
        # it will.
        env = os.environ
    else:
        si = None
        env = None

    # ``subprocess.check_output`` doesn't allow specifying ``stdout``::
    #
    #   Traceback (most recent call last):
    #     File "test_subprocess.py", line 58, in <module>
    #       **subprocess_args(stdout=None))
    #     File "C:\Python27\lib\subprocess.py", line 567, in check_output
    #       raise ValueError('stdout argument not allowed, it will be overridden.')
    #   ValueError: stdout argument not allowed, it will be overridden.
    #
    # So, add it only if it's needed.
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}

    # On Windows, running this from the binary produced by Pyinstaller
    # with the ``--noconsole`` option requires redirecting everything
    # (stdin, stdout, stderr) to avoid an OSError exception
    # "[Error 6] the handle is invalid."
    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env })
    return ret

# A simple test routine. Compare this output when run by Python, Pyinstaller,
# and Pyinstaller ``--noconsole``.
# class updateCheck(tk.Frame):
#
#     def __init__(self,parent, controller):
#
#         tk.Frame.__init__(self, parent)
#
#         update = False
#
#         #Gets downloaded version
#         versionSource = open('version.txt', 'r')
#         versionContents = versionSource.read()
#
#         #gets newest version
#         http = urllib3.PoolManager()
#         r = http.request('GET', 'https://github.com/MamdouhEl/MyHourlyStatus/version.txt')
#         updateContents = r.data
#         print(updateContents)
#         # updateSource = urllib.request.urlopen("https://github.com/MamdouhEl/MyHourlyStatus/version.txt")
#         # print("I am here");
#
#
#         #checks for updates
#         for i in range(0,20):
#             if updateContents[i] != versionContents[i]:
#                 versionLabel = Label(self,text="\n\nThere are version updates available.\n\n")
#                 versionLabel.pack()
#                 update = True
#                 B1 = ttk.Button(self, text="Update", command=lambda : controller.show_frame(Startup))
#                 B1.pack()
#                 break
#
#         if update == False:
#             versionLabel = self.Label(self,text="\n\nYou are already running the most up to date version.\n\n")
#             versionLabel.pack()
#             B1 = ttk.Button(self, text="Okay", command=lambda : self.UpdateApp(controller))
#             B1.pack()
#
#     def download(url, dst_file):
#         http = urllib3.PoolManager()
#         content = http.request('GET', url)
#         outfile = open(dst_file, "wb")
#         outfile.write(content.data)
#         outfile.close()
#     def install(prog):
#         process = Popen(prog, shell=True)
#         process.wait()
#     def main():
#         download('https://github.com/MamdouhEl/MyHourlyStatus/MyHourlyStatus.exe', './MyHourlyStatus')
#         install('./MyHourlyStatus')
#
#     def UpdateApp(self, controller):
#         self.main()
#         #run('pip install --src="." --upgrade -e', 'https://github.com/MamdouhEl/MyHourlyStatus/blob/master/Statusapp/MyHourlyStatus.exe')
#         controller.show_frame(Startup)
#
#
def print_status_info(info):
    total = info.get(u'total')
    downloaded = info.get(u'downloaded')
    status = info.get(u'status')
    print(downloaded, total, status)

# class Updater():
#
#
#     def __init__(self, url):
#         """URL Initializes the update procedure"""
#         ERR = False
#         VERSION = 1.0
#         FILE = U.urlopen(url)
#         #FILE = open("update.txt","r")
#         L = str(FILE.read()).splitlines()
#         print """
# UPDATER VERSION: %2.1f
# There are %d file(s) to be updated
#         """ % (VERSION,  len(L))
#         FILE.close()
#         for i in L:
#             SEARCH = re.search("FILENAME=(\w+.\w+)\s+VERSION=(\d+.\d+)\s+DIRECTORY=(\w+)\s+URL=([\w/\\:\.]+)\s+CHANGELOG=([\w+\s\.]+)",i)
#             ifile =  SEARCH.group(1)
#             iver = SEARCH.group(2)
#             idir = SEARCH.group(3)
#             iURL = SEARCH.group(4)
#             ilog = SEARCH.group(5)
#             print "[Downloading] %s from %s" % (ifile,iURL)
#             try:
#                 url = U.urlopen(iURL)
#                 OUT = open(ifile,"w")
#                 print "[Installing] %s" % (ifile)
#                 OUT.write(url.read())
#                 OUT.close()
#                 print "[ver:%s] %s successfully installed." % (iver, ifile)
#             except U.URLError:
#                 print "[Error] Error in downloading from %s" % iURL
#                 ERR=True
#         if ERR:
#             print "Update finished with error"
#         else:
#             print "Successfully updated!"

###############################################################################################
