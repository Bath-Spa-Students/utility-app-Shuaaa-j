import time
from prettytable import PrettyTable

class VendingMachine:

    def __init__(self):
        # Define menu items with codes, names, prices, categories, and stock
        self.menu = {
            'A1': {'name': 'Coca-Cola', 'price': 2.00, 'category': 'Drinks', 'stock': 5},
            'A2': {'name': 'Water', 'price': 1.00, 'category': 'Drinks', 'stock': 8},
            'B1': {'name': 'Cheetos', 'price': 4.00, 'category': 'Chips', 'stock': 3},
            'B2': {'name': 'Doritos', 'price': 7.25, 'category': 'Chips', 'stock': 4},
            'C1': {'name': 'Hershey', 'price': 2.50, 'category': 'Sweets', 'stock': 1},
            'C2': {'name': 'Snicker', 'price': 2.00, 'category': 'Sweets', 'stock': 8},
        }

        self.balance = 0  # Initialize user balance
        self.purchased_items = []  # To store purchased items for receipt

    def display(self):
        print(""" 
█░█ █▀▀ █▄░█ █▀▄ █ █▄░█ █▀▀   █▀▄▀█ ▄▀█ █▀▀ █░█ █ █▄░█ █▀▀
▀▄▀ ██▄ █░▀█ █▄▀ █ █░▀█ █▄█   █░▀░█ █▀█ █▄▄ █▀█ █ █░▀█ ██▄
             ________________________  
            |  ____________________  |
            | | []      []      [] | |
            | |--------------------| |
            | | []      []      [] | |
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
            table.add_row([code, item['name'], f"AED {item['price']:.2f}", item['category'], item['stock']])
        print(table)

    def money(self):
        # Prompt the user to insert money and handle input validation
        while True:
            try:
                money = float(input("Insert money: AED "))
                if money >= 0:  # Allow inserting zero for the remaining balance
                    return money  # Return the original amount without discount
                else:
                    print("Invalid amount. Please insert a valid amount.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def add_more(self):
        # Allow the user to add more money to their balance
        additional_money = self.money()
        self.balance += additional_money

    def select_item(self):
        # Allow the user to select items and handle balance, stock, and purchasing logic
        while True:
            code = input("\nEnter the code (or '0' to stop): ").upper()
            if code == '0':
                break
            if code in self.menu:
                item = self.menu[code]
                while item['stock'] > 0 and item['price'] > self.balance:
                    print(f"Insufficient funds for {item['name']}.")
                    add_more = input("Do you want to add more money? (yes/no): ").lower()
                    if add_more == 'yes':
                        self.add_more()
                    else:
                        print("\nOrdering stopped. Thank you for using the vending machine!")
                        return
                if item['stock'] > 0:
                    # Process the purchase, update balance, stock, and provide feedback to the user
                    self.balance -= item['price']
                    item['stock'] -= 1
                    print(f"\nDispensing {item['name']}...")
                    time.sleep(2)
                    print("\nEnjoy your", item['name'] + "!")
                    self.suggest(item['category'])
                    self.change_display()
                    self.purchased_items.append({'item_name': item['name'], 'item_price': item['price']})
                else:
                    print("Sorry, this item is out of stock.")
            else:
                print("Invalid code. Please enter a valid code.")

    def change_display(self):
        # Display the remaining balance if it's greater than zero
        if self.balance > 0:
            print(f"Remaining Balance: AED {self.balance:.2f}")

    def change_return(self):
        # Display and return the remaining balance to the user
        if self.balance > 0:
            print(f"Returning change: AED {self.balance:.2f}")
            time.sleep(1)

    def suggest(self, category):
        # Provide suggestions based on the category of the purchased item
        suggestions = {
            'Drinks': 'How about adding some snacks like Chips?',
            'Chips': 'Some sweets would go well after eating chips!',
            'Sweets': 'We recommend drinks alongside your sweets as refreshment!'
        }
        if category in suggestions:
            print(suggestions[category])

    def buy_item(self):
        # Ask the user if they want to make another purchase and handle the logic
        another_purchase = input("Do you want to make another purchase? (yes/no): ").lower()
        if another_purchase == 'yes':
            self.select_item()
        else:
            self.change_return()

    def run_vending(self):
        # Run the vending machine by displaying the menu, accepting money, and allowing item selection
        self.display()
        print(f"Current Balance: AED {self.balance:.2f}")
        money_inserted = self.money()
        self.balance += money_inserted
        self.select_item()

    def create_rec(self, apply_discount=True):
        # Generate a receipt with optional discount and return it as a string
        if apply_discount:
            coupon = input("Do you have a coupon? Enter coupon code (or 'No' to skip): ").upper()
            discount = 0
            if coupon == "RAFIA":  
                discount = 10  
                print(f"Applied {discount}% discount!")

        receipt = "\n===== Receipt =====\n"
        for item in self.purchased_items:
            receipt += f"{item['item_name']} -- AED {item['item_price']:.2f}\n"

        total_price = sum(item['item_price'] for item in self.purchased_items)
        if apply_discount:
            # Calculate discount and display it on the receipt
            discount_amount = (discount / 100) * total_price
            total_with_discount = total_price - discount_amount
            receipt += f"Original Price --- AED {total_price:.2f}\n"
            receipt += f"Given Price --- AED {total_with_discount:.2f}\n"
            if coupon != "RAFIA":  # Skip returning change if coupon is applied
                vending_machine.change_return()
        else:
            # Display the total price without discount and return change
            receipt += f"Total --- AED {total_price:.2f}\n"
            vending_machine.change_return()

        receipt += "===================\n"
        return receipt

if __name__ == "__main__":
    vending_machine = VendingMachine()  
    vending_machine.run_vending()

    while True:
        # Ask the user if they want a receipt
        end = input("Would you like a receipt? (yes/no): ").lower()

        if end == "no":
            # If the user doesn't want a receipt
            apply_discount = input("Do you have a coupon code? (yes/no): ").lower()
            if apply_discount == "yes":
                # If the user has a coupon but chooses not to get a receipt
                print("\nCoupon code can only be applied if you choose to receive a receipt as per company policy.")
                total_price = sum(item['item_price'] for item in vending_machine.purchased_items)
                print(f"\nTotal Price: AED {total_price:.2f}")
                vending_machine.change_return()
                print("Thank you for buying!")
                break  # Exit the loop after completing the transaction
            else:
                # If the user doesn't have a coupon and chooses not to get a receipt
                total_price = sum(item['item_price'] for item in vending_machine.purchased_items)
                print(f"\nTotal Price: AED {total_price:.2f}")
                vending_machine.change_return()
                print("Thank you for buying!")
                break  # Exit the loop after completing the transaction
        elif end == "yes":
            # If the user wants a receipt
            print(vending_machine.create_rec())
            break  # Exit the loop after generating the receipt
        else:
            # Invalid entry for the receipt preference
            print("Invalid entry. Please enter 'yes' or 'no'. Try again.")