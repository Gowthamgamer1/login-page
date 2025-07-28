import tkinter as tk
from tkinter import messagebox
import hashlib
import os
import json
import webbrowser

# ------------------------------
# Save Credentials (hashed)
# ------------------------------
CREDENTIALS_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_credentials(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(users, f)
    return True

def load_users():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    return {}

def verify_credentials(username, password):
    users = load_users()
    return username in users and users[username] == hash_password(password)

# ------------------------------
# Work / Game Site Launcher
# ------------------------------
work_sites = {
    "Khan Academy": "https://www.khanacademy.org/",
    "Coursera": "https://www.coursera.org/",
    "W3Schools": "https://www.w3schools.com/",
    "GeeksforGeeks": "https://www.geeksforgeeks.org/",
}

game_sites = {
    "CrazyGames": "https://www.crazygames.com/",
    "Miniclip": "https://www.miniclip.com/",
    "Poki": "https://poki.com/",
    "Armor Games": "https://armorgames.com/",
}

def open_website(url):
    webbrowser.open_new_tab(url)

def show_sites(category):
    clear_screen()
    label_text = " Study Websites" if category == "work" else " Gaming Websites"
    label = tk.Label(root, text=label_text, font=("Segoe UI", 16), bg="white")
    label.pack(pady=20)

    sites = work_sites if category == "work" else game_sites
    for name, url in sites.items():
        btn = tk.Button(root, text=name, font=("Segoe UI", 12), bg="#4CAF50" if category == "work" else "#f44336",
                        fg="white", width=30, command=lambda u=url: open_website(u))
        btn.pack(pady=6)

# ------------------------------
# Auth Interfaces
# ------------------------------
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def show_login():
    clear_screen()
    tk.Label(root, text=" Login", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=20)

    tk.Label(root, text="Username:", bg="white").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password:", bg="white").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def login_user():
        username = username_entry.get()
        password = password_entry.get()
        if verify_credentials(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            show_choice_menu()
        else:
            messagebox.showerror("Failed", "Invalid username or password")

    tk.Button(root, text="Login", command=login_user, bg="#2196F3", fg="white", width=20).pack(pady=10)
    tk.Button(root, text="No account? Register", command=show_register, bg="gray", fg="white").pack(pady=5)

def show_register():
    clear_screen()
    tk.Label(root, text=" Register", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=20)

    tk.Label(root, text="Choose a Username:", bg="white").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Choose a Password:", bg="white").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        if save_credentials(username, password):
            messagebox.showinfo("Registered", "Registration successful! Please log in.")
            show_login()
        else:
            messagebox.showerror("Error", "Username already exists.")

    tk.Button(root, text="Register", command=register_user, bg="#4CAF50", fg="white", width=20).pack(pady=10)
    tk.Button(root, text="Already have an account? Login", command=show_login, bg="gray", fg="white").pack(pady=5)

# ------------------------------
# Main Menu After Login
# ------------------------------
def show_choice_menu():
    clear_screen()
    tk.Label(root, text=" What do you want to do today?", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=40)

    tk.Button(root, text=" Work / Study", font=("Segoe UI", 14), bg="#2196F3", fg="white", width=20,
              command=lambda: show_sites("work")).pack(pady=20)

    tk.Button(root, text=" Play Games", font=("Segoe UI", 14), bg="#9C27B0", fg="white", width=20,
              command=lambda: show_sites("game")).pack(pady=10)

# ------------------------------
# Start App
# ------------------------------
root = tk.Tk()
root.title("Login Protected Productivity Launcher")
root.geometry("500x500")
root.config(bg="white")

show_login()

root.mainloop()
