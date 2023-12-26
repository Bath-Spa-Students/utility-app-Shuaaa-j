import time
from prettytable import PrettyTable

class VendingMachine:

    def __init__(self):
        # Define menu items with codes, names, prices, categories, and stock
        self.menu = {
            'A1': {'name': ' Coke', 'price': 1.50, 'category': 'Drinks', 'stock': 5},
            'A2': {'name': ' Water', 'price': 1.00, 'category': 'Drinks', 'stock': 8},
            'B1': {'name': ' Cheetos', 'price': 1.75, 'category': 'Chips', 'stock': 3},
            'B2': {'name': ' Doritos', 'price': 2.00, 'category': 'Chips', 'stock': 4},
            'C1': {'name': ' Kinder', 'price': 1.50, 'category': 'Sweets', 'stock': 5},
            'C2': {'name': 'Snicker', 'price': 1.00, 'category': 'Sweets', 'stock': 8},
        }

        self.balance = 0  # Initialize user balance
        self.purchased_items = []  # To store purchased items for receipt

    def display_menu(self):
        print(""" 
██╗░░░██╗███████╗███╗░░██╗██████╗░██╗███╗░░██╗░██████╗░  ███╗░░░███╗░█████╗░░█████╗░██╗░░██╗██╗███╗░░██╗███████╗
██║░░░██║██╔════╝████╗░██║██╔══██╗██║████╗░██║██╔════╝░  ████╗░████║██╔══██╗██╔══██╗██║░░██║██║████╗░██║██╔════╝
╚██╗░██╔╝█████╗░░██╔██╗██║██║░░██║██║██╔██╗██║██║░░██╗░  ██╔████╔██║███████║██║░░╚═╝███████║██║██╔██╗██║█████╗░░    
░╚████╔╝░██╔══╝░░██║╚████║██║░░██║██║██║╚████║██║░░╚██╗  ██║╚██╔╝██║██╔══██║██║░░██╗██╔══██║██║██║╚████║██╔══╝░░
░░╚██╔╝░░███████╗██║░╚███║██████╔╝██║██║░╚███║╚██████╔╝  ██║░╚═╝░██║██║░░██║╚█████╔╝██║░░██║██║██║░╚███║███████╗
░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚═════╝░╚═╝╚═╝░░╚══╝░╚═════╝░  ╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝ 
         ________________________  
        |  ____________________  |
        | | []  []  []  []  [] | |
        | |--------------------| |
        | | []  []  []  []  [] | |
        | |--------------------| |
        | |____________________| |
        | |  ________________  | |
        | | | COLLECT        | | |
        | | |           HERE | | |
        | |  ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅   | |
        |  ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅   |
        |̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ |
        |_|̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ |_|""")
        table = PrettyTable()
        table.field_names = ["Code", "Item", "Price", "Category", "Stock"]
        for code, item in self.menu.items():
            table.add_row([code, item['name'], f"${item['price']:.2f}", item['category'], item['stock']])
        print(table)

    def accept_money(self):
        while True:
            try:
                money = float(input("Insert money: AED"))
                if money >= 0:  # Allow inserting zero for the remaining balance
                    return money
                else:
                    print("Invalid amount. Please insert a valid amount.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def select_item(self):
        code = input("Enter the code: ").upper()
        if code in self.menu:
            item = self.menu[code]
            if item['stock'] > 0 and item['price'] <= self.balance:
                self.balance -= item['price']
                item['stock'] -= 1
                print(f"\nDispensing {item['name']}...")
                time.sleep(2)
                print("\nEnjoy your", item['name'] + "!")
                self.suggest_purchase(item['category'])
                self.display_change()
                self.buy_additional_item()
                self.purchased_items.append({'item_name': item['name'], 'item_price': item['price']})
            elif item['stock'] == 0:
                print("Sorry, this item is out of stock.")
            else:
                print("Insufficient funds. Please insert more money.")
        else:
            print("Invalid code. Please enter a valid code.")

    def display_change(self):
        if self.balance > 0:
            print(f"Remaining Balance: ${self.balance:.2f}")

    def return_change(self):    
        if self.balance > 0:
            print(f"Returning change: ${self.balance:.2f}")
            time.sleep(1)

    def suggest_purchase(self, category):
        suggestions = {
            'Drinks': 'How about adding some snacks like Chips?',
            'Snacks': 'Would you like to try a refreshing drink like Water?',
            'Sweets': 'Would you like Water?'
        }
        if category in suggestions:
            print(suggestions[category])

    def buy_additional_item(self):
        another_purchase = input("Do you want to make another purchase? (yes/no): ").lower()
        if another_purchase == 'yes':
            self.select_item()
        else:
            self.return_change()

    def run_vending_machine(self):
        self.display_menu()
        print(f"Current Balance: ${self.balance:.2f}")
        money_inserted = self.accept_money()
        self.balance += money_inserted
        self.select_item()

    def create_receipt(self):
        receipt = "\n===== Receipt =====\n"
        for item in self.purchased_items:
            receipt += f"\t{item['item_name']} -- ${item['item_price']:.2f}\n"
        receipt += f"\tTotal --- ${sum(item['item_price'] for item in self.purchased_items):.2f}\n"
        receipt += "===================\n"
        return receipt

if __name__ == "__main__":
    vending_machine = VendingMachine()
    vending_machine.run_vending_machine()

    rec_bool = int(input("1. Print the receipt? 2. Only print the total sum: "))
    if rec_bool == 1:
        print(vending_machine.create_receipt())
    elif rec_bool == 2:
        print(f"Total Sum: ${sum(item['item_price'] for item in vending_machine.purchased_items):.2f}")
    else:
        print("INVALID ENTRY")