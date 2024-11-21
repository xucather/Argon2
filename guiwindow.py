from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher
import re
import tkinter as tk
from tkinter import messagebox

# Class for all the functions
class Argon2Password:
    # Create a PasswordHasher object with desired parameters
    def __init__(self):
        self.ph = argon2.PasswordHasher(
            time_cost=3,  # Number of iterations
            memory_cost=65536,  # Memory usage in KiB
            parallelism=4,  # Number of parallel threads
            hash_len=32,  # Length of the hash in bytes
            salt_len=16  # Length of the salt in bytes
        )

    # Encrypts a password with a salt value and produces a hash value and has a username
    def password_hasher(self, username, password):
        hash = self.ph.hash(password)  # Hashes the password based on PasswordHasher object
        salt_value = hash.split('$')[4]  # Splits the salt value to isolate it
        print("Username:", username)  # Prints the username
        print("Hash:", hash)  # Prints hash with salt value in it
        print("Salt:", salt_value)  # Print just the salt value
        return username, hash, salt_value  # returns three values

    # Verify/Authenticate a password and username against the hash
    def password_verify(self, hash, password):
        try:
            valid = self.ph.verify(hash, password)
            if valid:
                print("Password is valid")
                return True
        except argon2.exceptions.VerifyMismatchError:
            print("Password is not valid")
        return False

    # Check the strength of the password
    def check_password_strength(self, password):
        contains_lowercase = re.search(r'[a-z]', password)
        contains_uppercase = re.search(r'[A-Z]', password)
        contains_digit = re.search(r'[0-9]', password)
        contains_special_char = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        length = len(password)

        if contains_lowercase and contains_uppercase and contains_digit and contains_special_char and length >= 8:
            strength = "Strong"
            print(f"Password Strength: {strength}")
        
        elif contains_lowercase and contains_uppercase and contains_digit and length >= 6:
            strength = "Moderate"
            print(f"Password Strength: {strength}")
        else:
            strength = "Weak"
            print(f"Password Strength: {strength}")
        return strength

    # Store the Hash, Salt, and Username into a text file
    def store_pass(self, hash_value, salt_value, username):
        with open("passwordstorage.txt", "a") as text_file:
            text_file.write("%s,%s,%s\n" % (hash_value, salt_value, username))

    # Reads from the text file to match the Hash, Salt, and Username
    def read_pass(self, hash_value, salt_value, username):
        with open("passwordstorage.txt", "r") as file:
            for line in file:
                print(line.strip())

# GUI for getting username and password input
def show_gui():
    def on_submit():
        global hash_value  
        username = entry_username.get()
        password = entry_password.get()

        if username and password:
            username, hash_value, salt_value = manager.password_hasher(username, password)
            pw_strength = manager.check_password_strength(password)

            # Display the password strength in a message box
            if pw_strength == "Weak":
                messagebox.showinfo("Password Strength", f"Password Strength: {pw_strength} \n\nWeak passwords do not satisfy all of the following conditions: \nAt least 1 lowercase letter \nAt least 1 uppercase letter \nAt least 1 digit \nAt least 1 special character \nAt least 8 total characters \n\nTime to Crack Through Brute Force: Instantly - 6tn Years")

            elif pw_strength == "Moderate":
                messagebox.showinfo("Password Strength", f"Password Strength: {pw_strength} \n\nModerate passwords do not satisfy all of the following conditions: \nAt least 1 lowercase letter \nAt least 1 uppercase letter \nAt least 1 digit \nAt least 1 special character \nAt least 8 total characters \n\nTime to Crack Through Brute Force: 1 Second - 100tn Years")

            elif pw_strength == "Strong":
                messagebox.showinfo("Password Strength", f"Password Strength: {pw_strength} \n\nStrong passwords satisfy all of the following conditions: \nAt least 1 lowercase letter \nAt least 1 uppercase letter \nAt least 1 digit \nAt least 1 special character \nAt least 6 total characters \n\nTime to Crack Through Brute Force: 8 Hours - 7qd Years")

            # Display the result in a message box
            messagebox.showinfo("Password Hashed", f"Username: {username}\nHash: {hash_value}\nSalt: {salt_value}")

            # Optionally store password in a file
            manager.store_pass(hash_value, salt_value, username)

            # Disable the input fields and change the label to ask for verification
            entry_username.config(state="disabled")
            entry_password.config(state="disabled")
            label_verification.pack(pady=10)

            # Add the verification password input field
            label_verify_password.pack(pady=5)
            entry_verify_password.pack(pady=5)
            button_verify.pack(pady=10)

        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    def on_verify():
        # Get the password entered in the verification field
        verify_password = entry_verify_password.get()
        if manager.password_verify(hash_value, verify_password):
            messagebox.showinfo("Verification Result", "Password verification successful.")
        else:
            messagebox.showwarning("Verification Failed", "Password verification failed.")

    # Create the GUI pop-up window
    global root
    root = tk.Tk()
    root.title("Argon2 Password Manager")
    root.geometry("400x400")

    # Username field
    tk.Label(root, text="Username:").pack(pady=5)
    global entry_username
    entry_username = tk.Entry(root, width=30)
    entry_username.pack(pady=5)

    # Password field
    tk.Label(root, text="Password:").pack(pady=5)
    global entry_password
    entry_password = tk.Entry(root, show="*", width=30)
    entry_password.pack(pady=5)

    # Submit button
    button_submit = tk.Button(root, text="Submit", command=on_submit)
    button_submit.pack(pady=20)

    # Label for verification
    global label_verification
    label_verification = tk.Label(root, text="Please verify your password below:")

    # Verification password field (hidden initially)
    global label_verify_password
    label_verify_password = tk.Label(root, text="Verify Password:")
    global entry_verify_password
    entry_verify_password = tk.Entry(root, show="*", width=30)

    # Verification button (hidden initially)
    global button_verify
    button_verify = tk.Button(root, text="Verify", command=on_verify)

   
    root.mainloop()


if __name__ == "__main__":
    manager = Argon2Password()
    show_gui()