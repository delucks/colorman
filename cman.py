#!/usr/bin/env python2
import argparse
import getpass
from py.color_common import *

# replaces the original 'cman' script, which was ugly bash

# quick hack to make sure the path is formatted right
COLORS_DIR='/home/{user}/dotfiles/colors'.format(user=getpass.getuser())
COLORSX='/home/{user}/.colorsX'.format(user=getpass.getuser())
I3_CONFIG='/home/{user}/.i3/config'.format(user=getpass.getuser())
I3_CONFIG_TEMPLATE='/home/{user}/.i3/config-template'.format(user=getpass.getuser())

''' 
writes a configuration template for i3 with a bunch of variables for the colors to the correct file
'''
def gen_i3():
    with open(I3_CONFIG_TEMPLATE, 'r') as f:
        contents = f.read()
    with open(COLORSX, 'r') as f:
        colors = ''
        color_dict = read_to_dict(f.read())
        for item in sorted(color_dict.keys()):
            colors += 'set ${c} {h}\n'.format(c=item, h=color_dict[item])
    with open(I3_CONFIG, 'w') as f:
        f.write(colors)
        f.write(contents)

'''
pretty-print your current terminal colors
'''
def print_colors():
    with open(COLORSX, 'r') as f:
        hexvals = read_to_dict(f.read())
    for item, val in sorted(hexvals.iteritems()):
        color_num = int(item.lstrip('color'))
        if  color_num < 8:
            print '\x1b[3{i}mCOLOR{i}  ########  {v}\x1b[39;49m'.format(i=color_num, v=val)
        else:
            lo = color_num - 8
            if lo < 2:
                print '\x1b[3{i};1mCOLOR{n}  ########  {v}\x1b[39;49m'.format(i=lo, n=color_num, v=val)
            else:
                print '\x1b[3{i};1mCOLOR{n} ########  {v}\x1b[39;49m'.format(i=lo, n=color_num, v=val)

'''
reformat a file from dotshare.it
'''
def dotgrab(dot_id, location):
    import urllib2
    USER_AGENT = 'https://github.com/delucks X colors manager'
    headers = {'User-Agent': USER_AGENT} 
    baseurl='http://dotshare.it/dots/{dotid}/0/raw'.format(dotid=dot_id) 
    r = urllib2.Request(baseurl, None, headers)
    reformat(urllib2.urlopen(r).read(), location, dot_id)

def read_from_file(file_path, name, location):
    with open(file_path) as f:
      reformat(f.read(), location, name)

def main(wall_dir='~/img/wallpapers', colors_dir=COLORS_DIR):  
    p = argparse.ArgumentParser(description='manage X11 color palletes')
    p.add_argument('-g', '--generate', help='generate a color scheme from an image')
    p.add_argument('-l', '--location',help='set alternate location for the generated color files',default='~/dotfiles/colors')
    p.add_argument('-c', '--change', help='swap to a different color scheme')
    p.add_argument('-f', '--reformat', help='reformat an existing file as a color scheme', nargs=2)
    p.add_argument('-s', '--select', help='open a selection dialog and pick a colorscheme', action='store_true')
    p.add_argument('-d', '--dotshare', help='download and format a color scheme from dotshare.it')
    p.add_argument('-i', '--generate-i3', help='generate an i3 config file from a template', action='store_true')
    args = p.parse_args()
    if args.generate:
        scheme = ImageScheme(image_path=args.generate)
        split_name = args.generate.split('/').pop()
        scheme.generate_xres(args.location, split_name)
    elif args.dotshare:
        dotgrab(args.dotshare, colors_dir)
    elif args.reformat:
        read_from_file(args.reformat[0], args.reformat[1], colors_dir)
    elif args.generate_i3:
        gen_i3()
    else:
        print_colors()

if (__name__ == '__main__'):
    main()
