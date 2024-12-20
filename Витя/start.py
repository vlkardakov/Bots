import time
def F(n):
    return n if n<9 else F(n%9) + F(n//9)


if __name__ == "__main__":
    count = 0
    time1 = time.time()
    for n in range(4*(6**7), 5*(6**7)):
        if F(n) == 121: count += 1
    print(time.time()-time1)
    print(count)
