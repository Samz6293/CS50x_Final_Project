from cs50 import SQL
from helpers import exit_now, decorate_bottom, decorate_bottom_long, decorate_top,decorate_top_long
from tabulate import tabulate
import sys

db = SQL("sqlite:///expenses.db")


def main():
    
    print()
    print("=" * 30)
    print("💰 Welcome to Expense Tracker!")
    print("~" * 30)
    
        
    while True:
        
        # Create a menu list for tabulate
        menu = [
        ["1. Add Expense", "5. Delete Expense"],
        ["2. View All",    "6. Add User"],
        ["3. By Category", "7. Delete User"],
        ["4. View Total",  "8. Exit"]
        ]

        print(tabulate(menu, tablefmt="rounded_grid")) 
        choice = input("\n👉 Enter your choice (1-8): ").strip()
        
            
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_by_category()
        elif choice == "4":
            view_total()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            add_user()
        elif choice == "7":
            delete_user()
        elif choice == "8":
            print("\n👋 Thanks for using Expense Tracker!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please try again. ❌")

def valid_id():
    
    # Getting and validating ID from user
    while True:
        user_id = input("\nSelect the id of user: ").strip()
        id_check = db.execute("SELECT * FROM users WHERE id=?", user_id)

        if id_check:
            return user_id
        print(f"❌ INVALID ID: {user_id}. Try again! ❌\n")


def valid_category():
    
    # Getting non-empty transaction category from user
    while True:
        category = input("Category: ").strip()
        if category:
            return category
        print("❌ Category cannot be empty. ❌\n")


def all_users():       

    # Showing users in the database
    users = db.execute("SELECT id,name FROM users ORDER BY id")
    if not users:
        print("No users in database, Insert a user first")
    else:
        decorate_top()
        print(tabulate(users, headers="keys", tablefmt="rounded_grid"))
        decorate_bottom()

def add_expense():
    
    all_users()

    # Getting valid user_id, category, amount and note from the user
    user_id = valid_id()
    category = valid_category()
    while True:
        try:
            amount = float(input("Amount: ").strip())
            if amount <= 0:
                raise ValueError
            break
        except ValueError:
            print("❌ Amount must be a positive number. ❌\n")
            continue   
    note = input("Note (optional): ").strip()
 
    # Inserting the values
    db.execute("INSERT INTO expenses (user_id, amount, category, note) VALUES (?, ?, ?, ?)",
               user_id, amount, category, note)
    
    # Success message
    print(f"\n✅ SUCCESS! Added $ {amount:,.2f} to '{category}' category")
    print(f"📝 Note: \"{note}\"\n" if note else "")

    exit_now()


def view_expenses():

    all_users()
    user_id = valid_id()
    expenses = db.execute("SELECT id AS transaction_id, category, amount, note, expense_at FROM expenses WHERE user_id=? ORDER BY expense_at", user_id)
    if not expenses:
        print("\n❌ No transaction record of the user found! ❌\n")
        return                
    
    # Showing all the expenses of a user in a decorated way
    decorate_top_long()
    print(tabulate(expenses, headers="keys", tablefmt="rounded_grid"))
    decorate_bottom_long()
    exit_now()

def view_by_category():
    
    all_users()
    user_id = valid_id()

    check_all = db.execute("SELECT id FROM expenses WHERE user_id=?", user_id)
    if not check_all:
        print("\n" + "~" * 34)
        print("🤷‍♂️ This user has no expenses yet!")
        print("~" * 34)
        exit_now()
        return
    
    print(f"\n📂 Available Categories for User {user_id}:")
    categories = db.execute("SELECT DISTINCT category FROM expenses WHERE user_id=?", user_id)
    
    # This prints a tiny, cute table of just the categories
    print(tabulate(categories, tablefmt="rounded_grid"))
    print("-" * 30)
    
    # Getting valid category from the user
    while True:
        category = valid_category()
        expenses = db.execute("SELECT * FROM expenses WHERE user_id=? AND category=?", user_id, category)
        if not expenses:
            print(f"\n❌ No expenses found in '{category}'. ❌")
            print(f"👉 Please pick a category from the list above.")
            continue
        break

    # Showing transactions based on category
    decorate_top_long()
    print(tabulate(expenses, headers="keys", tablefmt="rounded_grid"))
    decorate_bottom_long()
    exit_now()

def view_total():
    
    all_users()
    user_id = valid_id()
    expenses = db.execute("SELECT SUM(amount) AS total_expense FROM expenses WHERE user_id=?", user_id)
    name = db.execute("SELECT name FROM users WHERE id=?", user_id)
    
    total = expenses[0]["total_expense"]
    final_amount = total if total else 0 

    print("\n" + "- " * 17)
    print(f"Showing expense of user: {name[0]['name']}")
    print(f"💵 GRAND TOTAL: $ {final_amount:,.2f}")
    print("- " * 17 + "\n")
    exit_now()

def delete_expense():
    
    all_users()
    user_id = valid_id()
    expenses = db.execute("SELECT id AS transaction_id, category, amount, note FROM expenses WHERE user_id=?", user_id)

    if not expenses:
        print("\n" + "~" * 40)
        print("🤷‍♂️ This user has no expenses to delete!")
        print("~" * 40 + "\n")
        exit_now()
        return
    
    decorate_top_long()
    print(tabulate(expenses, headers="keys", tablefmt="rounded_grid"))
    decorate_bottom_long()

    while True:
        transaction_id = input("Select the transaction ID you want to Delete: ")
        if not transaction_id:
            print("\n❌ Transaction id cannot be empty. ❌")
            continue
        transaction = db.execute("SELECT * FROM expenses WHERE id=? AND user_id=?", transaction_id, user_id)
        if not transaction:   
            print("\n❌ Invalid transaction id. ❌")
            continue   
        break  

    db.execute("DELETE FROM expenses WHERE id=?", transaction_id)

    print("\n" + "~" * 25)
    print("\n🗑️  DELETED SUCCESSFULLY  🗑️\n")
    print("~" * 25)
    print(tabulate(transaction, headers="keys", tablefmt="rounded_grid"))

    exit_now()

def add_user():

    
    print("\n👤  ADD NEW USER")
    print("-" * 20)
    
    # Asking for a valid name
    while True:
        name = input("Name of user: ").strip()
        if not name:
            print("\n❌ Name cannot be empty! ❌")
            print("-" * 9 + "Try again." + "-" * 9 + "\n")
            continue
        check = db.execute("SELECT * FROM users WHERE name=?", name)
        if check:
            print(f"\n❌ The name '{name}' is already taken. ❌")
            print(f"👉 Please try a different name (e.g. {name}2).\n")
            continue
        break

    # Inserting the new user into the database
    db.execute("INSERT INTO users (name) VALUES (?)", name)   
    new_id = db.execute("SELECT id FROM users WHERE name=?", name)
    # Success Message
    print("\n" + "+~" * 16 + "+")
    print(f"✅  SUCCESS! User '{name}' created.")
    print(f"🆔  Assigned User ID: {new_id[0]['id']}")
    print("+~" * 16 + "+" + "\n") 
    exit_now()

def delete_user():
    
    all_users()
    user_id = valid_id()
    
    # Delete Warning
    decorate_top_long()
    print(f"⚠️  WARNING: You are about to delete User {user_id}")
    print("🗑️  This will permanently erase ALL their history.")
    decorate_bottom_long()
    
    # Confirmation before deleting
    confirm = input(f"⚠️  Are you sure you want to delete User {user_id} and ALL their data? (yes/no): ").lower()
    if confirm != 'yes':
        print("\n❌ Deletion cancelled. ❌\n")
        return

    # Deleting all user transactions
    db.execute("DELETE FROM expenses WHERE user_id=?", user_id)

    # Deleting the user
    db.execute("DELETE FROM users WHERE id=?", user_id)

    # Confirmation message
    print(f"\n✅ User {user_id} and all their expenses have been deleted. ✅\n")
    exit_now()


main()