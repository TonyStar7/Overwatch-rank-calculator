from tkinter import *
import json
import os
from PIL import Image, ImageTk
from .api_client import *
import time

class MyWindow(Tk):
    def __init__(self):
        super().__init__()

        self.json_file_path = os.path.join(os.getcwd(), "data", "save.json")
        self.IMG_DIR = os.path.join(project_root, "assets")
        self.acc_list = []
        self.sub_acc_list = []
        self.list_row_counter = 1
        self.bg_lightgray ="#858585"
        self.account = StringVar(value="Example : TonyStar#21880")

        self.role_list = []
        self.selected_accounts = []
        self.owner_list = []
        self.max_range_tuple = None
        self.min_range_tuple = None

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

        self.RANKS = [
            "BRONZE",
            "SILVER",
            "GOLD",
            "PLATINUM",
            "DIAMOND",
            "MASTER",
            "GRANDMASTER",
            "CHAMPION"
        ]
        

        self.load_file()

        self.cross_img = Image.open(os.path.join(IMG_DIR, "red_cross.png"))
        self.cross_photo = ImageTk.PhotoImage(self.cross_img)
        self.ow_img = Image.open(os.path.join(IMG_DIR, "ow_logo.png"))
        self.ow_photo = ImageTk.PhotoImage(self.ow_img)

        #Loading role icons
        self.tank_img = Image.open(os.path.join(IMG_DIR, "Tank_icon.png"))
        self.tank_photo = ImageTk.PhotoImage(self.tank_img)
        self.damage_img = Image.open(os.path.join(IMG_DIR, "Damage_icon.png"))
        self.damage_photo = ImageTk.PhotoImage(self.damage_img)
        self.support_img = Image.open(os.path.join(IMG_DIR, "Support_icon.png"))
        self.support_photo = ImageTk.PhotoImage(self.support_img)
        
        self.grandmaster_img = Image.open(os.path.join(IMG_DIR, "Grandmaster_icon.png"))
        self.grandmaster_photo = ImageTk.PhotoImage(self.grandmaster_img)
        self.master_img = Image.open(os.path.join(IMG_DIR, "Master_icon.png"))
        self.master_photo = ImageTk.PhotoImage(self.master_img)
        self.diamond_img = Image.open(os.path.join(IMG_DIR, "Diamond_icon.png"))
        self.diamond_photo = ImageTk.PhotoImage(self.diamond_img)
        self.platinum_img = Image.open(os.path.join(IMG_DIR, "Platinum_icon.png"))
        self.platinum_photo = ImageTk.PhotoImage(self.platinum_img)
        self.gold_img = Image.open(os.path.join(IMG_DIR, "Gold_icon.png"))
        self.gold_photo = ImageTk.PhotoImage(self.gold_img)
        self.silver_img = Image.open(os.path.join(IMG_DIR, "Silver_icon.png"))
        self.silver_photo = ImageTk.PhotoImage(self.silver_img)
        self.bronze_img = Image.open(os.path.join(IMG_DIR, "Bronze_icon.png"))
        self.bronze_photo = ImageTk.PhotoImage(self.bronze_img)

        #header
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1) #spacer column
        self.grid_columnconfigure(2, weight=0)

        #row for accs
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

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
            if column == 0:
                self.list_frame.grid_columnconfigure(column, weight=0)
            else:
                self.list_frame.grid_columnconfigure(column, weight=1)
        

        
        game = Label(self.list_frame, text="Game", fg="White", bg=self.bg_lightgray, font=("Calibri", 12))
        game.grid(column=1, row=0, padx=10)
        tag = Label(self.list_frame, text="Tag", fg="White", bg=self.bg_lightgray, font=("Calibri", 12))
        tag.grid(column=2, row=0, padx=10)
        acc = Button(self.list_frame, text="Accounts", fg="White",cursor="hand2", bg=self.bg_lightgray, font=("Calibri", 12), command=self.sort_alpha)
        acc.grid(column=3, row=0, padx=40)
        tank = Button(self.list_frame, image=self.tank_photo, cursor="hand2",border=0, bg=self.bg_lightgray, command=self.sort_tank)
        tank.grid(column=4, row=0, padx=40)
        dps = Button(self.list_frame, image=self.damage_photo, cursor="hand2", border=0, bg=self.bg_lightgray, command=self.sort_dps)
        dps.grid(column=5, row=0, padx=40)
        supp = Button(self.list_frame, image=self.support_photo, cursor="hand2",border=0, bg=self.bg_lightgray, command=self.sort_supp)
        supp.grid(column=6, row=0, padx=40)
        owner = Button(self.list_frame, text="Owner", border=0, cursor="hand2",bg=self.bg_lightgray, fg="White", font=("Calibri", 12), command=self.sort_owner)
        owner.grid(column=7, row=0, padx=40)
        



        self.squad_frame = Frame(self, bg="#858585", highlightbackground="white", highlightthickness=2)
        self.squad_frame.grid(row=2, column=1, columnspan=1, sticky="new")

        for column in range(5):
            self.squad_frame.grid_columnconfigure(column, weight=1)
            self.squad_frame.grid_rowconfigure(4, weight=1)


        self.populate_grid(self.acc_list)        #Populate with default list
        

        self.add_entry.bind("<FocusIn>", self.add_entry_click_delete)
        
        self.bind("<Button-1>", self.global_click)

        self.title("Overwatch Rank Calculator")
        self.configure(bg="#333333", padx=20, pady=20)
        self.geometry("1920x1080")
        




    def add_acc_to_list(self, player_id, tag, player_data):      

        # Call the info
        role_data = player_data["competitive"]["pc"]

        account_name = player_data["username"]
        tank= rank_info(player_data, "tank")
        tier_tank = role_data["tank"]["tier"] if tank not in ["UNRANKED", "PRIVATE"] else 0
        damage= rank_info(player_data, "damage")
        tier_damage = role_data["damage"]["tier"] if damage not in ["UNRANKED", "PRIVATE"] else 0
        support= rank_info(player_data, "support")
        tier_support = role_data["support"]["tier"] if support not in ["UNRANKED", "PRIVATE"] else 0
        owner = "N/A"
        
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
            tier_support,
            owner
        ]
        self._create_row_widgets(row_data)
        self.save_file(row_data)
        

# Function when add button is clicked
    def added_acc(self):
        player_id = self.add_entry.get()
        tag_position = player_id.find("#")  #find the tag
        tag = player_id[tag_position:]
        player_id = player_id.replace("#", "-")
        if "Example :" in player_id or not player_id.strip():
            return
        player_data = get_ow_player_data(player_id)

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


    def sort_owner(self):
        self.sub_acc_list = sorted(self.sub_acc_list, key=lambda account: account["owner"])
        self.populate_grid(self.sub_acc_list)
        

    def refresh(self):
        updated_acc_list = []
        for account in self.acc_list:
            clean_tag = account["Tag"].replace("#", "")
            player_id = f"{account["username"]}-{clean_tag}"
            player_data = get_ow_player_data(player_id)
            owner = account["owner"]

            if player_data is None:
                print(f"Skipping update for {player_id}. Keeping old data.")
                updated_acc_list.append(account) # Keep the old data if refresh failed
                continue
            try:
            # Call the info
                role_data = player_data["competitive"]["pc"]

                account_name = player_data["username"]
                tank= rank_info(player_data, "tank")
                print(tank)
                tier_tank = role_data["tank"]["tier"] if tank not in ["UNRANKED", "PRIVATE"] else 0
                damage= rank_info(player_data, "damage")
                print(damage)
                tier_damage = role_data["damage"]["tier"] if damage not in ["UNRANKED", "PRIVATE"] else 0
                support= rank_info(player_data, "support")
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
                    "tier_support": tier_support,
                    "owner": owner
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
            widget.grid_forget()
            widget.destroy()

        self.list_frame.master.update_idletasks()
        self.list_frame.update_idletasks()
        self.populate_grid(self.sub_acc_list)
        
    # Function to change the bg of the button when pressed (select function)
    def change_color(self, button, row_i, column_i):
        curr_color = button.cget("bg")
        if curr_color == self.bg_lightgray:
            new_color = "White"
            fg_color = "Black"
            target_color = "White"
            username_widget = self.list_frame.grid_slaves(row=row_i, column=3)
            if username_widget:
                username_frame = username_widget[0]
                if isinstance(username_frame, Frame):
                    username_button = username_frame.winfo_children()
                    if username_button:
                        username = username_button[0].cget("text")
            role_name = button.role_name
            role_rank = button.rank
            tier = int(button.rank_tier)
            self.rank_range(username, role_rank, tier, role_name)

        else:
            new_color = self.bg_lightgray
            fg_color = "White"
            target_color = self.bg_lightgray
        button.config(bg=new_color, fg=fg_color)
        
        

        if column_i == 3:
            for target_col in range(column_i + 1, column_i + 4):
                widgets = self.list_frame.grid_slaves(row=row_i, column=target_col)
            
                if widgets:
                    cell_frame = widgets[0]
                    inner_frame = cell_frame.winfo_children()[0] # icon frame
                
                    if inner_frame.winfo_children():
                        slave_button = inner_frame.winfo_children()[0] #icon button
                        slave_button.config(bg=target_color)
    
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
            "tier_support": data[8],
            "owner": data[9]
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
            player_data["owner"]
        ]
            self._create_row_widgets(row_data)
        

    # Seperate function to avoid infinite calls from populate_grid
    def _create_row_widgets(self, row_data):
        curr_row = self.list_row_counter
        button = Button(self.list_frame, 
                        image=self.cross_photo,
                        bg=self.bg_lightgray, 
                        font=("Calibri", 15), 
                        highlightthickness=2,
                        highlightbackground="#DB4F4F",
                        activeforeground=self.bg_lightgray,
                        border=0,
                        cursor="hand2",
                        command=lambda r=curr_row: self.delete_acc(r))
        button.grid(row=curr_row, column=0)

        # Create new row for each acc
        for col, content in enumerate(row_data):
            grid_col = col + 1
            
            # cover old frame
            cell_frame = Frame(self.list_frame, bg=self.bg_lightgray)
            cell_frame.grid(row=curr_row, column=grid_col, sticky="nsew")

            # seperating rank and tier in the rank name
            if isinstance(content, str):        # if is a str
                if " " in content:
                    rank_name, tier = content.split()
                else:
                    rank_name = content.upper()
                    tier = None
            
            # Putting the right icon image
            icon = None
            if rank_name == "CHAMPION":
                icon = self.champion_photo
            elif rank_name == "GRANDMASTER":
                icon = self.grandmaster_photo
            elif rank_name == "MASTER":
                icon = self.master_photo
            elif rank_name == "DIAMOND":
                icon = self.diamond_photo
            elif rank_name == "PLATINUM":
                icon = self.platinum_photo
            elif rank_name == "GOLD":
                icon = self.gold_photo
            elif rank_name == "SILVER":
                icon = self.silver_photo
            elif rank_name == "BRONZE":
                icon = self.bronze_photo
            
            # rank part
            if icon is not None and tier is not None:
                container_frame = Frame(cell_frame, bg="#858585")
                container_frame.pack(expand=True)
                role_map = {4: "tank", 5: "dps", 6: "support"}
                current_role = role_map.get(grid_col, "unknown")

                icon_button = Button(container_frame, 
                                    image=icon,
                                    text=rank_name,
                                    bg=self.bg_lightgray,
                                    border=0,
                                    cursor="hand2")
                icon_button.config(command=lambda b=icon_button, r=curr_row, c=grid_col: self.change_color(b, r, c))
                icon_button.rank_tier = tier
                icon_button.rank = rank_name
                icon_button.role_name = current_role
                icon_button.pack(side="left")
                icon_button.image = icon

                text_label = Label(container_frame, 
                                    text=tier, 
                                    fg="White", 
                                    bg=self.bg_lightgray, 
                                    font=("Calibri", 12, "bold"))
                text_label.pack(side="left", padx=2, pady=0)

            elif content == "OW":
                label = Label(cell_frame, image=self.ow_photo, bg=self.bg_lightgray,)
                label.pack(expand=True)
            elif col == 2: # acc column
                acc_button = Button(cell_frame, 
                                    text=content, 
                                    fg="White", 
                                    font=("Calibri", 13, "bold"), 
                                    bg=self.bg_lightgray, 
                                    border=0,
                                    cursor="hand2")
                acc_button.config(command=lambda b=acc_button, r=curr_row, c=grid_col: self.change_color(b, r, c))
                acc_button.pack(expand=True)
            elif col == len(row_data)-1:    # owner column
                owner_label = Label(cell_frame,
                                        text=content, 
                                        fg="White", 
                                        font=("Calibri", 12), 
                                        bg=self.bg_lightgray, 
                                        border=0)
                owner_label.pack(expand=True)
            else:
                label = Label(cell_frame, 
                                text=content, 
                                fg="White", 
                                bg=self.bg_lightgray, 
                                font=("Calibri", 12))
                label.pack(expand=True)
        
        self.list_row_counter += 1
        self.list_frame.grid_rowconfigure(curr_row, weight=1)


    def global_click(self, event):
        widget = event.widget
        if widget != self.add_entry:
            self.add_entry_default_text(event)
            self.focus()

    #add default text to add_entry
    def add_entry_default_text(self, event):
        if self.add_entry.get() == "":
            self.account.set("Example : TonyStar#21880")
            self.add_entry.config(fg="#858585")


    #auto delete default text of entry when clicked
    def add_entry_click_delete(self, event):
        if self.add_entry.get() == "Example : TonyStar#21880":
            self.add_entry.delete(0, END)

    def rank_tuple(self, rank, tier):
        return (self.RANK_ORDER.get(rank.upper(), 0), tier)
    
    def display_squad(self, selected_accounts):
        print("\n=== Current squad ===")
        for username, role_rank, tier, role_name  in selected_accounts:
            print(f"  • {username:15} ({role_name} {role_rank} {tier})")
        print("=" * 30)

    def rank_range(self, username, role_rank, tier, role_name):
        self.selected_accounts.append((username, role_rank, tier, role_name))
        self.owner_list.append(username)
        self.role_list.append(role_rank)
        
        if role_rank in ["MASTER", "GRANDMASTER", "CHAMPION"]:
            range_acc = 3
        elif role_rank == "DIAMOND":
            range_max = 3
            range_min = 5
        elif role_rank in ["BRONZE", "SILVER", "GOLD", "PLATINUM"]:
            range_acc = 5

        tier_up = tier - (range_max if role_rank == "DIAMOND" else range_acc)
        rank_up = 0

        if tier_up < 1:
            tier_up += 5
            rank_up = 1
        
        if rank_up == 0:
            possible_max = role_rank + f" {tier_up}"
            print(f"Possible maximum rank is : {possible_max}")
        else:
            possible_max = self.RANKS[self.RANKS.index(role_rank) + 1] + f" {tier_up}"
            print(f"Possible maximum rank is : {possible_max}")
        tier_down = tier + (range_min if role_rank == "DIAMOND" else range_acc)
        rank_down = 0

        if tier_down > 5:
            rank_down = -1
            tier_down -= 5

        if rank_down == 0:
            possible_min = role_rank + f" {tier_down}"
            print(f"Possible minimum rank is : {possible_min}")
        else:
            possible_min = self.RANKS[self.RANKS.index(role_rank) - 1] + f" {tier_down}"
            print(f"Possible minimum rank is : {possible_min}")
        self.max_range_tuple = self.rank_tuple(possible_max.split()[0], possible_max.split()[1])
        self.min_range_tuple = self.rank_tuple(possible_min.split()[0], possible_min.split()[1])

        self.display_squad(self.selected_accounts)