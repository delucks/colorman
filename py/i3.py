from color_common import read_to_dict
import sys

if len(sys.argv) < 1:
    print 'Usage: i3.py {xres}'

with open(sys.argv[1]) as f:
    colors = read_to_dict(f.read())
    for item in sorted(colors.keys()):
        print 'set ${c} {h}'.format(c=item, h=colors[item])
