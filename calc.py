import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect("calculator_history.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        num1 REAL,
        num2 REAL,
        operation TEXT,
        result REAL
    )
""")
conn.commit()

# Calculator operations
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

# Function to calculate result & store in DB
def calculate():
    try:
        a = entry1.get()
        b = entry2.get()
        ch = operator_var.get()
        
        if not a or not b:
            messagebox.showerror("Input Error", "Please enter both numbers.")
            return
        
        a = float(a)
        b = float(b)

        if ch == '+':
            res = add(a, b)
        elif ch == '-':
            res = subtract(a, b)
        elif ch == '*':
            res = multiply(a, b)
        elif ch == '/':
            res = divide(a, b)
        else:
            messagebox.showerror("Operator Error", "Invalid operator selected.")
            return
        
        result.set(res)

        # Store result in DB
        cursor.execute("INSERT INTO history (num1, num2, operation, result) VALUES (?, ?, ?, ?)", (a, b, ch, res))
        conn.commit()
        load_history()

    except ValueError:
        messagebox.showerror("Input Error", "Invalid input! Please enter numeric values.")

# Function to load history from DB
def load_history():
    history_listbox.delete(0, tk.END)
    cursor.execute("SELECT num1, operation, num2, result FROM history ORDER BY id DESC LIMIT 10")
    for row in cursor.fetchall():
        history_listbox.insert(tk.END, f"{row[0]} {row[1]} {row[2]} = {row[3]}")

# Function to clear input fields
def clear():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    result.set("")
    operator_var.set("+")

# Function to clear history
def clear_history():
    cursor.execute("DELETE FROM history")
    conn.commit()
    load_history()

# Function to exit the application
def exit_app():
    conn.close()
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Calculator with History")
root.geometry("400x450")
root.configure(bg="lightblue")

# Input Fields
tk.Label(root, text="Enter 1st number:", bg="lightblue").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Enter 2nd number:", bg="lightblue").pack()
entry2 = tk.Entry(root)
entry2.pack()

# Operator Selection
tk.Label(root, text="Select operation:", bg="lightblue").pack()
operator_var = tk.StringVar(value="+")
operator_menu = tk.OptionMenu(root, operator_var, "+", "-", "*", "/")
operator_menu.pack()

# Calculate Button
tk.Button(root, text="Calculate", command=calculate, bg="green", fg="white").pack(pady=5)

# Result Display
result = tk.StringVar()
tk.Label(root, text="Result:", bg="lightblue").pack()
tk.Entry(root, textvariable=result, state="readonly").pack()

# History Display
tk.Label(root, text="History (Last 10 calculations):", bg="lightblue").pack()
history_listbox = tk.Listbox(root, height=5)
history_listbox.pack()
load_history()

# Clear & Exit Buttons
tk.Button(root, text="Clear", command=clear, bg="orange").pack(pady=5)
tk.Button(root, text="Clear History", command=clear_history, bg="red").pack(pady=5)
tk.Button(root, text="Exit", command=exit_app, bg="gray").pack(pady=5)

# Run GUI
root.mainloop()
