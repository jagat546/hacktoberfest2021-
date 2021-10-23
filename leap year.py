
#enter year
year = int(input("Enter year: "))

#initialize leap to false
leap = False

#check if year is divisible by 4
if year%4 == 0:
    if year%100==0 and year%400!=0:
        leap = False
    else:
        leap = True
if leap is True:
    print(year,"is a leap year")
else:
    print(year,"is not a leap year")
