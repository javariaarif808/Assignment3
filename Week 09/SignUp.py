import tkinter as tk
from tkinter import messagebox

CREDENTIALS_FILE = "credentials.txt"


def save_credentials():
    """Save new user credentials (Sign Up)."""
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Empty Fields", "Please enter both username and password.")
        return

    # Check if user already exists
    if user_exists(username):
        messagebox.showerror("Error", "Username already taken.")
        return

    with open(CREDENTIALS_FILE, "a") as f:
        f.write(f"{username},{password}\n")

    messagebox.showinfo("Success", "Account created! You can now sign in.")


def user_exists(username):
    """Check if a username is already registered."""
    try:
        with open(CREDENTIALS_FILE, "r") as f:
            for line in f:
                saved_user, _ = line.strip().split(",", 1)
                if saved_user == username:
                    return True
    except FileNotFoundError:
        pass  # File doesn't exist yet — no users registered
    return False


def check_credentials():
    """Verify login credentials (Sign In)."""
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Empty Fields", "Please enter both username and password.")
        return

    try:
        with open(CREDENTIALS_FILE, "r") as f:
            for line in f:
                saved_user, saved_pass = line.strip().split(",", 1)
                if saved_user == username and saved_pass == password:
                    messagebox.showinfo("Welcome", f"Hello, {username}!")
                    return
    except FileNotFoundError:
        pass

    messagebox.showerror("Failed", "Invalid username or password.")


# --- UI setup ---
root = tk.Tk()
root.title("Sign In / Sign Up")
root.geometry("300x220")

tk.Label(root, text="Login", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

tk.Button(root, text="Sign In", width=15, command=check_credentials).pack(pady=2)
tk.Button(root, text="Sign Up", width=15, command=save_credentials).pack(pady=2)

root.mainloop()