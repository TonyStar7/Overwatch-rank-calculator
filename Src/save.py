import json


def save_file(data, path, acc_list, sub_acc_list):
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
        tag_exists = any(acc['Tag'] == write_data['Tag'] for acc in acc_list)
        if not tag_exists:
            acc_list.append(write_data)
            sub_acc_list.append(write_data)
        else:
            for i, acc in enumerate(acc_list):
                if acc["Tag"] == write_data["Tag"]:
                    acc_list[i] = write_data            #replace the account data with the new one
                    break
            sub_acc_list = acc_list.copy()
        with open(path, mode="w", encoding="utf-8") as file:
            json.dump(acc_list, file, indent=4)


def _save_data_to_file(path, acc_list):
        try:
            with open(path, mode="w", encoding="utf-8") as file:
                json.dump(acc_list, file, indent=4)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving file: {e}")


def load_file(path, acc_list, sub_acc_list):
        try:
            with open(path, encoding="utf-8") as file:
                acc_list = json.load(file)
                sub_acc_list = acc_list.copy()
        except FileNotFoundError:
            print("No file, start from []")
            acc_list = []
        except json.JSONDecodeError:
            acc_list = []