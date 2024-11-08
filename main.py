import argon2
from argon2 import PasswordHasher


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
    '''def password_verify(password):
        try:
            ph.verify(hash, password)
            print("Password is valid")
        except argon2.exceptions.VerifyMismatchError:
            print("Password is not valid")
        return True'''
    
        # Stores the Hash, Salt and Username into a text file
    def store_pass(hash_value,salt_value,username):
        with open("passwordstorage.txt", "a") as text_file:
            text_file.write("%s,%s,%s" % (hash_value, salt_value,username))
            
        # Reads from the text file for to match the Hash,Salt and Username
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
    username, hash_value, salt_value = manager.password_hasher(username, password)
    #password_verify(password)
