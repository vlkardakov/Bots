count = 0

total_count = int(input())

xyu=1000


for i in range(total_count):
    ch = int(input())
    if ch%3==0 and ch < xyu:
        xyu = ch



print(xyu)
