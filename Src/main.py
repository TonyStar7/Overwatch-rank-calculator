from tkinter import *
import requests
import json
import os

class MyWindow(Tk):
    def __init__(self):
        super().__init__()

        self.BASE_URL = "https://overfast-api.tekrop.fr"
        self.json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save.json")
        self.acc_list = []
        self.sub_acc_list = []
        self.list_row_counter = 1
        self.bg_lightgray ="#858585"
        self.account = StringVar(value="Example : TonyStar#21880")

        self.RANK_ORDER = {
            "BRONZE": 1,
            "SILVER": 2,
            "GOLD": 3,
            "PLATINUM": 4,
            "DIAMOND": 5,
            "MASTER": 6,
            "GRANDMASTER": 7,
            "CHAMPION": 8,
            "UNRANKED": 0,
        }

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
        refresh_button = Button(refresh_frame, text="REFRESH", padx=40, pady=5, command=self.refresh)
        refresh_button.grid(row=0, column=2, sticky="nsew")


        #list of acc
        self.list_frame = Frame(self, bg="#858585", highlightbackground="white", highlightthickness=2)
        self.list_frame.grid(row=1, column=1, columnspan=1, sticky="new")      
        for column in range(7):
            self.list_frame.grid_columnconfigure(column, weight=1)

        game = Label(self.list_frame, text="Game", fg="White", bg=self.bg_lightgray, font=("Calibri", 15))
        game.grid(column=1, row=0, padx=10)
        tag = Label(self.list_frame, text="Tag", fg="White", bg=self.bg_lightgray, font=("Calibri", 15))
        tag.grid(column=2, row=0, padx=10)
        acc = Button(self.list_frame, text="Account", fg="White", bg=self.bg_lightgray, font=("Calibri", 15), command=self.sort_alpha)
        acc.grid(column=3, row=0, padx=40)
        tank = Button(self.list_frame, text="Tank", fg="White", bg=self.bg_lightgray, font=("Calibri", 15), command=self.sort_tank)
        tank.grid(column=4, row=0, padx=40)
        dps = Button(self.list_frame, text="DPS", fg="White", bg=self.bg_lightgray, font=("Calibri", 15), command=self.sort_dps)
        dps.grid(column=5, row=0, padx=40)
        supp = Button(self.list_frame, text="Support", fg="White", bg=self.bg_lightgray, font=("Calibri", 15), command=self.sort_supp)
        supp.grid(column=6, row=0, padx=40)

        self.populate_grid(self.acc_list)        #Populate with default list

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
        

    def add_acc_to_list(self, player_id, tag, player_data):      

        # Call the info
        role_data = player_data["competitive"]["pc"]

        account_name = player_data["username"]
        tank= self.rank_info(player_data, "tank")
        tier_tank = role_data["tank"]["tier"] if tank not in ["UNRANKED", "PRIVATE"] else 0
        damage= self.rank_info(player_data, "damage")
        tier_damage = role_data["damage"]["tier"] if damage not in ["UNRANKED", "PRIVATE"] else 0
        support= self.rank_info(player_data, "support")
        tier_support = role_data["support"]["tier"] if support not in ["UNRANKED", "PRIVATE"] else 0
        
        # Put infos in a list
        row_data = [
            "OW",
            tag,
            account_name,
            tank,
            damage,
            support,
            tier_tank,
            tier_damage,
            tier_support
        ]
        curr_row = self.list_row_counter

        # Create new row for each acc
        for col, content in enumerate(row_data[:-3]):
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
        tag_position = player_id.find("#")  #find the tag
        tag = player_id[tag_position:]
        player_id = player_id.replace("#", "-")
        if "Example :" in player_id or not player_id.strip():
            return
        player_data = self.get_ow_player_data(player_id)

        if player_data:
            print("\nAPI response received")
            print(f"Username : {player_data["username"]}")
            self.add_acc_to_list(player_id, tag, player_data)
        else:
            print("Failed to retrieve player data.")
    


    #delete row in acc_list and sub_acc_list
    def delete_acc(self, row):
        list_index = row - 1
        try:
            remove_value = self.sub_acc_list.pop(list_index)
            self.acc_list.remove(remove_value)
            print("Data successfully deleted")
        except IndexError:
            print(f"Error: Could not delete at index {list_index}. List length is {len(self.acc_list)}.")
            return
        self._save_data_to_file()

        self.rebuild_grid()


    def sort_alpha(self):
        self.sub_acc_list = sorted(self.sub_acc_list, key=lambda account: account["username"])
        self.populate_grid(self.sub_acc_list)
    
    
    def sort_tank(self):
        MAX_TIER = 5
        self.sub_acc_list = sorted(self.sub_acc_list, key=lambda acc_rank: 
            (
            self.RANK_ORDER.get(acc_rank["tank"].split()[0], 99),
            MAX_TIER-acc_rank["tier_tank"]
            ),
            reverse = True
        )
        self.populate_grid(self.sub_acc_list)


    def sort_dps(self):
        MAX_TIER = 5
        self.sub_acc_list = sorted(self.sub_acc_list, key=lambda acc_rank: 
            (
            self.RANK_ORDER.get(acc_rank["dps"].split()[0], 99),
            MAX_TIER-acc_rank["tier_damage"]
            ),
            reverse = True
        )
        self.populate_grid(self.sub_acc_list)


    def sort_supp(self):
        MAX_TIER = 5
        self.sub_acc_list = sorted(self.sub_acc_list, key=lambda acc_rank: 
            (
            self.RANK_ORDER.get(acc_rank["support"].split()[0], 99),
            MAX_TIER-acc_rank["tier_support"]
            ),
            reverse = True
        )
        self.populate_grid(self.sub_acc_list)
        

    def refresh(self):
        updated_acc_list = []
        for account in self.acc_list:
            clean_tag = account["Tag"].replace("#", "")
            player_id = f"{account["username"]}-{clean_tag}"
            player_data = self.get_ow_player_data(player_id)

            if player_data is None:
                print(f"Skipping update for {player_id}. Keeping old data.")
                updated_acc_list.append(account) # Keep the old data if refresh failed
                continue
            try:
            # Call the info
                role_data = player_data["competitive"]["pc"]

                account_name = player_data["username"]
                tank= self.rank_info(player_data, "tank")
                print(tank)
                tier_tank = role_data["tank"]["tier"] if tank not in ["UNRANKED", "PRIVATE"] else 0
                damage= self.rank_info(player_data, "damage")
                print(damage)
                tier_damage = role_data["damage"]["tier"] if damage not in ["UNRANKED", "PRIVATE"] else 0
                support= self.rank_info(player_data, "support")
                print(support)
                tier_support = role_data["support"]["tier"] if support not in ["UNRANKED", "PRIVATE"] else 0
        
        # Put infos in a list
                updated_data = {
                    "Game": "OW",
                    "Tag": account["Tag"],
                    "username": account_name,
                    "tank": tank,
                    "dps": damage,
                    "support": support,
                    "tier_tank": tier_tank,
                    "tier_damage": tier_damage,
                    "tier_support": tier_support
                }
                updated_acc_list.append(updated_data)
            except KeyError as e:
                print(f"Error processing data for {player_id}: Missing key {e}. Keeping old data.")
                updated_acc_list.append(account)

        self.acc_list = updated_acc_list
        self.sub_acc_list = self.acc_list.copy()

        self._save_data_to_file()
        self.rebuild_grid()
    

    # Save list in json file
    def _save_data_to_file(self):
        try:
            with open(self.json_file_path, mode="w", encoding="utf-8") as file:
                json.dump(self.acc_list, file, indent=4)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving file: {e}")


    # Rebuild the grid after deleting
    def rebuild_grid(self):
        widgets_to_destroy = []
        for widget in self.list_frame.winfo_children():
            grid_data = widget.grid_info()
        
            if grid_data.get('row', 0) > 0:
                widgets_to_destroy.append(widget)
    
        for widget in widgets_to_destroy:
            widget.destroy()

        self.list_frame.update_idletasks()
        self.populate_grid(self.sub_acc_list)
        

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


    # Saving data in a JSON FILE
    def save_file(self, data):
        write_data = {
            "Game": data[0],
            "Tag": data[1],
            "username": data[2],
            "tank": data[3],
            "dps": data[4],
            "support": data[5],
            "tier_tank": data[6],
            "tier_damage": data[7],
            "tier_support": data[8]
        }
        tag_exists = any(acc['Tag'] == write_data['Tag'] for acc in self.acc_list)
        if not tag_exists:
            self.acc_list.append(write_data)
            self.sub_acc_list.append(write_data)
        else:
            for i, acc in enumerate(self.acc_list):
                if acc["Tag"] == write_data["Tag"]:
                    self.acc_list[i] = write_data            #replace the account data with the new one
                    break
            self.sub_acc_list = self.acc_list.copy()
        with open(self.json_file_path, mode="w", encoding="utf-8") as file:
            json.dump(self.acc_list, file, indent=4)


    # Load file
    def load_file(self):
        try:
            with open(self.json_file_path, encoding="utf-8") as file:
                self.acc_list = json.load(file)
                self.sub_acc_list = self.acc_list.copy()
        except FileNotFoundError:
            print("No file, start from []")
            self.acc_list = []
        except json.JSONDecodeError:
            self.acc_list = []
    

    #Load file data into the grid
    def populate_grid(self, list):
        self.list_row_counter = 1
        for player_data in list:
            row_data = [                # filter what to put in the grid
            player_data["Game"],
            player_data["Tag"],
            player_data["username"],
            player_data["tank"],
            player_data["dps"],
            player_data["support"],
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


