# Importing libraries..

from urllib.request import urlopen, hashlib

# Getting input from the user..

sha1hash = input("Enter the hash to crack : ")

# Opening a file full of password guesses..

ListOfPass = str(urlopen('https://yuvraj-kaushal.github.io/PasswordLists/pass.txt').read(), 'utf-8')

# I will take a guess from the list of passwords I opened, and split it by line..

for guess in ListOfPass.split('\n'):

# I will hash the guess we took from the password list so we can compare it to the hash the user gave us..

    hashedGuess = hashlib.sha1(bytes(guess, 'utf-8')).hexdigest()

# I will compare the hash the user gave us to the hashed version of the password guess and determine if they are equal..

    if hashedGuess == sha1hash:

# I will tell the program what to do if the password guess matches, which is to print the current guess and quit the program. And I will also tell the program what to do if the password guess don't match, which is to return to step 3 to get a new password from the list..
        print("The password is : ", str(guess))
        quit()
    elif hashedGuess != sha1hash:
        print("Password guessing.. ",str(guess)," doesn't match, trying next..")

# I will tell the program what to do if we get all the way through the password list without finding a match..
print("Password not in the file.. try again")