import argon2
from argon2 import PasswordHasher
import re

#inital

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
        salt_value = hash.split('$')[4]      # Splits the salt value to isolate it
        print("Username:", username)         # Prints the username
        print("Hash:", hash)                 # Prints hash with salt value in it
        print("Salt:", salt_value)           # Print just the salt value
        return username, hash, salt_value    # returns three values

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
            
        # Stores the Hash, Salt and Username into a text file
    def store_pass(hash_value,salt_value,username):
        with open("passwordstorage.txt", "a") as text_file:
            text_file.write("%s,%s,%s" % (hash_value, salt_value,username))

        # Reads from the text file to match the Hash,Salt and Username
    def read_pass(hash_value,salt_value,username):
        with open("passwordstorage.txt", "r") as file:
            for line in file:
                print(line.strip())

# Menu options and function declarations (STILL NEEDS TO BE FULLY IMPLEMENTED)
if __name__ == "__main__":
    manager = Argon2Password()
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    print("Password Given: ", password)               # For testing purposes only

    password_strength = manager.check_password_strength(password)
    username, hash_value, salt_value = manager.password_hasher(username, password)

    #password_verify(password)
    verify = input("Please type in your password again to verify: ")
    valid = manager.password_verify(hash_value, verify)
    if valid:
        print("Password verification result: Valid")
    else:
        print("Invalid")
