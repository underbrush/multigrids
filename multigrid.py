from tkinter import *
import random
from time import sleep
from math import sin, cos, pi, floor, atan2, sqrt


def HSL(hue, sat, lit):
    a = sat * lit * (1 - lit)
    cosh = cos(hue)
    sinh = sin(hue)

    R = 255 * (lit + a * (-0.14861 * cosh + 1.78277 * sinh))
    G = 255 * (lit + a * (-0.29227 * cosh - 0.90649 * sinh))
    B = 255 * (lit + a * (+1.97294 * cosh))

    R = min(max(0, round(R)), 255)
    G = min(max(0, round(G)), 255)
    B = min(max(0, round(B)), 255)

    return (R, G, B)


def cubehelix(hue, sat, lit):
    hue = ((hue % (2 * pi)) + 2 * pi) % (2 * pi)
    frac = 0.5 - (cos(hue) / 2)

    n = (0.3 + 0.4 * frac)
    new_l = (2 - 4 * n) * (lit ** 2) + (4 * n - 1) * lit

    return HSL(hue, min(1, sat * (0.5 + 0.75 * frac)), new_l)


def hexcolor(r, g, b):
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)


hs = (500, 400)
spacing = 40
num_ribbons = 8

directions = 4

a = [random.random() - 0.5 for i in range(directions - 3)]
e = -sum(a)

coordinates = [0, 0]
coordinates.extend(a)
coordinates.append(e)


# a = random.random() - 0.5
# c = random.random() - 0.5
# b = (a + c)
# coordinates = [a, 0, b, 0, c, 0]

coordinates = [1 / directions] * directions
coordinates = [-0.5, -0.5, -0.5, -0.5]


frac = directions * (1 if directions % 2 else 2)

vectors = [(cos(2 * i * pi / frac), sin(2 * i * pi / frac))
           for i in range(directions)]

print([round(i, 5) for i in coordinates])


def coloring_1(x, y, ind_1, ind_2):
    if (ind_1 - ind_2 + directions) % directions in (1, directions - 1):
        return ('light pink', 'grey50')
    elif (ind_1 - ind_2 + directions) % directions in (2, directions - 2):
        return ('light blue', 'grey50')
    elif (ind_1 - ind_2 + directions) % directions in (3, directions - 3):
        return ('light green', 'grey50')
    else:
        return ('light yellow', 'grey50')


def coloring_2(x, y, ind_1, ind_2):
    if (ind_1 - ind_2 + directions) % directions in (1, directions - 1):
        return coloring_3(x, y + (hs[1] * 0), ind_1, ind_2)
    elif (ind_1 - ind_2 + directions) % directions in (2, directions - 2):
        return ('', '')
    elif (ind_1 - ind_2 + directions) % directions in (3, directions - 3):
        return coloring_3(x + 2 * hs[0], y, ind_1, ind_2)
    else:
        return ('black', 'white')


def coloring_3(x, y, ind_1, ind_2):
    start_hue = pi * (0)
    end_hue = pi * (1 / 3)

    hue = x / (hs[0] * 2) * (end_hue - start_hue) + start_hue
    val = 0.75 - y / (hs[1] * 4.5)
    color = hexcolor(*cubehelix(hue, 1, val))
    return (color, 'white')


def coloring_4(x, y, ind_1, ind_2):
    return("white", "light grey")
    if 1 in (ind_1, ind_2):
        if 2 in (ind_1, ind_2):
            return ("orange", "black")
        return ("red", "black")
    elif 2 in (ind_1, ind_2):
        return ("yellow", "black")
    return ("white", "black")


def coloring_5(x, y, ind_1, ind_2):
    radius = -1
    x = x - hs[0]
    y = y - hs[1]

    if sqrt(y ** 2 + x ** 2) > radius and radius >= 0:
        return('', '')

    angle = atan2(y, -x)
    val = 0.7 - (sqrt(y ** 2 + x ** 2) * 0.001)
    color = hexcolor(*cubehelix(angle, 1, val))
    return(color, "black", 3)


getcolor = coloring_4


def find_intersection(ind_1, ind_2, dist_1, dist_2):
    d_1 = dist_1 + coordinates[ind_1]
    d_2 = dist_2 + coordinates[ind_2]
    e_1 = vectors[ind_1]
    e_2 = vectors[ind_2]
    denom = (e_1[0] * e_2[1] - e_1[1] * e_2[0])
    x = (d_1 * e_2[1] - d_2 * e_1[1]) / denom
    y = (d_2 * e_1[0] - d_1 * e_2[0]) / denom
    return (x, y)


def get_nums(x, y):
    output = []
    for i in range(directions):
        e_i = vectors[i]
        num = (x * e_i[0] + y * e_i[1] - coordinates[i])
        num = round(num * 10000)
        output.append(floor(num / 10000))
    return output


def get_point(nums):
    point = [0, 0]
    for i in range(directions):
        point[0] += vectors[i][0] * nums[i]
        point[1] += vectors[i][1] * nums[i]
    return point


def draw_rhomb(nums, info, canv):
    ind_1 = info[0]
    ind_2 = info[1]
    nums[ind_1] = info[2]
    nums[ind_2] = info[3]

    coords = get_point(nums)
    nums[ind_1] -= 1
    coords.extend(get_point(nums))
    nums[ind_2] -= 1
    coords.extend(get_point(nums))
    nums[ind_1] += 1
    coords.extend(get_point(nums))

    avgx = (coords[0] + coords[2] + coords[4] + coords[6]) / 4
    avgy = (coords[1] + coords[3] + coords[5] + coords[7]) / 4

    color = getcolor(avgx * spacing + hs[0],
                     avgy * spacing + hs[1],
                     ind_1, ind_2)

    fill = color[0]
    outline = color[1]
    thickness = 1
    if len(color) > 2:
        thickness = color[2]

    coords = [j * spacing + hs[i % 2] for i, j in enumerate(coords)]
    canv.create_polygon(*coords, fill=fill, outline=outline, width=thickness)


root = Tk()
canv = Canvas(root, width=hs[0] * 2, height=hs[1] * 2, background="grey")
canv.pack()

tilecoords = []

for ind_1 in range(directions - 1):
    for ind_2 in range(ind_1 + 1, directions):
        for d_1 in range(-num_ribbons, num_ribbons + 1):
            for d_2 in range(-num_ribbons, num_ribbons + 1):
                tilecoords.append((ind_1, ind_2, d_1, d_2))

# random.shuffle(tilecoords)

linecoords = []

while True:
    sleep(0.01)
    if tilecoords:
        nt = tilecoords.pop(0)
        intersection = find_intersection(*nt)
        draw_rhomb(get_nums(*intersection), nt, canv)
    elif linecoords:
        nl = linecoords.pop(0)
        draw_line(*nl, canv)
    root.update_idletasks()
    root.update()
