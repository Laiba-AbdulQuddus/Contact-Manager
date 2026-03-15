import json
from tabulate import tabulate

class ContactManager:
    def __init__(self):
        self.contacts_list = []
        self.count = 0
    
    def AddContacts(self):
        while True:
            name = input("Enter full name of the contact (enter 0 to exit): ")
            name = name.strip()
            if name == "0":
                break
            if any(contact["Name"] == name for contact in self.contacts_list):
                print("Name already exists. Try Again")
                continue
            while True:
                phone_number = input("Enter the phone number: ")
                if phone_number.isdigit():
                    break
                print("Please enter a valid Number")

            while True:
                email = input("Enter email address(Press 0 to skip email): ")
                if email == "0":
                    email = None
                    break
                if "@" in email:
                    break
                print("Please enter a valid email address.")
                
            print("Contact Saved Successfully!")
            contact = {
                "ContactID" : f"Contact{self.count}",
                "Name" : name,
                "Phone Number" : phone_number,
                "Email" : email
            }
            self.count += 1
            self.contacts_list.append(contact)
        with open("contacts.txt", 'w') as f:
            json.dump(self.contacts_list, f, indent=4)
        return self.contacts_list


    def ViewContacts(self):
        return self.contacts_list


    def SearchContacts(self):
        search_list = []
        search = input("Enter the name of the contact: ").strip()
        if search == "0":
            return search_list
        found = False
        for contact in self.contacts_list:
            if search.lower() in contact["Name"].lower():
                found = True
                search_list.append(contact)
        if not found:
            print("Contact not found")
        return search_list

    def UpdateContacts(self):
        update_name = input("Enter the full name of the contact you want to update: ").strip()
        for contact in self.contacts_list:
            if update_name.lower() == contact["Name"].lower():
                while True:
                    update = input("Enter what you want to update? Name, Phone Number, Email?: ") 
                    update_lower = update.lower()
                    if update_lower not in ["name", "phone number", "email"]:
                        print("Invalid input.")
                        continue 
                    if "number" in update_lower:
                        while True:
                            new_number = input("Enter New Number: ")
                            if new_number.isdigit():
                                break
                            print("Please enter a valid Number")
                        contact["Phone Number"] = new_number
                    if "email" in update_lower:
                        while True:
                            new_email = input("Enter New Email (Press 0 to skip email): ")
                            new_email = new_email.strip()
                            if new_email == "0":
                                new_email = None
                                break
                            if "@" in new_email:
                                break
                            print("Please enter a valid email address.")
                        contact["Email"] = new_email       
                    if "name" in update_lower:
                        new_name = input("Enter New Name: ")
                        contact["Name"] = new_name 
                    break             
                print("Contact Updated Successfully!!")
            with open("contacts.txt", 'w') as f:
                json.dump(self.contacts_list, f, indent=4)
            return self.contacts_list
        print("Name not found!")
        return self.contacts_list



    def DeleteContacts(self):
        while True:
            delete_id = input("Enter the ContactID to delete (or 0 to exit): ")
            if delete_id == "0":
                break
            found = False
            for contact in self.contacts_list:
                con_id = contact["ContactID"].replace("Contact", "")
                if delete_id == con_id:
                    found = True
                    self.contacts_list.remove(contact)
                    print(f"Contact {delete_id} deleted successfully!")
                    with open("contacts.txt", 'w') as f:
                        json.dump(self.contacts_list, f, indent=4)
                    return self.contacts_list
            if not found: 
                print("ID not found. Please try again.")
            else:
                break
        return self.contacts_list



try:
    with open("contacts.txt", 'r') as f:
        contacts_list = json.load(f)
        if contacts_list:
            max_id = max(int(contact["ContactID"].replace("Contact", "")) for contact in contacts_list)
            count = max_id + 1

except (FileNotFoundError, json.JSONDecodeError):
    contacts_list = []
    count = 0

Menu = [
    "1. Add Contact",
    "2. View Contacts",
    "3. Search Contact",
    "4. Update Contact",
    "5. Delete Contact",
    "6. Exit"
]

manager = ContactManager()
manager.contacts_list = contacts_list
manager.count = count

while True:

    print(f"Menu:\n {Menu[0]}\n {Menu[1]}\n {Menu[2]}\n {Menu[3]}\n {Menu[4]}\n {Menu[5]}\n Choose from the above Menu.")
    try:
        Choice = int(input("Enter any number between 1 - 6: "))
    except ValueError:
        print("Please enter a number between 1 - 6")
        continue

    if Choice == 1:
        contact = manager.AddContacts()
        print(tabulate(contact, headers="keys", tablefmt="grid"))
    elif Choice == 2:
        contact = manager.ViewContacts()
        print(tabulate(contact, headers="keys", tablefmt="grid"))
    elif Choice == 3:
        contact = manager.SearchContacts()
        print(tabulate(contact, headers="keys", tablefmt="grid"))
    elif Choice == 4:
        contact = manager.UpdateContacts()
        print(tabulate(contact, headers="keys", tablefmt="grid"))
    elif Choice == 5:
        contact = manager.DeleteContacts()
        print(tabulate(contact, headers="keys", tablefmt="grid"))
    elif Choice == 6:
        print("Exiting...Thankyou!")
        break
    else:
        print("Please enter a number between 1 - 6.")