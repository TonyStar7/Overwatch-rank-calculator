from tkinter import *

class MyWindow(Tk):
    def __init__(self):
        super().__init__()
        #Tk.__init__(self)

        self.account = StringVar(value="Example : TonyStar#21880")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        for column in range(6):
            self.grid_columnconfigure(column, weight=1)

        add_frame = Frame(self, bg="#333333", highlightbackground="red", highlightthickness=2)
        add_frame.grid(row=0, column=0)

        #init add button
        add_button = Button(add_frame, text="Add account", command=self.added_acc)
        add_button.pack(side="right")

        #add account entry
        self.add_entry = Entry(add_frame, textvariable=self.account, font=("Calibri", 12), fg="#858585")
        self.add_entry.pack(side="left", padx=(0,10), ipadx=10, ipady=5)

        #add refresh frame
        refresh_frame = Frame(self, bg="#333333", highlightbackground="green", highlightthickness=2)
        refresh_frame.grid(sticky="e", row=0, column=5)

        #add refresh button
        refresh_button = Button(refresh_frame, text="REFRESH", padx=40, pady=5)
        refresh_button.pack()


        #list of acc
        list = Frame(self, bg="#858585", highlightbackground="Black", highlightthickness=2)
        list.grid
        for column in range(6):
            list.grid_columnconfigure(column, weight=1)
        for row in range(4):
            list.grid_rowconfigure(row, weight=1)

        game = Label(list, text="Game", fg="White", bg="#858585", font=("Calibri", 15), highlightthickness=2, highlightbackground="Red")
        game.grid(column=0, row=0, padx=10)
        acc = Label(list, text="Account", fg="White", bg="#858585", font=("Calibri", 15))
        acc.grid(column=1, row=0, padx=40)
        tank = Label(list, text="Tank", fg="White", bg="#858585", font=("Calibri", 15))
        tank.grid(column=2, row=0, padx=40)
        dps = Label(list, text="DPS", fg="White", bg="#858585", font=("Calibri", 15))
        dps.grid(column=3, row=0, padx=40)
        supp = Label(list, text="Support", fg="White", bg="#858585", font=("Calibri", 15))
        supp.grid(column=4, row=0, padx=40)
        owner = Label(list, text="Owner", fg="White", bg="#858585", font=("Calibri", 15))
        owner.grid(column=5, row=0, padx=40)


        self.add_entry.bind("<FocusIn>", self.add_entry_click_delete)
        
        self.bind("<Button-1>", self.global_click)

        self.title("Hello")
        self.configure(bg="#333333", padx=20, pady=20)
        self.geometry("800x400")

    def added_acc(self):
        print("Added account")

    #auto delete default text of entry when clicked
    def add_entry_click_delete(self, event):
        if self.add_entry.get() == "Example : TonyStar#21880":
            self.add_entry.delete(0, END)

    #add default text to add_entry
    def add_entry_default_text(self, event):
        if self.add_entry.get() == "":
            self.account.set("Example : TonyStar#21880")
            self.add_entry.config(fg="#858585")
    
    def global_click(self, event):
        widget = event.widget
        if widget != self.add_entry:
            self.add_entry_default_text(event)
            self.focus()

        



window = MyWindow()
window.mainloop()
