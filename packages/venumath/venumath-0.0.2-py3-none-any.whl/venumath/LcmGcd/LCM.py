# Python program to find the L.C.M. of two input number



def lcm(x, y):
   """This function takes two
   integers and returns the L.C.M."""

     # choose the greater number
   if x > y:
       greater = x
   else:
       greater = y

   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1

   print("The L.C.M. of", x,"and", y,"is", lcm)



