#- Encrypt the password with a salt value

#- Store the password in text file 
#- Comma separated like (hashed value, salt value)

def store_pass(hash_value,salt_value):
    with open("passwordstorage.txt", "a") as text_file:
        text_file.write("%s %s\n" % (hash_value, salt_value))

store_pass("hash","salt")

#- Authenticate that the password can be retrieved
#- Verification

#- The menu options for encrption, decryptions, and closing (exiting) the program
#- Run in some kind of loop so the program doesn't have to relaunch every time.