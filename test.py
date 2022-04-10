def buildRange(value, limit=1024):
    lst = []
    x = value

    lst.append(f'{x}-{x - limit}')

    for i in range(int(value / limit)):
        x -= limit
        y = x - limit

        if y > 0:
            lst.append(f'{x}-{y}')
        elif y < 0:
            lst.append(f'{x}-{0}')
    return lst

# x = buildRange(6348, 2048)
# print(x)
