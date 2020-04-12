x = int(input("Insira a largura "))
y = int(input("Insira a altura "))

a = 1
b = 1

while b <= y:
    while a <=x:

        if b == 1 or b == y or a == 1 or a == x:
            print("# ", end = "")
        else:
            print ("  ", end ="")

        a = a + 1


    b = b + 1
    a = 1
    print ()
