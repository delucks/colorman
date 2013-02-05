import sys
import colorsys
from colorz import colorz
from math import sqrt

if len(sys.argv) < 2:
  print "Usage: {0} FILENAME [num_colors]".format(sys.argv[0])
  sys.exit()


print sys.argv[1]

WALLPAPER = sys.argv[1]
filename = WALLPAPER.split('/').pop()
COLORS = ".{0}.colors".format(filename)
XRESOURCES = ".{0}.Xres".format(filename)

cols = ''
xres = ''

def torgb(hexv):
    hexv = hexv[1:]
    r, g, b = (
        int(hexv[0:2], 16) / 256.0,
        int(hexv[2:4], 16) / 256.0,
        int(hexv[4:6], 16) / 256.0,
    )
    return r, g, b

def normalize(hexv, minv=128, maxv=256):
    r, g, b = torgb(hexv)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    minv = minv / 256.0
    maxv = maxv / 256.0
    if v < minv:
        v = minv
    if v > maxv:
        v = maxv
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return '#{:02x}{:02x}{:02x}'.format(int(r * 256), int(g * 256), int(b * 256))

def darkness(hexv):
  r, g, b = torgb(hexv)
  darkness = sqrt((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2)
  return darkness

def to_hsv(c):
    r, g, b = torgb(c)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v

if __name__ == '__main__':
    if len(sys.argv) == 2:
        n = 16
    else:
        n = int(sys.argv[2])


    i = 0
    with open('colorz.html', 'w') as f:
        f.write("""<img src="file://{}" height=200/>""".format(WALLPAPER))
        # sort by value, saturation, then hue
        colors = colorz(WALLPAPER, n=n)
        colors.sort(key=lambda  x:darkness(x), reverse=True)
        for c in colors:
            if i == 0:
                c = normalize(c, minv=0, maxv=32)
            elif i == 8:
                c = normalize(c, minv=128, maxv=192)
            elif i < 8:
                c = normalize(c, minv=160, maxv=224)
            else:
                c = normalize(c, minv=200, maxv=256)
            c = normalize(c, minv=32, maxv=224)
            f.write("""
                <div style="background-color: {0}; width: 100%; height: 50px">{1}: {0} </div>
                """.format(c, i)
            )
            xres += """*color{}: {}\n""".format(i, c)
            cols += """export COLOR{}="{}"\n""".format(i, c)
            i += 1

    with open(XRESOURCES, 'w') as f:
        f.write(xres)
    with open(COLORS, 'w') as f:
        f.write(cols)
