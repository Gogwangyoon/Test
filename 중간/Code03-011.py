for i in range(1,10):
    if i <= 5:
        for j in range(5-i):
            print(" ",end="")
        for j in range(2*i-1):
            print("*",end="")
        print()
    else:
        for j in range(i-5):
            print(" ",end="")
        for j in range((10-i)*2-1):
            print("*",end="")
        print()
