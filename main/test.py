t = 0
def prime(d):
    global t
    t += 1
    if (d % 2 == 0 and d != 2) or (d % 3 == 0 and d != 3) \
            or (d % 5 == 0 and d != 5) or (d % 7 == 0 and d != 7)\
            or (d % 11 == 0 and d != 11) or (d % 13 == 0 and d != 13):
        return d, 'Составное число', t
    else:
        return d, 'Простое число', t


for i in range(100,200):
    print(prime(i))