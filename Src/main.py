from tkinter import *
import requests
import json

class MyWindow(Tk):
    def __init__(self):
        super().__init__()
        #Tk.__init__(self)

        self.acc_list = []
        self.list_row_counter = 1
        self.bg_lightgray ="#858585"
        self.account = StringVar(value="Example : TonyStar-21880")

        self.load_file()


        #header
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1) #spacer column
        self.grid_columnconfigure(2, weight=0)

        #row for accs
        self.grid_rowconfigure(1, weight=1)

        self.add_frame = Frame(self, bg="#333333")
        self.add_frame.grid(row=0, column=0, sticky="nsew") #Put in grid on the left

        #init add button
        self.add_button = Button(self.add_frame, text="Add account", command=self.added_acc)
        self.add_button.pack(side="right")

        #add account entry
        self.add_entry = Entry(self.add_frame, textvariable=self.account, font=("Calibri", 12), fg="#858585")
        self.add_entry.pack(side="left", padx=(0,10), ipadx=10, ipady=5)

        #add refresh frame
        refresh_frame = Frame(self, bg="#333333")
        refresh_frame.grid(row=0, column=2, sticky="nsew") #Put in grid on the right

        #add refresh button
        refresh_button = Button(refresh_frame, text="REFRESH", padx=40, pady=5)
        refresh_button.grid(row=0, column=2, sticky="nsew")


        #list of acc
        self.list_frame = Frame(self, bg="#858585", highlightbackground="white", highlightthickness=2)
        self.list_frame.grid(row=1, column=1, columnspan=1, sticky="new")      
        for column in range(7):
            self.list_frame.grid_columnconfigure(column, weight=1)
        

        game = Label(self.list_frame, text="Game", fg="White", bg=self.bg_lightgray, font=("Calibri", 15))
        game.grid(column=1, row=0, padx=10)
        acc = Label(self.list_frame, text="Account", fg="White", bg=self.bg_lightgray, font=("Calibri", 15))
        acc.grid(column=2, row=0, padx=40)
        tank = Label(self.list_frame, text="Tank", fg="White", bg=self.bg_lightgray, font=("Calibri", 15))
        tank.grid(column=3, row=0, padx=40)
        dps = Label(self.list_frame, text="DPS", fg="White", bg=self.bg_lightgray, font=("Calibri", 15))
        dps.grid(column=4, row=0, padx=40)
        supp = Label(self.list_frame, text="Support", fg="White", bg=self.bg_lightgray, font=("Calibri", 15))
        supp.grid(column=5, row=0, padx=40)
        owner = Label(self.list_frame, text="Owner", fg="White", bg=self.bg_lightgray, font=("Calibri", 15))
        owner.grid(column=6, row=0, padx=40)

        self.populate_grid()

        self.add_entry.bind("<FocusIn>", self.add_entry_click_delete)
        
        self.bind("<Button-1>", self.global_click)

        self.title("Overwatch Rank Calculator")
        self.configure(bg="#333333", padx=20, pady=20)
        self.geometry("1920x1080")
        


# Function to get rank for each role
    def rank_info(self, player_data, role):
        try:
            rank_data = player_data["competitive"]["pc"][role]
            if rank_data and rank_data.get("division"):
                return f"{rank_data["division"].upper()} {rank_data["tier"]}"
            else:
                return "UNRANKED"
        except KeyError:
            return "PRIVATE"
        

    def add_acc_to_list(self, player_id, player_data):

        # Call the info
        account_name = player_data["username"]
        tank = self.rank_info(player_data, "tank")
        damage = self.rank_info(player_data, "damage")
        support = self.rank_info(player_data, "support")
        owner = "N/A"

        # Put infos in a list
        row_data = [
            "OW",
            account_name,
            tank,
            damage,
            support,
            owner,
        ]

        curr_row = self.list_row_counter

        # Create new row for each acc
        for col, content in enumerate(row_data):
            button = Button(self.list_frame, text="X", fg="White", bg=self.bg_lightgray, font=("Calibri", 15), command=lambda r=curr_row: self.delete_acc(r))    #delete button
            button.grid(row=curr_row, column=0, sticky="nsew")
            label = Label(self.list_frame, text=content, fg="White", bg=self.bg_lightgray, font=("Calibri", 15))
            label.grid(row=curr_row, column=col+1, sticky="nsew")
        self.list_row_counter += 1
        self.list_frame.grid_rowconfigure(curr_row, weight=1)
        self.save_file(row_data)


# Function when add button is clicked
    def added_acc(self):
        player_id = self.add_entry.get()
        if "Example :" in player_id or not player_id.strip():
            return
        player_data = self.get_ow_player_data(player_id)

        if player_data:
            print("\nAPI response received")
            print(f"Username : {player_data["username"]}")
            self.add_acc_to_list(player_id, player_data)
        else:
            print("Failed to retrieve player data.")
    


    #delete row in acc list
    def delete_acc(self, row):
        for widget in self.list_frame.winfo_children():
            grid_data = widget.grid_info()
            if grid_data.get('row') == row:
                widget.destroy()

    #auto delete default text of entry when clicked
    def add_entry_click_delete(self, event):
        if self.add_entry.get() == "Example : TonyStar-21880":
            self.add_entry.delete(0, END)

    #add default text to add_entry
    def add_entry_default_text(self, event):
        if self.add_entry.get() == "":
            self.account.set("Example : TonyStar-21880")
            self.add_entry.config(fg="#858585")
    
    def global_click(self, event):
        widget = event.widget
        if widget != self.add_entry:
            self.add_entry_default_text(event)
            self.focus()



    # Saving data in a json file
    def save_file(self, data):
        write_data = {
            "Game": data[0],
            "username": data[1],
            "tank": data[2],
            "dps": data[3],
            "support": data[4],
            "owner": data[5],
        }
        self.acc_list.append(write_data)
        with open("save.json", mode="w", encoding="utf-8") as file:
            json.dump(self.acc_list, file, indent=4)
        with open("save.json", encoding="utf-8") as file:
            content = json.load(file)
    


    # Load file
    def load_file(self):
        try:
            with open("save.json", encoding="utf-8") as file:
                self.acc_list = json.load(file)
        except FileNotFoundError:
            print("No file, start from []")
            self.acc_list = []
        except json.JSONDecodeError:
            self.acc_list = []
    

    #Load file data into the grid
    def populate_grid(self):
        self.list_row_counter = 1
        for player_data in self.acc_list:
            row_data = [
            player_data["Game"],
            player_data["username"],
            player_data["tank"],
            player_data["dps"],
            player_data["support"],
            player_data["owner"],
        ]
            self._create_row_widgets(row_data)
        

    # Seperate function to avoid infinite calls from populate_grid
    def _create_row_widgets(self, row_data):
        curr_row = self.list_row_counter
    
        # Create new row for each acc
        for col, content in enumerate(row_data):
            button = Button(self.list_frame, text="X", fg="White", bg=self.bg_lightgray, font=("Calibri", 15), command=lambda r=curr_row: self.delete_acc(r))
            button.grid(row=curr_row, column=0, sticky="nsew")
            label = Label(self.list_frame, text=content, fg="White", bg=self.bg_lightgray, font=("Calibri", 15))
            label.grid(row=curr_row, column=col+1, sticky="nsew")
        
        self.list_row_counter += 1
        self.list_frame.grid_rowconfigure(curr_row, weight=1)

    #API PART
    BASE_URL = "https://overfast-api.tekrop.fr"
    
    def get_ow_player_data(self, player_id):
        url =f"{self.BASE_URL}/players/{player_id}/summary"  #Access Player Summary
        response = requests.get(url)

        if response.status_code == 200:
            print(f"fetch successful for {player_id}")
            player_data = response.json()               #Convert to JSON data
            return player_data
        else:
            print(f"Problem accessing API, status code: {response.status_code}")
    
    

window = MyWindow()
window.mainloop()


