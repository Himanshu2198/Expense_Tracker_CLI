from functions import addExpense,viewExpense,deleteExpense,monthlySummary,exportToCSV

# FILENAME = "expense.json"

def menu():
    while True:
        print("\n*********Expense Tracker*********")
        print("1. Add Expense")
        print("2. View Expense")
        print("3. Delete Expense")
        print("4. View Monthly Summary")
        print("5. Export to CSV")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            amount = float(input("Enter Amount: "))
            category = input("Enter Category: ")
            addExpense(category,amount)

        elif choice == "2":
            viewExpense()

        elif choice == "3":
            # viewExpense()
            deleteExpense()

        elif choice == "4":
            monthlySummary()

        elif choice == "5":
            exportToCSV()

        elif choice =="6":
            print("Exiting...")
            break

        else:
            print("Invalid choice")

if __name__=="__main__":
    menu()
