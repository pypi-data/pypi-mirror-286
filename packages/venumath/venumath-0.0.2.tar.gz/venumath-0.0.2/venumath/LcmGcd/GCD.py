# Python program to find the H.C.F of two input number
def hcf(x, y):	# define a function
# choose the smaller number
    if x > y:
        smaller = y
    else:
        smaller = x
    for i in range(1, smaller+1):
        if((x % i == 0) and (y % i == 0)):
            hcf = i      
    print("The H.C.F. of", x,"and", y,"is", hcf)
#num1 = int(input("Enter first number: "))
#num2 = int(input("Enter second number: "))
#print("The H.C.F. of", num1,"and", num2,"is", computeHCF(num1, num2))


