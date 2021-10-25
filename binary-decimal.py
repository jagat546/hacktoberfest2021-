def binaryToNum(binary):
    result = 0
    for i in range(len(binary)):
        digit = binary.pop()
        if digit == '1':
            result = result + pow(2, i)
    print("Result: ", result)  

if __name__ == '__main__':
    try:
        bin = list(input("Input Binary Number: "))
        binaryToNum(bin)
    except:
        print("There's an error occurred") 