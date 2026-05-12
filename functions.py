import json
from datetime import datetime
from collections import defaultdict
import csv

# Add expense function
def addExpense(category,amount):
    expense = {
        "category": category,
        "amount" : float(amount),
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    try:
        with open("expense.json","r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    # append new entry
    data.append(expense)

    # save
    with open("expense.json","w") as file:
        json.dump(data,file,indent = 4)
        print("\nExpense Added")


# View expense function
def viewExpense():
    try:
        with open("expense.json","r") as file:
            data = json.load(file)

    except FileNotFoundError:
        print("No Data file exists!")
        return

    # Check if the data is empty
    except json.JSONDecodeError:
        print("You've not made any expense yet.")
        return

    exp_list = defaultdict(list)
    for expense in data:
        # print(expense) #Debug
        category = expense.get("category")
        amount = expense.get("amount")
        exp_date = expense.get("date")

        date = datetime.strptime(exp_date,"%Y-%m-%d")

        exp_list[category].append((amount,date))

    print (f"\nYour Compelete Expense")
    print("-"*30)


    for category,expenses in exp_list.items():
        print(f"\nCategory: {category}")

        for amount, date in expenses:
            print(f"₹{amount} on {date.strftime('%Y-%m-%d')}")

    # print(data)

# Delete expense function
def deleteExpense():
    try:
        with open("expense.json","r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("No Data file exists!")
        return
    
    # Check if the data is empty
    except json.JSONDecodeError:
        print("You've not made any expense yet.")
        return
    
    category = input("Enter the category to be deleted: ")
    new_data = [exp for exp in data if exp.get("category") != category]

    with open("expense.json","w") as file:
        json.dump(new_data,file,indent=4)

    print("Record successfully Deleted!")

# Summarise Monthly Expense method
def monthlySummary():
    try:
        with open("expense.json","r") as file:
            data = json.load(file)


            # print(data) # Debug
    except FileNotFoundError:
        print("No Data file exists!")
        return
    
    # Check if the data is empty
    except json.JSONDecodeError:
        print("You've not made any expense yet.")
        return
    
    month = int(input("Enter the month (1-12):"))
    year = int(input("Enter the year: "))
    
    summary = defaultdict(float)
    for expense in data:
        # print(expense) #Debug
        exp_date = expense.get("date")

        date = datetime.strptime(exp_date,"%Y-%m-%d")

        if date.month == month and date.year == year:
            category = expense.get("category")
            amount = expense.get("amount")
            summary[category] += amount

    print (f"\nExpense Summary for the {month}/{year}")
    print("-"*30)

    total = 0

    if not summary:
        print("No expenses found for this month.")

    for category,amount in summary.items():
        print(f"{category} : ₹{amount}")

        total += amount

    print("-"*30)
    print(f"Total Expense :₹{total}")

def exportToCSV():

    try:
        with open("expense.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        print("No expense data file found!")
        return

    except json.JSONDecodeError:
        print("Expense file is empty!")
        return

    with open("expense.csv", "w", newline="") as csv_file:

        fieldnames = ["category", "amount", "date"]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write column headers
        writer.writeheader()

        # Write expense rows
        writer.writerows(data)

    print("Expenses exported successfully to expense.csv")