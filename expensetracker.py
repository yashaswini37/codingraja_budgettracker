import tkinter as tk
from tkinter import messagebox
import csv
from collections import defaultdict

def load_budget():
    budget = defaultdict(float)
    try:
        with open("budget.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                budget[row['Category']] += float(row['Amount'])
    except FileNotFoundError:
        print("Budget file not found. Creating a new budget file.")
    return budget

def save_budget(budget):
    with open("budget.csv", "w", newline='') as file:
        fieldnames = ['Category', 'Amount']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for category, amount in budget.items():
            writer.writerow({'Category': category, 'Amount': amount})

def add_transaction():
    category = category_entry.get()
    amount = float(amount_entry.get())

    if category and amount:
        if transaction_type.get() == "Income":
            budget[category] += amount
        else:
            budget[category] -= amount
        save_budget(budget)
        update_display()
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter both category and amount.")

def update_display():
    remaining_budget_var.set(f"Remaining Budget: ${calculate_remaining_budget():.2f}")

def calculate_remaining_budget():
    total_income = sum(amount for category, amount in budget.items() if amount > 0)
    total_expense = sum(amount for category, amount in budget.items() if amount < 0)
    remaining_budget = total_income + total_expense
    return remaining_budget

def display_spending_trends():
    trends = ""
    for category, amount in budget.items():
        if amount < 0:
            trends += f"{category}: ${-amount:.2f}\n"
    messagebox.showinfo("Spending Trends", trends)

def reset_budget():
    global budget
    budget = defaultdict(float)
    save_budget(budget)
    update_display()

budget = load_budget()

root = tk.Tk()
root.title("Budget Tracker")

transaction_type = tk.StringVar()
transaction_type.set("Expense")

tk.Label(root, text="Category:").grid(row=0, column=0, sticky="w")
category_entry = tk.Entry(root, width=30)
category_entry.grid(row=0, column=1)

tk.Label(root, text="Amount:").grid(row=1, column=0, sticky="w")
amount_entry = tk.Entry(root, width=30)
amount_entry.grid(row=1, column=1)

income_radio = tk.Radiobutton(root, text="Income", variable=transaction_type, value="Income")
income_radio.grid(row=2, column=0)
expense_radio = tk.Radiobutton(root, text="Expense", variable=transaction_type, value="Expense")
expense_radio.grid(row=2, column=1)

add_button = tk.Button(root, text="Add Transaction", command=add_transaction)
add_button.grid(row=3, columnspan=2, pady=10)

remaining_budget_var = tk.StringVar()
remaining_budget_var.set(f"Remaining Budget: ${calculate_remaining_budget():.2f}")
remaining_budget_label = tk.Label(root, textvariable=remaining_budget_var)
remaining_budget_label.grid(row=4, columnspan=2)

spending_trends_button = tk.Button(root, text="Spending Trends", command=display_spending_trends)
spending_trends_button.grid(row=5, columnspan=2, pady=10)

reset_button = tk.Button(root, text="Reset", command=reset_budget)
reset_button.grid(row=6, columnspan=2, pady=10)

# Center the window
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

root.mainloop()
