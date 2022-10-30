from tkinter import *
import random
from time import sleep
from math import sin, cos, pi, floor, atan2, sqrt
from PIL import Image


def HSL(hue, sat, lit):
    lit = min(1, lit)
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


hs = (400, 400)
spacing = 15
num_ribbons = 23

a = random.random() - 0.5
b = random.random() - 0.5
c = -a - b

coordinates = (0,
               0,
               a,
               b,
               c)

# coordinates = tuple([-2 / 5] * 5)
# coordinates = tuple([-1 / 5] * 5)
coordinates = (0, 0, 0.0001, 0.0002, -0.0003)

angle = 0

vectors = ((cos(angle + 0 * pi / 5), sin(angle + 0 * pi / 5)),
           (cos(angle + 2 * pi / 5), sin(angle + 2 * pi / 5)),
           (cos(angle + 4 * pi / 5), sin(angle + 4 * pi / 5)),
           (cos(angle + 6 * pi / 5), sin(angle + 6 * pi / 5)),
           (cos(angle + 8 * pi / 5), sin(angle + 8 * pi / 5)))

print([round(i, 5) for i in coordinates])

stars = []


def coloring_1(x, y, ind_1, ind_2):
    if (ind_1 - ind_2 + 5) % 5 in (1, 4):
        return ('light blue', 'grey50')
    else:
        return ('light green', 'grey50')


def coloring_2(x, y, ind_1, ind_2):
    # return ('white', 'black', 3)
    if (ind_1 - ind_2 + 5) % 5 in (1, 4):
        return ('', '')
    else:
        return ('white', 'white', 3)


def coloring_3(x, y, ind_1, ind_2):
    start_hue = 0
    end_hue = pi * 2

    hue = x / (hs[0] * 2) * (end_hue - start_hue) + start_hue

    if (ind_1 - ind_2 + 5) % 5 in (1, 4):
        val = 0.65 - y / (hs[1] * 7)
    else:
        val = 0.5 - y / (hs[1] * 7)
    color = hexcolor(*cubehelix(hue, 1, val))
    return (color, 'white', 1)


def coloring_3_2(x, y, ind_1, ind_2):
    x_mod = abs(hs[0] - x)

    start_hue = -pi * (0.2)
    end_hue = pi * (0.95)

    start_val = 0.3
    end_val = 0.8

    start_sat = 0.75
    end_sat = 1

    hue = y / (hs[1] * 2) * (end_hue - start_hue) + start_hue

    val = (y - x_mod) / (hs[1] * 2) * (end_val - start_val) + start_val

    sat = y / (hs[1] * 2) * (end_sat - start_sat) + start_sat

    color2 = hexcolor(*HSL(hue, sat - 0.1, (val * 1.15) + 0.2))

    star_val = min(max(val, (val * -5 / 7) + (16 / 13)), 1)
    color3 = hexcolor(*HSL(hue, sat, star_val))

    if (ind_1 - ind_2 + 5) % 5 in (2, 3):
        val -= 0.2

    color = hexcolor(*HSL(hue, sat, val))

    if (ind_1 - ind_2 + 5) % 5 in (1, 4) and random.random() > 0.1:
        stars.append((x, y, color3))
    return (color, color2, 2)


def coloring_4(x, y, ind_1, ind_2):
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

    angle = atan2(y, x)
    val = 0.7 - (sqrt(y ** 2 + x ** 2) * 0.001)
    color = hexcolor(*cubehelix(angle, 1, val))
    return(color, "white", 3)


def coloring_6(x, y, ind_1, ind_2):
    image = Image.open('image.png')
    if not (0 <= x < hs[0] * 2 and 0 <= y < hs[1] * 2):
        return ('', '')
    x_ratio = image.size[0] / (hs[0] * 2)
    y_ratio = image.size[1] / (hs[1] * 2)
    return (hexcolor(*image.getpixel((int(x * x_ratio),
                                      int(y * y_ratio)))[:3]), '')


getcolor = coloring_3


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
    for i in range(5):
        e_i = vectors[i]
        num = (x * e_i[0] + y * e_i[1] - coordinates[i])
        num = round(num * 10000)
        output.append(floor(num / 10000))
    return output


def get_point(nums):
    point = [0, 0]
    for i in range(5):
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


# some stuff i used to make a phone bg
def draw_star(canv, star):
    x = star[0] + (random.random() - 0.5) * 8
    y = star[1] + (random.random() - 0.5) * 8
    color = star[2]
    canv.create_oval(x - 0.5, y - 0.5, x + 0.5, y + 0.5,
                     fill=color, outline=color)


def ground_helper(left, right, std, resolution):
    if resolution == 0:
        return [left, right]
    avg = (left + right) / 2
    mid = avg + random.gauss(0, 1) * std
    midstd = std * 0.41
    return ground_helper(left, mid, midstd, resolution - 1)[:-1]\
        + ground_helper(mid, right, midstd, resolution - 1)


def draw_ground(canv, left, mid, right, resolution):
    n_left = (2 * hs[1]) - left
    n_right = (2 * hs[1]) - right
    n_mid = (2 * hs[1]) - mid

    #####
    points = ground_helper(n_left, n_mid, 30, resolution - 1)[:-1]\
        + ground_helper(n_mid, n_right, 30, resolution - 1)

    data = list(zip([2 * hs[0] / (2 ** (resolution) - 1) * i
                     for i in range(2 ** resolution + 1)],
                    [hs[1] * 2 - i for i in points]))
    data.extend([hs[0] * 3, hs[1] * 3, 0, hs[1] * 3])

    color = hexcolor(*cubehelix(0.1, 0.3, 0.3))
    color2 = hexcolor(*cubehelix(0.1, 0.3, 0.2))

    canv.create_polygon(*data, fill=color, outline='')
    b = canv.create_polygon(*data, fill=color2, outline='')
    canv.move(b, 0, 35)


root = Tk()
canv = Canvas(root, width=hs[0] * 2, height=hs[1] * 2, bg="black")
canv.pack()

tilecoords = []

for ind_1 in range(4):
    for ind_2 in range(ind_1 + 1, 5):
        for d_1 in range(-num_ribbons, num_ribbons + 1):
            for d_2 in range(-num_ribbons, num_ribbons + 1):
                tilecoords.append((ind_1, ind_2, d_1, d_2))

# random.shuffle(tilecoords)
tilecoords = sorted(tilecoords, key=lambda x: sum([abs(i) for i in x[2:]]))

linecoords = []

ground = not True

while True:
    # sleep(0.01)
    if tilecoords:
        nt = tilecoords.pop(0)
        intersection = find_intersection(*nt)
        draw_rhomb(get_nums(*intersection), nt, canv)
    elif linecoords:
        nl = linecoords.pop(0)
        draw_line(*nl, canv)
    elif stars:
        draw_star(canv, stars.pop())
    elif ground:
        draw_ground(canv, 730, 715, 600, 5)
        ground = False
    root.update_idletasks()
    root.update()
