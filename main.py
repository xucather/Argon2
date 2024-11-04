import argon2
from argon2 import PasswordHasher


#inital


# Prompt for password 
password = input("Please enter your password: ")
print("Password Given:", password)

# Create a PasswordHasher object with desired parameters
ph = argon2.PasswordHasher(
    time_cost=3,  # Number of iterations
    memory_cost=65536,  # Memory usage in KiB
    parallelism=4,  # Number of parallel threads
    hash_len=32,  # Length of the hash in bytes
    salt_len=16  # Length of the salt in bytes
)

# Encryption with salt
password = "mysecretpassword"
hash = ph.hash(password)
print(hash)


# Verify a password against the hash
try:
    ph.verify(hash, password)
    print("Password is valid")
except argon2.exceptions.VerifyMismatchError:
    print("Password is not valid")