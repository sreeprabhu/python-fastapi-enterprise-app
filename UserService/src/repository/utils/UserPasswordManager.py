import bcrypt

def saltAndHashedPW(password: str):
    #Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    return hashed_password

def verifyHashedPW(password: str, hashed_password):
    #Verify password later
    if bcrypt.checkpw(password, hashed_password):
        print("✅ Password is correct!")
    else:
        print("❌ Incorrect password.")
