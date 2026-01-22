import sys

def decorate_top_long():
    print()
    print("=" * 84)
    print("~" * 84)
    print()

def decorate_top():
    print()
    print("=" * 30)
    print("~" * 30)
    print()

def decorate_bottom():
    print()
    print("~" * 30)
    print("=" * 30)
    print()

def decorate_bottom_long():
    print()
    print("~" * 84)
    print("=" * 84)
    print()

def exit_now():
    key = input("Press any key to continue or Q to quit: ").strip().lower()
    if key == "q":
        print("\n👋 Thanks for using Expense Tracker!")
        sys.exit(0)
    