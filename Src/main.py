from tkinter import *

class MyWindow(Tk):
    def __init__(self):
        super().__init__()
        #Tk.__init__(self)

        bg_lightgray ="#858585"

        self.account = StringVar(value="Example : TonyStar#21880")

        #header
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1) #spacer column
        self.grid_columnconfigure(2, weight=0)

        #row for accs
        self.grid_rowconfigure(1, weight=1)

        self.add_frame = Frame(self, bg="#333333", highlightbackground="red", highlightthickness=2)
        self.add_frame.grid(row=0, column=0, sticky="nsew") #Put in grid on the left

        #init add button
        self.add_button = Button(self.add_frame, text="Add account", command=self.added_acc)
        self.add_button.pack(side="right")

        #add account entry
        self.add_entry = Entry(self.add_frame, textvariable=self.account, font=("Calibri", 12), fg="#858585")
        self.add_entry.pack(side="left", padx=(0,10), ipadx=10, ipady=5)

        #add refresh frame
        refresh_frame = Frame(self, bg="#333333", highlightbackground="green", highlightthickness=2)
        refresh_frame.grid(row=0, column=2, sticky="nsew") #Put in grid on the right

        #add refresh button
        refresh_button = Button(refresh_frame, text="REFRESH", padx=40, pady=5)
        refresh_button.grid(row=0, column=2, sticky="nsew")


        #list of acc
        list = Frame(self, bg="#858585", highlightbackground="white", highlightthickness=2)
        list.grid(row=1, column=1, columnspan=1, sticky="new")      
        for column in range(6):
            list.grid_columnconfigure(column, weight=1)
        for row in range(4):
            list.grid_rowconfigure(row, weight=1)

        game = Label(list, text="Game", fg="White", bg=bg_lightgray, font=("Calibri", 15), highlightthickness=2, highlightbackground="Red")
        game.grid(column=0, row=0, padx=10)
        acc = Label(list, text="Account", fg="White", bg=bg_lightgray, font=("Calibri", 15))
        acc.grid(column=1, row=0, padx=40)
        tank = Label(list, text="Tank", fg="White", bg=bg_lightgray, font=("Calibri", 15))
        tank.grid(column=2, row=0, padx=40)
        dps = Label(list, text="DPS", fg="White", bg=bg_lightgray, font=("Calibri", 15))
        dps.grid(column=3, row=0, padx=40)
        supp = Label(list, text="Support", fg="White", bg=bg_lightgray, font=("Calibri", 15))
        supp.grid(column=4, row=0, padx=40)
        owner = Label(list, text="Owner", fg="White", bg=bg_lightgray, font=("Calibri", 15))
        owner.grid(column=5, row=0, padx=40)


        acc_game = Label(list, text="Overwatch", fg="White", bg=bg_lightgray, font=("Calibri", 15))
        acc_game.grid(row=1, column=0)


        self.add_entry.bind("<FocusIn>", self.add_entry_click_delete)
        
        self.bind("<Button-1>", self.global_click)

        self.title("Overwatch Rank Calculator")
        self.configure(bg="#333333", padx=20, pady=20)
        self.geometry("1600x800")

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
