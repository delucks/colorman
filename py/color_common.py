import re
import colorsys
from collections import namedtuple
from math import sqrt
import random
try:
    import Image
except ImportError:
    from PIL import Image

def read_to_dict(text):
  colors = {}
  RE_COLORS = re.compile(".*(color[0-9]{1,2})(?:[\t\ ]*):(?:[\t\ ]*)(?:\[[0-9]{1,3}\])?(#[a-zA-Z0-9]{3,6})",re.IGNORECASE)
  BG_COLORS = re.compile(".*(foreground|background)(?:[\t\ ]*):(?:[\t\ ]*)(?:\[[0-9]{1,3}\])?(#[a-zA-Z0-9]{3,6})",re.IGNORECASE) 
  # read line by line and attempt to match the colors
  for line in re.finditer('.*?\n',text):
      l = line.group(0).strip()
      if len(l) is 0:
        continue
      if not l.startswith('!'):
        m = RE_COLORS.match(l)
        if m is not None:
          colors[m.group(1)] = m.group(2)
        else:
          b = BG_COLORS.match(l)
          if b is not None:
            colors[b.group(1)] = b.group(2)
  
  return colors

def reformat(text, location, name):
  COLORS = "{dst}/{fn}.colors".format(dst=location,fn=name)
  XRESOURCES = "{dst}/{fn}.colorsX".format(dst=location,fn=name) 
  xres = ''
  cols = ''
  colors = read_to_dict(text)

  for item in sorted(colors.keys()):
    xres += "*{color}: {hexval}\n".format(color=item,hexval=colors[item])
    cols += "export {color}=\"{hexval}\"\n".format(color=item.upper(),hexval=colors[item])

  with open(XRESOURCES, 'w+') as f:
    f.write(xres)
  with open(COLORS, 'w+') as f:
    f.write(cols)

'''
takes in an image, processes it into a colorscheme
'''
class ImageScheme(object):
    def __init__(self, image_path, n=16):
        self.n = n
        self.image_path = image_path
        self.img = Image.open(self.image_path)
        self.Point = namedtuple('Point', ('coords', 'n', 'ct'))
        self.Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

    def euclidean(self, p1, p2):
        return sqrt(sum([
            (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
        ]))

    def get_points(self):
        points = []
        w, h = self.img.size
        for count, color in self.img.getcolors(w * h):
            points.append(self.Point(color, 3, count))
        return points

    def calculate_center(self, points, n):
        vals = [0.0 for i in range(n)]
        plen = 0
        for p in points:
            plen += p.ct
            for i in range(n):
                vals[i] += (p.coords[i] * p.ct)
        return self.Point([(v / plen) for v in vals], n, 1)

    def kmeans(self, points, k, min_diff):
        clusters = [self.Cluster([p], p, p.n) for p in random.sample(points, k)]
        while 1:
            plists = [[] for i in range(k)]
            for p in points:
                smallest_distance = float('Inf')
                for i in range(k):
                    distance = self.euclidean(p, clusters[i].center)
                    if distance < smallest_distance:
                        smallest_distance = distance
                        idx = i
                plists[idx].append(p)
            diff = 0
            for i in range(k):
                old = clusters[i]
                center = self.calculate_center(plists[i], old.n)
                new = self.Cluster(plists[i], center, old.n)
                clusters[i] = new
                diff = max(diff, self.euclidean(old.center, new.center))
            if diff < min_diff:
                break
        return clusters

    def get_colors(self):
        points = self.get_points()
        clusters = self.kmeans(points, self.n, 1)
        rgbs = [map(int, c.center.coords) for c in clusters]
        rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))
        return map(rtoh, rgbs)

    def torgb(self, hexv):
        hexv = hexv[1:]
        r, g, b = (
            int(hexv[0:2], 16) / 256.0,
            int(hexv[2:4], 16) / 256.0,
            int(hexv[4:6], 16) / 256.0,
        )
        return r, g, b

    def darkness(self, hexv):
      r, g, b = self.torgb(hexv)
      darkness = sqrt((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2)
      return darkness

    def normalize(self, hexv, minv=128, maxv=256):
        r, g, b = self.torgb(hexv)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        minv = minv / 256.0
        maxv = maxv / 256.0
        if v < minv:
            v = minv
        if v > maxv:
            v = maxv
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return '#{:02x}{:02x}{:02x}'.format(int(r * 256), int(g * 256), int(b * 256))

    def generate_xres(self, location, name):
        COLORS = '{dst}/{fn}.colors'.format(dst=location,fn=name)
        XRESOURCES = '{dst}/{fn}.colorsX'.format(dst=location,fn=name) 
        xres = ''
        cols = ''
        i = 0
        colors = self.get_colors()
        colors.sort(key=lambda  x:self.darkness(x), reverse=True)
        for c in colors:
            if i == 0:
                c = self.normalize(c, minv=0, maxv=32)
            elif i == 8:
                c = self.normalize(c, minv=128, maxv=192)
            elif i < 8:
                c = self.normalize(c, minv=160, maxv=224)
            else:
                c = self.normalize(c, minv=200, maxv=256)
            c = self.normalize(c, minv=32, maxv=224)
            xres += '''*color{}: {}\n'''.format(i, c)
            cols += '''export COLOR{}="{}"\n'''.format(i, c)
            i += 1

        with open(XRESOURCES, 'w+') as f:
            f.write(xres)
        with open(COLORS, 'w+') as f:
            f.write(cols)

if (__name__ == '__main__'):
    import argparse
    p = argparse.ArgumentParser(description='use k-means to generate colors from an image file')
    p.add_argument('filename',help='the image file you want to generate the colors from')
    p.add_argument('-l','--location',help='set alternate location for the generated color files',default='~/dotfiles/colors')
    p.add_argument('-n','--number',help='set the number of colors to generate',default=16)
    args = p.parse_args()
    scheme = ImageScheme(image_path=args.filename, n=args.number)
    split_name = args.filename.split('/').pop()
    scheme.generate_xres(args.location, split_name)
