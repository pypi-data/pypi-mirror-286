def mult(*args):
    ''' Using for multiplication and Usage: mult(num1,num2,....etc)'''
    multi=1
    for i in args:
        multi=multi*i
    print(f"Multiplication: {multi}")
